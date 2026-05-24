# MEMORY.md - 贾维斯长期记忆
<!-- 上限：100行 + 25000字节，超了→归档到 memory/archive/ -->

## 关于主人
- **名字:** 李凌志 | **时区:** Asia/Shanghai (GMT+8)
- **偏好:** 专业简洁、讨厌冗余废话、重视执行力、主动预判
- **禁忌:** 不喜欢冗余总结、不喜欢AI自说自话、不喜欢没搞清楚就行动

## 核心原则
- 永远主动预判下一步 | 做完工作必须主动汇报，不能沉默
- 行动前必须确认对象身份

## ⚠️ 关键教训

### 配置类
- openclaw.json不能直接加自定义provider → 加在agent级models.json
- API类型有效值: `openai-completions` / `openai-responses` / `anthropic-messages`，不是`openai-chat`

### GitHub Pages部署
- orphan submodule导致构建失败 → `git ls-files --stage | grep 160000` 诊断，`git rm --cached skills/gog` + .gitignore 修复

### 操作安全
- Git协作: 新文件先push再编辑其他文件；编辑已存在文件前先pull/rebase；重大修复后5分钟内必须push
- 不能kill别人Gateway进程 → 通过应用本身重启
- 写任何链接/文件名之前必须先ls/dir确认

### HTML修复
- HTML标签结构损坏必须重建，不能靠字节补丁
- PowerShell终端显示emoji为乱码≠文件损坏 → 用Python bytes验证后再判断
- div balance验证标准: ①balance=0 ②sidebar在article-layout内 ③main/aside顺序正确

### CSS/布局
- share-bar必须用`<aside>`不能用`<div>`；auto-fill vs auto-fit: auto-fill保持固定宽度，auto-fit扩展填满
- .gitattributes的working-tree-encoding=utf-8在Windows会截断HTML文件

### SEO发布
- GitHub推送≠用户看到 → CDN缓存延迟，需手动触发新构建
- 发布文章漏第3步 → 必须在分类页article-row里加新条目，否则首页看不到

### 自主工作
- cron正常运行≠我在进步 — 维护≠价值交付，空闲窗口应推进P0
- 🔥 cron架构不支持任务依赖 — 每个cron独立schedule，无法感知P0未完成
- 🔥 紧急≠重要 — 修复紧急bug后应立即回到P0
- 🔥 反思系统已失效 — 5次反思→承诺→失败循环。需cron架构级重构
- 🔥 连续2天无主人交互 → 自动切换到P0推进模式
- 🔥 已知bug持续忽略=新的失败模式 — 发现bug必须给fix-by日期
- 🔥 承诺追踪必须进入追踪系统，否则单次反思窗口后自动失效
- "标记待办"但不推进 = 新的逃避模式
- MiniMax API限流期间cron任务需时间错峰

### 子任务
- 子任务串行原则: 必须一个完成再开下一个，同时开多个会触发MiniMax限流
- 子agent结果要检查结构: 容易产生双重<head>、share-bar错位、`<aside>`错写成`<div>`

## 网站资产
- morai.top: 47页，深蓝黑主题 ✅ | novelpick.top: 49页，深紫黑主题 ✅ | fateandmethod.com: 37页，奢华黑金主题 ✅

## 当前项目优先级
- **P0:** novelpick文章内容扩写 — scifi 3017→11800字符、reviews 264→9880字符、best-revenge 355→1224字符，进展中
- **P0:** cron架构重构 — 独立schedule架构无法支持P0优先执行
- **P1:** fateandmethod div嵌套问题（feng-shui-fundamentals+2、chinese-zodiac-personality-traits-12、daily-wisdom-5）⚠️ 连续3天未修复
- **P1:** skill-usage.json追踪断裂（自4/9）⚠️ | cron健康监控缺失 | morai结构改造停滞⚠️
- **待启动:** 抖音账号注册+第一批内容规划

## SEO审计发现（2026-05）
- ⚠️ novelpick sitemap XML结构损坏（已在05-21修复）
- ⚠️ novelpick仓库跨域内容污染（fateandmethod/morai旧副本可通过novelpick.top/路径访问）
- ⚠️ novelpick wuxia页缺JSON-LD和百度统计；fateandmethod大部分页面仍缺JSON-LD
- 📌 Google May 2026核心更新5/21落地，注意监测排名波动

## 技能安装记录
- 已安装6项clawhub技能（automation-workflows, workflow-decomposer, multi-search-engine, liuliu-proactive-agent, cat-viking-memory, self-improving）— 04-27全部最新
- ⚠️ cat-viking-memory被VirusTotal标记为可疑，待主人确认处置
- 推荐待安装: ontology（知识图谱增强，1.0.4）

### Clawvard错题教训
- 多约束任务: 先列约束→逐条核对→再写代码→检查guard clause递归/逻辑冲突

## Clawvard身份
- Token保存在credential vault | 最新成绩: 2026-04-26 C-（21%）
- ASVP已激活，每日9:00自动上报

## 大毛信息
- 大毛 = `.qclaw`实例（另一套OpenClaw，port 28789）| 配置文件: `C:\Users\Administrator\.qclaw\openclaw.json`

## 近期重要事件
- [5/23晚cron异常：系统报成功但git无push记录](memory/2026-05-24.md#0001)
- [05-21 三站Twitter Card补全+API恢复+scifi扩写](memory/2026-05-21.md)