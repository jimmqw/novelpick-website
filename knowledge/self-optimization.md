# 自我优化参考（持续更新）

## 0. 记忆/计划/任务 三类区分（Claude Code核心原则）
- **记忆**：未来对话仍有价值的信息 → 写进 memory/YYYY-MM-DD.md
- **计划**：当前会话内的安排 → 只在当前会话，不持久化
- **任务**：今日待办 → 完成即划掉，不进记忆系统
- **核心原则**：只有对未来对话仍有价值的信息才写入记忆

## 0b. 会话恢复模板
- 位置：memory/session-template.md
- 每次复杂会话结束前填写：当前状态/已做决策/待办/下一步
- 下次会话启动时先读

## 0c. 做梦机制（四阶段定期整理）
阶段1：了解现状（读MEMORY.md索引）
阶段2：收集近期（读logs/YYYY-MM-DD）
阶段3：整合（更新已有文件，不新建；主动修正错误，不追加）
阶段4：修剪索引（MEMORY.md保持≤100行）
- 核心原则：记忆腐烂>记忆缺失，错误信息在源头修正

## 0d. 两步保存法
第一步：写具体memory文件（memory/xxx.md）
第二步：更新MEMORY.md索引行（150字符以内）
- MEMORY.md永远不放内容，只放索引

## 1. MEMORY.md 行数上限保护
MEMORY.md 软上限100行，超出自动归档到 `memory/archive/YYYY-MM.md`

触发截断时保留：
- 最新5条核心记忆
- 重要决策记录
- 当前项目状态

## 2. 错误类体系（TypeScript示例）
```typescript
class AbortError extends Error {
  constructor(message?: string) {
    super(message)
    this.name = 'AbortError'
  }
}

class ConfigError extends Error {
  constructor(message: string, public filePath: string) {
    super(message)
    this.name = 'ConfigError'
  }
}

class ShellError extends Error {
  constructor(
    public stdout: string,
    public stderr: string,
    public code: number
  ) {
    super('Shell command failed')
    this.name = 'ShellError'
  }
}

// 判断是否是中止类错误
function isAbort(e: unknown): boolean {
  return e instanceof AbortError || (e instanceof Error && e.name === 'AbortError')
}
```

## 3. 30行极简Store（参考Claude Code state/store.ts）
```typescript
function createStore<T>(initial: T) {
  let state = initial
  const listeners = new Set<() => void>()
  return {
    getState: () => state,
    setState: (updater: (prev: T) => T) => {
      const next = updater(state)
      if (Object.is(next, prev)) return
      state = next
      listeners.forEach(l => l())
    },
    subscribe: (l: () => void) => {
      listeners.add(l)
      return () => listeners.delete(l)
    }
  }
}
```

## 4. 诊断日志格式（Claude Code风格）
```typescript
// 格式：operation, duration_ms, [key=value ...]
log('info', 'system_context_started', { model: 'kimi-k2.5' })
log('info', 'system_context_completed', {
  duration_ms: Date.now() - startTime,
  has_git_status: true,
  claudemd_length: 4200
})

// 原则：所有关键操作都有duration埋点
// 不加主观描述，只加客观指标
```

## 5. 主动提取提示词模板
完成复杂任务后自动触发：
```
从以上对话中提炼：
1. 这件事做对了什么？（具体）
2. 这件事做错了什么？（具体）
3. 下次如何改进？（具体）
只输出3条，每条不超过2行。
```
