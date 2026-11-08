#!/usr/bin/env python3
"""Validate every SKILL.md against the Agent Skills spec (stdlib only).

Checks skills/*/SKILL.md and plugins/*/skills/*/SKILL.md:
  - frontmatter delimited by '---' lines at the top of the file
  - name: present, equals folder name, ^[a-z0-9]+(-[a-z0-9]+)*$, <= 64 chars
  - description: present, non-empty, <= 1024 chars
  - allowed-tools (if present): space-delimited, no commas
  - SKILL.md > 500 lines -> WARNING only

Usage: python3 scripts/validate-skills.py [repo_root]
Exit 1 if any error, 0 otherwise (warnings never fail).
"""
import os
import re
import sys
from pathlib import Path

GHA = os.environ.get("GITHUB_ACTIONS") == "true"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
TOP_KEY_RE = re.compile(r"^([A-Za-z0-9_-]+):(.*)$")


def unquote(v):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        inner = v[1:-1]
        return inner.replace("''", "'") if v[0] == "'" else inner.replace('\\"', '"')
    return v


def parse_frontmatter(text):
    """Return (dict of top-level keys -> string value, error or None).

    Minimal YAML: handles `key: value`, quoted scalars, block scalars (| / >),
    and plain multi-line continuations. Nested mappings (e.g. metadata:) are
    captured as raw text, which is enough for the checks here.
    """
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "missing frontmatter (file must start with '---')"
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration:
        return None, "unterminated frontmatter (no closing '---')"
    fm, key, buf, style = {}, None, [], None

    def flush():
        if key is None:
            return
        body = [b for b in buf]
        if style == "|":
            fm[key] = "\n".join(b.strip() for b in body).strip()
        else:
            fm[key] = unquote(" ".join(b.strip() for b in body if b.strip()))

    for raw in lines[1:end]:
        if raw.strip().startswith("#") and not raw.startswith(" "):
            continue
        m = TOP_KEY_RE.match(raw) if not raw[:1].isspace() else None
        if m:
            flush()
            key, rest = m.group(1), m.group(2).strip()
            if rest[:1] in ("|", ">"):
                style, buf = rest[0], []
            else:
                style, buf = None, [rest] if rest else []
        elif key is not None:
            buf.append(raw)
    flush()
    return fm, None


def validate(skill_md):
    errors, warnings = [], []
    folder = skill_md.parent.name
    text = skill_md.read_text(encoding="utf-8")
    fm, err = parse_frontmatter(text)
    if err:
        return [err], warnings

    name = fm.get("name", "").strip()
    if not name:
        errors.append("name: missing")
    else:
        if name != folder:
            errors.append(f"name: '{name}' does not match folder '{folder}'")
        if not NAME_RE.match(name):
            errors.append(f"name: '{name}' must match ^[a-z0-9]+(-[a-z0-9]+)*$")
        if len(name) > 64:
            errors.append(f"name: {len(name)} chars (max 64)")

    desc = fm.get("description", "").strip()
    if not desc:
        errors.append("description: missing or empty")
    elif len(desc) > 1024:
        errors.append(f"description: {len(desc)} chars (max 1024)")

    if "allowed-tools" in fm and "," in fm["allowed-tools"]:
        errors.append("allowed-tools: must be space-delimited (found commas)")

    n = len(text.splitlines())
    if n > 500:
        warnings.append(f"SKILL.md is {n} lines (recommended <= 500)")
    return errors, warnings


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    files = sorted(root.glob("skills/*/SKILL.md")) + sorted(
        root.glob("plugins/*/skills/*/SKILL.md")
    )
    if not files:
        print("No SKILL.md files found.")
        return 1
    n_err = n_warn = 0
    for f in files:
        rel = f.relative_to(root)
        errors, warnings = validate(f)
        status = "FAIL" if errors else ("WARN" if warnings else "OK  ")
        print(f"{status} {rel}")
        for e in errors:
            print(f"     ERROR: {e}")
            if GHA:
                print(f"::error file={rel}::{e}")
        for w in warnings:
            print(f"     WARNING: {w}")
            if GHA:
                print(f"::warning file={rel}::{w}")
        n_err += bool(errors)
        n_warn += bool(warnings)
    print(f"\n{len(files)} skills checked: {n_err} failed, {n_warn} with warnings.")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
