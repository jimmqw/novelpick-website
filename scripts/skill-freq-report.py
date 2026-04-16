"""
技能使用频率排行报告
直接读取 skill-usage.json，生成按调用次数排序的技能排行
用法：python scripts/skill-freq-report.py [--days N]
"""

import json
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path
from collections import Counter

SKILL_USAGE_FILE = Path(__file__).parent.parent / "memory" / "skill-usage.json"
SKILLS_DIR = Path(__file__).parent.parent / "skills"
NOW = datetime.now(timezone(timedelta(hours=8)))

def load_usage():
    with open(SKILL_USAGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_all_installed_skills():
    """获取所有已安装技能"""
    skills = set()
    for base in [
        Path(__file__).parent.parent / "skills",
        Path(__file__).parent.parent / ".openclaw" / "skills"
    ]:
        if base.exists():
            for d in base.iterdir():
                if d.is_dir() and (d / "SKILL.md").exists():
                    skills.add(d.name)
    return skills

def build_report(data, days_limit=None):
    records = data.get("records", [])
    installed = get_all_installed_skills()

    # 按时间过滤
    if days_limit:
        cutoff = NOW - timedelta(days=days_limit)
        filtered = []
        for r in records:
            try:
                rdt = datetime.fromisoformat(r["timestamp"])
                if rdt >= cutoff:
                    filtered.append(r)
            except:
                pass
        records = filtered

    # 统计每个技能的使用次数
    counter = Counter(r["skill"] for r in records)
    total = len(records)

    lines = []
    lines.append(f"{'='*50}")
    lines.append(f"  Skill Usage Frequency Report")
    if days_limit:
        lines.append(f"  Last {days_limit} days")
    else:
        lines.append(f"  All time")
    lines.append(f"  Generated: {NOW.strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"{'='*50}")
    lines.append(f"")
    lines.append(f"[Summary]")
    lines.append(f"  Total usage records: {total}")
    lines.append(f"  Unique skills used: {len(counter)}")
    lines.append(f"  Installed skills: {len(installed)}")
    lines.append(f"  Unused (installed): {len(installed) - len(counter)}")
    lines.append(f"")

    # Top排行
    if counter:
        lines.append(f"[Top Skills by Usage]")
        for rank, (skill, count) in enumerate(counter.most_common(), 1):
            pct = count / total * 100 if total > 0 else 0
            bar = "#" * int(pct / 5) + "-" * (20 - int(pct / 5))
            lines.append(f"  {rank:2}. [{count:3}x] {skill:<35} {bar} {pct:.1f}%")
        lines.append(f"")

    # 未使用的技能
    unused = installed - counter.keys()
    if unused:
        lines.append(f"[Installed but Never Used] ({len(unused)})")
        for skill in sorted(unused):
            lines.append(f"  - {skill}")
        lines.append(f"")

    # 最近使用记录
    if records:
        lines.append(f"[Recent Records] (last 10)")
        sorted_records = sorted(records, key=lambda r: r["timestamp"], reverse=True)
        for r in sorted_records[:10]:
            try:
                rdt = datetime.fromisoformat(r["timestamp"])
                age = (NOW - rdt).total_seconds() / 3600
                age_str = f"{age:.1f}h ago" if age < 24 else f"{(age/24):.1f}d ago"
            except:
                age_str = "?"
            lines.append(f"  {r['skill']:<30} {r.get('use_case',''):<30} {age_str}")
        lines.append(f"")

    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--days", type=int, default=None, help="只看最近N天")
    args = parser.parse_args()

    if not SKILL_USAGE_FILE.exists():
        print(f"[Error] {SKILL_USAGE_FILE} not found. Run log-skill-usage.py first.")
        return

    data = load_usage()
    print(build_report(data, days_limit=args.days))


if __name__ == "__main__":
    main()
