# How to Access the Swipe File

The swipe file is a Qdrant vector database containing analyzed marketing content (sales letters, video scripts, ad creatives, landing pages, and more).

## Preferred: MCP Connector (Swipe File MCP)

The swipe file has a dedicated MCP connector at `https://connectors.agentskillshop.com/swipe-file/mcp` that exposes four purpose-built tools — one per retrieval dimension. When this MCP server is installed, **use the MCP tools instead of curl**. They handle vector routing, search_mode flags, and granularity automatically.

### MCP Tools

| MCP Tool | Maps To | Use When |
|----------|---------|----------|
| `search_swipe_content` | `content_dense` (page-level) | Finding content by topic, niche, product, phrase, or industry |
| `search_swipe_strategy` | `analysis_dense` (page-level) | Studying HOW content persuades — techniques, frameworks, structural patterns |
| `search_swipe_visuals` | `image_dense` + `search_mode: image_text` | Finding content by visual appearance — layout, color, composition |
| `search_swipe_sections` | `content_dense` + `granularity: section` | Finding landing page building blocks (heroes, feature grids, CTAs, etc.) |

The four tools map 1:1 to the four-parallel-query pattern described below. Run all four in parallel for design/layout work.

### Detecting MCP Availability

Before your first swipe file query, check whether the MCP tools are available in your current session. Look for tools matching `search_swipe_content`, `search_swipe_strategy`, `search_swipe_visuals`, or `search_swipe_sections`.

- **MCP available** — use the MCP tools directly. No curl needed.
- **MCP not available** — alert the user: _"The Swipe File MCP connector is not installed in this session. You can add it from `https://connectors.agentskillshop.com/swipe-file/mcp` in your Claude Code MCP settings. Falling back to direct API calls."_ Then use the curl fallback below.

### Graceful Degradation (no MCP, no API)

If neither the MCP tools nor the curl API are reachable:
1. Alert the user that the swipe file is unavailable.
2. Proceed using the framework references and deliverable specs in `bmad-mkt-knowledge/references/frameworks/` and `bmad-mkt-knowledge/resources/deliverable-specs/`. These contain the strategic principles and structural patterns the swipe file grounds — they are less specific (no real-world examples) but sufficient for production work.
3. Note "Swipe file unavailable — proceeding with framework references only" in your output so the user knows the work was not swipe-grounded.

---

## Fallback: Direct API (curl)

When the MCP connector is not installed, query the Cloudflare Worker REST API directly. No API key required.

```bash
curl -s -X POST "https://swipe-to-qdrant.jesse-41b.workers.dev/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "<your search query>",
    "vector": "analysis_dense",
    "content_type": "<content_type from swipe_query>",
    "limit": <limit from swipe_query>
  }'
```

Parse the JSON response — results are in the `results` array. Each result includes:
- `name` — title of the content piece
- `analysis_text` — the AI-generated strategic analysis (**READ THIS** — it's what grounds your creative decisions)
- `analysis_section` — which analysis field matched (e.g., "Hook Analysis", "Belief Chain")
- `content_text` — the raw source material
- `image_urls` — presigned URLs for any images (fetch and view these for graphic results)
- `score` — relevance score (0-1)
- `content_type`, `industry`, `persuasion_techniques` — metadata
- `granularity`, `section_label`, `section_text`, `item_count`, `layout_orientation`, `archetype_tags` — present on section-level hits (see "Granularity" section below)
- `funnel_group`, `funnel_step`, `funnel_role` — present on landing_page hits that belong to a funnel (see "Funnel Queries" section below)

## Query Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `query` | Yes (in semantic mode) | Natural language search query. Ignored when `mode: structured`. |
| `mode` | No (default: `semantic`) | `"semantic"` embeds the query and ranks by similarity. `"structured"` is a pure metadata scroll — no embedding, no ranking (score=0), requires at least one filter. Use structured when the query is a *shape*, not a *meaning*. |
| `vector` | No (default: `content_dense`) | `content_dense` (topic/copy search), `analysis_dense` (technique/strategy search, page-level only), or `image_dense` (visual search, page-level only). Forced to `image_dense` when `search_mode: image_text`. |
| `granularity` | No (no default — both page and section returned) | `"page"` restricts to whole-page points (content chunks, analysis sections, images). `"section"` restricts to per-section landing-page legos. **Section points exist only on `content_dense` for `content_type: landing_page`.** |
| `section_label` | No | Exact primary-label match on section points: `hero`, `feature_grid`, `founder_story`, `pricing_table`, `social_proof_logos`, `testimonial_quote`, `faq_accordion`, `cta_band`, `comparison_table`, `process_steps`, `stat_callout`, `problem_agitation`, `benefit_list`, `guarantee_band`, `bonus_stack`, `trust_bar`, `lead_magnet_optin`. Pair with `granularity: section`. |
| `archetype_tags` | No | Array of archetype names (OR-matched). Returns sections whose `archetype_tags` contains any of these. Use for cross-cut retrieval across primary labels. Common tags: `social_proof`, `authority_proof`, `transformation_story`, `risk_reversal`, `urgency_trigger`, `scarcity_trigger`, `objection_handler`. |
| `item_count` | No | Exact integer match (e.g., `6` for 6-item feature grids). Pair with `granularity: section`. |
| `layout_orientation` | No | One of `vertical`, `horizontal`, `grid`, `carousel`, `alternating`. Pair with `granularity: section`. |
| `content_type` | No | Filter to a single content type: `video_script`, `sales_letter`, `youtube_video`, `graphic`, `video_short`, `landing_page`, `video_ad` |
| `industry` | No | Filter: `saas`, `ecommerce`, `coaching`, `agency`, `info products`, `health`, `finance`, etc. |
| `analysis_section` | No | Filter to a specific analysis field on `analysis_dense` hits: `Hook Analysis`, `Belief Chain`, `Funnel Strategy`, `Offer Structure`, `Visual Hierarchy`, etc. |
| `search_mode` | No (default: `text`) | **REQUIRED when `vector: image_dense`.** Set to `image_text` for visual similarity search. Without it, image_dense queries fail with a 1536/512 dimension mismatch. |
| `limit` | No (default: 10) | Number of results (1-50) |
| `group_by_record` | No (default: true for page, false for section) | Dedupe results to one row per `baserow_id`. Auto-flips to `false` when `granularity: section` so you get multiple legos per page. |
| `include_content` | No (default: true) | Set false for lightweight metadata-only results |
| `funnel_group` | No | String. Shared slug for all pages in the same funnel (e.g. `"aesthetic-micro-offer"`). Use to retrieve a complete funnel sequence. Landing-page only. |
| `funnel_step` | No | Integer. 1-indexed position in the funnel sequence. Use to compare how different funnels open (`funnel_step: 1`) or to retrieve a specific step. Landing-page only. |
| `funnel_role` | No | String. Functional role of the page: `offer`, `checkout`, `schedule`, `thank_you`, `upsell`, `downsell`, `confirmation`, `opt_in`, `sales_page`, `bridge`. Use for cross-funnel pattern matching by role. Landing-page only. |
| `inactive` | No (default: exclude inactive) | Boolean. By default, inactive items (retired from the swipe file) are excluded. Pass `true` to include them. |
| `placeholder_copy` | No (no default) | Boolean. Filter on placeholder-copy flag. `false` excludes GHL templates and other design-focused items with lorem ipsum / generic copy. Omit to include everything. |

## Critical Rules

1. **You MUST attempt to query the swipe file.** Try MCP tools first; fall back to curl; only skip if both are unavailable. See "Detecting MCP Availability" above.
2. **Read the `analysis_text`** from every result. This is the strategic analysis that grounds your creative decisions — not just metadata.
3. **For graphic results**, fetch and view the `image_urls` using the Read tool (Claude Code can view images natively).
4. **NEVER query `vector: image_dense` without `search_mode: image_text`** (curl fallback only — the `search_swipe_visuals` MCP tool handles this automatically).
5. **Section points live on `content_dense` only** (curl fallback only — the `search_swipe_sections` MCP tool handles this automatically). Do not pair `granularity: section` with `analysis_dense` or `image_dense`.
6. **By default, inactive items are excluded.** Placeholder-copy items (GHL templates, design-focused content with lorem ipsum) are NOT excluded by default — add `placeholder_copy: false` to exclude them from copy-focused queries.
7. **Peggy (copywriter):** ALWAYS include `placeholder_copy: false` in every query. **Stan (designer):** Omit `placeholder_copy` — GHL templates are excellent design references regardless of copy quality.

---

## Granularity: Page-Level vs Section-Level Points

All landing-page content lives in the same collection, discriminated by the `granularity` payload field.

### Page-level points (`granularity: "page"`)
- `content_dense` — chunks of Copy Skeleton / Transcript / Letter Content
- `analysis_dense` — one point per analysis field (Functional Analysis, Structural Analysis, Funnel Strategy, Hook Analysis, etc.); filter by `analysis_section`
- `image_dense` — one point per screenshot/thumbnail/image file (requires `search_mode: image_text`)

### Section-level points (`granularity: "section"`) — landing_page only
- `content_dense` only — embedding of the compact ~50-word section description
- **No `analysis_dense` per section** — analysis lives at page level and describes the whole funnel, not individual legos
- **No `image_dense` per section** — screenshots are embedded whole-page via Jina, not cropped per lego

### Implications for query routing

| Question | Vector | Granularity | Notes |
|---|---|---|---|
| "Show me pages that look like X" | `image_dense` + `search_mode: image_text` | page | Can't be done at section level — no visual index exists |
| "Show me the funnel strategy of pages like X" | `analysis_dense` + `analysis_section: "Funnel Strategy"` | page | Analysis is whole-page only |
| "Show me hero legos / feature_grid legos / testimonial legos" | `content_dense` + `section_label` | section | Primary-label retrieval |
| "Show me all social_proof sections across any primary label" | `content_dense` + `archetype_tags: ["social_proof"]` | section | Cross-cut retrieval via archetype tags |
| "Show me all 6-item feature grids with grid layout" | `mode: structured` + structural filters | section | Shape query, no embedding needed |
| "Show me the copy patterns across full pages for this topic" | `content_dense` | page | Traditional page-level content search |

---

## The Four-Parallel-Query Pattern (RECOMMENDED for design/layout work)

For any creative task that involves copy + layout + strategy (landing pages, section design, ad creatives, carousels, reels), **run four parallel queries** — one per retrieval dimension — and merge the results. Each query answers a different question:

| # | MCP Tool | Curl vector | Question it answers | Use for |
|---|---|---|---|---|
| 1 | `search_swipe_content` | `content_dense`, `granularity: page` | "What proven copy/layout patterns exist at the whole-page level for this topic?" | Page-level topic matching, industry patterns |
| 2 | `search_swipe_strategy` | `analysis_dense` + `analysis_section` filter | "What strategic technique / funnel structure works here?" | Persuasion framework, hook structure, offer mechanics |
| 3 | `search_swipe_visuals` | `image_dense` + `search_mode: image_text` | "What visual pattern is proven?" | Layout, color, typography, composition |
| 4 | `search_swipe_sections` | `content_dense`, `granularity: section` (+ `section_label` or `archetype_tags`) | "What proven legos can I remix?" | Section-level retrieval — the surgical lego layer |

### Why four queries and not one

A single vector space misses the other three dimensions. Page-level copy tells you what whole pages look like for a topic; strategic analysis tells you why they work; visual similarity tells you how they look; and section-level retrieval tells you what individual legos are proven — which is what you actually remix when designing a specific section.

**Weighting:**
- **Section-level deliverables** (hero, feature grid, testimonial section, etc.) — call #4 is the primary; calls 1-3 provide page-level context
- **Whole-page deliverables** (full landing page, funnel analysis) — calls 1-3 are primary; call #4 is optional scan
- **Strategy brief (Don)** — calls 2-3 are primary (funnel strategy + visual direction)
- **Asset generation (Sal)** — call #3 only (visual refs for fal.ai prompts)

Merge results before designing. If the same reference appears in multiple queries, it's a strong signal — prioritize it.

### Empirical validation

- **2026-04-08** — For B2B course landing page queries, `analysis_dense + analysis_section="Funnel Strategy"` returns the ContentCreators AI Course reference (swipe file row 49) as result #1 with a 0.682 score. This is the pro-quality reference we're benchmarking against.
- **2026-04-09** — Section-level retrieval shipped (swipe-to-qdrant-24f, Phases 1/2/4). Row 49 now has per-section points retrievable via `content_dense + granularity: section` with structural metadata (`section_label`, `item_count`, `layout_orientation`, `archetype_tags`).

Other analysis_section filters that work well for call #2:
- `"Hook Analysis"` — for opening/headline patterns
- `"Offer Structure"` — for pricing/stack architecture
- `"Visual Hierarchy"` — for layout priority
- `"Structural Analysis"` — for section sequence + persuasion framework
- `"Functional Analysis"` — for conversion mechanics

### Four-Query Example (designing a hero section)

```bash
# Query 1: page-level content patterns (what do whole winning pages look like)
curl -s -X POST "https://swipe-to-qdrant.jesse-41b.workers.dev/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "B2B AI course landing page for content creators",
    "vector": "content_dense",
    "granularity": "page",
    "content_type": "landing_page",
    "limit": 5
  }'

# Query 2: strategic priors (funnel structure)
curl -s -X POST "https://swipe-to-qdrant.jesse-41b.workers.dev/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "B2B AI course landing page for content creators",
    "vector": "analysis_dense",
    "analysis_section": "Funnel Strategy",
    "limit": 5
  }'

# Query 3: visual similarity (REQUIRED: search_mode: image_text)
curl -s -X POST "https://swipe-to-qdrant.jesse-41b.workers.dev/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "clean modern SaaS hero with bold contrast-pair headline and gradient background",
    "vector": "image_dense",
    "search_mode": "image_text",
    "content_type": "landing_page",
    "limit": 5
  }'

# Query 4: section-level legos (NEW — the surgical retrieval layer)
curl -s -X POST "https://swipe-to-qdrant.jesse-41b.workers.dev/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "hero with contrast-pair headline and mechanism subhead",
    "vector": "content_dense",
    "granularity": "section",
    "section_label": "hero",
    "limit": 10
  }'
```

---

## Structured Lookups — `mode: "structured"`

Structured mode is a pure metadata scroll: no embedding, no ranking, `score: 0` on every result. It requires at least one filter and is designed for **shape queries** — "give me all sections of this shape," not "give me sections similar to this meaning."

Use structured mode when:
- You want ALL sections matching a structural pattern (not the top N most similar)
- Your query is a *shape* (6-item grid, horizontal comparison table) not a *concept*
- You need exhaustive retrieval for a design pattern library or audit

### Examples

**All 6-item feature grids with grid layout:**
```bash
curl -s -X POST "https://swipe-to-qdrant.jesse-41b.workers.dev/query" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "structured",
    "granularity": "section",
    "section_label": "feature_grid",
    "item_count": 6,
    "layout_orientation": "grid",
    "limit": 20
  }'
```

**All social_proof sections regardless of primary label:**
```bash
curl -s -X POST "https://swipe-to-qdrant.jesse-41b.workers.dev/query" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "structured",
    "granularity": "section",
    "archetype_tags": ["social_proof"],
    "limit": 20
  }'
```

**All sections that double as authority proof AND transformation story:**
```bash
curl -s -X POST "https://swipe-to-qdrant.jesse-41b.workers.dev/query" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "structured",
    "granularity": "section",
    "archetype_tags": ["authority_proof", "transformation_story"],
    "limit": 20
  }'
```

Note: `archetype_tags` is OR-matched — the second example returns sections tagged with EITHER `authority_proof` OR `transformation_story`.

---

## Funnel Queries (landing_page only)

Landing pages that belong to a multi-page funnel carry three metadata fields: `funnel_group` (shared slug), `funnel_step` (1-indexed position), and `funnel_role` (functional role). These enable three query patterns:

### Full funnel retrieval

Retrieve every page in a known funnel sequence. Sort results by `funnel_step` to reconstruct the flow.

```bash
curl -s -X POST "https://swipe-to-qdrant.jesse-41b.workers.dev/query" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "structured",
    "content_type": "landing_page",
    "funnel_group": "aesthetic-micro-offer",
    "limit": 20
  }'
```

### Cross-funnel role patterns

Find all pages that serve the same functional role across different funnels — e.g., all checkout pages, all upsell pages, all opt-in pages.

```bash
curl -s -X POST "https://swipe-to-qdrant.jesse-41b.workers.dev/query" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "structured",
    "content_type": "landing_page",
    "funnel_role": "checkout",
    "limit": 20
  }'
```

### Funnel step comparison

Compare how different funnels open (or close) by filtering to a specific step position across all funnels.

```bash
curl -s -X POST "https://swipe-to-qdrant.jesse-41b.workers.dev/query" \
  -H "Content-Type: application/json" \
  -d '{
    "mode": "structured",
    "content_type": "landing_page",
    "funnel_step": 1,
    "limit": 20
  }'
```

### Funnel roles vocabulary

`offer`, `checkout`, `schedule`, `thank_you`, `upsell`, `downsell`, `confirmation`, `opt_in`, `sales_page`, `bridge`

---

## Canonical Section Vocabulary

### Primary labels (`section_label`)
`hero`, `feature_grid`, `founder_story`, `pricing_table`, `social_proof_logos`, `testimonial_quote`, `faq_accordion`, `cta_band`, `comparison_table`, `process_steps`, `stat_callout`, `problem_agitation`, `benefit_list`, `guarantee_band`, `bonus_stack`, `trust_bar`, `lead_magnet_optin`

Claude may invent new labels for novel patterns — treat the list above as the canonical vocabulary but not a closed set.

### Secondary archetype tags (`archetype_tags`)
A section can carry multiple archetype tags beyond its primary label. Common secondary tags:
`social_proof`, `authority_proof`, `transformation_story`, `risk_reversal`, `urgency_trigger`, `scarcity_trigger`, `objection_handler`

Example: a customer testimonial section has primary label `testimonial_quote` AND archetype tags `["social_proof", "transformation_story", "authority_proof"]`. A 3-tier pricing table has primary label `pricing_table` AND archetype tag `["comparison_table"]`. The primary label is NOT repeated in `archetype_tags`.

---

## Visual Search — Using `image_dense`

The `image_dense` vector enables visual similarity search. Use it to find design inspiration based on layout, color, composition, and visual style — not just topic or strategy.

### REQUIRED: Always include `search_mode: image_text`

```json
{
  "vector": "image_dense",
  "search_mode": "image_text"
}
```

Without `search_mode: image_text`, the query fails because the server tries to embed the text into the wrong vector space (1536-dim text vs. 512-dim image).

### Visual search is page-level only

There is no `image_dense` at section granularity. Screenshots are embedded whole-page via Jina CLIP v2, not cropped per lego. "Find me sections that look like a green neon hero" is not supported at the retrieval layer — use page-level visual search + section-level content retrieval as complementary calls (query #3 + query #4 of the four-parallel pattern).

### Visual Search Examples

#### Landing page visual inspiration
```bash
curl -s -X POST "https://swipe-to-qdrant.jesse-41b.workers.dev/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "clean modern SaaS landing page with bold hero typography and gradient background",
    "vector": "image_dense",
    "search_mode": "image_text",
    "content_type": "landing_page",
    "limit": 5
  }'
```

#### Ad creative visual patterns
```bash
curl -s -X POST "https://swipe-to-qdrant.jesse-41b.workers.dev/query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "scroll-stopping ad creative with bold text overlay, high contrast colors, and pattern interrupt visual",
    "vector": "image_dense",
    "search_mode": "image_text",
    "content_type": "graphic",
    "limit": 5
  }'
```

### Working with Image Results

- Always check `image_urls` in the response — these are presigned URLs for the original visual assets.
- **Fetch and view `image_urls` using the Read tool** — Claude can view images natively. This is how you study the actual visual design, not just the text analysis.
- Combine image viewing with `analysis_text` to understand both what you see AND the strategic reasoning behind the design.
- When building creative briefs or visual direction documents, reference specific images from results by name and describe what you observed.

See `{project-root}/.claude/skills/bmad-mkt-knowledge/references/swipe-file-schema.md` for the full API reference with all parameters, response fields, and usage examples.
