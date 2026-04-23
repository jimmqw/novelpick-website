# Reflection Log

<!-- Append-only record of reflection cycles. -->
<!-- Meta-reflection reads this to understand evolution. -->

## Reflection #18 — 2026-04-20

### Status
- **Outcome**: approved
- **Tokens used**: 8,000 (baseline)
- **Memories processed**: 2 episodes (Apr 19-20)

### 做得好的3件事
1. **精准HTML修复**：novelpick 3个页面div修复，一次到位，无副作用
2. **主动发现关键SEO bug**：best-apocalypse-survival页面meta description在"civili"处截断，主动修复
3. **OUTREACH-KIT.md主动建设**：超出任务要求，主动建立完整外链工具包（模板+策略+清单），主人可直接执行

### 可改进的3件事
1. **计划执行不彻底**：Day 5"技术SEO巡检"（truncated description跨站检查+morai死链batch 4）未完成，被新任务（OUTREACH-KIT）打断
2. **子任务串行原则执行不一致**：有时代码一顿输出后才想起来"应该先完成一件事再做下一件"
3. **外部工具受限意识不足**：browser/web_fetch无法访问外网这个限制，应该在OUTREACH-KIT创建前就预判到，而不是做完才发现需要主人手动执行

### 关键教训
- PowerShell数组pop操作坑：1元素数组用`$stack[0..(.Count-2)]`会产生@(0,-1)——用System.Collections.ArrayList的RemoveAt()
- novelpick duplicate URL澄清：apocalypse vs apocalyptic是完全不同内容，无需canonical合并
- morai footer标准bug模式：share-section后有多余</div>，批量修复时已掌握规律

### 下次注意
- 任务切换前确认：当前计划任务是否已完成？打断前先问"是否需要先完成当前计划？"
- 外部工具能力边界：web_fetch/browser失效时，立即标记"需主人手动执行"

### MEMORY.md更新
- 无需大改，今日教训已记录在案（PowerShell坑→已有教训）
- 今日OUTREACH-KIT.md是新建文件，已在USER.md无记录（OUTREACH-KIT.md属workspace内部文件，主人需知道有这东西）

---

## Reflection #19 — 2026-04-21

### Status
- **Outcome**: approved
- **Tokens used**: 8,000 (baseline)
- **Memories processed**: 1 episode (Apr 21)

### 做得好的3件事
1. **正确诊断而非盲目修复**：meihua.html用Python bytes对比git版本，验证字节完全一致，避免了不必要的"修复"（4个U+FFFD都在CSS content属性里，不影响渲染）
2. **根本原因分析到位**：daily-wisdom.html布局错乱的根因是`</div>`被截断成部分字节，fetch live page提取干净内容后完整重建整个tips section
3. **主动记录重要发现**：PowerShell/GBK终端显示emoji为乱码≠文件损坏，需用Python bytes检查——这条经验直接防止了误判

### 可改进的3件事
1. **Cron执行失败率高**：每日23点总结、每日反思GoingToSleep、每日SEO学习三个cron连续error，没有主动调查失败原因
2. **cron任务失败后无重试/上报机制**：13:00 SEO学习cron报告"编辑knowledge/website-ops.md失败（内容已生成但保存失败）"，这种半失败状态应该标记并重试，而非忽略
3. **P0任务novelpick文章扩充一直未启动**：连续多天挂在待办里，主人没有手动帮我推进，应该主动问"novelpick文章扩充是否还P0优先级？需要我用什么方式推进？"

### 关键教训
- **HTML标签结构损坏必须重建**：字节补丁无法修复结构损坏，必须fetch干净内容后重建整个区块（教训：daily-wisdom完整重建）
- **PowerShell GBK终端显示乱码≠文件损坏**：用Python bytes检查更可靠
- **Cron半失败状态也是失败**：内容生成但保存失败 = 任务失败，需标记重试

### 下次注意
- Cron error连续出现时，主动在heartbeat里调查并汇报
- P0任务长期未动时，主动向主人确认优先级和推进方式
- 任何"内容生成但保存失败"都应视为任务失败，记录并重试

### MEMORY.md更新
- 无重大更新，今日教训已补充到MEMORY.md关键教训区：
  - 新增："HTML标签结构损坏必须重建，不能靠字节补丁"
  - 新增："PowerShell终端显示emoji为乱码≠文件损坏，应用Python bytes验证"

---

<!-- Format:

## Reflection #N — YYYY-MM-DD

### Status
- **Outcome**: approved / partial / rejected
- **Tokens used**: X / 8,000
- **Memories processed**: N episodes, N entities, N procedures

### Key Changes
- [Brief summary]

### Philosophical Insight
- [Main insight from meta-reflection]

### Threads Touched
- Continued: [thread from evolution.md]
- New: [new thread opened]

### Notes for Future
- [What to pay attention to next time]

-->


<!-- Meta-reflection reads this to understand evolution. -->

<!-- Format:

## Reflection #N — YYYY-MM-DD

### Status
- **Outcome**: approved / partial / rejected
- **Tokens used**: X / 8,000
- **Memories processed**: N episodes, N entities, N procedures

### Key Changes
- [Brief summary]

### Philosophical Insight
- [Main insight from meta-reflection]

### Threads Touched
- Continued: [thread from evolution.md]
- New: [new thread opened]

### Notes for Future
- [What to pay attention to next time]

-->
