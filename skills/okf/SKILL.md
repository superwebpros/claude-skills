---
name: okf
description: Configure, audit, and adapt folders to Google's Open Knowledge Format (OKF v0.2), a knowledge bundle of markdown concepts with YAML frontmatter (type, title, description, sources, generated/verified trust, status/stale_after lifecycle, Attested Computations) plus index.md listings and log.md histories. Use when the user mentions OKF, Open Knowledge Format, knowledge bundles, or Knowledge Catalog, or wants to make a docs/wiki/notes folder agent-readable, check a bundle for conformance, add provenance/trust/freshness metadata, generate index.md files, or migrate OKF v0.1 to v0.2.
compatibility: Needs Python 3.9+ with PyYAML, or uv (`uv run` installs PyYAML automatically).
metadata:
  author: superwebpros
  version: "1.0"
  okf-version: "0.2"
---

# OKF: Open Knowledge Format bundles

OKF ([spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)) is a directory of markdown files. Each file is one **concept**, and its YAML frontmatter must include `type`. `index.md` and `log.md` are reserved names at every level of the tree. The spec standardizes a few optional field families that let readers judge provenance, trust, and freshness. Conformance is deliberately loose (only `type` is required), so most of the value comes from the SHOULD-level guidance. That guidance is what this skill's audit checks.

For field-level rules, see [references/okf-cheatsheet.md](references/okf-cheatsheet.md).

## Tooling

Everything goes through one script. Run it with uv, which installs PyYAML:

```bash
OKF="uv run <this-skill-dir>/scripts/okf.py"    # or: python3 <skill-dir>/scripts/okf.py (needs pyyaml)
$OKF audit  ROOT                 # conformance + lint + trust/freshness summary
$OKF plan   ROOT --out plan.json # propose edits for an existing folder (writes nothing else)
$OKF apply  plan.json [--dry-run]
$OKF index  ROOT [--group-by type] [--check]
$OKF init   ROOT
$OKF new    ROOT path/to/concept.md --type T --description "..." --by ACTOR [--log]
$OKF log    ROOT --kind Update --message "..."
```

`ROOT` is the bundle root. It can be a subdirectory of a larger repo. Dot-directories and `node_modules` are always skipped; add `--exclude GLOB` for anything else that isn't knowledge (vendored docs, build output). Run `$OKF <cmd> -h` to see all flags.

## Choose the mode

| User wants to… | Mode |
|---|---|
| start a new knowledge bundle or add concepts | **Configure** |
| check whether a folder is OKF and how healthy it is | **Audit** |
| turn an existing docs/wiki/notes folder into OKF, or move from v0.1 to v0.2 | **Adapt** |
| edit concepts in a bundle that already conforms | **Maintain** |

If the user doesn't say which folder, ask. Never assume the repo root is the bundle.

---

## Configure: a new bundle

1. Agree on the layout before creating files. Directories group concepts however suits the domain (`tables/`, `metrics/`, `playbooks/`, `computations/`). Put run instructions and attester code under `references/` (spec 6.3).
2. Agree on a **type vocabulary**: a short list of descriptive types such as `BigQuery Table`, `Metric`, `Playbook`, `Decision Record`. Types aren't registered anywhere, so consistency inside the bundle is what matters. See [references/adapting.md](references/adapting.md#type-vocabulary).
3. `$OKF init ROOT` creates a root `index.md` declaring `okf_version: "0.2"` and a `log.md` with an Initialization entry.
4. Create each concept with `$OKF new ROOT dir/name.md --type ... --description "..." --by <actor> --log`, then write the body. Prefer structural markdown (headings, tables, lists). Use the conventional headings `# Schema`, `# Examples`, and `# Computation` where they fit.
5. `$OKF index ROOT`, then `$OKF audit ROOT`.

For **Attested Computations**, `new --type "Attested Computation" --runtime bigquery` produces the full contract skeleton. Fill in `parameters` and the computation (one fenced block, or a `computation:` file path). Point `executor.resource` and `attester.resource` at real files. The attester must be deterministic code with no LLM in it.

## Audit: an existing bundle

1. `$OKF audit ROOT`. The exit code is 1 when the bundle isn't conformant (add `--strict` to also fail on warnings). Use `--json` when you need every finding to work through.
2. Report back in this order:
   - **Verdict**: conformant or not, plus the counts.
   - **Errors**: these break spec 11 conformance. Usually there are few and each fix is mechanical.
   - **Trust and freshness**: the tier breakdown (unverified / machine-confirmed / human-reviewed), stale concepts, and the share of concepts that have `sources` or `generated`. This is what tells the user whether agents can rely on the bundle.
   - **Warnings**, grouped by code. Don't list them file by file when one code covers 40 files.
3. Offer fixes. Each code and its fix is in [references/audit-checks.md](references/audit-checks.md). Mechanical fixes include missing types and descriptions, v0.1 fields, and index drift; send those through **Adapt**, which goes through a plan you can review. Fixes that need judgment, such as stale content, unkeyed footnotes, or missing provenance, need the user or the source material.

The audit never fails a bundle for unknown types, unknown keys, broken links, or missing `index.md` files, because the spec forbids rejecting a bundle for those. They show up as info.

## Adapt: an existing folder

Changes go through a reviewable plan. Don't hand-edit dozens of files.

1. **Survey.** Run `$OKF audit ROOT` to get the baseline and see what's there. Look at the tree. Ask the user who wrote the existing content, because that determines the actor in `generated.by` (see "Honest metadata" below).
2. **Plan.** Run `$OKF plan ROOT --out plan.json [--rule 'runbooks/**=Playbook' ...] [--default-type Reference] [--by human:<id>]`. Without `--by`, no provenance is added.
3. **Review the plan.** This is the step that matters. Read `plan.json` and edit it directly:
   - Look at every entry whose `type_source` is `heuristic` or `default`. Set a better `add.type` where needed, or re-run with `--rule` patterns. Keep the vocabulary small and consistent.
   - Rewrite weak `add.description` values. Each should be one sentence saying what the concept *is*, not the first line of its body.
   - `review-reserved`: an `index.md` or `log.md` that is really a concept. Either set `rename_to`, or fix the file so it follows the index/log format.
   - `fix-frontmatter-manually`: YAML that doesn't parse. Fix these by hand.
   - `migrate-v0.1`: check the generated `sources` ids. After applying, key the body footnotes to those ids.
   - Show the user a summary covering type counts, renames, and anything ambiguous before you apply.
4. **Apply.** Run `$OKF apply plan.json --dry-run`, then `$OKF apply plan.json`. Apply only inserts and migrates frontmatter keys. It never rewrites a concept body; the one exception is removing a migrated `# Citations` section. Existing keys and unknown fields are kept.
5. If anything was renamed, re-run `plan` (renamed files still need frontmatter), then run `$OKF index ROOT` and `$OKF audit ROOT`.
6. Add a log entry: `$OKF log ROOT --kind Update --message "Adapted folder to OKF v0.2 (N concepts)."`

Patterns for other ecosystems (Obsidian, Jekyll/Hugo, Notion/Confluence exports, READMEs, files that aren't markdown) are in [references/adapting.md](references/adapting.md).

## Maintain: editing a conformant bundle

Whenever you change a concept's meaning:
- Update `generated: { by: <you>, at: <now, UTC> }`. Leave `verified` alone. A re-verification is a separate event, and only the verifier can record it.
- When a source is added, append it to `sources` with a stable `id`, and attribute claims with `[^id]` footnotes.
- To retire a concept, set `status: deprecated` instead of deleting it. Other concepts may link to it.
- Afterwards, run `$OKF index ROOT` (it only rewrites indexes it generated), add a `$OKF log` entry, and run `$OKF audit ROOT`.

---

## Honest metadata (non-negotiable)

These fields exist so readers can trust the corpus. Wrong values are worse than missing ones.

- **`generated.by`** names whoever wrote the *current content*. For you, that's `<producer>/<version>`, e.g. `claude-code/claude-opus-5-5`. For content a person wrote, use `human:<id>`, and only when the user confirms who it was. For pipelines, use `process:<id>`.
- **Never write `verified`** unless the user tells you that this person or process actually confirmed the content. In particular, never write a `human:` verifier on your own initiative. An entry like that promotes the concept to "human-reviewed".
- **Never invent** `usage_count`, `usage_window`, `last_modified`, or `stale_after`. Take them from real data, or ask the user. A `stale_after` date is a policy decision that belongs to the user.
- **Attested Computations:** never author or edit the computation, which means the SQL or model inside the `# Computation` fence or `computation` file (spec 10.3). You may fill in the surrounding contract and prose; changing what gets computed is the owner's job.
- Every timestamp needs an ISO 8601 value with an explicit offset: `2026-06-30T14:00:00Z`.

## Gotchas

- **Relative paths in `executor.resource`/`attester.resource`/`computation`** resolve from the concept's own directory (spec 6.2). The spec's own examples write `references/...` but mean the bundle root. Write `/references/...` (bundle-relative). The audit reports this as `path-resolved-from-root`.
- **`okf_version` is allowed only in the root `index.md`'s frontmatter, and must be quoted** (`"0.2"`). Any other `index.md` may not have frontmatter at all. `log.md` date headings must be `## YYYY-MM-DD`, newest first.
- **README.md is a concept.** Only `index.md` and `log.md` are reserved, so a README needs a `type` too (usually `Overview`).
- **`index` overwrites only files it generated**, which it marks with an `<!-- okf:generated ... -->` line. Hand-curated indexes are skipped unless you pass `--force`. Use `index --check` in CI.
- **Broken links are allowed.** They may point to knowledge that hasn't been written yet. Report them; don't "fix" them by deleting the link.
- Keep **one concept per file**. When a v0.1 doc holds several figures with SQL, split each figure into its own Attested Computation and link to them from a narrative concept (spec Appendix A).

## Reference files

- [references/okf-cheatsheet.md](references/okf-cheatsheet.md): every field, with MUST/SHOULD level and spec section.
- [references/audit-checks.md](references/audit-checks.md): every audit code, what it means, and how to fix it.
- [references/adapting.md](references/adapting.md): type vocabulary, plan JSON format, and recipes for specific ecosystems.
