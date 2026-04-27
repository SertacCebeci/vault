#!/usr/bin/env python3
"""
Rebuild the vault's mechanical projections per §26.4:
  - wiki/_meta/index.md         — main catalog (all entries grouped by category)
  - wiki/_meta/indexes/{d}.md   — one per active domain

These are caches. The source of truth is `wiki/entries/`. Re-run any time
entries are added, removed, or reclassified.

Usage:
  python3 scripts/build_vault_indexes.py
"""

from __future__ import annotations
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = REPO_ROOT / "wiki" / "entries"
META_DIR = REPO_ROOT / "wiki" / "_meta"
INDEX_FILE = META_DIR / "index.md"
DOMAIN_INDEX_DIR = META_DIR / "indexes"
NOTICEBOARD_DIR = META_DIR / "noticeboards"

# Noticeboard catalog per §23.2. Each tuple: (filename, title, source_predicate)
# source_predicate is a fn(entry) -> bool that selects which entries appear.
NOTICEBOARDS: list[tuple[str, str, str]] = [
    ("slug-uniqueness.md",            "Slug uniqueness",            "finding-slug-collision-*"),
    ("broken-wikilink.md",            "Broken wikilinks",           "finding-broken-wikilink-*"),
    ("contradictions.md",             "Open contradictions",        "relation-* with predicate=contradicts"),
    ("high-stakes.md",                "High-stakes claim removal",  "finding-high-stakes-removal-*"),
    ("evidence-below-floor.md",       "Evidence below floor",       "finding-evidence-below-floor-*"),
    ("pending-changes.md",            "Pending changes",            "pending-* with status=pending"),
    ("notability-deferrals.md",       "Notability deferrals",       "finding-deferred-*"),
    ("cluster-coverage.md",           "Cluster coverage",           "finding-cluster-without-structure-note-*"),
    ("stale-discussions.md",          "Stale discussions",          "finding-stale-discussion-* and discussions inactive >2 weeks"),
    ("stale-findings.md",             "Stale findings",             "finding-stale-finding-* and findings open >60 days"),
    ("agent-test-failures.md",        "Agent-test failures",        "finding-persona-test-fail-*"),
    ("domain-non-subscriber-edits.md", "Domain non-subscriber edits", "finding-domain-non-subscriber-edit-*"),
    ("frontmatter-violations.md",     "Frontmatter violations",     "finding-* tied to frontmatter rules"),
    ("lifecycle-issues.md",           "Lifecycle issues",           "finding-agent-direct-merge-*, finding-immutable-merge-*, agent retirement findings"),
    ("coverage-regressions.md",       "Coverage regressions",       "finding-coverage-regression-*"),
]

# Display order in the main and domain indexes.
CATEGORY_ORDER = [
    "lens",
    "domain",
    "policy",
    "guideline",
    "essay",
    "source",
    "structure-note",
    "concept",
    "insight",
    "entity",
    "process",
    "application",
    "illustration",
    "claim",
    "relation",
    "question",
    "disambiguation",
    "agent",
    "agent-test",
    "discussion",
    "notification",
    "pending",
    "run",
    "finding",
]

CATEGORY_PRETTY = {
    "lens": "Lenses",
    "domain": "Domains",
    "policy": "Policies",
    "guideline": "Guidelines",
    "essay": "Essays",
    "source": "Sources",
    "structure-note": "Structure Notes",
    "concept": "Concepts",
    "insight": "Insights",
    "entity": "Entities",
    "process": "Processes",
    "application": "Applications",
    "illustration": "Illustrations",
    "claim": "Claims",
    "relation": "Relations",
    "question": "Questions",
    "disambiguation": "Disambiguations",
    "agent": "Agents",
    "agent-test": "Agent Tests",
    "discussion": "Discussions",
    "notification": "Notifications",
    "pending": "Pending Proposals",
    "run": "Runs",
    "finding": "Findings",
}

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def parse_fields(fm_text: str) -> dict[str, object]:
    fields: dict[str, object] = {}
    lines = fm_text.split("\n")
    for line in lines:
        if not line or line.startswith(" ") or line.startswith("\t") or line.startswith("-"):
            continue
        m = re.match(r"^([a-zA-Z_][\w-]*)\s*:\s*(.*)$", line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            fields[key] = [s.strip().strip('"').strip("'") for s in inner.split(",")] if inner else []
        else:
            fields[key] = value.strip().strip('"').strip("'")
    return fields


def extract_lead_or_first_line(body: str) -> str:
    """Return the entry's `## Lead` content if present; else first non-heading line."""
    m = re.search(r"(?ms)^## Lead\s*\n+(.*?)(?=\n##\s|\Z)", body)
    if m:
        text = m.group(1).strip().split("\n\n")[0].strip()
        return _shorten(text)
    # else: first non-heading paragraph
    for para in re.split(r"\n\s*\n", body):
        para = para.strip()
        if not para or para.startswith("#") or para.startswith("---"):
            continue
        return _shorten(para)
    return ""


def _shorten(text: str, limit: int = 140) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    cut = text[: limit - 1]
    sp = cut.rfind(" ")
    if sp > 60:
        cut = cut[:sp]
    return cut + "…"


def collect_entries() -> list[dict]:
    out: list[dict] = []
    for p in sorted(ENTRIES_DIR.glob("*.md")):
        raw = p.read_text(encoding="utf-8")
        m = FRONTMATTER_RE.match(raw)
        fm = m.group(1) if m else ""
        body = raw[m.end():] if m else raw
        fields = parse_fields(fm)
        out.append({
            "slug": p.stem,
            "title": fields.get("title", p.stem),
            "category": fields.get("category", "<unknown>"),
            "domains": fields.get("domains", []) if isinstance(fields.get("domains"), list) else [],
            "status": fields.get("status", ""),
            "lead": extract_lead_or_first_line(body),
        })
    return out


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")


# --- main index -------------------------------------------------------------

def build_main_index(entries: list[dict]) -> str:
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        by_cat[e["category"]].append(e)

    lines: list[str] = []
    lines.append("# main index")
    lines.append("")
    lines.append(f"last rebuild: {now_stamp()}")
    lines.append(f"entry count: {len(entries)}")
    lines.append("")
    lines.append("> Auto-generated by `scripts/build_vault_indexes.py`. Do not hand-edit.")
    lines.append("> Source of truth: `wiki/entries/`. Re-run after any add/remove/reclassify.")
    lines.append("")
    lines.append("## by category")
    lines.append("")

    seen_cats = set()
    ordered = [c for c in CATEGORY_ORDER if c in by_cat] + [c for c in sorted(by_cat) if c not in CATEGORY_ORDER]
    for cat in ordered:
        if cat in seen_cats:
            continue
        seen_cats.add(cat)
        rows = sorted(by_cat[cat], key=lambda e: e["slug"])
        pretty = CATEGORY_PRETTY.get(cat, cat)
        lines.append(f"### {pretty} ({len(rows)})")
        lines.append("")
        for e in rows:
            doms = ", ".join(e["domains"]) if e["domains"] else "—"
            lead = e["lead"]
            suffix = f" — {lead}" if lead else ""
            lines.append(f"- [[{e['slug']}]] — {e['title']} _(domains: {doms})_{suffix}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


# --- per-domain index -------------------------------------------------------

def build_domain_index(domain_slug: str, entries: list[dict], domain_entry: dict | None) -> str:
    in_domain = [e for e in entries if domain_slug in e["domains"]]
    by_cat: dict[str, list[dict]] = defaultdict(list)
    for e in in_domain:
        by_cat[e["category"]].append(e)

    title = domain_entry["title"] if domain_entry else domain_slug

    lines: list[str] = []
    lines.append(f"# domain: {title}")
    lines.append("")
    lines.append(f"last rebuild: {now_stamp()}")
    lines.append(f"entry count: {len(in_domain)}")
    lines.append("")
    lines.append("> Auto-generated by `scripts/build_vault_indexes.py`. Do not hand-edit.")
    lines.append(f"> Source of truth: the domain entry [[{domain_slug}]] and the entries' frontmatter.")
    lines.append("")

    if domain_entry and domain_entry.get("lead"):
        lines.append("## scope")
        lines.append("")
        lines.append(domain_entry["lead"])
        lines.append("")

    questions = [e for e in in_domain if e["category"] == "question"]
    if questions:
        lines.append("## open questions")
        lines.append("")
        for q in sorted(questions, key=lambda e: e["slug"]):
            lines.append(f"- [[{q['slug']}]] — {q['title']}")
        lines.append("")

    structures = [e for e in in_domain if e["category"] == "structure-note"]
    if structures:
        lines.append("## load-bearing structure notes")
        lines.append("")
        for s in sorted(structures, key=lambda e: e["slug"]):
            lines.append(f"- [[{s['slug']}]] — {s['title']}")
        lines.append("")

    lines.append("## by category")
    lines.append("")
    ordered = [c for c in CATEGORY_ORDER if c in by_cat] + [c for c in sorted(by_cat) if c not in CATEGORY_ORDER]
    for cat in ordered:
        if cat in {"question", "structure-note"}:
            continue
        rows = sorted(by_cat[cat], key=lambda e: e["slug"])
        pretty = CATEGORY_PRETTY.get(cat, cat)
        lines.append(f"### {pretty} ({len(rows)})")
        lines.append("")
        for e in rows:
            lead = e["lead"]
            suffix = f" — {lead}" if lead else ""
            lines.append(f"- [[{e['slug']}]] — {e['title']}{suffix}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


# --- noticeboards -----------------------------------------------------------

def select_for_noticeboard(filename: str, entries: list[dict]) -> list[dict]:
    """
    Map a noticeboard filename to the entries that belong on it.
    For finding-driven boards, match by finding_kind prefix.
    For relation/pending boards, filter on category + frontmatter state.
    """
    by_slug_pfx = {
        "slug-uniqueness.md":             "finding-slug-collision-",
        "broken-wikilink.md":             "finding-broken-wikilink-",
        "high-stakes.md":                 "finding-high-stakes-removal-",
        "evidence-below-floor.md":        "finding-evidence-below-floor-",
        "notability-deferrals.md":        "finding-deferred-",
        "cluster-coverage.md":            "finding-cluster-without-structure-note-",
        "stale-discussions.md":           "finding-stale-discussion-",
        "stale-findings.md":              "finding-stale-finding-",
        "agent-test-failures.md":         "finding-persona-test-fail-",
        "domain-non-subscriber-edits.md": "finding-domain-non-subscriber-edit-",
        "coverage-regressions.md":        "finding-coverage-regression-",
    }
    if filename in by_slug_pfx:
        pfx = by_slug_pfx[filename]
        return [e for e in entries if e["slug"].startswith(pfx) and e.get("status") != "resolved"]
    if filename == "contradictions.md":
        return [e for e in entries if e["category"] == "relation" and e.get("predicate") == "contradicts"]
    if filename == "pending-changes.md":
        return [e for e in entries if e["category"] == "pending"]
    if filename == "frontmatter-violations.md":
        # any finding whose slug name suggests a frontmatter rule
        fm_rules = ("finding-id-filename-mismatch", "finding-unknown-category", "finding-unknown-domain",
                    "finding-entry-without-domain", "finding-missing-required-list",
                    "finding-category-fields-presence", "finding-frontmatter-yaml-invalid",
                    "finding-tag-shadowing-domain", "finding-classification-consistency",
                    "finding-infrastructure-without-produced-by", "finding-infrastructure-classified-by-lens")
        return [e for e in entries if any(e["slug"].startswith(r) for r in fm_rules)]
    if filename == "lifecycle-issues.md":
        pfxs = ("finding-agent-direct-merge-", "finding-immutable-merge-", "finding-agent-retire-")
        return [e for e in entries if any(e["slug"].startswith(p) for p in pfxs)]
    return []


def build_noticeboard(title: str, source_desc: str, items: list[dict]) -> str:
    lines: list[str] = []
    lines.append(f"# noticeboard: {title}")
    lines.append("")
    lines.append(f"last rebuild: {now_stamp()}")
    lines.append(f"open count: {len(items)}")
    lines.append("")
    lines.append("> Auto-generated by `scripts/build_vault_indexes.py`. Do not hand-edit.")
    lines.append(f"> Selects: {source_desc}")
    lines.append("")
    if not items:
        lines.append("_No open items._")
        lines.append("")
        return "\n".join(lines).rstrip() + "\n"
    for it in sorted(items, key=lambda e: e["slug"]):
        title_text = it.get("title", it["slug"])
        lead = it.get("lead", "")
        suffix = f" — {lead}" if lead else ""
        lines.append(f"- [[{it['slug']}]] — {title_text}{suffix}")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_noticeboards_readme() -> str:
    lines: list[str] = []
    lines.append("# noticeboards")
    lines.append("")
    lines.append(f"last rebuild: {now_stamp()}")
    lines.append("")
    lines.append("> Auto-generated by `scripts/build_vault_indexes.py`. Do not hand-edit.")
    lines.append("")
    lines.append("Each noticeboard projects a slice of `wiki/entries/finding-*` (and a few peer-kind entries) that subscribed agents read instead of scanning all findings. See spec §23 for the full design.")
    lines.append("")
    lines.append("| file | listing |")
    lines.append("|---|---|")
    for filename, _, source_desc in NOTICEBOARDS:
        lines.append(f"| [{filename}](./{filename}) | {source_desc} |")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


# --- main -------------------------------------------------------------------

def main() -> int:
    if not ENTRIES_DIR.is_dir():
        print(f"error: {ENTRIES_DIR} not found", file=sys.stderr)
        return 1

    entries = collect_entries()
    domain_entries = {e["slug"]: e for e in entries if e["category"] == "domain"}

    # main index
    META_DIR.mkdir(exist_ok=True)
    INDEX_FILE.write_text(build_main_index(entries), encoding="utf-8")
    print(f"WROTE {INDEX_FILE.relative_to(REPO_ROOT)}  ({len(entries)} entries)")

    # per-domain indexes
    DOMAIN_INDEX_DIR.mkdir(parents=True, exist_ok=True)
    written_domains = 0
    for slug, dom in sorted(domain_entries.items()):
        path = DOMAIN_INDEX_DIR / f"{slug}.md"
        path.write_text(build_domain_index(slug, entries, dom), encoding="utf-8")
        in_domain = sum(1 for e in entries if slug in e["domains"])
        print(f"WROTE {path.relative_to(REPO_ROOT)}  ({in_domain} entries)")
        written_domains += 1

    # noticeboards
    NOTICEBOARD_DIR.mkdir(parents=True, exist_ok=True)
    readme = NOTICEBOARD_DIR / "README.md"
    readme.write_text(build_noticeboards_readme(), encoding="utf-8")
    print(f"WROTE {readme.relative_to(REPO_ROOT)}")
    written_boards = 0
    for filename, title, source_desc in NOTICEBOARDS:
        items = select_for_noticeboard(filename, entries)
        path = NOTICEBOARD_DIR / filename
        path.write_text(build_noticeboard(title, source_desc, items), encoding="utf-8")
        print(f"WROTE {path.relative_to(REPO_ROOT)}  ({len(items)} open)")
        written_boards += 1

    # also catch any domain referenced by entries but missing as a domain entry
    referenced = set()
    for e in entries:
        for d in e["domains"]:
            referenced.add(d)
    orphan_domains = referenced - set(domain_entries.keys())
    if orphan_domains:
        print(f"\nwarning: {len(orphan_domains)} domain(s) referenced but no domain entry:")
        for d in sorted(orphan_domains):
            print(f"  - {d}")

    print(f"\n=== build_vault_indexes.py — main + {written_domains} domains + {written_boards} noticeboards ===")
    return 0


if __name__ == "__main__":
    sys.exit(main())
