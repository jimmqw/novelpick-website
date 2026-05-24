# Claude Code KAIROS 白日梦后台守护模式研究

## 源码路径
`C:\Users\Administrator\Desktop\src-claudecode(1)\src\`

---

## 一、核心机制

### 1. 两个后台记忆系统的区别

| 系统 | 文件 | 触发时机 | 目的 |
|---|---|---|---|
| `extractMemories` | `services/extractMemories/extractMemories.ts` | 每轮对话结束时（模型产生最终响应后） | 从当前会话提取记忆写入 memory 目录 |
| `autoDream` | `services/autoDream/autoDream.ts` | 时间+会话数量阈值触发 | 跨会话整合记忆（白日梦） |

**KAIROS 模式下**，`autoDream` 被禁用（`isGateOpen()` 返回 false），改用 disk-skill 驱动的 dream 实现。

---

### 2. autoDream 触发条件（白日梦门控）

```
触发需要同时满足：
1. 时间门：距离上次整合 >= minHours（默认24h，可通过 GrowthBook `tengu_onyx_plover` 配置）
2. 会话门：自上次整合以来有新消息的会话数 >= minSessions（默认5）
3. 锁门：没有其他进程正在整合（`.consolidate-lock` 文件锁）
4. KAIROS 门：KAIROS 激活时禁用（KAIROS 用自己的 disk-skill dream）
```

**扫描节流**：即使时间门通过，如果距上次扫描不足10分钟，跳过（避免每轮都 stat）。

**会话发现**：扫描 transcript JSONL 文件的 mtime（文件修改时间），而非创建时间。

---

### 3. 后台整合流程（autoDream）

```
1. 检查 isGateOpen() — KAIROS/远程模式/自动记忆未启用 → 不触发
2. 读取 .consolidate-lock 的 mtime 作为 lastConsolidatedAt
3. 时间门检查
4. 扫描节流检查（10min 间隔）
5. listSessionsTouchedSince() 找出新会话
6. 排除当前会话
7. 会话数门检查
8. tryAcquireConsolidationLock() — 写 PID，获取锁
9. runForkedAgent() 启动 forked 子进程
10. DreamTask 注册到任务系统（UI 可见）
11. 子进程输出通过 makeDreamProgressWatcher 同步到 DreamTaskState
12. 完成 → completeDreamTask → appendSystemMessage("Improved N memories")
13. 失败 → failDreamTask → rollbackConsolidationLock(priorMtime)
```

**锁机制**：
- 锁文件 mtime = lastConsolidatedAt（复用这个值作为时间戳）
- 持有者写自己 PID；检测到 stale（>1h）或 PID 不存在则允许抢占
- 失败时回滚 mtime 到 pre-acquire 值

---

### 4. Forked Agent 模式（runForkedAgent）

**核心文件**：`utils/forkedAgent.ts`

这是两个记忆系统的共同底层：

```
与父进程共享：
- systemPrompt、tools、model、messages prefix（CacheSafeParams）
- 这保证了 API prompt cache hit（子进程读取父进程缓存）

与父进程隔离：
- 独立 AbortController（可被 DreamTask.kill 终止）
- 独立 toolUseContext
- 不写入主 transcript（skipTranscript: true）

工具限制（createAutoMemCanUseTool）：
- 允许：Read/Grep/Glob（无限制）
- 允许：read-only Bash（ls/find/grep/cat/stat/wc/head/tail）
- 允许：Edit/Write 仅限 memoryDir 内部
- 拒绝：其他所有
```

---

### 5. DreamTask UI 层

**文件**：`tasks/DreamTask/DreamTask.ts`

```
DreamTaskState {
  type: 'dream'
  phase: 'starting' | 'updating'  // 第一个 Edit/Write 出现后从 starting 变 updating
  sessionsReviewing: number
  filesTouched: string[]          // 不完整——只捕获 tool_use 里的路径，bash 写入会漏
  turns: DreamTurn[]               // assistant 文本响应，tool_use 折叠成计数
  priorMtime: number                // 用于 kill 时回滚锁
}

UI 展示：
- Footer pill 显示 "dreaming" 状态
- Shift+Down 对话框可查看进度
- 用户可 kill → abortController.abort() + 回滚锁 mtime
```

---

### 6. extractMemories（每轮提取）

```
触发：每轮 stopHooks 时（模型产生无 tool_calls 的最终响应）
每轮成本：GB cache read + 一次 stat

与 autoDream 的关系：
- 同一个 canUseTool 约束
- autoDream 整合旧会话，extractMemories 提取当前会话
- 如果主 agent 写了 memory 文件，extractMemories 跳过（hasMemoryWritesSince 检查）
- 两者互斥：主 agent 写了 → forked extraction 跳过
```

---

### 7. 背景保洁（startBackgroundHousekeeping）

**文件**：`utils/backgroundHousekeeping.ts`

启动时调用一次，注册：
```
- initAutoDream()          // 注册 autoDream runner
- initExtractMemories()    // 注册 extractMemories runner
- initMagicDocs()
- initSkillImprovement()
- autoUpdateMarketplacesAndPluginsInBackground()
- DELAY_VERY_SLOW_OPS (10min 后)：cleanupOldMessageFiles + cleanupOldVersions
- 24h 周期清理（ANT 用户专属）：cleanupNpmCache + cleanupOldVersions
```

---

### 8. IdleTimeoutManager（SDK 模式）

**文件**：`services/autoDream/autoDream.ts`（底部）

```
环境变量：CLAUDE_CODE_EXIT_AFTER_STOP_DELAY（毫秒）
isIdle() 函数由调用者提供
启动后等待 idle 持续 delayMs → gracefulShutdownSync()
stop() 可取消定时器
```

---

## 二、与 Gateway 的交互方式

**结论：KAIROS 后台守护模式不直接与 Gateway 交互。**

"Gateway" 在 Claude Code 中指远程执行基础设施（Lodestone/CCR），相关文件：
- `utils/background/remote/remoteSession.ts` — 远程会话的背景前置条件检查
- `utils/background/remote/preconditions.ts` — 远程环境、GitHub App 安装状态检查

这些是 **teleport 远程会话** 的前置条件，与 autoDream 白日梦无关。

KAIROS 模式的 disk-skill dream 走的是 skill 加载机制，而非 HTTP/WebSocket gateway。

---

## 三、KAIROS 模式特殊处理

```typescript
// bootstrap/state.ts
kairosActive: boolean  // 初始化为 false

// autoDream.ts isGateOpen()
if (getKairosActive()) return false  // KAIROS 激活时禁用 autoDream
```

KAIROS 模式激活时，`autoDream` 完全不触发。KAIROS 有自己的基于 disk-skill 的 dream 实现（通过 skill 机制加载，而非 `runForkedAgent`）。

---

## 四、贾维斯实现方案

### 目标：类似 autoDream 的后台记忆整合能力

### 方案 A：轻量实现（推荐）

基于现有 OpenClaw 机制，不需要新建进程/子代理。

**前提条件**：
1. ✅ 已实现：记忆文件目录（`memory/` 或 `memdir/`）
2. ✅ 已实现：定期触发机制（cron、heartbeat）
3. ✅ 已实现：forked agent 或独立 agent 调用能力

**实现思路**：

```
触发器：
- cron job 每 24h 检查一次（仿 autoDream 时间门）
- 或 heartbeat 时顺便检查（仿每轮 extractMemories）

检查逻辑（memory/ 目录下）：
- 读取 .consolidate-lock mtime（或自己维护 lastConsolidatedAt）
- 检查距上次整合是否 >= 24h
- 扫描会话文件（如果有）或检查是否有未整合的新内容

执行：
- 用 OpenClaw 的 agent 调用能力（类似 runForkedAgent）
- 传入记忆目录路径 + 整合 prompt
- 工具限制：只读 Bash + 仅允许写 memory/ 目录

锁机制（防止并发）：
- 在 memory/ 下创建 .consolidate-lock 文件
- 写入进程 PID
- 检测 stale 时允许抢占

结果写入：
- 直接写 memory/ 下的 .md 文件
- 主 agent 下次启动时自动加载
```

### 方案 B：完整仿制

参照 `autoDream.ts` 的 `initAutoDream()` + `executeAutoDream()` 模式，在贾维斯中实现：
1. 启动时注册 background runner
2. 每轮 REPL turn 后（或 cron 触发）调用 `executeAutoDream()`
3. DreamTask 类似物：注册到任务系统，UI 显示进度
4. 支持用户 kill

**复杂度**：高。需要任务注册系统、UI 进度展示、AbortController 传播等。

### 推荐方案 A 的理由

贾维斯的场景与 Claude Code 不同：
- Claude Code 是开发者工具，用户在场；白日梦在用户不使用时静默运行
- 贾维斯是私人助理，更适合 **按需或低频触发**（每次启动时检查 + cron）
- 不需要复杂的 DreamTask UI（用户不需要看后台任务进度）

---

## 五、贾维斯实现所需前提条件

| 条件 | 状态 | 说明 |
|---|---|---|
| 记忆文件目录 | 需确认 | `memory/` 或 `memdir/` 是否已实现 |
| 定期触发机制 | ✅ | cron、heartbeat 都已可用 |
| 后台 agent 调用 | 需确认 | OpenClaw 是否有类似 runForkedAgent 的能力 |
| 会话列表/mtime 追踪 | 需确认 | 如果要实现会话级别的增量整合 |
| 工具限制能力 | 需确认 | canUseTool 约束是否可复用 |
| 锁文件机制 | ✅ | 可直接复用文件锁模式 |

**最小实现路径**：
1. 确认记忆文件目录结构（`MEMORY.md` + topic files）
2. heartbeat 中加一段"检查是否需要整合"的逻辑
3. 满足条件时，用现有 agent 调用能力执行整合 prompt
4. 整合结果直接写 memory/ 下的 .md 文件

---

## 六、关键文件索引

| 文件 | 用途 |
|---|---|
| `services/autoDream/autoDream.ts` | 白日梦核心逻辑 |
| `services/autoDream/consolidationPrompt.ts` | 整合 prompt（4阶段：orient/gather/consolidate/prune） |
| `services/autoDream/consolidationLock.ts` | 锁文件机制 |
| `services/autoDream/config.ts` | isAutoDreamEnabled 门控 |
| `tasks/DreamTask/DreamTask.ts` | DreamTask 状态注册与 kill 实现 |
| `services/extractMemories/extractMemories.ts` | 每轮记忆提取（createAutoMemCanUseTool 在此） |
| `utils/backgroundHousekeeping.ts` | 启动时注册各后台服务 |
| `utils/forkedAgent.ts` | forked agent 底层（cache 共享机制） |
| `bootstrap/state.ts` | `getKairosActive()` 定义处 |
| `utils/idleTimeout.ts` | SDK 模式空闲退出管理器 |
| `components/IdleReturnDialog.tsx` | 长时间空闲后的用户交互对话框 |
| `hooks/useSessionBackgrounding.ts` | Ctrl+B 后台/前景会话管理 |
| `memdir/memdir.ts` | MEMORY.md 入口点规范 |
| `memdir/paths.ts` | `getAutoMemPath()` — 记忆目录路径 |
