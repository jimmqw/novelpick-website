# 文章检查错误教训 (Article Audit Error Lessons)

## 常见问题模式

### 1. 百度统计遗漏 (Baidu Analytics Missing)
- **触发条件**: 新文章没有自动添加百度统计代码
- **教训**: 每次新建文章必须检查 `<script>var _hmt=_hmt||[];...hm.baidu.com/hm.js?...</script>`
- **检查文件**: novelpick.top 和 morai.top 都需要

### 2. og:site_name 缺失
- **触发条件**: 从模板复制时容易遗漏 `<meta property="og:site_name" content="NovelPick">`
- **教训**: 所有文章页都需要 og:site_name，缺失会导致社交分享没有站点标识

### 3. 分享按钮缺失
- **触发条件**: 从旧模板复制时遗漏 share-section
- **教训**: 每个文章结尾（prev-next 之前）必须有分享按钮区块

### 4. Footer 版权信息缺失
- **触发条件**: footer 中没有 `&copy;` 或 `copyright` 字样
- **教训**: 所有 footer 必须包含 `&copy; 2026 [站点名] · All rights reserved`

### 5. prev-next 导航缺失
- **触发条件**: 从不完整的模板创建文章时遗漏
- **教训**: 每个文章必须在 `</main>` 前包含 prev-next 导航

### 6. Baidu 统计代码位置
- **位置**: 在 `</head>` 标签之前
- **格式**: 
```html
<script>
var _hmt = _hmt || [];
(function() {
  var hm = document.createElement("script");
  hm.src = "https://hm.baidu.com/hm.js?[统计ID]";
  var s = document.getElementsByTagName("script")[0];
  s.parentNode.insertBefore(hm, s);
})();
</script>
```

## 修复命令 (快速检查脚本)
```python
# 检查所有问题
python check_article_quality.py
```

## 站点统计ID
- morai.top: d1d9d04b764a3f8f5a92e975825446e6
- novelpick.top: d6d20fb609876081e0de8872c69e39aa

## 新建文章检查清单
- [ ] 百度统计代码 (head末端)
- [ ] og:site_name meta
- [ ] og:title, og:description, og:type, og:url, og:image
- [ ] link rel="canonical"
- [ ] 分享按钮区块 (article-footer-extra 或 prev-next 前)
- [ ] prev-next 导航
- [ ] footer 含版权声明
- [ ] sidebar 组件