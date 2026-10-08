# Audit checks

`okf.py audit` reports three severities:

- **error**: breaks spec 11 conformance. The exit code is 1.
- **warning**: goes against SHOULD-level guidance or a MUST inside an optional family. The exit code is 1 only with `--strict`.
- **info**: tolerated by the spec but worth knowing. Hidden unless you pass `--min-severity info`.

"Adapt" in the Fix column means `plan`/`apply` fixes it mechanically.

## Errors (conformance)

| Code | Meaning | Fix |
|---|---|---|
| `missing-frontmatter` | A concept `.md` file has no `---` YAML block | Adapt (`add-frontmatter`) |
| `invalid-frontmatter` | The block isn't parseable YAML or isn't a mapping | By hand: usually an unquoted `:`, `[`, or `#` in a value. Quote it. |
| `missing-type` | No `type`, or `type` is empty or not a string | Adapt (`add-fields`), then review the inferred type |
| `not-utf8` | The file isn't UTF-8 | Re-encode (`iconv -f latin1 -t utf-8`) |
| `index-frontmatter` | A non-root `index.md` has frontmatter, or the root one has keys other than `okf_version` | Move the metadata into a concept, or delete it |
| `log-bad-date` | A `##` heading in `log.md` isn't `YYYY-MM-DD` | Rewrite the headings as dates. If the file is really a concept, rename it (Adapt `review-reserved`) |

## Warnings

| Code | Meaning | Fix |
|---|---|---|
| `missing-description` | No one-sentence `description` | Adapt proposes one from the first paragraph. Rewrite weak ones. |
| `tags-not-list` | `tags: a, b` written as a string | Adapt (`fix-fields`) |
| `invalid-status` | `status` isn't draft, stable, or deprecated | Map it (e.g. `wip`→`draft`, `archived`→`deprecated`) |
| `stale` | `now >= stale_after` | Re-check against the sources. If still true, record verification (only the verifier can) and move `stale_after` forward. Otherwise update the content or deprecate it. |
| `bad-datetime` | A timestamp isn't ISO 8601 with an explicit offset | Add `Z` or `+00:00`. Date-only values need a time. |
| `bad-actor` | `generated.by`/`verified.by` doesn't follow the actor convention | `tool/version`, `human:id`, or `process:id` |
| `bad-generated` | `generated` isn't `{ by, at }` or has no `by` | Add `by` |
| `bad-verified` | A `verified` entry is missing `by` or `at` | Fix the entry. Never invent a verifier. |
| `bad-sources` | A sources entry has no `resource`, `usage_count` isn't an integer, or `usage_window` is malformed | Fix the entry |
| `duplicate-source-id` | Two sources share an `id` | Make the ids unique and update the footnotes |
| `footnote-unkeyed` | A footnote label (e.g. `[^1]`) doesn't match any `sources[].id` | Rename the footnote to the source id it relies on. This needs judgment, so read the claim. |
| `legacy-timestamp` | v0.1 `timestamp` | Adapt (`migrate-v0.1`, requires `--by` or setting `migrate.generated.by`) |
| `legacy-citations` | v0.1 `# Citations` section | Adapt moves it to `sources`. Then key the footnotes. |
| `ac-missing-runtime` | Attested Computation without `runtime` | Ask the owner which engine runs it |
| `ac-bad-parameters` | A parameter entry lacks `name`/`type`/`required` | Complete it |
| `ac-no-computation` | No `# Computation` fence and no `computation:` path | Ask the owner. Don't write the computation yourself. |
| `ac-ambiguous-computation` | Both a `computation:` path and an inline fence | Keep one. Ask which one is sanctioned. |
| `ac-multiple-fences` | More than one fenced block under `# Computation` | Split into separate computations, or move extras elsewhere |
| `ac-bad-executor` / `ac-bad-attester` | No `resource`, or `receipt` isn't a list | Complete the contract |
| `missing-path-target` | `computation`/`executor.resource`/`attester.resource` points at nothing | Create the file or fix the path |
| `path-outside-bundle` | The path escapes the bundle root | Mirror the material under `references/` |
| `index-structure` | `index.md` isn't headed sections of `* [T](url) - desc` items | `okf.py index --force`, or restructure it by hand |
| `index-missing-entry` | A concept or subdirectory isn't listed in its directory's `index.md` | `okf.py index`, or add the entry if the index is hand-curated |
| `index-dead-entry` | An index entry points at a missing file | Remove the entry or restore the file |
| `okf-version-unquoted` | `okf_version: 0.2` parses as a float | Quote it: `"0.2"` |
| `log-frontmatter` | `log.md` has frontmatter | Remove it |
| `log-order` | Log dates aren't newest first | Reorder the sections |

## Info

| Code | Meaning |
|---|---|
| `missing-title` | No `title`. Readers fall back to the filename. |
| `long-description` | The description runs over one sentence or 240 characters. |
| `broken-link` | A link's target doesn't exist. The spec tolerates this (it may be unwritten knowledge). |
| `footnotes-without-sources` | There are footnotes but no keyed `sources`. |
| `usage-without-window` | `usage_count` with no `usage_window` framing it. |
| `path-resolved-from-root` | A relative path only resolves from the bundle root. Write `/path`. |
| `ac-no-executor` / `ac-no-attester` | A computation that nothing can run or check yet. |
| `no-root-index` | No root `index.md`, so no `okf_version` is declared. |
| `reserved-name-case` | e.g. `Index.md`, which differs from a reserved name only by case. |

## Summary fields (`--json` → `summary`)

`conformant`, `concepts`, `errors/warnings/info`, `by_type`, `trust_tiers` (unverified / machine-confirmed / human-reviewed), `status`, `stale` (list of paths), `attested_computations`, `with_sources`, `with_generated`, `directories_without_index`, `okf_version`.

For a health read-out, the share of concepts that are human-reviewed and the share that have `sources` tell you more than the error count.
