# Session: 2026-04-19 14:44:40 UTC

- **Session Key**: agent:main:main
- **Session ID**: 81ffb2af-5fbd-4a82-8af6-da4af867f0af
- **Source**: webchat

## Conversation Summary

assistant: 

**不是同一个东西。**

| | 价格（输入/输出） |
|---|---|
| **GPT-5.4-nano** | $0.2 / $1.25 |
| **Codex专属** | $2.07 / $12.42 |

差了约10倍。**GPT-5.4-nano是轻量版**，便宜但能力弱；**Codex是编程专用模型**，贵但强很多。

而且第二个表里那些分组（default/官转/BLT等）是不同渠道代理，价格各不相同。BLT-origin最贵（$27/$216），default最便宜（$2/$12）。

你想用来做什么？编程的话Codex合适，普通对话用nano够用。
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Sat 2026-04-18 00:07 GMT+8] Seedance 2.0 和即梦 3.5 Pro是同一个吗？
assistant: 


**不是同一个东西。**

- **Seedance 2.0** = 字节跳动官方视频生成模型，底层模型
- **即梦** = 字节旗下的AI创作工具（产品），底层调用Seedance

简单说：即梦是外壳，Seedance是内核。

即梦 3.5 Pro 用的是 Seedance 2.0，类似iPhone用的是苹果芯片。
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Sat 2026-04-18 00:09 GMT+8] 都是用的Seedance 2.0那不就是一样的东西吗？
assistant: 

你说得对。对于**使用者**来说没区别，都是调用Seedance 2.0，效果一样。

区别在于：
- **即梦** = 现成产品（网页/App），直接用
- **Seedance** = 底层API，给开发者调用的

普通用户用即梦就行。开发者才需要 Seedance API。
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Sat 2026-04-18 00:10 GMT+8] wan2.7-i2v
wan2.7系列的图生视频功能，稳定保持图像主体、风格和文字等细节信息
API
视频生成
价格:
￥0.7/秒 起
这个和万相 2.6 参考生
万相2.6官方版参考生视频模型，支持上传参考图片提取角色形象，生成单角色或多角色互动视频。提供快速和高质量两档画质，支持720P/1080P分辨率，最长可生成10秒视频。

什么是智能调度？
了解价格优先、速度优先、成功率优先的区别
官方直连
按次
单次价格
⚡0.3105
24h成功率
100%
24h响应
145.43s这个的价格差别好大啊
assistant: 

**单位不一样：**
- wan2.7 = **¥0.7/秒**
- 万相 = **¥0.31/次**（不是秒）

如果生成10秒视频：
- wan2.7：约 ¥7
- 万相：约 ¥0.31

**差20多倍**，万相便宜很多。

不过效果也有差别，万相是"参考生"（参考图提取角色），wan2.7是纯图生视频。用途不同，价格自然不同。
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Sat 2026-04-18 00:12 GMT+8] 官方什么价格？
assistant: 

搜不到阿里云万相2.6的官方价格（可能没公开或我没权限）。

**估算：**
- 行业惯例：AI视频生成约 **¥1-3/秒**
- 聚合平台 ¥0.31/次 属于**地板价**，可能是：
  1. 补贴引流
  2. 扣了生成时长（实际可能只算几秒）
  3. 低质量模式

建议直接问那个平台客服，确认"0.31/次"具体生成几秒、什么画质。
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Sat 2026-04-18 00:19 GMT+8] qwen3.5-plus
阿里巴巴推出的Qwen3.5系列，支持多模态
模型
语言大模型
Model capability: image
Model capability: video
Model capability: thinking
Model capability: function_call
 输入:
￥0.84/1M tokens起
 输出:
￥4.83/1M tokens起和
千问 3.5 Plus
阿里云百炼千问3.5 Plus，原生多模态旗舰模型，支持100万Token超长上下文、深度思考与联网搜索，具备图片/视频多模态理解能力，在复杂推理、代码编程与结构化输出上表现优异。

什么是智能调度？
了解价格优先、速度优先、成功率优先的区别
官方渠道
按token
输入价格
⚡2.9568/百万token
输出价格
⚡17.7408/百万token
24h成功率
100%
24h响应
4.22s这两个价格差距好大
assistant: 

**差很多：**

| | 输入 | 输出 |
|---|---|---|
| **聚合平台** | ¥0.84 | ¥4.83 |
| **官方渠道** | ¥2.96 | ¥17.74 |

聚合便宜约3-4倍。可能原因：
1. **官方直连 vs 套壳** — 聚合可能用特殊渠道/优惠
2. **计量方式不同** — 官方按token，聚合可能按次/按问题
3. **限量优惠** — 聚合的首单/引流价

建议确认聚合平台是不是真的调官方API，还是自己套的模型（效果可能打折扣）。
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Sat 2026-04-18 00:20 GMT+8] 这两个都不是官方的
assistant: 

对，都是**分销商/代理**，价格差3-4倍原因：

- **渠道不同** — 有的拿货价低，有的量大优惠
- **计费方式** — 可能一个按token一个按次
- **服务等级** — 响应速度、成功率、并发限制不同

¥0.84那个更便宜，但要注意：
- 稳定性怎么样
- 有没有并发/TPM限制
- 成功率是否打折

如果只是自用测试，便宜的就行；如果是正式项目，建议选贵的更稳。
user: Sender (untrusted metadata):
```json
{
  "label": "openclaw-control-ui",
  "id": "openclaw-control-ui"
}
```

[Sat 2026-04-18 00:27 GMT+8] 你现在用的minimax是每秒多少钱百万token？
assistant: 

我用的 MiniMax-M2.7 价格：

- **输入**：$0.3 / 1M tokens（约 ¥2.2）
- **输出**：$1.2 / 1M tokens（约 ¥8.7）

按token计费，不是按秒。生成1000字大约消耗几百到几千token。
