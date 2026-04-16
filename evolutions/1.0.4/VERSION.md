# 版本 1.0.4
_2026-04-05 11:15_

## 来源
Claude Code 泄露源码第四轮学习

## 新研究模块

### 1. context.ts - 上下文构建
- getSystemContext(): Git状态、缓存中断注入
- getUserContext(): CLAUDE.md加载、当前日期
- memoize缓存机制

### 2. BashTool - 工具实现范例
- buildTool() 工厂函数创建工具
- isReadOnly() 命令验证
- 安全沙箱机制
- 进度显示阈值（2秒后显示）

### 3. tasks/ - 任务系统
- LocalAgentTask: 本地后台Agent
- DreamTask: 记忆整合任务
- RemoteAgentTask: 远程Agent
- 任务状态机设计

### 4. keybindings/ - 快捷键系统
- 默认快捷键定义
- 用户自定义覆盖
- 平台适配（Windows/Mac/Linux）

## 核心架构发现

### Tool架构
```typescript
// 工具定义模式
const Tool = buildTool({
  name: 'tool_name',
  description: (input, context) => z.string(),
  isEnabled: () => boolean,
  render: (props) => JSX,
  handle: async (input, context) => {
    // 工具逻辑
    return { content: [...] }
  }
})
```

### Context构建模式
- System context: Git状态、缓存控制
- User context: CLAUDE.md、日期时间
- 双重memoize缓存（系统+用户）

## 待定优化

### 1. 技能注册表系统
建立类似 registerBundledSkill 的技能注册表
- 技能元数据（名称、描述、启用条件）
- 动态启用/禁用

### 2. 工具权限系统
学习 Claude Code 的 canUseTool 权限模式
- 预检查工具权限
- 交互式权限请求
- 自动模式拒绝处理

### 3. 任务状态机
建立自己的后台任务状态管理

## 包含文件
- MEMORY.md
- AGENTS.md
- SOUL.md
- memory/MEMORY-SYSTEM-V2.md
