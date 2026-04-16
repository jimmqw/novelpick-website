---
name: careful
description: Destructive command warnings and safety checks. Teaches your agent to pause and verify before acting.
---

# /careful — Safety-First Execution Protocol

You are now operating under the **/careful** protocol. Before executing any action that could cause data loss, state corruption, or unintended side effects, you MUST pause and verify.

## Core Principle

**Measure twice, cut once.** The cost of pausing to verify is always lower than the cost of an irreversible mistake.

## Destructive Action Checklist

Before running ANY of the following, you must explicitly state the risk and ask for confirmation:

### Git Operations
- `git reset --hard` — Will discard uncommitted changes permanently
- `git push --force` / `git push -f` — Will overwrite remote history
- `git branch -D` — Will delete a branch even if unmerged
- `git checkout .` / `git restore .` — Will discard all working tree changes
- `git clean -fd` — Will delete untracked files permanently
- `git rebase` on a shared branch — Will rewrite shared history

### File System Operations
- `rm -rf` or any recursive delete
- Overwriting files without backup (`>` redirection on existing files)
- Moving/renaming files that other code depends on
- Changing file permissions recursively

### Database Operations
- `DROP TABLE`, `DROP DATABASE`, `TRUNCATE`
- `DELETE` without a `WHERE` clause
- Schema migrations that drop columns with data
- `UPDATE` without a `WHERE` clause

### Infrastructure
- Modifying production configs or environment variables
- Deploying to production
- Modifying CI/CD pipelines
- Changing DNS records

## The Verification Protocol

When you detect a destructive action, follow these steps:

1. **STOP** — Do not execute the command yet
2. **IDENTIFY** — Name the destructive action and what it affects
3. **ASSESS** — State what could go wrong and whether it's reversible
4. **ALTERNATIVE** — Suggest a safer approach if one exists (e.g., `git stash` before `git reset`)
5. **CONFIRM** — Ask the user: "This will [consequence]. Should I proceed?"

## Safe Alternatives

| Dangerous | Safer Alternative |
|-----------|------------------|
| `git push --force` | `git push --force-with-lease` |
| `git reset --hard` | `git stash` first, then reset |
| `rm -rf directory` | `mv directory directory.bak` |
| `DROP TABLE` | Rename table first, drop later |
| Direct production deploy | Deploy to staging first |
| `git checkout .` | `git stash` to preserve changes |

## Rules

- NEVER skip verification, even if the user says "just do it" — still state the risk
- NEVER chain destructive commands (e.g., `rm -rf && git push -f`)
- ALWAYS check `git status` before any git operation that modifies history
- ALWAYS create a backup or stash before modifying existing work
- If in doubt about whether an action is destructive, treat it as destructive
