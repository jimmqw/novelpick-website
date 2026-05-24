# 工具踩坑记录

## PS1文件编码问题
- 日期：2026-04-06
- 问题：PowerShell脚本含中文字符时解析失败
- 原因：PS1文件解析器对中文支持有问题
- 解决：改用node.js执行HTTPS请求

## node HTTPS超时
- 日期：2026-04-06
- 问题：clawvard.school网络请求超时
- 解决：增加超时时间、重试机制

## exec命令编码
- 日期：2026-04-06
- 问题：&& 和 || 在PowerShell解析有问题
- 解决：用分号分隔或单独命令

---

## 检索不完整导致错误汇报
- 日期：2026-04-07
- 问题：汇报技能数量时只检查了workspace/skills，漏掉~/.openclaw/skills/，导致27→51的严重错误
- 原因：没有按TOOLS.md规范完整检索三个路径
- 教训：汇报任何清单前，必须检查所有三个位置：workspace/skills + ~/.openclaw/skills/ + npm/node_modules/openclaw/extensions/
- 状态：已记录，以后汇报前先确认路径完整性

_最后更新：2026-04-07_
