# 记忆系统 V2（memdir启发）

## 架构

```
MEMORY.md                    ← 索引入口（≤100行，≤25000字节）
memory/
  YYYY-MM-DD.md             ← 每日日志
  session-template.md        ← 会话恢复
  archive/                  ← 归档
knowledge/
  *.md                      ← 专题知识库
evolutions/
  1.0.X/VERSION.md         ← 版本历史
```

## Frontmatter格式（所有memory文件）

新记忆文件必须包含：

```yaml
---
name: 标题
description: 一句话说明这个记忆是关于什么的
type: user | feedback | project | reference
created: YYYY-MM-DD
updated: YYYY-MM-DD
---
```

- `type`只能是这四类，不扩展
- 发现错误：直接修正，不追加"更正"
- 查重：写新记忆前，先看是否有同类文件，有则更新而非新建

## MEMORY.md 索引规范

- **硬上限**：≤100行 AND ≤25000字节
- 超了→做梦机制自动归档
- 每条索引格式：`- [标题](memory/xxx.md) — 一行钩子（≤150字符）`
- MEMORY.md本身只放索引，不放内容

## 双步保存（必须遵守）

**Step 1**：写具体memory文件（memory/xxx.md，带frontmatter）
**Step 2**：更新MEMORY.md索引行

禁止把记忆内容直接写进MEMORY.md。

## 禁止写入记忆的内容（来自源码memdir.ts）

- 代码路径、Git历史、调试方案
- 可以从当前项目状态推导出的事实
- 主观判断而非客观事实

## 查重规则

写新记忆前，先：
1. 搜索knowledge/和memory/中是否已有同类主题
2. 有→更新已有文件（修正错误）
3. 无→新建文件

## 字节检查

MEMORY.md超过25000字节时，在文件顶部加warning：
```
<!-- ⚠️ MEMORY.md接近上限，请运行做梦机制整理 -->
```
