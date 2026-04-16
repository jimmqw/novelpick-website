"""
技能使用记录工具
用法：
  python scripts/log-skill-usage.py <skill_name> <use_case> [--notes "备注"]

示例：
  python scripts/log-skill-usage.py clawhub "安装新技能" --notes "安装了seo-optimization"
  python scripts/log-skill-usage.py github "推送代码" --notes "推送了网站更新"
"""

import json
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

SKILL_USAGE_FILE = Path(__file__).parent.parent / "memory" / "skill-usage.json"

def log(skill, use_case, notes="", session=None):
    data = json.load(open(SKILL_USAGE_FILE, "r", encoding="utf-8"))

    now = datetime.now(timezone(timedelta(hours=8)))
    record = {
        "skill": skill,
        "timestamp": now.isoformat(),
        "use_case": use_case,
        "session": session or now.strftime("%Y-%m-%d-%H%M"),
        "notes": notes
    }

    data["records"].append(record)
    data["stats"]["total_records"] = len(data["records"])
    data["stats"]["last_updated"] = now.isoformat()

    unique_skills = set(r["skill"] for r in data["records"])
    data["stats"]["unique_skills_used"] = len(unique_skills)

    with open(SKILL_USAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"[OK] Logged: {skill} - {use_case}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="记录技能使用")
    parser.add_argument("skill", help="技能名称")
    parser.add_argument("use_case", help="使用场景")
    parser.add_argument("--notes", default="", help="备注")
    parser.add_argument("--session", default=None, help="会话ID")
    args = parser.parse_args()

    log(args.skill, args.use_case, args.notes, args.session)
