#!/usr/bin/env python3
"""
Scaffold a `run-*` entry per spec §25.3.

Used during seed phase by humans (later by the runtime) to record an agent
execution: what was read, what was written, what findings were raised, what
policy and lens versions were active.

Usage:
  python3 runner/run_emitter.py \\
      --kind edit \\
      --agent agent-editor-learning-theory \\
      --writes desirable-difficulty,fluency-illusion \\
      --reads make-it-stick,desirable-difficulty \\
      --notes "phase 2 staging of chapter 1 sub-section 1"

  python3 runner/run_emitter.py --kind ingest --agent human-reviewer --notes "bootstrap pass"

The script prints the path it would write. Pass `--apply` to actually create
the file. The slug is `run-{kind}-{YYYY-MM-DD-HHMM}-{nonce}` to ensure
uniqueness within a minute.
"""

from __future__ import annotations
import argparse
import sys
import secrets
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = REPO_ROOT / "wiki" / "entries"

VALID_KINDS = {
    "edit", "lint", "assess", "ingest", "review", "merge", "promotion",
    "quorum", "lifecycle", "rollback", "notification-flush", "archival",
    "bootstrap",
}


def fmt_list(items: list[str]) -> str:
    if not items:
        return "_(none)_"
    return "\n".join(f"- [[{i}]]" for i in items)


def fmt_yaml_list(items: list[str]) -> str:
    if not items:
        return "[]"
    quoted = [f'"[[{i}]]"' for i in items]
    return "[" + ", ".join(quoted) + "]"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kind", required=True, choices=sorted(VALID_KINDS))
    parser.add_argument("--agent", required=True, help="Agent slug (e.g., agent-editor-learning-theory) or 'human-reviewer'")
    parser.add_argument("--reads", default="", help="Comma-separated slugs read")
    parser.add_argument("--writes", default="", help="Comma-separated slugs written, in `slug:action` form (action: created|modified|merged|deleted; default modified)")
    parser.add_argument("--findings", default="", help="Comma-separated finding slugs raised")
    parser.add_argument("--findings-resolved", default="", help="Comma-separated finding slugs resolved")
    parser.add_argument("--notes", default="", help="Free-form note for the body")
    parser.add_argument("--apply", action="store_true", help="Write the entry (default: print path only)")
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    started = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    stamp = now.strftime("%Y-%m-%d-%H%M")
    nonce = secrets.token_hex(2)
    slug = f"run-{args.kind}-{stamp}-{nonce}"
    today = now.strftime("%Y-%m-%d")

    reads = [s.strip() for s in args.reads.split(",") if s.strip()]
    writes_pairs = []
    for w in args.writes.split(","):
        w = w.strip()
        if not w:
            continue
        if ":" in w:
            ws, action = w.split(":", 1)
            writes_pairs.append((ws.strip(), action.strip() or "modified"))
        else:
            writes_pairs.append((w, "modified"))
    findings = [s.strip() for s in args.findings.split(",") if s.strip()]
    findings_resolved = [s.strip() for s in args.findings_resolved.split(",") if s.strip()]

    summary = args.notes if args.notes else f"{args.kind} run by {args.agent}"

    fm = f"""---
id: {slug}
title: "Run — {args.kind} — {stamp}"
category: run
produced_by: lifecycle-run-emit
domains: [meta]
tags: [run, {args.kind}]
sources: []
aliases: []
created: {today}
updated: {today}
confidence: high
status: complete
notability_status: n/a
edit_hardness: locked
high_stakes_class: none
quality: c
run_kind: {args.kind}
agent: "[[{args.agent}]]"
started: {started}
finished: {started}
reads: {fmt_yaml_list(reads)}
writes: {fmt_yaml_list([w for w, _ in writes_pairs])}
findings_raised: {fmt_yaml_list(findings)}
---
"""

    body = f"""
# run {args.kind} — {stamp} — {summary[:80]}

## Lead

{summary}

## Reads

{fmt_list(reads)}

## Writes

"""
    if not writes_pairs:
        body += "_(none)_\n"
    else:
        for ws, action in writes_pairs:
            body += f"- [[{ws}]] — {action}\n"

    body += f"""
## Findings raised

{fmt_list(findings)}

## Findings resolved

{fmt_list(findings_resolved)}

## Active versions

_Recorded by the runtime when policy- and lens-version tracking is wired up; left empty during seed-phase manual emission._

## Notes

{args.notes or "_(no additional notes)_"}
"""

    path = ENTRIES_DIR / f"{slug}.md"
    if args.apply:
        if path.exists():
            print(f"error: {path} already exists", file=sys.stderr)
            return 1
        path.write_text(fm + body, encoding="utf-8")
        print(f"WROTE {path.relative_to(REPO_ROOT)}")
    else:
        print(f"WOULD WRITE {path.relative_to(REPO_ROOT)}  ({len(fm + body)} bytes)")
        print("\nrun with --apply to create the entry.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
