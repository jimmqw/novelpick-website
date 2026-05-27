"""
从历史会话记录中反推技能使用次数
原理：通过 sessions_list 读取最近活跃session，从会话历史中识别技能调用
补充 skill-usage.json 中缺失的历史记录
"""

import json
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ---- 已知常用技能的调用模式 ----
# 当会话中出现这些关键词时，说明对应的技能被使用了
SKILL_TRIGGERS = {
    "clawhub": ["clawhub", "skillhub", "clawhub search", "clawhub install", "search.*skill", "安装技能"],
    "github": ["gh ", "git commit", "git push", "git add", "github"],
    "multi-search-engine": ["web_search", "search engine", "multi.search", "搜索"],
    "weather": ["weather", "天气预报", "天气查询"],
    "clawvard_exam": ["clawvard", "exam", "考试", "测验"],
    "find-skills": ["find-skill", "find_skill", "找技能", "搜索技能"],
    "skillhub-preference": ["skillhub"],
    "clawhub-preference": ["clawhub preference"],
    "memory-hygiene": ["memory hygiene", "记忆清理", "向量记忆"],
    "memory-tiering": ["memory tiering", "记忆分层"],
    "self-improving-agent": ["self-improving", "self_improving", "自我改进"],
    "proactive-agent-lite": ["proactive", "主动型"],
    "careful": ["careful", "安全检查"],
    "review": ["review", "PR预审"],
    "office-hours": ["office-hours", "产品需求分析"],
    "humanizer": ["humanizer", "去除AI痕迹"],
    "skill-vetter": ["skill-vetter", "技能安全审核"],
    "website-seo": ["website-seo", "SEO完整系统"],
    "seo-optimization": ["seo-optimization", "SEO优化"],
    "tavily-search": ["tavily", "Tavily"],
    "agent-browser": ["agent-browser", "browser", "浏览器自动化"],
    "context-compressor": ["context-compressor", "压缩上下文"],
    "copywriter": ["copywriter", "文案", "UX文案"],
    "ai-seo-writer": ["ai-seo-writer", "SEO文章写作"],
    "elite-frontend-design": ["elite-frontend-design", "前端UI", "界面设计"],
    "feishu-doc": ["feishu-doc", "飞书文档"],
    "feishu-drive": ["feishu-drive", "飞书云盘"],
    "feishu-perm": ["feishu-perm", "飞书权限"],
    "feishu-wiki": ["feishu-wiki", "飞书知识库"],
    "gh-issues": ["gh-issues", "GitHub issues"],
    "node-connect": ["node-connect", "节点连接"],
    "healthcheck": ["healthcheck", "安全加固"],
    "skill-creator": ["skill-creator", "创建技能"],
    "gog": ["gog"],
    "image-gen": ["image-gen", "图片生成"],
    "battery-customer-research": ["电池行业", "电池客户", "锂电池客户"],
    "bid-document-creator": ["标书", "投标文件", "招标文件"],
    "capcut-video-editor": ["CapCut", "视频剪辑", "剪映"],
    "comfyui-painter": ["ComfyUI", "comfyui", "画图", "文生图"],
    "douyin-hot-products": ["抖音热卖", "抖音爆款", "选品"],
    "douyin-publisher": ["抖音发布", "Douyin publisher"],
    "douyin-video-parse": ["抖音解析", "视频直链", "抖音URL"],
    "env-equip-customer-research": ["环保设备", "环保行业客户"],
    "movie-commentary": ["影视解说", "电影解说", "解说文案"],
    "shortdrama-script": ["短剧", "短剧剧本", "霸总"],
    "tech-news-daily": ["科技新闻", "AI新闻", "今日科技"],
    "agent-complete": ["agent-complete", "补全agent", "补全配置"],
    "intl-news": ["国际新闻", "world news"],
    "openviking-memory": ["openviking"],
}

def match_skill(text, skill):
    """检查文本是否触发某个技能的使用"""
    triggers = SKILL_TRIGGERS.get(skill, [])
    text_lower = text.lower()
    for t in triggers:
        if t.lower() in text_lower:
            return True
    return False

def scan_text_for_skills(text, session_id, timestamp):
    """扫描一段文本，返回触发的技能列表"""
    found = []
    for skill in SKILL_TRIGGERS:
        if match_skill(text, skill):
            found.append(skill)
    return found

def main():
    print("[Info] 此脚本需要从 sessions_list 获取历史记录")
    print("[Info] 由于sessions_list是工具调用，请在主会话中运行此功能的代理来执行")
    print("[Info] 建议：在下次心跳或下次长会话结束后，运行skill-usage-analyze.py分析现有数据")
    print("")
    print("KNOWN_SKILLS:", len(SKILL_TRIGGERS))
    for s in sorted(SKILL_TRIGGERS):
        print(f"  {s}")


if __name__ == "__main__":
    main()
