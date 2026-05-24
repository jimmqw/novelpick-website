# Claude Code 源码深度研究 — 全量学习报告

> 基于 Claude Code 泄露源码（1.0.0~1.0.6）全面研究
> 研究时间：2026-04-05 ~ 2026-04-06
> 参与子任务：3个并行 → 串行优化后全部完成

---

## 一、多Agent协调架构

### 三种Agent模式

| 模式 | 触发方式 | 核心机制 | 适用场景 |
|------|---------|---------|---------|
| **Fork** | Agent tool 不传subagent_type | 继承父完整上下文，共享API prompt cache | 并行只读研究 |
| **Teammate** | 传 name + team_name | 显式命名+team文件+mailbox系统 | 长期多角色协作 |
| **Worktree** | isolation:'worktree' | 基于git worktree创建隔离工作目录 | 并行写代码 |

### Coordinator四阶段工作流

```
Research(并行) → Synthesis(Coordinator合成) → Implementation(串行) → Verification
```

**CC协调器精髓：**
- Coordinator自己合成worker结果，不懒传递
- Continue vs Spawn按上下文重叠度决策
- `<task-notification>` XML结构化通知
- 任务分阶段有清晰边界

### 贾维斯适配方案

**不照搬CC的理由：** CC是CLI编程工具，强调并行research/实现分离；贾维斯是个人助理，强调主动和连贯。

**贾维斯架构：改进的Fork**

```
主Agent（贾维斯本体）
  - 理解用户意图
  - 规划任务分解
  - 协调 sub-agent
  - 合成结果、主动汇报
        │ Agent() 隐式分叉（Fork）
        ▼
  ┌──────────────┐  ┌──────────────┐
  │ Sub-agent A  │  │ Sub-agent B  │  （并行 Research）
  └──────────────┘  └──────────────┘
        │ SendMessage 反馈结果
        ▼
  主Agent 合成 → 决策
        │
        │ Agent() 继续执行（Implementation）
        ▼
  ┌──────────────┐
  │ Sub-agent C  │  （执行具体任务）
  └──────────────┘
```

**贾维斯与CC的关键区别：**

| 维度 | CC | 贾维斯 |
|------|----|--------|
| 团队持久化 | TeamFile持久化 | 临时会话，无持久化 |
| Mailbox | 完整消息队列 | 不需要，Fork结果直接回调 |
| Worktree | git隔离 | 不需要 |
| 生命周期 | 显式管理stop/resume | 简单spawn→等待→合成 |

**待实现清单：**

- [ ] Fork Sub-agent机制（继承父上下文）
- [ ] Agent生命周期管理（spawn/等待通知/超时/失败重试）
- [ ] 结果合成（主agent解析sub-agent结果并综合）
- [ ] 并行任务调度（同时fork多个sub-agent）

---

## 二、47个工具模块系统

### 工具分类

| 类别 | 数量 | 代表工具 |
|------|------|---------|
| Agent/子智能体 | 8 | AgentTool、Task系列、TeamCreateTool |
| 文件操作 | 5 | FileEditTool、FileReadTool、GlobTool、GrepTool |
| Shell执行 | 3 | BashTool、PowerShellTool、REPLTool |
| 知识/Web | 4 | WebSearchTool、WebFetchTool |
| MCP集成 | 2 | MCPTool、McpAuthTool |
| 定时任务 | 3 | CronCreateTool、CronDeleteTool、CronListTool |
| 计划/工作流 | 4 | EnterPlanModeTool、EnterWorktreeTool |
| 其他 | 6 | ConfigTool、BriefTool、NotebookEditTool |

### 五大设计模式

**1. 工具工厂模式（buildTool）**
```typescript
export const FileEditTool = buildTool({
  name: FILE_EDIT_TOOL_NAME,
  inputSchema,      // Zod schema
  outputSchema,
  validateInput,    // 权限前前置校验
  checkPermissions, // 权限判断
  call,             // 执行逻辑
  renderToolUseMessage,
  renderToolResultMessage,
  // 十几个可选钩子
})
```

**2. 三层权限架构**
```
validateInput()     ← 输入校验（文件存在性、字符串匹配、路径检查）
        ↓
checkPermissions() ← 规则匹配（allow/deny/ask + 前缀/通配符）
        ↓
call()              ← 实际执行
```

**3. BashTool安全架构（200+检查）**
```
命令输入
  ↓
[Phase 1] tree-sitter AST解析
  ↓
[Phase 2] 精确规则匹配
  ↓
[Phase 3] Haiku分类器（denyDescriptions/askDescriptions）
  ↓
[Phase 4] 子命令拆分（max=50）
  ↓
[Phase 5] 每子命令权限检查
  ↓
[Phase 6] Haiku allow分类器（异步+推测执行）
  ↓
结果: allow / deny / ask / passthrough
```

**4. Zod Schema + lazySchema**
```typescript
// lazySchema - 延迟加载，避免循环依赖
const inputSchema = lazySchema(() =>
  z.strictObject({
    subject: z.string().describe('...'),
    description: z.string().describe('...'),
  })
)
```

**5. 错误码体系**
```typescript
errorCode 0: 团队内存密钥泄露
errorCode 1: 无变化
errorCode 2: 路径被deny规则阻止
errorCode 3: 创建已存在文件
errorCode 4: 文件不存在
errorCode 7: 文件在读取后被修改（staleness check）
errorCode 8: 字符串不匹配
// ...共10+种错误码
```

### 贾维斯可借鉴点

| 优先级 | 模式 | 当前状态 | 实施建议 |
|--------|------|---------|---------|
| **高** | 工具工厂模式 | 无统一工厂 | 创建createSkill()工厂 |
| **高** | Zod Schema全面schema化 | 部分使用 | 全面迁移 |
| **高** | 错误码枚举体系 | 杂散错误 | 建立JErrorCode枚举 |
| **高** | validate/check/execute分离 | 混用 | 分层解耦 |
| **中** | 文件staleness check | 未实施 | 文件系统操作技能需此机制 |
| **中** | 推测执行 | 未实施 | 网络请求类技能可提前启动 |
| **中** | maxResultSizeChars | 未实施 | 大结果截断+持久化 |
| **低** | tree-sitter AST安全 | 未实施 | Shell类技能需类似架构 |

---

## 三、KAIROS白日梦后台守护模式

### 两个记忆系统对比

| 系统 | 触发时机 | 目的 |
|------|---------|------|
| `extractMemories` | 每轮对话结束时 | 从当前会话提取记忆 |
| `autoDream` | 时间+会话数量阈值触发 | 跨会话整合记忆 |

### autoDream触发条件（同时满足）

```
1. 时间门：距上次整合 >= 24h（minHours）
2. 会话门：新消息会话数 >= 5（minSessions）
3. 锁门：无其他进程正在整合（.consolidate-lock）
4. KAIROS门：KAIROS激活时禁用
```

### Forked Agent模式（runForkedAgent）

**与父进程共享：**
- systemPrompt、tools、model、messages prefix（CacheSafeParams）
- API prompt cache hit

**工具限制（createAutoMemCanUseTool）：**
- 允许：Read/Grep/Glob（无限制）
- 允许：read-only Bash（ls/find/grep/cat/stat/wc/head/tail）
- 允许：Edit/Write仅限memoryDir内部
- 拒绝：其他所有

### 整合Prompt四阶段

```
orient → gather → consolidate → prune
1. orient: 理解记忆目录结构
2. gather: 收集所有相关记忆
3. consolidate: 整合、提炼、去重
4. prune: 删除过时/无用记忆
```

### 贾维斯实现方案（推荐轻量版）

**基于现有机制，不需要新建进程/子代理：**

```
触发器：
- cron job每24h检查一次
- 或heartbeat时顺便检查

检查逻辑：
- 读取.consolidate-lock mtime
- 检查距上次整合是否>=24h
- 扫描是否有未整合的新内容

执行：
- 用OpenClaw agent调用能力
- 工具限制：只读Bash + 仅允许写memory/

锁机制：
- 在memory/下创建.consolidate-lock
- 写入进程PID
- 检测stale时允许抢占

结果写入：
- 直接写memory/下的.md文件
```

**贾维斯实现所需前提条件：**

| 条件 | 状态 |
|------|------|
| 记忆文件目录 | 需确认（memory/或memdir/） |
| 定期触发机制 | ✅ cron、heartbeat已可用 |
| 后台agent调用 | 需确认 |
| 锁文件机制 | ✅ 可直接复用 |

---

## 四、总体落地评估

### 各模块落地优先级

| 模块 | 来源 | 落地优先级 | 理由 |
|------|------|-----------|------|
| 定时cron调度 | tools/CronTool | **P0** | 已有完整实现 |
| 情绪检测 | notifications.tsx | **P0** | 轻量高收益 |
| 四类记忆分类 | memoryTypes.ts | **P0** | 已有V2实现 |
| 工具工厂模式 | buildTool | **P1** | 技能系统化的基础 |
| Zod Schema | 各工具 | **P1** | 依赖工厂模式 |
| 错误码体系 | 各工具 | **P1** | 依赖工厂模式 |
| Fork Sub-agent | coordinator | **P2** | 复杂任务并行能力 |
| KAIROS轻量版 | autoDream | **P2** | 记忆整合自动化 |
| BashTool安全 | BashTool | **P3** | Shell类技能需要 |
| 多Agent协调 | coordinator | **P3** | 长期架构 |

### 核心差距总结

| 类别 | 未落地项 | 原因 |
|------|---------|------|
| 记忆系统 | 遗忘机制 | 记忆量未到需要自动遗忘的程度 |
| 工具系统 | 工厂模式迁移 | 需要较大重构 |
| KAIROS | 轻量版实现 | 等确认需求 |
| 多Agent | Fork/Teammate | 长期项目，待规划 |

---

## 五、研究过程踩坑记录

### 教训1：子任务不能同时启动
- **问题：** 三个子任务同时spawn，触发模型切换冲突（LiveSessionModelSwitchError），两个任务失败
- **解决方案：** 改为串行启动，完成一个再启动下一个
- **经验：** OpenClaw子Agent共享模型实例，并发有上限

### 教训2：执行规范比想象中重要
- **问题：** Clawvard考试F级，Execution/Retrieval/Reflection三项零分
- **原因：** 任务做一半、检索用泛词、不验证就输出
- **解决方案：** 执行/检索/反思三模块规范写入SOUL.md

### 教训3：不是所有源码都值得学
- **问题：** 把Claude Code的1100+功能全学了一遍
- **原因：** 没有先问"这个对我的实际工作有没有用"
- **教训：** 多Agent协调/三路并行/KAIROS对现在的贾维斯帮助有限，是为未来储备

---

_本报告整合了CC-COORDINATOR-STUDY.md / CC-TOOLS-STUDY.md / CC-KAIROS-STUDY.md三份子研究_
