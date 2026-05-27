"""
技能使用分析脚本 - 每月1号运行
功能：
1. 统计各技能使用次数
2. 标记90天未使用的技能（建议归档）
3. 标记30天未使用的技能（警告）
4. 生成报告
"""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

SKILL_USAGE_FILE = Path(__file__).parent.parent / "memory" / "skill-usage.json"
SKILLS_DIR = Path(__file__).parent.parent / "skills"
ARCHIVE_DIR = Path(__file__).parent.parent / "skills-archive"

WARN_DAYS = 30
ARCHIVE_DAYS = 90
NOW = datetime.now(timezone(timedelta(hours=8)))  # Asia/Shanghai

def load_usage():
    with open(SKILL_USAGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_last_used(skill_name, records):
    """获取技能最后一次使用时间"""
    skill_records = [r for r in records if r.get("skill") == skill_name]
    if not skill_records:
        return None
    skill_records.sort(key=lambda r: r["timestamp"], reverse=True)
    return skill_records[0]["timestamp"]

def get_all_skill_dirs():
    """获取所有技能目录（含skills和.openclaw/skills）"""
    skills = []
    for base in [
        Path(__file__).parent.parent / "skills",
        Path(__file__).parent.parent / ".openclaw" / "skills"
    ]:
        if base.exists():
            for d in base.iterdir():
                if d.is_dir() and (d / "SKILL.md").exists():
                    skills.append(d)
    return skills

def analyze():
    data = load_usage()
    records = data.get("records", [])

    # 统计每个技能的使用次数
    skill_count = {}
    for r in records:
        s = r.get("skill")
        skill_count[s] = skill_count.get(s, 0) + 1

    # 获取所有已安装技能
    all_skills = get_all_skill_dirs()
    skill_names = [s.name for s in all_skills]

    # 分析每个技能
    cold = []    # 90天未使用 → 建议归档
    warm = []    # 30-90天未使用 → 警告
    active = []   # 30天内使用过
    never_used = []  # 从未使用过

    for name in skill_names:
        last_used = get_last_used(name, records)
        if last_used is None:
            never_used.append(name)
            continue

        last_dt = datetime.fromisoformat(last_used)
        days_ago = (NOW - last_dt).days

        entry = {
            "skill": name,
            "last_used": last_used,
            "days_ago": days_ago,
            "use_count": skill_count.get(name, 0)
        }

        if days_ago >= ARCHIVE_DAYS:
            cold.append(entry)
        elif days_ago >= WARN_DAYS:
            warm.append(entry)
        else:
            active.append(entry)

    # 生成报告
    report = []
    report.append(f"=== Skill Usage Report ===")
    report.append(f"Generated: {NOW.isoformat()}")
    report.append(f"")
    report.append(f"[Overview]")
    report.append(f"  Total installed: {len(skill_names)}")
    report.append(f"  Active (30d): {len(active)}")
    report.append(f"  Warning (30-90d): {len(warm)}")
    report.append(f"  Cold (90d+): {len(cold)}")
    report.append(f"  Never used: {len(never_used)}")
    report.append(f"")

    if warm:
        report.append(f"[!] 30-90 days unused ({len(warm)})")
        for e in sorted(warm, key=lambda x: x["days_ago"], reverse=True):
            report.append(f"  - {e['skill']}: {e['days_ago']}d unused (used {e['use_count']}x)")
        report.append(f"")

    if cold:
        report.append(f"[X] Recommend archive (90d+ unused) ({len(cold)})")
        for e in sorted(cold, key=lambda x: x["days_ago"], reverse=True):
            report.append(f"  - {e['skill']}: {e['days_ago']}d unused (used {e['use_count']}x)")
        report.append(f"  -> Dry run: python scripts/skill-archive.py --dry-run")
        report.append(f"  -> Confirm: python scripts/skill-archive.py")
        report.append(f"")

    if never_used:
        report.append(f"[*] Never used ({len(never_used)})")
        for name in sorted(never_used):
            report.append(f"  - {name}")
        report.append(f"")

    report_text = "\n".join(report)
    print(report_text)

    # 更新stats
    data["stats"] = {
        "total_records": len(records),
        "unique_skills_used": len(skill_count),
        "last_analyzed": NOW.isoformat(),
        "cold_count": len(cold),
        "warm_count": len(warm),
        "never_used_count": len(never_used)
    }
    with open(SKILL_USAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return report_text

if __name__ == "__main__":
    analyze()
