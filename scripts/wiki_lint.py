#!/usr/bin/env python3
"""
Wiki lint — mechanical subset of the §20.2 catalog.

This v0 lint reports findings to stdout. It does NOT yet create `finding-*`
entries (that requires a runtime that can manage finding lifecycle); the
spec's lint catalog is honored in name and severity.

Checks implemented (rule name → severity → finding kind in §20.2):
  - slug-uniqueness                       blocking
  - id-filename-mismatch                  blocking
  - unknown-category                      blocking
  - classification-consistency            blocking
  - infrastructure-classified-by-lens     blocking
  - lens-self-classification              blocking
  - unknown-domain                        blocking
  - entry-without-domain                  blocking
  - tag-shadowing-domain                  advisory
  - reserved-prefix-misuse                blocking
  - broken-wikilink                       blocking
  - notability-stamp-missing              blocking
  - lead-missing                          advisory (or blocking when entry is structure-note/source)
  - low-link-density                      advisory
  - orphan-entry                          advisory

Usage:
  python3 scripts/wiki_lint.py             # full run, summary on stdout
  python3 scripts/wiki_lint.py --strict    # exit non-zero if any blocking finding
  python3 scripts/wiki_lint.py --rule R    # restrict to one rule (for debugging)
"""

from __future__ import annotations
import argparse
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENTRIES_DIR = REPO_ROOT / "wiki" / "entries"

# --- kind taxonomy ----------------------------------------------------------

CONTENT_KINDS = {
    "concept", "source", "illustration", "application", "entity",
    "process", "insight", "claim", "relation", "structure-note",
    "disambiguation", "question",
}
INFRA_KINDS = {
    "lens", "domain", "policy", "guideline", "essay", "agent",
    "run", "finding", "agent-test", "discussion", "notification", "pending",
}
ALL_KINDS = CONTENT_KINDS | INFRA_KINDS

# Reserved slug prefixes per §6.5
RESERVED_PREFIX_FOR_KIND = {
    "lens": "lens-",
    "policy": "policy-",
    "guideline": "guideline-",
    "essay": "essay-",
    "agent": "agent-",
    "run": "run-",
    "finding": "finding-",
    "agent-test": "agent-test-",
    "discussion": "discussion-",
    "notification": "notification-",
    "pending": "pending-",
    "claim": "claim-",
    "relation": "relation-",
    "structure-note": "structure-",
    "disambiguation": "disambiguation-",
    "question": "question-",
}
RESERVED_PREFIXES = sorted(set(RESERVED_PREFIX_FOR_KIND.values()), key=len, reverse=True)

# Free-slug content kinds that must NOT use any reserved prefix
FREE_SLUG_CONTENT_KINDS = {"concept", "source", "illustration", "application", "entity", "process", "insight"}

# --- frontmatter parsing ----------------------------------------------------

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+?)(?:\|[^\]]*?)?(?:#[^\]]*?)?\]\]")

@dataclass
class Entry:
    path: Path
    slug: str
    raw: str
    fm_text: str
    body: str
    fields: dict[str, str | list[str]]


def parse_frontmatter(text: str) -> tuple[str, str] | None:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    return m.group(1), text[m.end():]


def parse_fields(fm_text: str) -> dict[str, str | list[str]]:
    """
    Minimal YAML-like parser for top-level keys we care about.
    Supports:
      - scalar:      key: value   (string)
      - inline list: key: [a, b]  (list of strings)
      - block list:  key:
                       - "item"
    Quoted strings have their quotes stripped.
    """
    fields: dict[str, str | list[str]] = {}
    lines = fm_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip() or line.startswith(" ") or line.startswith("\t") or line.startswith("-"):
            i += 1
            continue
        m = re.match(r"^([a-zA-Z_][\w-]*)\s*:\s*(.*)$", line)
        if not m:
            i += 1
            continue
        key, value = m.group(1), m.group(2).strip()
        if value == "":
            # block list — collect indented `- item` lines
            items: list[str] = []
            j = i + 1
            while j < len(lines) and (lines[j].startswith("  -") or lines[j].startswith("- ") or (lines[j].strip() == "" and j+1 < len(lines) and lines[j+1].lstrip().startswith("-"))):
                line2 = lines[j].strip()
                if line2.startswith("-"):
                    item = line2[1:].strip().strip('"').strip("'")
                    items.append(item)
                j += 1
            fields[key] = items
            i = j
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            if inner == "":
                fields[key] = []
            else:
                fields[key] = [s.strip().strip('"').strip("'") for s in inner.split(",")]
            i += 1
        else:
            v = value.strip().strip('"').strip("'")
            # strip trailing inline comment
            v = re.sub(r"\s+#.*$", "", v)
            fields[key] = v
            i += 1
    return fields


def load_entries() -> list[Entry]:
    out: list[Entry] = []
    for p in sorted(ENTRIES_DIR.glob("*.md")):
        raw = p.read_text(encoding="utf-8")
        parsed = parse_frontmatter(raw)
        if parsed is None:
            out.append(Entry(p, p.stem, raw, "", raw, {}))
            continue
        fm_text, body = parsed
        out.append(Entry(p, p.stem, raw, fm_text, body, parse_fields(fm_text)))
    return out


# --- finding model ----------------------------------------------------------

@dataclass
class Finding:
    rule: str
    severity: str           # "blocking" | "advisory"
    slug: str
    detail: str

    def __str__(self) -> str:
        sev = "[BLOCK]" if self.severity == "blocking" else "[advisory]"
        return f"  {sev} {self.rule:35s}  {self.slug}  — {self.detail}"


# --- the rules --------------------------------------------------------------

def rule_slug_uniqueness(entries: list[Entry]) -> list[Finding]:
    seen: dict[str, list[str]] = defaultdict(list)
    for e in entries:
        seen[e.slug].append(str(e.path.name))
    out: list[Finding] = []
    for slug, paths in seen.items():
        if len(paths) > 1:
            out.append(Finding("slug-uniqueness", "blocking", slug, f"duplicate slug across files: {paths}"))
    return out


def rule_id_filename_mismatch(entries: list[Entry]) -> list[Finding]:
    out: list[Finding] = []
    for e in entries:
        fm_id = e.fields.get("id")
        if fm_id is None or fm_id != e.slug:
            out.append(Finding("id-filename-mismatch", "blocking", e.slug, f"frontmatter id={fm_id!r} != filename={e.slug!r}"))
    return out


def rule_unknown_category(entries: list[Entry]) -> list[Finding]:
    out: list[Finding] = []
    for e in entries:
        cat = e.fields.get("category")
        if cat is None:
            out.append(Finding("unknown-category", "blocking", e.slug, "no `category` field"))
        elif cat not in ALL_KINDS:
            out.append(Finding("unknown-category", "blocking", e.slug, f"category={cat!r} not in §3 kind catalog"))
    return out


def rule_classification_consistency(entries: list[Entry], lens_covers: dict[str, str | list[str]]) -> list[Finding]:
    out: list[Finding] = []
    for e in entries:
        cat = e.fields.get("category")
        clf = e.fields.get("classified_by")
        if cat in CONTENT_KINDS and cat != "claim" and cat is not None:
            # content entries (other than claims, relations etc which still have classified_by) must have classified_by
            if not clf:
                # actually all content kinds need classified_by per §4.2
                out.append(Finding("classification-consistency", "blocking", e.slug, "content entry missing `classified_by`"))
                continue
        if clf and isinstance(clf, str):
            covers = lens_covers.get(clf)
            if covers is None:
                out.append(Finding("classification-consistency", "blocking", e.slug, f"classified_by={clf!r} but no such lens"))
            else:
                # covers may be a list (lens-policy-tier) or scalar
                covered_kinds = covers if isinstance(covers, list) else [covers]
                if cat not in covered_kinds:
                    out.append(Finding("classification-consistency", "blocking", e.slug, f"classified_by={clf!r} covers {covers!r} but entry is {cat!r}"))
    return out


def rule_infrastructure_classified_by_lens(entries: list[Entry]) -> list[Finding]:
    out: list[Finding] = []
    for e in entries:
        cat = e.fields.get("category")
        if cat in INFRA_KINDS and cat != "lens":
            if e.fields.get("classified_by"):
                out.append(Finding("infrastructure-classified-by-lens", "blocking", e.slug, f"infrastructure entry has classified_by={e.fields['classified_by']!r}; should use produced_by only"))
    return out


def rule_lens_self_classification(entries: list[Entry]) -> list[Finding]:
    out: list[Finding] = []
    for e in entries:
        if e.fields.get("category") == "lens":
            if e.fields.get("classified_by") != "lens-lens":
                out.append(Finding("lens-self-classification", "blocking", e.slug, f"lens classified_by={e.fields.get('classified_by')!r}; must be 'lens-lens'"))
    return out


def rule_unknown_domain(entries: list[Entry], known_domains: set[str]) -> list[Finding]:
    out: list[Finding] = []
    for e in entries:
        domains = e.fields.get("domains")
        if not isinstance(domains, list):
            continue
        for d in domains:
            if d and d not in known_domains:
                out.append(Finding("unknown-domain", "blocking", e.slug, f"domain={d!r} has no domain entry"))
    return out


def rule_entry_without_domain(entries: list[Entry]) -> list[Finding]:
    out: list[Finding] = []
    for e in entries:
        domains = e.fields.get("domains")
        if not isinstance(domains, list) or len(domains) == 0:
            out.append(Finding("entry-without-domain", "blocking", e.slug, "domains list missing or empty"))
    return out


def rule_tag_shadowing_domain(entries: list[Entry], known_domains: set[str]) -> list[Finding]:
    out: list[Finding] = []
    for e in entries:
        tags = e.fields.get("tags") or []
        if not isinstance(tags, list):
            continue
        shadow = [t for t in tags if t in known_domains]
        if shadow:
            out.append(Finding("tag-shadowing-domain", "advisory", e.slug, f"tag(s) shadow domain names: {shadow}"))
    return out


def rule_reserved_prefix_misuse(entries: list[Entry]) -> list[Finding]:
    out: list[Finding] = []
    for e in entries:
        cat = e.fields.get("category")
        slug = e.slug
        # If kind has a required prefix, slug must use it.
        required = RESERVED_PREFIX_FOR_KIND.get(cat) if isinstance(cat, str) else None
        if required and not slug.startswith(required):
            out.append(Finding("reserved-prefix-misuse", "blocking", slug, f"kind={cat!r} requires prefix {required!r}"))
            continue
        # If kind is a free-slug content kind, slug must NOT use any reserved prefix.
        if cat in FREE_SLUG_CONTENT_KINDS:
            for pfx in RESERVED_PREFIXES:
                if slug.startswith(pfx):
                    out.append(Finding("reserved-prefix-misuse", "blocking", slug, f"kind={cat!r} (free-slug) but slug uses reserved prefix {pfx!r}"))
                    break
    return out


def rule_broken_wikilink(entries: list[Entry], slug_index: set[str]) -> list[Finding]:
    out: list[Finding] = []
    for e in entries:
        seen_targets: set[str] = set()
        for m in WIKILINK_RE.finditer(e.body):
            target = m.group(1).strip()
            if not target or target.startswith("http"):
                continue
            if target in seen_targets:
                continue
            seen_targets.add(target)
            if target not in slug_index:
                out.append(Finding("broken-wikilink", "blocking", e.slug, f"unresolved wikilink to [[{target}]]"))
    return out


def rule_notability_stamp_missing(entries: list[Entry]) -> list[Finding]:
    out: list[Finding] = []
    for e in entries:
        if not e.fields.get("notability_status"):
            out.append(Finding("notability-stamp-missing", "blocking", e.slug, "no notability_status"))
    return out


def rule_lead_missing(entries: list[Entry]) -> list[Finding]:
    out: list[Finding] = []
    for e in entries:
        cat = e.fields.get("category")
        # threshold: body >200 words OR >2 paragraphs
        body_no_lead_section = e.body
        words = len(re.findall(r"\b\w+\b", body_no_lead_section))
        # paragraphs: blocks separated by blank lines, with >1 sentence (approx by '.')
        paragraphs = [p for p in re.split(r"\n\s*\n", body_no_lead_section) if p.strip() and not p.strip().startswith("#")]
        long_paragraphs = [p for p in paragraphs if p.count(".") > 1]
        has_lead = re.search(r"(?m)^##\s+Lead\b", body_no_lead_section) is not None
        always_required = cat in {"structure-note", "source"}
        threshold_hit = words > 200 or len(long_paragraphs) > 2
        if (always_required or threshold_hit) and not has_lead:
            severity = "blocking" if always_required else "advisory"
            out.append(Finding("lead-missing", severity, e.slug, f"body words={words}, long paragraphs={len(long_paragraphs)}; no `## Lead`"))
    return out


def rule_low_link_density(entries: list[Entry]) -> list[Finding]:
    out: list[Finding] = []
    for e in entries:
        cat = e.fields.get("category")
        if cat not in CONTENT_KINDS:
            continue
        # count outbound wikilinks; relations and disambiguations have their own rules
        links = set()
        for m in WIKILINK_RE.finditer(e.body):
            t = m.group(1).strip()
            if t and not t.startswith("http"):
                links.add(t)
        if len(links) < 2:
            out.append(Finding("low-link-density", "advisory", e.slug, f"{len(links)} outbound wikilinks (floor 2)"))
    return out


def rule_orphan_entry(entries: list[Entry]) -> list[Finding]:
    """Content entry with no inbound wikilinks from any other entry's body."""
    inbound: dict[str, set[str]] = defaultdict(set)
    for e in entries:
        for m in WIKILINK_RE.finditer(e.body):
            t = m.group(1).strip()
            if t and not t.startswith("http"):
                inbound[t].add(e.slug)
    out: list[Finding] = []
    for e in entries:
        cat = e.fields.get("category")
        if cat not in CONTENT_KINDS:
            continue
        if not inbound.get(e.slug):
            out.append(Finding("orphan-entry", "advisory", e.slug, "no inbound wikilinks from other entries"))
    return out


# --- main -------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true", help="Exit non-zero if any blocking finding")
    parser.add_argument("--rule", help="Restrict to one rule by name")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-finding output; only summary")
    args = parser.parse_args()

    entries = load_entries()
    slug_index = {e.slug for e in entries}
    known_domains = {e.slug for e in entries if e.fields.get("category") == "domain"}

    # build lens_covers index from lens entries
    lens_covers: dict[str, str | list[str]] = {}
    for e in entries:
        if e.fields.get("category") == "lens":
            cov = e.fields.get("lens_covers_category")
            if cov is not None:
                lens_covers[e.slug] = cov

    rules = [
        ("slug-uniqueness",                  rule_slug_uniqueness,                  (entries,)),
        ("id-filename-mismatch",             rule_id_filename_mismatch,             (entries,)),
        ("unknown-category",                 rule_unknown_category,                 (entries,)),
        ("classification-consistency",       rule_classification_consistency,       (entries, lens_covers)),
        ("infrastructure-classified-by-lens", rule_infrastructure_classified_by_lens, (entries,)),
        ("lens-self-classification",         rule_lens_self_classification,         (entries,)),
        ("unknown-domain",                   rule_unknown_domain,                   (entries, known_domains)),
        ("entry-without-domain",             rule_entry_without_domain,             (entries,)),
        ("tag-shadowing-domain",             rule_tag_shadowing_domain,             (entries, known_domains)),
        ("reserved-prefix-misuse",           rule_reserved_prefix_misuse,           (entries,)),
        ("broken-wikilink",                  rule_broken_wikilink,                  (entries, slug_index)),
        ("notability-stamp-missing",         rule_notability_stamp_missing,         (entries,)),
        ("lead-missing",                     rule_lead_missing,                     (entries,)),
        ("low-link-density",                 rule_low_link_density,                 (entries,)),
        ("orphan-entry",                     rule_orphan_entry,                     (entries,)),
    ]

    findings: list[Finding] = []
    by_rule: Counter = Counter()
    for name, fn, fnargs in rules:
        if args.rule and name != args.rule:
            continue
        out = fn(*fnargs)
        for f in out:
            findings.append(f)
            by_rule[(f.rule, f.severity)] += 1

    # group by rule for output
    print(f"=== wiki_lint.py — {len(entries)} entries scanned ===")
    if not findings:
        print("\nNo findings.")
        return 0

    if not args.quiet:
        for rule_name, _, _ in rules:
            rs = [f for f in findings if f.rule == rule_name]
            if not rs:
                continue
            print(f"\n--- {rule_name} ({len(rs)}) ---")
            for f in rs[:50]:
                print(str(f))
            if len(rs) > 50:
                print(f"  ... and {len(rs) - 50} more")

    print("\n=== summary ===")
    blocking = sum(c for (_, sev), c in by_rule.items() if sev == "blocking")
    advisory = sum(c for (_, sev), c in by_rule.items() if sev == "advisory")
    for (rule_name, sev), count in sorted(by_rule.items(), key=lambda x: (-x[1], x[0][0])):
        print(f"  {sev:9s}  {rule_name:35s}  {count}")
    print(f"  blocking total: {blocking}")
    print(f"  advisory total: {advisory}")

    if args.strict and blocking > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
