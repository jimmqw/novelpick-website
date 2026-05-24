# Claude Code 工具系统研究报告

## 一、工具分类总览

共 **47个工具**，分布在 `src/tools/` 下，分为以下类别：

### 1. Agent / 子智能体 (8个)
| 工具 | 用途 | 关键设计 |
|------|------|----------|
| `AgentTool` | 主智能体运行 | 内置6种子智能体(claudeCodeGuide/explore/generalPurpose/plan/statusline/verification)，支持forkSubagent、内存快照、色彩管理 |
| `TaskCreateTool` | 创建任务 | lazySchema，hook驱动，任务创建后自动展开任务列表 |
| `TaskListTool` | 列出任务 | TodoV2支持 |
| `TaskGetTool` | 获取任务详情 | - |
| `TaskUpdateTool` | 更新任务状态 | - |
| `TaskStopTool` | 停止任务 | - |
| `TaskOutputTool` | 获取任务输出 | - |
| `TeamCreateTool/TeamDeleteTool` | 团队管理 | 支持in-process tmux/subagent多后端 |

### 2. 文件操作 (5个)
| 工具 | 用途 | 关键设计 |
|------|------|----------|
| `FileEditTool` | 编辑文件 | 双指针(old_string/new_string)，quote风格保持，Jupyter检测，文件变更检测，maxResultSizeChars=100k |
| `FileReadTool` | 读取文件 | 编码检测(utf16le/utf8)，offset+limit分片，图片处理 |
| `FileWriteTool` | 写文件 | - |
| `GlobTool` | 文件搜索 | glob模式匹配 |
| `GrepTool` | 内容搜索 | - |

### 3. Shell执行 (3个)
| 工具 | 用途 | 关键设计 |
|------|------|----------|
| `BashTool` | Bash命令 | 最复杂，200+安全检查，tree-sitter AST，权限分类器，sandbox，沙箱 |
| `PowerShellTool` | PowerShell | 类似Bash的权限+验证体系，git安全检查 |
| `REPLTool` | 交互式REPL | primitiveTools子模块，支持多种shell |

### 4. 知识/Web (4个)
| 工具 | 用途 | 关键设计 |
|------|------|----------|
| `WebSearchTool` | 网络搜索 | 模型流式查询，结果schema化 |
| `WebFetchTool` | 抓取网页 | 预批准域名白名单，内容限制 |
| `ReadMcpResourceTool` | 读MCP资源 | - |
| `ListMcpResourcesTool` | 列出MCP资源 | - |

### 5. MCP集成 (2个)
| 工具 | 用途 | 关键设计 |
|------|------|----------|
| `MCPTool` | 通用MCP工具 | 泛型schema(passthrough)，进度追踪 |
| `McpAuthTool` | MCP认证 | - |

### 6. 定时任务 (3个)
| 工具 | 用途 |
|------|------|
| `CronCreateTool` | 创建定时任务 |
| `CronDeleteTool` | 删除定时任务 |
| `CronListTool` | 列出定时任务 |

### 7. 消息发送 (1个)
`SendMessageTool` - 跨agent/团队消息传递

### 8. 技能系统 (1个)
`SkillTool` - 加载+执行外部技能，支持MCP skills/prompts

### 9. 计划/工作流模式 (4个)
`EnterPlanModeTool` / `ExitPlanModeTool` / `EnterWorktreeTool` / `ExitWorktreeTool`

### 10. 其他 (6个)
| 工具 | 用途 |
|------|------|
| `ConfigTool` | 配置读写 |
| `BriefTool` | 附件上传 |
| `NotebookEditTool` | Jupyter notebook编辑 |
| `SyntheticOutputTool` | 合成输出 |
| `SleepTool` | 延迟 |
| `ToolSearchTool` | 工具搜索(延迟加载) |
| `RemoteTriggerTool` | 远程触发 |

---

## 二、设计模式清单

### 2.1 工具工厂模式 (`buildTool()`)

```typescript
// 每个工具都是通过 buildTool() 工厂创建
export const FileEditTool = buildTool({
  name: FILE_EDIT_TOOL_NAME,
  searchHint: '...',        // 3-10词，用于ToolSearch关键词匹配
  maxResultSizeChars: 100_000,
  strict: true,              // 开启严格模式
  inputSchema,              // Zod schema
  outputSchema,
  validateInput,             // 权限前的前置校验
  checkPermissions,         // 权限判断
  call,                     // 执行逻辑
  renderToolUseMessage,
  renderToolResultMessage,
  mapToolResultToToolResultBlockParam,
  // ... 十几个可选钩子
})
```

**关键启发**：贾维斯的技能应统一通过工厂函数创建，所有技能共享同一套生命周期钩子。

### 2.2 权限系统 (三层架构)

```
validateInput()     ← 输入校验(文件存在性、字符串匹配、路径检查)
        ↓
checkPermissions() ← 规则匹配(allow/deny/ask + 前缀/通配符)
        ↓
call()              ← 实际执行
```

**规则匹配优先级**：
1. exact match (精确规则)
2. deny rules (显式拒绝)
3. ask rules (显式询问)
4. path constraints (路径边界)
5. sed constraints
6. mode-specific (readonly等)
7. classifier (Haiku模型)
8. passthrough (用户确认)

### 2.3 BashTool 安全架构 (最完整)

```
命令输入
  ↓
[Phase 1] tree-sitter AST解析
  ├─ too-complex → ask (拒绝复杂结构)
  └─ simple → checkSemantics (语义检查)
        ↓
[Phase 2] 精确规则匹配 (exact match deny/ask/allow)
        ↓
[Phase 3] Haiku分类器 (denyDescriptions/askDescriptions)
        ↓
[Phase 4] 子命令拆分 (splitCommand，max=50)
  ├─ cd+git复合命令检测
  ├─ 多cd检测
  └─ 路径约束检查
        ↓
[Phase 5] 每子命令权限检查
  ├─ 前缀规则匹配
  ├─ pathValidation
  ├─ sedValidation
  └─ readOnlyValidation
        ↓
[Phase 6] Haiku allow分类器 (异步+推测执行)
        ↓
结果: allow / deny / ask / passthrough
```

**关键安全机制**：
- `stripSafeWrappers`: 剥离timeout/time/nice/nohup
- `stripSafeEnvVars`: 剥离安全环境变量
- `SAFE_ENV_VARS` 白名单 (不含PATH/NODE_OPTIONS/PYTHONPATH等)
- `BINARY_HIJACK_VARS` 黑名单
- 命令注入检测: `$()`、反引号、`${}`、heredoc、Zsh特殊命令(zmodload/sysopen/ztcp等)
- 标志混淆检测: ANSI-C `$'...'`、`$"..."`、空引号邻接`""`-、多引子
- `tree-sitter-bash` WASM解析 (回退到legacy正则)
- sandbox沙箱 + auto-allow

### 2.4 Zod Schema 模式

```typescript
// lazySchema - 延迟加载，避免循环依赖
const inputSchema = lazySchema(() =>
  z.strictObject({
    subject: z.string().describe('...'),
    description: z.string().describe('...'),
    metadata: z.record(z.string(), z.unknown()).optional(),
  })
)

// FileEditTool 的复杂schema
inputSchema = z.object({
  file_path: z.string(),
  old_string: z.string(),
  new_string: z.string(),
  replace_all: z.boolean().default(false),
})
```

### 2.5 错误代码模式

```typescript
// FileEditTool 的 errorCode 体系
validateInput() 返回:
  errorCode 0: 团队内存密钥泄露
  errorCode 1: 无变化(old_string === new_string)
  errorCode 2: 路径被deny规则阻止
  errorCode 3: 创建已存在文件
  errorCode 4: 文件不存在
  errorCode 5: Jupyter文件需要NotebookEditTool
  errorCode 6: 文件未读先写
  errorCode 7: 文件在读取后被修改(staleness check)
  errorCode 8: 字符串不匹配
  errorCode 9: 多匹配但replace_all=false
  errorCode 10: 文件过大(>1GB)
```

**启发**：贾维斯技能应使用统一的错误码体系，便于调试和用户反馈。

### 2.6 文件陈旧检测

```typescript
// FileEditTool 在call()前检查
readTimestamp = readFileState.get(fullFilePath)
if (lastWriteTime > readTimestamp.timestamp) {
  // 时间戳变化，但内容可能未变(云同步等)
  if (fileContent === readTimestamp.content) {
    // 内容一致，安全继续
  } else {
    // 真变更，拒绝
  }
}
```

### 2.7 推测执行 (Speculative Execution)

```typescript
// BashTool: 在用户确认前就启动分类器检查
startSpeculativeClassifierCheck(command, ...)  // 提前启动
// ...
consumeSpeculativeClassifierCheck(command)     // 快速消费结果
executeAsyncClassifierCheck(...)               // 异步执行，auto-approve
```

### 2.8 延迟加载 (Deferral)

```typescript
// ToolSearchTool 工具延迟加载
shouldDefer: true  // 首次不加载，需要ToolSearch触发
alwaysLoad: true   // 始终加载(不延迟)
```

### 2.9 工具别名

```typescript
aliases?: string[]  // 向后兼容工具重命名
```

### 2.10 分类标签系统

```typescript
// 每个工具可声明自己的分类
isSearchOrReadCommand?(input) → { isSearch, isRead, isList }
isOpenWorld?(input) → boolean  // 是否联网
isConcurrencySafe?() → boolean // 是否可并发
isDestructive?(input) → boolean  // 是否破坏性
```

### 2.11 共享基础设施

```
src/tools/shared/
├── gitOperationTracking.ts   # Git操作计量(commit/push/PR)
├── spawnMultiAgent.ts        # 跨agent/团队创建(支持tmux/in-process)
```

---

## 三、贾维斯可借鉴点

### 高优先级 (可直接迁移)

| 模式 | 当前贾维斯状态 | 实施建议 |
|------|--------------|---------|
| **工具工厂模式** | 无统一工厂 | 创建 `createSkill()` 工厂，统一生命周期(validate/prepare/execute/render) |
| **Zod Schema** | 部分使用 | 全面迁移，所有技能输入输出必须schema化 |
| **lazySchema** | 未使用 | 避免循环依赖，技能间解耦 |
| **错误码体系** | 杂散错误 | 建立 `JErrorCode` 枚举，按技能分类 |
| **validateInput + checkPermissions 分离** | 混用 | validateInput做输入校验，checkPermissions做权限决策 |

### 中优先级 (需适配)

| 模式 | 说明 | 贾维斯适配方案 |
|------|------|--------------|
| **文件staleness check** | 读写之间检测文件变更 | 适用于技能涉及文件系统操作的场景 |
| **推测执行** | 提前启动耗时验证 | 适用于网络请求类技能 |
| **maxResultSizeChars** | 结果截断+持久化 | 贾维斯大结果(视频生成等)需此机制 |
| **searchHint** | 工具搜索关键词 | 技能发现机制可借鉴 |
| **shouldDefer/alwaysLoad** | 按需加载 | 大型技能(如CapCut)可延迟加载 |

### 低优先级 (架构参考)

| 模式 | 说明 |
|------|------|
| **tree-sitter AST安全** | 命令执行类技能(Shell/PowerShell)需类似架构 |
| **多分类器并行** | Haiku deny+ask并行检查，allow异步推测 |
| **命令前缀提取** | `getSimpleCommandPrefix` 自动生成权限规则建议 |
| **工具别名** | 技能版本迭代时的向后兼容 |

### BashTool安全检查清单 (可直接复制的检测项)

```
□ 空白/不完整命令检测
□ 命令注入: $() / `` / ${} / <() / =() 
□ Heredoc安全模式检测
□ Git commit消息注入
□ jq system()函数
□ 标志混淆: ANSI-C $'...' / 空引目 / 多引子
□ 反斜杠转义操作符 \;\ |\&
□ 路径遍历 (\../)
□ IFS注入
□ Zsh危险命令 (zmodload/zpty/ztcp/emulate fc -e)
□ 回车符CR注入 (shell-quote vs bash tokenization差异)
□ brace expansion {a,b} 解析差异
□ Unicode空格
□ mid-word # (注释vs内容)
□ 评论内引号导致的引号状态去同步
□ 带引号换行符 (stripCommentLines bypass)
□ 进程替换 /proc/environ访问
□ 复合命令cd+git检测 (bare repo攻击)
□ tree-sitter vs 正则解析的分歧计量
```

---

## 四、贾维斯技能开发建议架构

```typescript
// 贾维斯技能基础接口
interface JarvisSkill<Input, Output> {
  // 标识
  name: string
  aliases?: string[]
  searchHint?: string
  
  // Schema
  inputSchema: LazyZodSchema<Input>
  outputSchema: LazyZodSchema<Output>
  
  // 生命周期
  validate?(input: Input, context: JarvisContext): ValidationResult
  checkPermissions?(input: Input, context: JarvisContext): PermissionResult
  prepare?(input: Input, context: JarvisContext): Promise<void>
  execute(input: Input, context: JarvisContext): Promise<ToolResult<Output>>
  
  // UI渲染
  renderUse?(input: Input): ToolUseBlockParam
  renderResult?(output: Output): ToolResultBlockParam
  
  // 分类
  isSearchOrRead?(input: Input): { isSearch: boolean; isRead: boolean }
  isOpenWorld?(input: Input): boolean
  isDestructive?(input: Input): boolean
  maxResultSize?: number  // 默认100k
  
  // 加载策略
  shouldDefer?: boolean
  alwaysLoad?: boolean
}

// 错误码枚举
enum JarvisErrorCode {
  // 通用
  INVALID_INPUT = 1000,
  PERMISSION_DENIED = 1001,
  FILE_NOT_FOUND = 1002,
  FILE_MODIFIED = 1003,
  FILE_TOO_LARGE = 1004,
  // 技能特定码在各自模块定义
}
```

---

## 五、总结

Claude Code的工具系统设计极为成熟，核心价值：

1. **统一抽象** - 47个工具共享同一工厂和生命周期
2. **安全深度** - BashTool展示了如何在灵活性和安全性之间取得平衡
3. **渐进式校验** - validateInput → checkPermissions → execute，每层可独立决策
4. **用户体验** - 详细的错误消息、errorCode、文件staleness check、suggestion系统
5. **工程严谨** - lazySchema防循环依赖、错误码体系、feature flag控制、telemetry

贾维斯应优先迁移工厂模式+Zod Schema+错误码体系，这是技能系统化的基础。
