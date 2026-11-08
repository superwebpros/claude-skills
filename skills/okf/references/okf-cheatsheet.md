# OKF v0.2 cheatsheet

Condensed from the [OKF v0.2 spec](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md). Section numbers (§) refer to the spec. MUST means required for conformance, SHOULD means recommended guidance, and MAY means optional.

## Bundle layout (§3)

```
bundle/
  index.md        # optional listing (§8); root one MAY carry `okf_version: "0.2"` frontmatter
  log.md          # optional history (§9)
  <concept>.md    # every other .md file is a concept
  <dir>/index.md, <dir>/log.md, <dir>/<concept>.md ...
  references/     # convention: mirrored external material, run instructions, attester code (§6.3)
```

- The **concept ID** is the file's path inside the bundle, without `.md`.
- `index.md` and `log.md` are reserved at every level and MUST NOT be used as concept files.
- A bundle can be shipped as a git repo (recommended), a tarball or zip, or a subdirectory of a larger repo.

## Conformance (§11): the only hard rules

1. Every non-reserved `.md` has a frontmatter block that parses as YAML.
2. Every frontmatter block has a non-empty `type`.
3. Any `index.md` follows §8 and any `log.md` follows §9.

Consumers MUST NOT reject a bundle for missing optional fields, unknown types, unknown keys, broken links, or missing `index.md` files. They MUST treat a bare `verified` mapping as a list with one element.

## Concept frontmatter (§4.1)

| Key | Level | Notes |
|---|---|---|
| `type` | **MUST** | Short descriptive string. Not centrally registered; unknown types are treated as generic concepts. |
| `title` | SHOULD | Display name; falls back to the filename. |
| `description` | SHOULD | One sentence. Used in `index.md`, search snippets, and previews. |
| `resource` | SHOULD (when bound) | Canonical URI of the underlying asset. Leave it out for abstract concepts. |
| `tags` | MAY | YAML list of short strings. |
| *anything else* | MAY | Extensions. Consumers keep them when round-tripping and never reject them. |

## Provenance (§5.1)

```yaml
sources:
  - id: ga4-schema                 # SHOULD when the body cites it; stable key for footnotes
    resource: https://...          # REQUIRED per entry: URL, /bundle/path, relative path, or a scope descriptor
    title: GA4 BigQuery Export schema
    author: team:ga4-docs          # credibility signal (actor-like)
    usage_count: 5000              # credibility signal, framed by usage_window
    last_modified: 2026-05-30T00:00:00Z
usage_window: { from: 2026-06-01T00:00:00Z, to: 2026-06-30T00:00:00Z }   # sibling of sources; entries may override
```

- Attribute a claim with a **keyed footnote**, `[^ga4-schema]`. The label must match a `sources[].id`; don't use positional labels like `[^1]`.
- OKF stores signals, not scores. Credibility is something a reader *infers* from them.
- Lineage is expressed as links. A `resource` that points at another concept is already an edge in the graph.

## Trust (§5.2, §5.3, §7)

```yaml
generated: { by: claude-code/claude-opus-5-5, at: 2026-06-20T22:53:05Z }   # by REQUIRED inside generated
verified:
  - { by: human:ahormati, at: 2026-06-25T09:00:00Z }
  - { by: process:finance-nightly, at: 2026-06-26T02:00:00Z }
```

- **Actors:** `<producer>/<version>` for an agent or tool, `human:<id>` for a person, `process:<id>` for an automated process. Anything a person wrote or confirmed MUST use `human:`.
- **Tiers:** no `verified` means **unverified**; non-human verifiers only means **machine-confirmed**; any `human:` verifier means **human-reviewed**. Tiers are advisory and are not access control.
- `generated.at` is the last *meaningful content change*. It's separate from `verified`.

## Lifecycle (§5.4, §5.5)

```yaml
status: stable                         # draft | stable | deprecated ; absent ⇒ stable
stale_after: 2026-09-23T00:00:00Z      # stale when now >= stale_after (absolute instant, not a TTL)
```

All timestamps are ISO 8601 with an explicit UTC offset.

## Links and paths (§6)

- Use `[text](/tables/customers.md)` to link relative to the bundle root (**recommended**), or `[text](./other.md)` for a relative link.
- Path-valued fields are `resource`, `sources[].resource`, `computation`, `executor.resource`, and `attester.resource`. Each takes a URL, a `/bundle-path`, or a path relative to the concept file.
- A link asserts an untyped relationship; the surrounding prose says what kind. Broken links are tolerated.

## Body (§4.2)

There are no required sections, and structured markdown is preferred. Conventional headings: `# Schema`, `# Examples`, `# Computation`. The v0.1 `# Citations` heading is superseded by `sources` plus footnotes.

## Attested Computation (§10)

```yaml
type: Attested Computation
runtime: bigquery                      # REQUIRED for this type; defines what parameters mean
parameters:
  - { name: year, type: integer, required: true }
computation: /references/computations/revenue.sql   # optional; else ONE fenced block under `# Computation`
executor:
  resource: /references/skills/run-on-bq.md         # run instructions/code
  receipt: [job_id, executed_sql, result]           # fields a run must return
attester:
  resource: /references/attesters/sql-equality.py   # deterministic, no-LLM verdict over the receipt
```

- Each figure is its own concept. A Metric or overview concept links to one computation per figure.
- Agents supply **parameter values only**. They MUST NOT author or edit the computation.
- `verified` confirms the *definition*. **Attestation** confirms a single *run*, happens at runtime, and is never stored in the bundle.

## index.md (§8)

```markdown
# Section heading

* [Title](relative-url) - description from the concept's frontmatter
* [Subdirectory](subdir/) - what's in it
```

`index.md` takes no frontmatter, except that the bundle-root one may hold `okf_version: "0.2"`.

## log.md (§9)

```markdown
# Directory Update Log

## 2026-05-22
* **Update**: Added [Customer Metrics](/tables/customer-metrics.md).
* **Creation**: Established the [Dataplex Playbook](/playbooks/dataplex.md).
```

Date headings MUST be `YYYY-MM-DD`, newest first. The leading bold word is a convention.

## v0.1 → v0.2 (§13)

- `timestamp` becomes `generated: { by, at }`. Readers may fall back to `timestamp`.
- A body `# Citations` list becomes frontmatter `sources` plus keyed footnotes.
- Everything else is additive.
