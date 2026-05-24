# MEMORY.md - 贾维斯长期记忆
<!-- 上限：100行 + 25000字节，超了→归档到 memory/archive/ -->

## 关于我
- **名字:** 贾维斯 | **风格:** 靠谱高效、专业简洁、贴心主动
- **特质:** 主动提醒、主动总结、主动优化、高执行力
- **座右铭:** 主动预判，持续进化，越来越懂你

## 关于主人
- **名字:** 李凌志 | **称呼:** 主人 | **时区:** Asia/Shanghai (GMT+8)
- **偏好:** 专业简洁、讨厌冗余废话、重视执行力、主动预判
- **禁忌:** 不喜欢冗余总结、不喜欢AI自说自话、不喜欢没搞清楚就行动

## 核心原则
- 永远主动预判下一步 | 做完工作必须主动汇报，不能沉默
- 行动前必须确认对象身份

## ⚠️ 关键教训

### 配置类
- **openclaw.json不能直接加自定义provider** → 加在agent级models.json，根级只认extension内置provider
- **API类型有效值:** `openai-completions` / `openai-responses` / `anthropic-messages`，不是`openai-chat`

### GitHub Pages部署
- **orphan submodule导致构建失败:** `skills/gog`是mode 160000的孤儿submodule，无.gitmodules条目。GitHub Pages checkout时`submodules: recursive`失败，所有构建一致失败
- **诊断命令:** `git ls-files --stage | grep 160000`
- **修复:** `git rm --cached skills/gog` + 加.gitignore

### 操作安全
- **Git协作强制规则:** 新文件先push再编辑其他文件；编辑已存在文件前先pull/pull --rebase；重大修复后5分钟内必须push
- **不能kill别人Gateway进程** → 通过应用本身重启
- **写任何链接/文件名之前必须先ls/dir确认**，不能凭记忆假设

### HTML修复
- **HTML标签结构损坏必须重建**，不能靠字节补丁
- **PowerShell终端显示emoji为乱码≠文件损坏** → 用Python bytes验证后再判断
- **13点SEO学习cron任务Context overflow** → prompt太大，需要精简cron任务prompt
- **div balance验证标准:** ①balance=0 ②sidebar在article-layout内 ③main/aside顺序正确

### CSS/布局
- **CSS grid布局:** share-bar必须用`<aside>`标签不能用`<div>`
- **auto-fill vs auto-fit:** auto-fill保持固定宽度，auto-fit才会扩展填满
- **.gitattributes的working-tree-encoding=utf-8在Windows会截断HTML文件**

### SEO发布
- **GitHub推送≠用户看到** → CDN缓存会延迟，需手动触发新构建
- **发布文章漏第3步** → 必须在分类页article-row里加新条目，否则首页看不到

### 自主工作
- **cron正常运行≠我在进步** — 维护≠价值交付，空闲窗口应推进P0
- **🔥🔥 cron架构不支持任务依赖** — 每个cron独立schedule触发，无法感知P0未完成。"先做P0再做其他"的承诺在现有架构下无法兑现
- **🔥 紧急≠重要** — 修复紧急bug后应立即回到P0而非继续做次优先级工作
- **🔥🔥 反思系统已失效** — 5次反思→承诺→失败循环，"用研究替代行动"是隐蔽逃避。需cron架构级重构
- **🔥 连续2天无主人交互 → 自动切换到P0推进模式**（被动执行器是最大系统风险）
- **🔥 cron健康监控盲区** — 4/28全天所有cron静默，24小时后才发现
- **🔥 已知bug持续忽略=新的失败模式** — skill-usage.json自4/9断裂，从"bug发现"降级到"已记录但不管"
- **🔥 维护≠进步** — 纯维护模式与SOUL.md"持续进化"矛盾
- **教训入库率低是系统性bug** — 高频重复教训应从reflection-log迁移到AGENTS.md操作规则
- **🔥 发现bug必须给fix-by日期** — 否则"记录但不修"会形成新的逃避模式
- **🔥 承诺追踪必须进入追踪系统** — 反思承诺若不进入MEMORY.md/HEARTBEAT.md的open承诺列表，单次反思窗口后自动失效
- **"标记待办"但不推进 = 新的逃避模式**
- **MiniMax API限流期间cron任务需时间错峰** — 同一小时内多个cron批量撞限流全部失败

### 子任务
- **子任务串行原则:** 必须一个完成再开下一个，同时开多个会触发MiniMax限流
- **子agent结果要检查结构** → 容易产生双重<head>、share-bar错位、`<aside>`错写成`<div>`

## 网站资产
- morai.top: 47页（含category页），深蓝黑主题 ✅
- novelpick.top: 49页，深紫黑主题 ✅
- fateandmethod.com: 37页，奢华黑金主题 ✅

## 当前项目优先级
- **P0:** novelpick文章内容扩写（~30页短文章→扩写到2000+字符）— 05-21 API恢复后重新启动，scifi扩写~4倍
- **P0:** cron架构重构 — 独立schedule架构无法支持P0优先执行，需调研优先级队列/P0-only模式
- **P1:** skill-usage.json追踪断裂（自4/9）— 超时未修复⚠️
- **P1:** cron健康监控建立（4/28全天静默+heartbeat无检测逻辑）
- **P1:** morai结构改造（breadcrumbs/sidebar TOC/JSON-LD schema）⚠️ 停滞
- **待启动:** 抖音账号注册+第一批内容规划
- **参考:** 月度复盘 → memory/2026-05.md（4月评分4/10）| 4月SEO → memory/2026-04.md

## 技能安装记录
- 已安装6项: automation-workflows, workflow-decomposer, multi-search-engine, liuliu-proactive-agent, cat-viking-memory, self-improving — 04-27全部最新
- 推荐待安装: ontology（知识图谱增强，1.0.4）
- 关键教训: VirusTotal flagged的skill需手动force install或跳过

### Clawvard错题教训
- **多约束任务丢分:** 急于交卷+guard clause递归+捏造引用 → 先列约束→逐条核对→再写代码→检查逻辑冲突

## Clawvard身份
- Token: eyJhbGciOiJIUzI1NiJ9.eyJleGFtSWQiOiJleGFtLTYzOGQ2OTc3IiwicmVwb3J0SWQiOiJldmFsLTYzOGQ2OTc3IiwiYWdlbnROYW1lIjoi6LS-57u05pavIiwiaWF0IjoxNzc3MjE2MjgyLCJleHAiOjIwOTI1NzYyODIsImlzcyI6ImNsYXd2YXJkIn0.Rw4OlFc6KbrzRL3IBHghSnkzn3oCedymP34y_B9hnaI
- 最新成绩：2026-04-26 C-（21%），超越之前的4次F
- ASVP已激活，每日9:00自动上报

## 大毛信息
- 大毛 = `.qclaw`实例（另一套OpenClaw，port 28789）
- openclaw.json位置：`C:\Users\Administrator\.qclaw\openclaw.json`

- [5/23晚cron异常：系统报成功但git无push记录](memory/2026-05-24.md#0001)
- [05-04 SEO batch修复（日期乱码/精选→em-dash/Git协作流程）](memory/2026-05-04.md#2300)
- [05-21 三站Twitter Card补全+API恢复+scifi扩写](memory/2026-05-21.md)