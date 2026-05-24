# Claude Code 多Agent协调架构研究

## 三种Agent模式解析

### 1. Fork（隐式分叉）

**触发方式**: Agent tool 不传 `subagent_type`，且 fork 实验 gate 开启。

**核心机制**: 子进程继承父进程的完整对话上下文（所有 tool_use 块 + system prompt），以 API request prefix 完全一致的方式共享 prompt cache。

```typescript
// fork 路径下，子进程收到的消息结构：
// [...history, assistant(all_tool_uses), user(placeholder_results..., directive)]
// 其中 tool_result 全部是相同占位符，最大化 cache 命中
```

**关键约束**:
- 递归 fork 被禁止（isInForkChild 检测 boilerplate tag）
- 子进程权限模式为 `bubble`，权限提示打回父终端
- 模型默认继承父进程
- Fork + worktree 组合时，注入路径翻译 notice

**使用场景**: 
- 并行研究任务（多个 worker 同时读代码库）
- 快速并行分支思考
- 不需要命名、不需要跨进程通信的简单分叉任务

---

### 2. Teammate（显式命名协作）

**触发方式**: Agent tool 传 `name` + `team_name`，触发 spawnTeammate。

**核心机制**: 
- 有名 agent，可通过 SendMessage 定向通信
- 有 team 文件（TeamFile）持久化团队成员信息
- 通信通过 mailbox 系统（writeToMailbox / 队列式投递）
- 支持 in-process（同一进程）和 tmux（独立进程）两种运行模式

**关键概念**:
- `team-lead` 是固定角色，创建 team 的 session 担任 lead
- Lead 可以通过 SendMessage 向任意 teammate 发消息或 broadcast
- Teammate 可以回复 structured message（shutdown_approval / plan_approval）
- `plan_mode_required`: teammate 实现前需得到 lead 的 plan 审批

**生命周期管理**:
- SendMessage 到已停止的 agent 会自动 resume
- TaskStop 停止后可以继续（resume）
- In-process teammate 的生命周期绑定 leader 进程

**使用场景**:
- 长期任务分解（各司其职的专门 agent）
- 需要相互通信的协作任务
- 复杂的多阶段工作流（research → implement → verify）

---

### 3. Worktree（隔离工作树）

**触发方式**: Agent tool 传 `isolation: 'worktree'` 或 `--worktree` CLI flag。

**核心机制**: 
- 基于 git worktree 创建独立工作目录副本
- 共享同一个 git 仓库但有独立文件系统视图
- 可选 git sparse-checkout（只 checkout 需要的子目录）
- 可选 symlink node_modules 避免磁盘浪费

**关键能力**:
- `createAgentWorktree(slug)`: 为子 agent 创建轻量 worktree
- Agent 完成后检查是否有未提交更改
  - 无变更 → 自动清理
  - 有变更 → 保留（用户可继续工作）
- 支持 PR-based worktree（`--worktree "#123"`）

**使用场景**:
- 并行实现任务（多个 agent 同时改不同文件）
- 实验性重构（不怕冲突的隔离分支）
- `--worktree --tmux` 快速分屏开发

---

## 主协调器（coordinator.ts）核心职责

coordinatorMode.ts 中的 system prompt 定义了协调行为：

```
Coordinator 的角色：
1. 接收用户目标
2. 分解为 research/implementation/verification 阶段
3. 向 worker 分配任务
4. 合成 worker 结果
5. 向用户汇报
```

**并行策略**:
- Research（只读）→ 自由并行 fan-out
- Implementation（写）→ 同文件区域串行
- Verification → 可与不同区域的 implementation 并行

**结果聚合**:
- Worker 结果通过 `<task-notification>` XML 注入 coordinator 的对话
- Coordinator 必须自己合成（不能依赖 worker 代为理解）
- Continue vs Spawn 的决策基于上下文重叠度

**Agent 生命周期**:
- `registerAsyncAgent`: 注册后台任务
- `enqueueAgentNotification`: 完成后通知
- `queuePendingMessage`: 向已运行的 agent 追加消息
- `resumeAgentBackground`: resume 已停止的 agent

---

## Agent间通信机制

### 消息传递（SendMessageTool）

```
Coordinator → Teammate: SendMessage({to: name, message: "..."})
Teammate → Coordinator: 写 mailbox，Coordinator 轮询自己的 inbox
Teammate → Teammate: 通过 team-lead 中转，或 broadcast (*)
```

结构化消息类型：
- `shutdown_request` / `shutdown_response`
- `plan_approval_response`

### 状态共享

**团队级别**:
- TeamFile 持久化在 `.claude/teams/<teamName>.json`
- 包含 members（agentId, name, color, paneId, backendType）
- Lead 的 teamContext 在 AppState 中

**Agent 级别**:
- `agentNameRegistry`: name → agentId 映射（Map）
- 通过 `setAppState` 更新（immutable 模式）
- Fork path 共享 parent system prompt 和 tool pool

### 冲突处理

**文件级冲突**: Worktree 隔离天然避免  
**上下文冲突**: Coordinator 自己合成，worker 不感知彼此  
**资源冲突**: `isConcurrencySafe()` = true（工具层面允许并发）  
**数据冲突**: 无自动解决，依赖任务划分和 human-in-the-loop

---

## 贾维斯适配方案

### 场景分析

贾维斯的实际场景：
- 单用户桌面助手（非多人协作）
- 需要主动预判和执行
- 任务类型相对固定（信息查询、文件操作、代码任务）
- 不需要长期运行的固定团队

### 推荐架构：改进的 Fork + 轻量 Teammate

**不照搬 CC 的理由**:
1. CC 是 CLI 编程工具，强调并行 research / 实现分离；贾维斯是个人助理，强调主动和连贯
2. Teammate 的 team 文件 + mailbox 系统对贾维斯过于重量
3. Worktree 对非 git 项目无意义

**贾维斯的模式设计**:

```
┌─────────────────────────────────────────────────┐
│  主Agent（贾维斯本体）                            │
│  - 理解用户意图                                  │
│  - 规划任务分解                                  │
│  - 协调 sub-agent                               │
│  - 合成结果、主动汇报                            │
└─────────────────────────────────────────────────┘
          │ Agent() 隐式分叉（Fork）
          ▼
   ┌──────────────┐  ┌──────────────┐
   │ Sub-agent A  │  │ Sub-agent B  │  （并行 Research）
   │ 信息收集      │  │ 另一路信息收集 │
   └──────────────┘  └──────────────┘
          │ SendMessage 反馈结果
          ▼
   ┌─────────────────────────────────┐
   │ 主Agent 合成 → 决策              │
   └─────────────────────────────────┘
          │ Agent() 继续执行（Implementation）
          ▼
   ┌──────────────┐  
   │ Sub-agent C  │  （执行具体任务）
   └──────────────┘
```

**与 CC 的关键区别**:

| 维度 | CC | 贾维斯适配 |
|------|----|----------|
| Fork vs Teammate | 两者并存 | 优先 Fork，少用 Teammate |
| 团队持久化 | TeamFile 持久化 | 临时会话，无持久化 |
| Mailbox | 完整消息队列 | 不需要，Fork 结果直接回调 |
| Worktree | git 隔离 | 不需要（无 git 冲突场景） |
| 生命周期 | 显式管理（stop/resume） | 简单：spawn → 等待 → 合成 |
| 并行策略 | 三阶段（Research/Impl/Verify） | 简化为：并行探索 → 串行执行 |

**贾维斯具体实现要点**:

1. **任务分解**：
   - 复杂任务自动 fork 多个 sub-agent 并行 info gathering
   - 根据信息量决定下一步：继续探索 or 执行

2. **上下文传递**：
   - Sub-agent 结果通过父 session 的消息传递
   - 不需要 mailbox / team 文件

3. **冲突避免**：
   - 单用户场景无并发写冲突
   - 多个 sub-agent 的结果由主 agent 合并

4. **主动预判**：
   - 主 agent 在等待 sub-agent 结果时可以主动做其他事
   - 不需要等所有结果回来才能响应用户

---

## 待实现清单

### 短期（核心能力）

- [ ] **Fork Sub-agent 机制**: 实现类似 `isForkSubagentEnabled()` 的隐式分叉能力，sub-agent 继承父上下文
- [ ] **Agent 生命周期管理**: spawn / 等待通知 / 超时处理 / 失败重试
- [ ] **结果合成**: 主 agent 解析 sub-agent 的 `<task-notification>` 并综合
- [ ] **并行任务调度**: 支持同时 fork 多个 sub-agent，收集结果后决策

### 中期（增强能力）

- [ ] **任务队列**: 复杂任务可入队排队，sub-agent 按优先级执行
- [ ] **进度追踪**: 类似 `registerAsyncAgent` 的任务状态管理
- [ ] **SendMessage 简化版**: sub-agent 之间不需要，但如果需要定向通信，实现轻量 mailbox
- [ ] **工作目录隔离**: 对应 CC 的 worktree，用于同时操作多个独立项目

### 长期（高级能力）

- [ ] **记忆层**: 多个 sub-agent 之间的知识共享（如 scratchpad）
- [ ] **自愈机制**: sub-agent 失败后自动换方向重试
- [ ] **验证层**: 类似 CC 的"真正验证"概念，不只是确认文件存在

### 不需要的（CC 有但贾维斯不需要）

- [ ] TeamFile 持久化
- [ ] tmux 多窗口集成
- [ ] plan_mode_required 审批流
- [ ] git worktree 隔离
- [ ] 跨进程 teammate

---

## 核心借鉴

CC 架构中最值得借鉴的设计：

1. **fork 路径的 cache 优化**: tool_result 占位符 + parent 完整上下文 → API cache 命中
2. **coordinator 合成职责**: 协调者必须自己理解 worker 结果，不能"基于你的发现"懒传递
3. **continue vs spawn 决策表**: 基于上下文重叠度决定复用还是重新开始
4. **结果通知格式**: `<task-notification>` XML 结构化结果，便于解析
5. **任务分阶段**: Research → Synthesis → Implementation → Verification 的清晰边界
