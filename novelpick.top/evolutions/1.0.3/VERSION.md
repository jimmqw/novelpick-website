# 版本 1.0.3
_2026-04-05 11:05_

## 来源
Claude Code 泄露源码第三轮深度学习

## 新研究模块

### 1. extractMemories 服务
- 自动记忆提取服务
- 运行时机：每次完整查询结束时（模型产生最终响应且无工具调用）
- 使用forked agent模式（与主会话共享prompt cache）
- 限制工具权限：只允许读写memory目录

### 2. autoDream 服务 (KAIROS)
- 后台记忆整合服务
- 时间门控：每24小时+5个会话
- 需要Gateway配对支持
- 状态：**暂不实施**，等待主人确认

### 3. model/ 模型系统
- 模型选择优先级：会话override > 启动flag > 环境变量 > 设置
- 小型快速模型用于辅助任务
- 支持模型别名解析

### 4. memoryTypes 完整规范

**必须保存:**
- user: 用户角色/目标/偏好
- feedback: 纠正和确认（包含Why和How to apply）
- project: 项目状态/目标/initiative
- reference: 外部系统指针

**禁止保存:**
- 代码模式/架构/文件路径（可从代码推导）
- Git历史（用git log/blame）
- 调试方案（代码里已有）
- CLAUDE.md已有的内容
- 临时任务详情

**记忆漂移处理:**
- 信任观察到的状态 > 记忆
- 使用记忆作为"某时间点的真实情况"上下文
- 发现冲突时更新/删除陈旧记忆

## 可立即应用的优化

### 1. 强化记忆写入规范
更新MEMORY-SYSTEM-V2.md，增加"禁止保存"列表和"记忆漂移处理"规则。

### 2. 自动记忆验证
在读取记忆后，验证记忆与当前状态是否一致。

## 待定优化

### KAIROS后台守护
- autoDream：定期后台整合记忆
- 需要Gateway配对
- 状态：保留，等主人确认

## 包含文件
- MEMORY.md
- AGENTS.md
- SOUL.md
- memory/MEMORY-SYSTEM-V2.md
