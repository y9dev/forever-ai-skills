#!/usr/bin/env python3
"""Install the workflow's role files as Claude Code subagents (optional).

Claude Code does not auto-register Markdown files that live inside a skill folder.
This script copies agents/*.md to a subagents directory so they can be used as
`subagent_type: "sew-<role>"`, with the tool restrictions from their frontmatter.

Usage:
  python install_agents.py                 # user level: ~/.claude/agents
  python install_agents.py --project       # project level: ./.claude/agents
  python install_agents.py --dry-run
  python install_agents.py --uninstall
The files keep their `sew-` names from the frontmatter. Restart Claude Code (or reload agents) afterwards.
"""
import argparse
import re
import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent.parent / "agents"
NAME_RE = re.compile(r"^name:\s*(sew-[a-z0-9-]+)\s*$", re.MULTILINE)


def agent_name(text: str, path: Path) -> str:
    if not text.startswith("---"):
        raise ValueError(f"{path.name}: missing frontmatter")
    head = text.split("---", 2)[1]
    m = NAME_RE.search(head)
    if not m:
        raise ValueError(f"{path.name}: frontmatter needs 'name: sew-<role>'")
    return m.group(1)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--project", action="store_true", help="install into ./.claude/agents instead of ~/.claude/agents")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--uninstall", action="store_true", help="remove previously installed sew-* agents")
    args = ap.parse_args()

    dest = (Path.cwd() / ".claude" / "agents") if args.project else (Path.home() / ".claude" / "agents")
    files = sorted(SRC.glob("*.md"))
    if not files:
        print(f"No role files found in {SRC}", file=sys.stderr)
        return 1

    if not args.dry_run:
        dest.mkdir(parents=True, exist_ok=True)
    for f in files:
        try:
            name = agent_name(f.read_text(encoding="utf-8"), f)
        except ValueError as e:
            print(f"ERROR {e}", file=sys.stderr)
            return 1
        target = dest / f"{name}.md"
        if args.uninstall:
            print(f"{'would remove' if args.dry_run else 'remove'}: {target}")
            if not args.dry_run and target.exists():
                target.unlink()
            continue
        verb = "overwrite" if target.exists() else "create"
        print(f"{'would ' if args.dry_run else ''}{verb}: {target}")
        if not args.dry_run:
            target.write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
    print("Done. Restart Claude Code or reload agents to pick up changes." if not args.dry_run else "Dry run only.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
