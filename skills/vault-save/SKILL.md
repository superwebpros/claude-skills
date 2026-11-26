---
name: vault-save
description: Save new content into a markdown knowledge vault (Obsidian, OKF bundle, notes repo) so it is findable later without anyone being told where it went. Resolves the right folder from the vault's own routing (AGENTS.md, index.md, registry), writes the file with the vault's frontmatter, adds its line to the folder index, and appends a dated entry to log.md. Use whenever you create, file or substantially update a document in a vault (a draft, ad, script, note, report, plan, recipe, statement), or the user says "save", "file", "put it in the vault", "draft this". Also use to find recently saved work.
metadata:
  author: superwebpros
  version: "1.0"
---

# Vault save

A vault only stays useful if every new file lands in its known place and is linked from somewhere. Do
all four steps every time you save; a file with no index line and no log entry is effectively lost.

The skill is vault-agnostic. Each vault describes its own layout; read it, don't assume it.

## 0. Find the vault root

Walk up from your working directory (or from the target path, if you were given one) to the first
folder that has an `AGENTS.md`, a root `index.md`, or a `.obsidian/` folder. That is `VAULT`. All
paths below are relative to it. If you can't find one, ask where to save instead of guessing.

## 1. Resolve the path

Read, in this order, stopping once the home is clear:

1. `VAULT/AGENTS.md` (and `CLAUDE.md` if it carries rules rather than just pointing to `AGENTS.md`).
   Look for "where things live", scoping rules, inbox rules and save rules.
2. `VAULT/index.md`, then follow its links down: the area's `index.md` or `README.md`, then the
   sub-area's. Descend until you reach the folder that describes this kind of content.
3. A routing table if the vault has one (`registry.md` or similar), whenever the content has to be
   attributed to a product, client, campaign or account. Route by the table, never by a name.

Pick the **deepest existing folder** that the indexes describe as the home for this kind of content
(e.g. a campaign's `copy/` or `drafts/` folder rather than the campaign root, a `finance/` folder
for a statement). Rules:

- Prefer an existing folder. Create a new subfolder only when the index or `AGENTS.md` names a
  pattern for it (e.g. `campaigns/<YYYY-MM>_<slug>/`) and the content fits that pattern.
- Never create a new top-level folder, and never move or rename existing files as part of a save.
- If the vault has an inbox rule (for example, "recommendations go to `_inbox/`"), follow it.
- If two homes fit equally well, ask. If you can't ask (unattended run), save to the vault's inbox
  folder if it has one and say so in your reply.

**Filename.** Match the siblings: dated (`YYYY-MM-DD_slug.md`), numbered (`06-slug.md`, next free
number), or plain kebab-case. Check the name is free first. Never overwrite another file; if the
file you mean to update already exists, edit it on purpose and treat it as an update (step 4).

## 2. Write the file with the vault's frontmatter

Copy the frontmatter shape from one or two siblings in the same folder, then check it against the
conventions in `AGENTS.md`. Minimum for any OKF vault:

```yaml
---
type: Ad Draft                  # REQUIRED in OKF vaults; reuse the type siblings use
title: "Human-readable title"
description: One sentence; it is reused as the index line.
status: draft                   # if the vault uses status
generated: { by: <your actor string, e.g. bot-name/model>, at: 2026-01-31T14:05:00Z }
tags: [short, list]
---
```

Add every field the vault asks for (for example `product`, `sources`, `stale_after`). Rules:

- `type` is mandatory if the vault is OKF or says so. Never leave a concept file without it.
- Agent-written content is unverified: leave the `verified` field out entirely (not even
  `verified: false`). Only a person adds it.
- `generated.at` is an ISO 8601 timestamp in UTC; other dates are `YYYY-MM-DD`.
- Links inside the body follow the vault's style (bundle-absolute `/area/file.md` or relative).
- No secrets, tokens or credentials, ever. Refer to them by file and variable name if needed.

`index.md` and `log.md` are reserved names in OKF: never use them for content.

## 3. Add or update the folder's index line

Find the index for the folder you wrote into: its own `index.md`, else its `README.md`. If it has
neither, use the nearest ancestor `index.md`/`README.md` that lists the folder.

- **Generated block present** (`<!-- generated:start -->` … `<!-- generated:end -->`): do not edit
  inside the markers. A scheduled reindex job rebuilds that block from each file's frontmatter
  (`title`, `description`), so good frontmatter is all you need. Don't add a hand line for the same
  file elsewhere in that index either. Say "index: generated block, picked up on the next reindex".
- **Hand-written index**: add one line in the style already used there, in the right section:
  - OKF catalog bullet: `* [Title](/path/to/file.md) - description`
  - a plain list, a table row, or a tree diagram entry (`│   ├── 06-slug.md   # description`):
    copy whatever the file already does, including its link style.
- **Folder not listed by any index**: add a line for the folder (or the file) to the nearest
  ancestor index, so a reader can reach it from the vault root. Don't create a new `index.md`
  unless `AGENTS.md` says every folder has one.
- **Updating an existing file**: keep its existing line; edit the description only if it changed.

Change only your line. Don't reformat, reorder or "tidy" the rest of the index.

## 4. Append a dated entry to `VAULT/log.md`

If the vault has no `log.md`, create it at the root:

```markdown
# Log

## 2026-01-31
* **Creation**: ...
```

Follow the existing log's format exactly. Usually that is `## YYYY-MM-DD` date headings with
bullets `* **Kind**: what changed, with the path`. Kind is a short bold word: `Creation`, `Update`,
`Draft`, `Report`, or a topic label if that's the house style.

- Use today's local date. If a heading for today already exists, add your bullet at the end of that
  day's bullets. Don't add a second heading for the same date.
- Otherwise add a new heading where this log puts new days. Look at the dates: if the newest date is
  at the bottom, append at the end of the file; if it's at the top, insert below the title. A new
  log is newest-first (OKF §9).
- One bullet per save: what it is, its path in backticks or as a link, and who saved it (your
  name). Example:
  ``* **Draft**: Holiday ad variant B saved to `campaigns/2026-01_launch/copy/variant-b.md` (Copywriter, unverified).``

## 5. Vault-specific extras, then report

If `AGENTS.md` asks for more on every save (an external catalog row, a changelog, a task update),
do it or say plainly that you didn't. Then report in one short block:

```
Saved:  <path>
Index:  <index file> (line added | line updated | generated block, next reindex)
Log:    log.md, <date> entry
```

## Finding saved work

To answer "where is the latest X" without being told the path:

1. Read the newest entries in `VAULT/log.md` (top or bottom, per its order) and search it for the
   topic.
2. If the vault has a changed-files report (for example `_meta/changed.md` written by a nightly
   job), read it.
3. Walk `index.md` down to the area and read its index, or search the vault (`grep -ril`) for the
   title or frontmatter `type`.

Give the path, the title, the date from the log, and who saved it.
