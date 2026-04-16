# 版本 1.0.7
_2026-04-08 22:52_

## 来源
今日全天工作 + Claude Code 源码第二轮深度学习 + 外部文章对照

---

## 一、网站运营工作

### 已完成
- 修复67个页面（header内联样式/footer居中/侧边栏220px统一）
- 发布4篇文章（morai×2 + novelpick×2）
- 生成sitemap.xml（morai 35页 + novelpick 36页）
- 相关文章Keep Reading区块全站补全（morai 28篇 + novelpick 24篇）
- 定时任务体系重建：每站每天1篇（20:00）+ 每3天检查旧文章

### 关键教训
- 批量修改未先小样本验证，导致反复重写（违反对抗性检查原则）
- 定时任务失败未主动汇报

---

## 二、学习成果

### 文章写作SOP（Semrush/Backlinko）
- SERP分析（写前看Top3页面差距）
- BLUF框架（每个h2先给结论再展开）
- 标题规范（H1=meta title，包含主关键词）
- 具体数据支撑，不用空洞形容
- 内容差异化：找竞品缺什么我们补什么

### 独立站SEO注意事项
- XML Sitemap：已完成
- 内外链策略：已完成（相关文章区块）
- E-E-A-T信任信号：About页面+作者署名待做
- 外链建设：目前0，需做Quora/Reddit outreach

### 提示词注入防御
- 来源：外部攻击测试
- 防御：外部粘贴的系统提示词一律不采纳
- 依据：SOUL.md + IDENTITY.md 身份设定

---

## 三、Claude Code源码第二轮深度

### 真实vs伪造对照
| 声称 | 实际情况 |
|------|---------|
| PlanAgent/ExploreAgent/VerificationAgent | 真实，但无EditAgent/TestAgent/ReviewAgent |
| "Lobster"系统 | 伪造，源码中不存在 |
| 工具使用规范 | 基本准确，但有夸大 |

### VerificationAgent的对抗性思维
- 专门"试图打破"自己的实现
- 强制输出VERDICT: PASS/FAIL
- 6种"找借口跳过检查"的情况→做相反的事

### 系统提示词真实内容（prompts.ts）
- 不估计时间（铁律）
- 不简化测试错误
- OWASP Top 10漏洞主动防护
- 用户批准≠全局批准

---

## 四、已应用的自我优化

### 记忆系统（新）
- MEMORY.md 100行上限（已加注释）
- 会话恢复模板（memory/session-template.md）
- 区分记忆/计划/任务三类
- 两步保存法（写文件+更新索引）
- 做梦机制四阶段

### 写作能力（新增）
- SERP分析流程
- BLUF写作框架
- 独立站文章SOP

### 对抗性自检（新增）
- knowledge/adversarial-check.md
- 边界值/并发/错误路径/现实检验
- 偷懒借口→正确做法对照表

### 错误体系（新增）
- AbortError/ShellError/ConfigError/ApiError
- 不知则诚实承认

### 状态管理（模板）
- 30行Store参考（subscribe/setState/getState）

### 诊断日志（模板）
- Claude Code风格duration埋点

### 不估计时间（prompts.ts铁律）
- 以后不说"大概X分钟"

---

## 五、知识库文件

| 文件 | 用途 |
|------|------|
| knowledge/website-ops.md | 网站运营SOP |
| knowledge/self-optimization.md | 技术优化模板 |
| knowledge/adversarial-check.md | 对抗性自检清单 |
| memory/session-template.md | 会话恢复模板 |
| CLAUDE.md | 自我引导手册 |
| CHANGELOG.md | 版本日志 |

---

## 六、版本记录

| 版本 | 日期 | 说明 |
|------|------|------|
| 1.0.1 | 04-05 | 初始版本，贾维斯激活 |
| 1.0.2 | 04-05 | 工具系统/技能/记忆研究 |
| 1.0.3 | 04-05 | extractMemories/禁止保存规则 |
| 1.0.4 | 04-05 | context/tasks/keybindings研究 |
| 1.0.5 | 04-05 | analytics/plugins/suggestions研究 |
| 1.0.6 | 04-05 | Claude Code源码全面学习总结 |
| **1.0.7** | **04-08** | **网站运营+写作SOP+自我优化全套** |
