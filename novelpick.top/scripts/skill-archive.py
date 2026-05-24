"""
技能归档脚本
功能：
1. dry-run 模式：预览将被归档的技能（90天+未使用）
2. 正式模式：将技能移入 skills-archive/
3. 支持指定技能单独归档

用法：
  python scripts/skill-archive.py --dry-run        # 预览
  python scripts/skill-archive.py                  # 正式归档（需确认）
  python scripts/skill-archive.py --skill xxx     # 归档指定技能
"""

import json
import shutil
import argparse
from datetime import datetime, timezone, timedelta
from pathlib import Path

SKILL_USAGE_FILE = Path(__file__).parent.parent / "memory" / "skill-usage.json"
SKILLS_DIR = Path(__file__).parent.parent / "skills"
ARCHIVE_DIR = Path(__file__).parent.parent / "skills-archive"
ARCHIVE_DAYS = 90
NOW = datetime.now(timezone(timedelta(hours=8)))

def load_usage():
    with open(SKILL_USAGE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_last_used(skill_name, records):
    skill_records = sorted(
        [r for r in records if r.get("skill") == skill_name],
        key=lambda r: r["timestamp"],
        reverse=True
    )
    return skill_records[0]["timestamp"] if skill_records else None

def get_stale_skills(records):
    stale = []
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir() or not (skill_dir / "SKILL.md").exists():
            continue
        last_used = get_last_used(skill_dir.name, records)
        if last_used is None:
            last_dt = NOW - timedelta(days=ARCHIVE_DAYS + 1)
            days_ago = ARCHIVE_DAYS + 1
        else:
            last_dt = datetime.fromisoformat(last_used)
            days_ago = (NOW - last_dt).days

        if days_ago >= ARCHIVE_DAYS:
            stale.append({
                "skill": skill_dir.name,
                "last_used": last_used,
                "days_ago": days_ago,
                "path": str(skill_dir)
            })
    return stale

def archive_skill(skill_name, dry_run=False):
    skill_path = SKILLS_DIR / skill_name
    if not skill_path.exists():
        print(f"  技能不存在: {skill_name}")
        return False

    ARCHIVE_DIR.mkdir(exist_ok=True)
    dest = ARCHIVE_DIR / skill_name

    if dry_run:
        print(f"  [DRY-RUN] 将归档: {skill_name}")
        return True

    # 实际归档
    shutil.copytree(skill_path, dest, dirs_exist_ok=True)
    shutil.rmtree(skill_path)

    # 记录归档日志
    archive_log = ARCHIVE_DIR / "archive-log.json"
    log = json.load(open(archive_log, "a", encoding="utf-8")) if archive_log.exists() else {"archives": []}
    log["archives"].append({
        "skill": skill_name,
        "archived_at": NOW.isoformat(),
        "from": str(skill_path),
        "to": str(dest)
    })
    with open(archive_log, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    print(f"  ✅ 已归档: {skill_name} → {dest}")
    return True

def main():
    parser = argparse.ArgumentParser(description="技能归档工具")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际归档")
    parser.add_argument("--skill", type=str, help="指定单个技能归档")
    args = parser.parse_args()

    data = load_usage()
    records = data.get("records", [])

    if args.skill:
        stale = [{"skill": args.skill, "path": str(SKILLS_DIR / args.skill)}]
    else:
        stale = get_stale_skills(records)

    if not stale:
        print("没有需要归档的技能。")
        return

    print(f"=== 技能归档 {'预览' if args.dry_run else '执行'} ===")
    print(f"将归档 {len(stale)} 个技能:\n")

    for item in stale:
        print(f"  - {item['skill']} ({item.get('days_ago', '?')}天未用)")

    if args.dry_run:
        print(f"\n(加上 --skill xxx 可指定单个技能)")
        return

    confirm = input(f"\n确认归档这 {len(stale)} 个技能？输入 y 确认: ")
    if confirm.lower() != "y":
        print("取消。")
        return

    for item in stale:
        archive_skill(item["skill"], dry_run=False)

    print("\n归档完成。")

if __name__ == "__main__":
    main()
