# Adapting existing folders

## Type vocabulary

`type` has no central registry. It's the main routing signal for readers, so keep it **descriptive, consistent, and small**: aim for 5 to 15 types per bundle. Examples from the spec and its conventions:

| Type | For |
|---|---|
| `BigQuery Table`, `BigQuery Dataset`, `Postgres Table` | Physical data assets. Name the platform; set `resource` to the asset URI. |
| `API Endpoint` | One endpoint or operation. Use `resource` for its URL or OpenAPI pointer. |
| `Metric` | A business definition. Link to its Attested Computation(s). |
| `Attested Computation` | A sanctioned, parameterized computation (spec §10). |
| `Playbook` | Runbooks and incident steps. |
| `Reference` | Mirrored external material and run instructions under `references/`. |
| `Overview` | READMEs and landing pages. |
| `Decision Record`, `Policy`, `Process`, `Guide`, `Glossary Term`, `Meeting Notes`, `Specification` | Common wiki content. |

Rules of thumb:
- Prefer a platform-specific type (`BigQuery Table`) over a generic one (`Table`) when the platform matters to readers.
- Don't encode status or team in `type`. Use `status` and `tags` for that.
- When one folder mixes kinds of content, pass `--rule` globs to `plan` instead of patching JSON by hand: `--rule 'adr/*=Decision Record' --rule '**/runbook*=Playbook'`. The first matching rule wins.

## How `plan` decides

For each concept file, in this order:

1. **type**: `--rule` glob (`type_source: rule`), then an existing `kind`/`category`/`layout`/`doc_type` field (`existing-field:<k>`), then keywords in the filename and directories (`heuristic`), then `--default-type` (`default`). Always review `heuristic` and `default`.
2. **title**: existing `title`, then the first `# H1`, then the humanized filename.
3. **description**: existing `summary`/`excerpt`/`abstract`, then the first sentence of the first prose paragraph (capped at 200 characters).
4. **generated**: added only when you pass `--by`. `at` comes from the file's last git commit, falling back to its mtime.
5. **v0.1**: a `timestamp` becomes `generated` (needs `by`); a `# Citations` list becomes `sources` with slug ids.
6. **reserved names**: an `index.md` that reads like prose, or a `log.md` without date headings, is flagged `review-reserved` with a `suggested_rename`. Nothing is renamed unless you set `rename_to`.

## Plan JSON

```json
{
  "okf_plan": 1, "root": "/abs/path", "by": "human:jesse",
  "summary": { "files_scanned": 120, "files_to_change": 97, "actions": {...}, "type_sources": {...}, "proposed_types": {...} },
  "files": [
    {
      "path": "runbooks/oncall.md",
      "actions": ["add-frontmatter"],          // add-frontmatter | add-fields | fix-fields | migrate-v0.1 | review-reserved | fix-frontmatter-manually
      "type_source": "heuristic",
      "add":     { "type": "Playbook", "title": "...", "description": "...", "generated": { "by": "...", "at": "..." } },
      "fix":     { "tags": ["a", "b"] },         // replaces an existing single-line key
      "migrate": { "generated": {...}, "sources": [ { "id": "...", "resource": "...", "title": "..." } ] },
      "rename_to": null, "suggested_rename": "notes/notes-overview.md",
      "notes": ["..."]
    }
  ]
}
```

Edit it freely before running `apply`:
- Delete a key from `add` to leave it out. Delete a whole entry to skip that file.
- Set `migrate.generated.by` when you know who wrote a v0.1 file.
- Set `rename_to` to move a reserved-name concept. Inbound links aren't rewritten; the audit reports them as `broken-link`, so fix them afterwards with a search-and-replace.

`apply` re-reads every file, inserts only the keys that are still missing, checks that the result parses before writing, and skips files that changed shape since planning. It is safe to re-run.

## Ecosystem recipes

**Obsidian vaults.** Keep the existing frontmatter; extensions are allowed. `[[wikilinks]]` aren't OKF links, so convert the ones that matter to `[text](/path.md)`. Exclude `.obsidian/` (dot-directories are skipped automatically) and `--exclude 'templates/*'`. Tags written as `#tag` in the body don't count; lift them into the `tags:` list.

**Jekyll / Hugo / Docusaurus sites.** `layout`, `category`, and `kind` give type hints. `date` is publication time, not content provenance, so only map it to `generated.at` if the user confirms nothing changed after publication. Exclude `_site/`, `public/`, `build/`, and includes or partials. `_index.md` (Hugo) isn't reserved in OKF, so it's a concept, typically an `Overview`.

**Notion / Confluence exports.** Filenames often carry ID hashes (`Page 3f9a…md`). Rename to slugs *before* planning so concept IDs stay stable. Attachments go under `references/` or stay alongside the pages; only `.md` files are concepts.

**Code repos with docs.** Use `docs/` (or wherever the knowledge lives) as ROOT, not the repo root, unless the user wants every README in the repo to be a concept. Exclude `CHANGELOG.md`, `CONTRIBUTING.md`, and similar files unless they're useful as knowledge.

**Data catalogs and schema dumps.** One concept per asset: `type: BigQuery Table`, `resource:` set to the console or asset URI, a `# Schema` table, and joins as links. Generate these from the catalog API with a small script rather than writing them by hand.

**Non-markdown knowledge (PDFs, sheets, SQL files).** Leave the files where they are. Create a concept per artifact whose `resource` points at the file or URL, with a description and summary written in the body. SQL that defines a sanctioned figure should become an Attested Computation with `computation: /path/to/file.sql`.

**v0.1 bundles.** Run `plan --by <actor>`. That migrates `timestamp` and `# Citations`. Then split multi-figure docs into Attested Computations linked from a narrative concept (spec Appendix A), and key the footnotes to the new source ids.

## After adapting

1. `okf.py index ROOT` (add `--group-by type` for large flat directories).
2. `okf.py audit ROOT`. It should report 0 errors.
3. Report: concepts by type, trust tiers (expect all unverified at this point, which is honest), and what's left that needs human judgment: descriptions, footnote keys, `verified`, `stale_after` policy.
4. `okf.py log ROOT --kind Update --message "Adapted to OKF v0.2"`.
