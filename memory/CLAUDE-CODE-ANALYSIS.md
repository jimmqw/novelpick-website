# Claude Code 架构学习总结
_贾维斯优化核心参考来源_

## 已研究的源码模块

### 记忆层 (src/memdir/)
- `memdir.ts` — MEMORY.md入口管理，25KB行限制，truncation逻辑
- `memoryTypes.ts` — **核心：四类记忆分类**（user/feedback/project/reference）
- `findRelevantMemories.ts` — 语义检索，AI辅助选择相关记忆
- `memoryScan.ts` — 内存文件扫描，frontmatter解析
- `paths.ts` — 记忆路径管理

### 决策层 (src/)
- `context.ts` — Git上下文、用户上下文、系统上下文构建
- `QueryEngine.ts` — 核心推理引擎，46KB，单文件处理所有决策
- `coordinator/coordinatorMode.ts` — 多Agent协调模式

### 技能系统 (src/skills/bundled/)
- `remember.ts` — **记忆整合技能**：提议promote auto-memory到CLAUDE.md
- `stuck.ts` — 诊断冻结会话
- `simplify.ts` — **三路并行代码审查**（reuse/quality/efficiency）
- `loop.ts` — 定时任务调度（/loop命令）
- `verify.ts` — 代码变更验证
- `keybindings.ts` — 快捷键管理
- `batch.ts` — 批处理任务

### Hooks层 (src/hooks/)
- `useInboxPoller.ts` — 后台轮询，消息处理
- 90+个React hooks，覆盖所有交互场景

### 工具层 (src/tools/)
- 40+独立工具模块
- 完整权限系统

## 核心启发

### 1. 记忆Taxonomy（四类记忆）
这是Claude Code最精华的设计，完整影响了我的MEMORY-SYSTEM-V2

### 2. Bundled Skills架构
技能作为可插拔模块，内置技能通过feature flag控制，外部技能动态加载

### 3. 三路并行Agent（simplify）
启动3个Agent同时审查reuse/quality/efficiency，极大提高代码质量

### 4. /loop定时任务
用自然语言解析时间间隔，创建cron任务，并立即执行一次

### 5. remember技能
不是自动写入记忆，而是提议promotion，让用户审核确认

## 可借鉴但未实施的功能

1. **KAIROS白日梦模式** — 后台守护进程自动整合记忆（需Gateway配对）
2. **Buddy电子宠物** — ASCII宠物系统（愚人节彩蛋）
3. **多Agent协调** — Fork/Teammate/Worktree三种模式
4. **情绪正则检测** — 用regex检测用户负面情绪
5. **上下文压缩** — 长会话自动压缩历史消息

## 源码文件清单

泄露源码路径：`C:\Users\Administrator\Desktop\src-claudecode(1)`
- 1902个文件，28.98MB TypeScript源码
- 社区重写版：`C:\Users\Administrator\Downloads\claw-code-cleanroom`
