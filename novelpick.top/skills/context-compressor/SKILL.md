# Context Compressor Skill

## 触发条件（任一满足）
- 单个 session 消息数超过 150 条
- cron 每4小时检查一次活跃 session
- 手动调用：`/compress` 或 "帮我压缩上下文"

## 压缩流程

### Step 1: 评估
通过 `sessions_list` 获取所有活跃 session 的消息数。

### Step 2: 读取需要压缩的 session
通过 `sessions_history` 读取目标 session 的完整历史（limit=200）。

### Step 3: 生成摘要
将前 N 条消息（保留最近50条）压缩为3-5句核心信息摘要，格式：
```
[压缩摘要 YYYY-MM-DD]
- 关键决策：[决策1] / [决策2]
- 重要事实：[事实1] / [事实2]
- 进行中任务：[任务描述]
```

### Step 4: 保存摘要
写入 `memory/session-compressions/YYYY-MM-DD-[sessionKey简写].md`

### Step 5: 通知主人
告诉主人："Session [名称] 上下文已压缩，节省了约 X 条消息的 token 占用。"

## 保留规则
- 最近 50 条消息**不压缩**，保留原始上下文
- 消息中的工具调用结果**优先保留**
- 记忆文件路径和决策结论**必须保留**

## 限制
- 不压缩当前正在进行的对话（只压缩已完成或空闲 session）
- 单次压缩不超过 200 条历史消息
