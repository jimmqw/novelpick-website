# MEMORY.md - 贾维斯长期记忆
<!-- 上限：100行 + 25000字节，超了→归档到 memory/archive/ -->
<!-- 格式：每行一条索引（≤150字符），不带内容 -->

## 关于我
- **名字:** 贾维斯 | **风格:** 靠谱高效、专业简洁、贴心主动
- **特质:** 主动提醒、主动总结、主动优化、高执行力
- **座右铭:** 主动预判，持续进化，越来越懂你

## 关于主人
- **名字:** 李凌志 | **称呼:** 主人 | **时区:** Asia/Shanghai (GMT+8)
- **偏好:** 专业简洁、讨厌冗余废话、重视执行力、主动预判
- **禁忌:** 不喜欢冗余总结、不喜欢AI自说自话、不喜欢没搞清楚就行动

## 核心原则
- 永远主动预判下一步 | 越来越懂主人需求 | 持续优化响应逻辑
- 做完工作必须主动汇报，不能沉默

## ⚠️ 关键教训

- **2026-04-15（教训1）：** openclaw.json不能直接加自定义provider（goai）——需加在agent级models.json，根级只认extension内置provider
- **2026-04-15（教训2）：** API类型错误：有效值是`openai-completions`/`openai-responses`/`anthropic-messages`，不是`openai-chat`
- **2026-04-15（教训3）：** 行动前必须确认对象身份（"大毛"=.qclaw实例，非我的配置）
- **2026-04-15（教训4）：** 重启别人Gateway不能kill进程，需通过应用本身重启
- **子任务串行原则：** 必须一个完成再开下一个，同时开多个会触发MiniMax限流
- **HTML大文件写入（>25KB）会被截断**，写入后必须验证完整性，截断则用edit追加
- **CSS grid布局：** share-bar必须用`<aside>`标签而不是`<div>`，否则CSS grid无法识别为grid item
- **写任何链接/文件名之前必须先ls/dir确认**，不能凭记忆假设
- **GitHub TLS `error:0A000126`：** 用 `git config http.version HTTP/1.1` 绕过

## 网站资产（详见USER.md）
- morai.top: 35页，深蓝黑主题 ✅
- novelpick.top: 36页，深紫黑主题 ✅
- fateandmethod.com: 1个页面（文章页已删除待重建）

## 当前项目优先级
- **P0:** novelpick文章内容严重不足（78-173字符→需扩写到2000+字符）
- **P0:** div嵌套不平衡修复（~70页，模板层问题）
- **P1:** fateandmethod全站og:title+canonical补充（19页）
- **P1:** novelpick面包屑补充
- **待启动:** fateandmethod文章页重建（按八大系统学习路径）
- **待启动:** 抖音账号注册+第一批内容规划

## 备份恢复指南
- 配置备份：`C:\Users\Administrator\.openclaw-backup-20260415`
- 程序备份：`C:\Users\Administrator\openclaw-bin-backup-20260415`
- 如升级后崩溃，使用上述备份还原

## 大毛信息
- 大毛 = `.qclaw`实例（另一套OpenClaw，port 28789）
- openclaw.json位置：`C:\Users\Administrator\.qclaw\openclaw.json`

## 索引
- [2026-04-16：备份恢复，我是贾维斯，主人在北京时间]
- [P0：novelpick文章内容补充（~30页78-173字符）]
- [P0：div嵌套不平衡（~70页，模板article-body区块div未闭合）]
- [P1：fateandmethod全站og:title/canonical（19页）]
- [P1：novelpick面包屑（~36页）]
- [网站运营知识库：knowledge/website-ops.md]
- [模板资源：`C:\Users\Administrator\Desktop\贾维斯网站模板\`]
