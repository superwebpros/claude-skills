# Swipe File Reference

How to search the swipe file vector database. This is a curated library of marketing content -- sales letters, video scripts, ad creatives, landing pages, and more -- that has been analyzed, enriched, and indexed for semantic search.

Use this reference whenever you need to find real-world examples of marketing techniques, copy patterns, or creative strategies.

---

## 1. Overview

The swipe file is a searchable collection of marketing content stored in a Qdrant vector database. Each record has been:

- **Ingested** from its original source (transcript, letter text, HTML, image)
- **Enriched** with AI-generated analysis (structural breakdowns, persuasion techniques, emotional arcs, hook analysis, etc.)
- **Vectorized** into three separate embedding spaces so you can search by content, by strategic technique, or by visual similarity

There are **seven content types** covering the major formats marketers produce: long-form video scripts (VSLs), classic sales letters, YouTube videos, ad graphics, short-form video, landing pages, and paid video ads.

You can search for content by what it says ("find scripts about weight loss"), by how it works ("find examples that use authority positioning and social proof"), or by what it looks like ("find ad creatives visually similar to this split-screen layout").

---

## 2. Query Endpoint

**Preferred:** Use the Swipe File MCP connector (`https://connectors.agentskillshop.com/swipe-file/mcp`) which exposes four purpose-built tools: `search_swipe_content`, `search_swipe_strategy`, `search_swipe_visuals`, `search_swipe_sections`. See `swipe-file-access.md` for MCP tool mapping, detection, and graceful degradation.

**Fallback (curl):** When MCP is not installed, query the REST API directly:

**URL:** `https://swipe-to-qdrant.jesse-41b.workers.dev/query`
**Method:** `POST`
**Content-Type:** `application/json`

### Request Body

| Field | Type | Required | Default | Description |
|---|---|---|---|---|
| `query` | string | Yes (semantic mode) | -- | Natural language search query. Required for `mode: "semantic"`. Ignored when `mode: "structured"`. |
| `mode` | string | No | `"semantic"` | `"semantic"` embeds the query and ranks by similarity. `"structured"` is a pure metadata scroll — no embedding, no ranking (score=0), requires ≥1 filter. Use structured when the query is a *shape*, not a *meaning*. See Section 4b. |
| `vector` | string | No | `"content_dense"` | Which vector space to search: `"content_dense"`, `"analysis_dense"`, or `"image_dense"`. See Section 4 for when to use which. Ignored when `search_mode` is `"image_text"` (forced to `image_dense`). Section-level points exist on `content_dense` only. |
| `search_mode` | string | No | `"text"` | `"text"` for content/analysis search (OpenAI embeddings), `"image_text"` for cross-modal visual search (Jina CLIP v2). When `"image_text"`, the query text is embedded in the image vector space and matched against image embeddings. |
| `granularity` | string | No | (both) | `"page"` restricts to whole-page points. `"section"` restricts to per-section landing-page legos. Section points exist only for `content_type: landing_page` and only on `content_dense`. See Section 4b. |
| `section_label` | string | No | — | Exact primary-label match on section points (e.g. `"hero"`, `"feature_grid"`). Pair with `granularity: "section"`. See Section 5b for the canonical vocabulary. |
| `archetype_tags` | string[] | No | — | Array of archetype names, OR-matched. Returns sections whose `archetype_tags` contains ANY of these. Use for cross-cut retrieval across primary labels. See Section 5b. |
| `item_count` | integer | No | — | Exact integer match (e.g., `6` for 6-item feature grids). Pair with `granularity: "section"`. |
| `layout_orientation` | string | No | — | One of `vertical`, `horizontal`, `grid`, `carousel`, `alternating`. Pair with `granularity: "section"`. |
| `content_type` | string | No | all types | Filter to a single content type. One of: `video_script`, `sales_letter`, `youtube_video`, `graphic`, `video_short`, `landing_page`, `video_ad`. |
| `industry` | string | No | all industries | Filter to a single industry. See Section 5 for the vocabulary. |
| `limit` | integer | No | `10` | Number of results to return. Min 1, max 50. |
| `group_by_record` | boolean | No | `true` for page, `false` for section | When true, returns one result per record. Auto-flips to `false` when `granularity: "section"` so you get multiple legos per page instead of one collapsed hit. |
| `analysis_section` | string | No | all sections | Filter results to a specific analysis section (e.g. "Hook Analysis", "Belief Chain", "Problem Agitation Analysis"). See Section 4 for available sections per content type. |
| `include_content` | boolean | No | `true` | Set to false to get lightweight results without text content (just metadata + scores). Useful when you only need IDs for a follow-up fetch. |
| `funnel_group` | string | No | — | Shared slug for all pages in the same funnel (e.g. `"aesthetic-micro-offer"`). Landing-page only. |
| `funnel_step` | integer | No | — | 1-indexed position in the funnel sequence. Landing-page only. |
| `funnel_role` | string | No | — | Functional role: `offer`, `checkout`, `schedule`, `thank_you`, `upsell`, `downsell`, `confirmation`, `opt_in`, `sales_page`, `bridge`. Landing-page only. |
| `inactive` | boolean | No | exclude inactive | By default, inactive (retired) items are excluded. Pass `true` to include them. |
| `placeholder_copy` | boolean | No | (no default) | Filter on placeholder-copy flag. `false` excludes GHL templates and design-focused items with lorem ipsum / generic copy. Omit to include everything. |

### Response Shape

```json
{
  "results": [
    {
      "baserow_id": 142,
      "baserow_table": "video_scripts",
      "content_type": "video_script",
      "name": "ClickFunnels 2.0 VSL - Russell Brunson",
      "url": "https://example.com/vsl",
      "score": 0.87,
      "industry": "saas",
      "persuasion_techniques": ["authority", "social proof", "storytelling"],
      "content_text": "The actual matched chunk text...",
      "analysis_text": "The analysis section text that matched...",
      "analysis_section": "Belief Chain",
      "chunk_index": 0,
      "chunk_total": 3,
      "image_urls": ["https://...presigned-url..."]
    }
  ]
}
```

### Response Fields

| Field | Type | Description |
|---|---|---|
| `baserow_id` | integer | The record's unique ID in the source database. Use this if you need to fetch the full record. |
| `baserow_table` | string | Which table the record lives in (e.g., `video_scripts`, `sales_letters`). |
| `content_type` | string | The content type (matches the filter values). |
| `name` | string | Human-readable name of the piece of content. |
| `url` | string | Link to the original source material. |
| `score` | float | Relevance score from 0 to 1. Higher is more relevant. |
| `industry` | string | Industry this content is tagged with. |
| `persuasion_techniques` | string[] | Persuasion techniques identified in this content. |
| `content_text` | string (optional) | The actual source material text from the matched chunk. Present on `content_dense` matches. Omitted when `include_content` is false. |
| `analysis_text` | string (optional) | The analysis section text that matched. Present on `analysis_dense` matches. Omitted when `include_content` is false. |
| `analysis_section` | string (optional) | Which analysis field matched (e.g. "Hook Analysis", "Belief Chain", "Structural Analysis"). Present on `analysis_dense` matches. |
| `chunk_index` | integer | Which chunk of the record this result represents (0-based). |
| `chunk_total` | integer | Total number of chunks for this record. |
| `image_url` | string (optional) | Fresh presigned URL for a single image. Present on `image_dense` matches (one per slide/image). |
| `image_urls` | string[] (optional) | Fresh presigned URLs for all images in the record. Present on `content_dense` and `analysis_dense` matches for content types that have images. |
| `slide_index` | integer (optional) | Which slide/image this point represents (0-based). Present on `image_dense` matches. |
| `slide_total` | integer (optional) | Total number of slides/images in the record. Present on `image_dense` matches. |
| `is_cover` | boolean (optional) | Whether this is the first (cover) image. Present on `image_dense` matches. |

### Error Responses

- **400** if `query` is missing or empty
- **400** if `vector` is not one of the valid options
- **400** if `content_type` is not a recognized type
- **400** if `industry` is not a non-empty string

---

## 3. Content Types

### `video_script` (table 1809)

Long-form video sales letters (VSLs), webinar scripts, and presentation transcripts. These are typically 15-60+ minutes of persuasion-heavy content. Each record has a full transcript plus 12+ deep analysis fields covering belief chains, emotional arcs, objection handling, proof architecture, and more. This is the most richly analyzed content type.

**Best for:** Studying long-form persuasion structure, offer framing, belief shifting, and high-ticket sales narratives.

### `sales_letter` (table 1724)

Classic direct-response sales letters, including Gary Halbert letters and direct mail pieces. Each record has the full letter content plus framework analysis and editorial notes. Many of these are legendary pieces of copy studied for decades.

**Best for:** Studying headline formulas, lead-ins, offer structure, guarantee framing, and classic direct-response copywriting principles.

### `youtube_video` (table 1810)

YouTube content including educational videos, talking-head content, and marketing breakdowns. Each record has a transcript plus hook analysis, content structure breakdown, and key takeaways.

**Best for:** Studying retention tactics, hook patterns, content structure for video, and educational framing.

### `graphic` (table 1699)

Ad creatives, social media graphics, carousel posts, and visual marketing assets. These are image-based records with extracted copy and visual analysis. Carousel posts may have multiple slides.

**Best for:** Studying visual ad formats, copy-on-image patterns, creative hooks, and social media ad design.

### `video_short` (table 1700)

Short-form video content -- Reels, TikToks, YouTube Shorts. Each record has a transcript plus extracted on-screen copy and visual analysis.

**Best for:** Studying short-form hooks, retention mechanics, visual storytelling in under 60 seconds, and organic social content.

### `landing_page` (table 1701)

Sales pages, opt-in pages, webinar registration pages, and other conversion-focused web pages. Each record has extracted copy, structural analysis, and funnel strategy breakdown.

**Best for:** Studying page layout, conversion copy, funnel positioning, CTA strategy, and opt-in mechanics.

### `video_ad` (table 1818)

Paid video advertisements -- Facebook ads, Instagram ads, YouTube pre-rolls, and other paid video creatives. Each record has a transcript (when available) plus ad-specific analysis covering conversion mechanics, thumb-stop techniques, CTA patterns, and offer framing. Analyzed through a direct-response advertising and campaign planning lens using AIDA, PAS, and Cialdini frameworks.

**Best for:** Studying paid media creative strategy, conversion-focused video structure, thumb-stop hooks, CTA patterns, offer framing, urgency/scarcity mechanics, and platform-optimized ad formats. Use this when planning paid campaigns rather than organic content.

---

## 4. Vector Types -- When to Use Which

There are three searchable vector spaces. Choosing the right one determines the quality of your results.

### `content_dense` (default)

Searches the **raw source material** -- transcripts, letter text, extracted copy, page content. This is the actual words the creator wrote or spoke.

**Use when you want to find content ABOUT a topic.**

Examples:
- "Find VSLs about SaaS products"
- "Find sales letters selling supplements"
- "Find landing pages for webinar funnels"
- "Find content mentioning Russell Brunson"

### `analysis_dense`

Searches the **AI-generated strategic analysis** -- structural breakdowns, persuasion technique descriptions, hook analysis, belief chains, funnel strategy, etc. This is the analytical layer on top of the content.

**Analysis is indexed at the section level.** Each analysis field (e.g. Hook Analysis, Belief Chain, Structural Analysis) is its own separate vector, not one big blob per record. This means:

- Searching for "epiphany bridge" will match the **specific section** that discusses it (e.g. "Belief Chain") rather than matching the whole record's analysis as a vague hit
- The `analysis_section` response field tells you exactly which analysis field matched
- Scores are higher and more differentiated because matching is more precise

**Available analysis sections by content type:**

- **video_script**: Hook Analysis, Functional Analysis, Structural Analysis, Belief Chain, Emotional Arc, Target Avatar Signals, Offer Reveal Timing & Framing, Proof Architecture, Objection Handling Map, Scarcity & Urgency Mechanics, Identity & Transformation Language, Power Phrases, Executive Summary, Problem Agitation Analysis, Origin Story Analysis
- **sales_letter**: Functional Analysis, Structural Analysis, Framework, Notes, Hook & Lead Analysis, Problem Agitation Analysis, Proof Architecture, Offer & Value Stack Analysis, Emotional Arc, Power Phrases & Fascinations
- **youtube_video**: Hook Analysis, Functional Analysis, Structural Analysis, Retention Tactics, Key Takeaways
- **graphic**: Visual Analysis, Functional Analysis, Structural Analysis
- **video_short**: Hook Analysis, Visual Analysis, Functional Analysis, Structural Analysis
- **landing_page**: Functional Analysis, Structural Analysis, Funnel Strategy
- **video_ad**: Hook Analysis, Conversion Analysis, Functional Analysis, Structural Analysis

**The analysis text uses canonical copywriting framework terminology**, so technique-specific queries match well:

- Named frameworks: Epiphany Bridge, PAS, AIDA, Perfect Webinar, State-Story-Solution
- Schwartz terminology: awareness levels, sophistication levels, lead types
- Halbert terminology: A-pile/B-pile, fascinations, damaging admission, bucket brigade
- Ad creative terminology: thumb-stop mechanic, pattern interrupt, CTA pattern, offer framing, friction reduction, funnel position, Cialdini principles

**Use when you want to find content that USES a specific technique or structure.**

Examples:
- "Find examples that use strong authority positioning"
- "Find content with an emotional transformation arc"
- "Find letters with a problem-agitation-solution structure"
- "Find scripts with tiered offer reveals and price anchoring"
- "Find VSLs using the Epiphany Bridge framework"
- "Find sales letters with A-pile fascinations"

### `image_dense` (requires `search_mode: "image_text"`)

Searches the **visual embedding space** using Jina CLIP v2 cross-modal embeddings. Your text query is embedded in the same space as the images, enabling text-to-image semantic search.

**Important:** You must set `"search_mode": "image_text"` to use this vector. The `vector` param is ignored when `search_mode` is `"image_text"` — it automatically uses `image_dense`.

Each image in a record (e.g. each slide in a carousel graphic) is its own Qdrant point with its own `image_dense` vector. Results include `image_url` (fresh presigned URL for the matched image), `slide_index`, `slide_total`, and `is_cover`.

**Use when you want to find content that LOOKS like something.**

Examples:
- "neon split-screen before and after comparison"
- "minimalist text-on-dark-background with bold headline"
- "person pointing at whiteboard with annotations"
- "carousel infographic with numbered steps"

### Rule of Thumb

| If your query is about... | Use |
|---|---|
| A topic, product, or niche | `content_dense` |
| A copywriting technique or structural pattern | `analysis_dense` |
| A specific phrase or claim | `content_dense` |
| A persuasion strategy or framework | `analysis_dense` |
| A visual style, layout, or aesthetic | `image_dense` (with `search_mode: "image_text"`) |
| A specific section lego (hero, feature grid, testimonial, etc.) | `content_dense` + `granularity: "section"` |
| A shape query ("all 6-item grids") | `mode: "structured"` + filters |

---

## 4b. Page vs Section Granularity

Landing page content is indexed at two levels within the same collection, discriminated by the `granularity` payload field.

### Page-level points (`granularity: "page"`)

All seven content types live here. For landing pages, this covers:

- `content_dense` — chunks of Copy Skeleton / Page Content (whole-page copy)
- `analysis_dense` — one point per analysis field (Functional Analysis, Structural Analysis, Funnel Strategy, etc.); filter by `analysis_section`
- `image_dense` — one point per full-page screenshot (requires `search_mode: "image_text"`)

### Section-level points (`granularity: "section"`) — landing_page only

Shipped 2026-04-09 (swipe-to-qdrant-24f, Phases 1/2/4). Per-section children parsed from `Sections JSON`:

- `content_dense` only — embedding of the compact ~50-word section description written by Claude during the sectionize enrichment batch
- **No `analysis_dense` per section** — analysis lives at page level and describes the whole funnel, not individual legos
- **No `image_dense` per section** — screenshots are not cropped per lego; Jina CLIP v2 embeds the whole screenshot at page level

### Query routing by question

| Question | Vector | Granularity | Notes |
|---|---|---|---|
| "Pages that look like X" | `image_dense` + `search_mode: "image_text"` | page | Can't be done at section level — no visual index |
| "Funnel strategy of pages like X" | `analysis_dense` + `analysis_section: "Funnel Strategy"` | page | Analysis is whole-page only |
| "Hero legos / feature_grid legos / testimonial legos" | `content_dense` + `section_label` | section | Primary-label retrieval |
| "All social_proof sections across any primary label" | `content_dense` + `archetype_tags: ["social_proof"]` | section | Cross-cut retrieval via archetype tags |
| "All 6-item feature grids in grid layout" | `mode: "structured"` + structural filters | section | Shape query, no embedding needed |
| "Copy patterns across full pages for this topic" | `content_dense` | page | Traditional page-level content search |
| "All pages in the aesthetic-micro-offer funnel" | `mode: "structured"` + `funnel_group` | page | Full funnel retrieval — sort results by `funnel_step` |
| "All checkout pages across funnels" | `mode: "structured"` + `funnel_role: "checkout"` | page | Cross-funnel role pattern matching |
| "How do different funnels open?" | `mode: "structured"` + `funnel_step: 1` | page | Funnel step comparison across funnels |

### Four-parallel-query pattern for design work

Run four queries in parallel for any design/layout task — they answer different questions:

1. `content_dense`, `granularity: "page"` — whole-page copy patterns for the topic
2. `analysis_dense` + `analysis_section` filter — strategic priors (page-level)
3. `image_dense` + `search_mode: "image_text"` — visual similarity (page-level)
4. `content_dense`, `granularity: "section"` (+ `section_label` or `archetype_tags`) — structural legos

Weight call #4 heaviest for section-level deliverables (hero, feature grid, etc.). Weight calls 1-3 heaviest for whole-page assembly, strategy briefs, and visual reference work.

See `{project-root}/.claude/skills/bmad-mkt-knowledge/references/swipe-file-access.md` for example bodies.

---

## 5. Filter Options

### Content Type Filter (`content_type`)

Pass one of these exact strings:

| Value | What It Matches |
|---|---|
| `video_script` | VSLs, webinar scripts, long-form video presentations |
| `sales_letter` | Direct mail, Gary Halbert letters, long-form sales letters |
| `youtube_video` | YouTube content, video essays, educational marketing videos |
| `graphic` | Ad creatives, social graphics, carousel posts |
| `video_short` | Reels, TikToks, YouTube Shorts |
| `landing_page` | Sales pages, opt-in pages, registration pages |
| `video_ad` | Paid video ads (Facebook, Instagram, YouTube pre-roll) |

Omit this field to search across all content types.

### Industry Filter (`industry`)

Pass a single string value. Results match if their industry tag contains the provided value.

| Value | Description |
|---|---|
| `saas` | Software-as-a-service products |
| `ecommerce` | Online retail, physical products, DTC brands |
| `coaching` | Coaching, consulting, mentorship programs |
| `agency` | Marketing agencies, service businesses |
| `info products` | Courses, digital products, info-marketing |
| `health` | Health, wellness, supplements, fitness |
| `finance` | Finance, investing, trading, insurance |
| `real estate` | Real estate, property investing |
| `local business` | Local services, brick-and-mortar businesses |
| `other` | Anything not covered above |

### Section Label Filter (`section_label`)

Exact primary-label match on section points. Pair with `granularity: "section"`. Canonical vocabulary (Claude may invent new labels for novel patterns):

| Value | What it matches |
|---|---|
| `hero` | Above-the-fold headline + subhead + primary CTA section |
| `feature_grid` | Multi-item feature/benefit grid |
| `founder_story` | Origin story / founder narrative section |
| `pricing_table` | Pricing tiers or single-price presentation |
| `social_proof_logos` | "As seen in" / customer logo band |
| `testimonial_quote` | Customer quote or case study callout |
| `faq_accordion` | FAQ section |
| `cta_band` | Standalone CTA band or "final push" block |
| `comparison_table` | Us-vs-them or tier comparison table |
| `process_steps` | Numbered how-it-works / step-by-step section |
| `stat_callout` | Big number / statistic feature |
| `problem_agitation` | Pain point enumeration + agitation |
| `benefit_list` | Bullet-list of benefits |
| `guarantee_band` | Guarantee / risk reversal callout |
| `bonus_stack` | Bonus or value stack presentation |
| `trust_bar` | Trust badge / security / integration row |
| `lead_magnet_optin` | Email capture / lead magnet form section |

### Archetype Tags Filter (`archetype_tags`)

Array of secondary archetype labels, OR-matched. A single section can carry multiple archetype tags beyond its primary `section_label` — e.g., a customer testimonial has primary label `testimonial_quote` AND archetype tags `["social_proof", "transformation_story", "authority_proof"]`.

Use for cross-cut retrieval across primary labels: "find all sections tagged `social_proof` regardless of whether they're testimonials, logo bands, stat callouts, or founder stories."

Common secondary archetype tags:

| Tag | What it matches |
|---|---|
| `social_proof` | Sections that function as social proof (testimonials, logos, user counts) |
| `authority_proof` | Sections establishing expertise, credentials, media features |
| `transformation_story` | Before/after narratives, customer journey, outcome stories |
| `risk_reversal` | Guarantees, money-back promises, free trials, liability shifting |
| `urgency_trigger` | Deadlines, countdown timers, limited-time framing |
| `scarcity_trigger` | Limited quantity, exclusive access, "last N spots" |
| `objection_handler` | Sections that directly address common objections |

The primary `section_label` is NOT repeated in `archetype_tags`. Filter semantics: `archetype_tags: ["social_proof", "authority_proof"]` matches sections whose archetype_tags contains EITHER (OR logic).

### Inactive & Placeholder Copy Filter Semantics

- `inactive`: Uses a `must_not` pattern — inactive items are excluded by default. The filter is safe when the field is absent on a point (absence = not inactive = included).
- `placeholder_copy`: When `placeholder_copy: false` is passed, the server excludes points where `placeholder_copy` is `true`. Points that lack the field entirely are treated as non-placeholder and included. This means older items indexed before the field existed still appear normally.

### Persuasion Techniques (payload field, not a request filter)

These are returned in the response payload for each result. They are not currently available as a request filter, but you can use them to evaluate results after retrieval.

| Value | Description |
|---|---|
| `scarcity` | Limited availability, exclusive access, limited-time offers |
| `social proof` | Testimonials, case studies, user counts, endorsements |
| `authority` | Expert positioning, credentials, media features, celebrity association |
| `reciprocity` | Free value, gifts, lead magnets that create obligation |
| `commitment` | Small yeses, micro-commitments, foot-in-the-door sequences |
| `liking` | Relatability, shared identity, personal stories, vulnerability |
| `urgency` | Deadlines, countdown timers, fast-action bonuses |
| `anchoring` | Price comparisons, value stacking, "worth $X but you get it for $Y" |
| `loss aversion` | Risk reversal, "what you'll miss", cost of inaction framing |
| `storytelling` | Origin stories, customer journeys, narrative-driven persuasion |

---

## 6. Payload Fields

Every result returned from the query endpoint includes these fields:

| Field | Type | Present On | Description |
|---|---|---|---|
| `baserow_id` | integer | All | Unique record ID in the source database |
| `baserow_table` | string | All | Table slug: `video_scripts`, `sales_letters`, `youtube_videos`, `graphics`, `video_shorts`, `landing_pages`, `video_ads` |
| `content_type` | string | All | One of the seven content types |
| `name` | string | All | Title or name of the content piece |
| `url` | string | All | URL to the original source |
| `score` | float | All | Semantic similarity score (0-1, higher is better) |
| `industry` | string | All | Tagged industry for this record |
| `persuasion_techniques` | string[] | All | Persuasion techniques identified in this content |
| `content_text` | string | content_dense matches | The actual source material text from the matched chunk. Omitted when `include_content` is false. |
| `analysis_text` | string | analysis_dense matches | The analysis section text that matched. Omitted when `include_content` is false. |
| `analysis_section` | string | analysis_dense matches | Which analysis field matched (e.g. "Hook Analysis", "Belief Chain", "Structural Analysis") |
| `chunk_index` | integer | All | Which chunk of the record this result represents (0-based) |
| `chunk_total` | integer | All | Total number of chunks for this record |
| `image_url` | string | image_dense matches | Fresh presigned URL for the matched image/slide |
| `image_urls` | string[] | content_dense + analysis_dense matches | Fresh presigned URLs for all images in the record (for content types with images) |
| `slide_index` | integer | image_dense matches | Which slide/image this point represents (0-based) |
| `slide_total` | integer | image_dense matches | Total slides/images in the record |
| `is_cover` | boolean | image_dense matches | Whether this is the first (cover) image |
| `granularity` | string | All (new) | `"page"` or `"section"` — discriminator for page-level vs section-level points |
| `section_order` | integer | section hits | Position of this section within its parent page (0-based) |
| `section_label` | string | section hits | Primary archetype label (e.g. `"hero"`, `"feature_grid"`) |
| `section_text` | string | section hits | Compact ~50-word description of the section that was embedded |
| `item_count` | integer (nullable) | section hits | Number of discrete items in the section (e.g., 6 for a 6-feature grid; null for non-enumerable sections) |
| `layout_orientation` | string (nullable) | section hits | Layout shape: `vertical`, `horizontal`, `grid`, `carousel`, `alternating`, or null |
| `archetype_tags` | string[] | section hits | Additional archetype labels beyond the primary `section_label` (e.g., a testimonial_quote that's also `["social_proof", "transformation_story"]`) |

Additional payload fields exist on the underlying Qdrant points but are not currently surfaced through the query endpoint:

| Field | Type | Present On | Description |
|---|---|---|---|
| `inactive` | boolean | All | Whether the record has been retired from the swipe file (Inactive checkbox in Baserow). `true` = retired. |
| `placeholder_copy` | boolean | All | Whether the item has placeholder / lorem ipsum copy (GHL templates, design-focused content). `true` = placeholder copy. |
| `author` | string | sales_letters, video_shorts | Author of the content |
| `platform` | string | graphics, video_shorts, youtube_videos | Platform the content was published on |
| `type` | string | video_scripts, youtube_videos, video_shorts | Sub-type of the content |
| `page_type` | string | landing_pages | Type of page (e.g., "sales page", "opt-in page") |
| `layout_pattern` | string | graphics, landing_pages | Visual layout description |
| `funnel_stage` | string | landing_pages | Where this page sits in a funnel |
| `funnel_group` | string | landing_pages | Shared slug for all pages in the same funnel (e.g. `"aesthetic-micro-offer"`) |
| `funnel_step` | integer | landing_pages | 1-indexed position in the funnel sequence |
| `funnel_role` | string | landing_pages | Functional role of the page: `offer`, `checkout`, `schedule`, `thank_you`, `upsell`, `downsell`, `confirmation`, `opt_in`, `sales_page`, `bridge` |
| `is_carousel` | boolean | graphics, video_shorts | Whether the content is a multi-slide carousel |

---

## 7. Usage Examples

### Example 1: Find VSLs about SaaS products

Search the raw content for topic relevance, filtered to video scripts in the SaaS industry.

```json
{
  "query": "software product demo with free trial offer",
  "vector": "content_dense",
  "content_type": "video_script",
  "industry": "saas",
  "limit": 5
}
```

### Example 2: Find sales letters that use strong authority positioning

Search the analysis layer for technique-based matches across all sales letters. Results now include the matched analysis text and which section it came from.

```json
{
  "query": "authority positioning with credentials, expert endorsements, and media features",
  "vector": "analysis_dense",
  "content_type": "sales_letter",
  "limit": 10
}
```

A typical result will include `analysis_text` with the matched analysis and `analysis_section` telling you which field matched (e.g. "Structural Analysis"). Read the `analysis_text` to understand how the technique is used, then fetch the full record if you need the original copy.

### Example 3: Find ad creatives for coaching businesses

Search graphics filtered to the coaching industry.

```json
{
  "query": "coaching program enrollment ad creative with testimonial",
  "vector": "content_dense",
  "content_type": "graphic",
  "industry": "coaching",
  "limit": 10
}
```

### Example 4: Find landing pages with scarcity techniques

Search the analysis layer for pages that employ scarcity and urgency in their strategy.

```json
{
  "query": "scarcity mechanics with limited spots, countdown timers, and deadline-driven urgency",
  "vector": "analysis_dense",
  "content_type": "landing_page",
  "limit": 10
}
```

### Example 5: Find hook analysis examples for video scripts

Filter to a specific analysis section to find only hook-related analysis across video scripts.

```json
{
  "query": "pattern interrupt opening with bold claim and curiosity loop",
  "vector": "analysis_dense",
  "content_type": "video_script",
  "analysis_section": "Hook Analysis",
  "limit": 10
}
```

### Example 6: Lightweight metadata-only search

When you only need record IDs and scores (e.g., for a follow-up fetch), set `include_content` to false to skip the text fields.

```json
{
  "query": "webinar registration page with countdown timer",
  "vector": "content_dense",
  "content_type": "landing_page",
  "include_content": false,
  "limit": 20
}
```

### Example 7: Visual similarity search for ad creatives

Find graphics that visually resemble a split-screen comparison layout. Uses cross-modal search -- your text query is matched against image embeddings.

```json
{
  "query": "neon split-screen before and after comparison with bold headline",
  "search_mode": "image_text",
  "content_type": "graphic",
  "limit": 5
}
```

Results include `image_url` (a fresh presigned URL you can fetch or display), `slide_index` (which slide matched), and `slide_total` (how many slides the carousel has). Use `is_cover: true` results if you only want the first slide of each creative.

### Example 8: Cross-type analysis search

Find any content type that uses problem-agitation structure. Omit `content_type` to search across all six types.

```json
{
  "query": "problem agitation with vivid pain points and emotional escalation",
  "vector": "analysis_dense",
  "analysis_section": "Problem Agitation Analysis",
  "limit": 10
}
```

### Example 9: Section-level semantic retrieval (hero legos)

Retrieve hero sections semantically ranked by similarity to a description. Each result is a single hero lego, not a whole page.

```json
{
  "query": "hero with contrast-pair headline and mechanism subhead",
  "vector": "content_dense",
  "granularity": "section",
  "section_label": "hero",
  "limit": 10
}
```

### Example 10: Structured shape query (all 6-item grids)

Pure metadata scroll — no embedding, no ranking. Use for exhaustive structural retrieval.

```json
{
  "mode": "structured",
  "granularity": "section",
  "section_label": "feature_grid",
  "item_count": 6,
  "layout_orientation": "grid",
  "limit": 20
}
```

### Example 11: Cross-archetype retrieval (social proof across primary labels)

Find every section tagged `social_proof` regardless of whether it's a testimonial, logo band, stat callout, or founder story.

```json
{
  "query": "proof that the transformation is real and the authority is earned",
  "vector": "content_dense",
  "granularity": "section",
  "archetype_tags": ["social_proof", "authority_proof"],
  "limit": 15
}
```

### Tips for Better Queries

- **Be descriptive.** "SaaS onboarding email sequence VSL with free trial offer" will outperform "SaaS VSL".
- **Match your vector to your intent.** Searching for a topic? Use `content_dense`. Searching for a technique? Use `analysis_dense`.
- **Use industry filters to narrow results** when you know the vertical, rather than putting the industry name in the query text.
- **Start with `group_by_record: true`** (the default) to get unique records. Set it to `false` only if you want to see which specific chunks matched.
- **Combine filters.** You can filter by both `content_type` and `industry` simultaneously to get highly targeted results.
- **Read the analysis_text.** When searching `analysis_dense`, results now include the actual analysis text that matched. Use it to understand the technique before fetching the full record.
- **Check analysis_section.** The `analysis_section` field tells you which aspect of the analysis was relevant (e.g. "Belief Chain", "Hook Analysis"). This helps you understand why a result matched.
- **Use canonical framework terms.** The analysis text uses standard copywriting terminology (Epiphany Bridge, PAS, AIDA, A-pile/B-pile, etc.), so queries using these terms will match more precisely on `analysis_dense`.
- **Typical analysis_dense workflow:** search -> read `analysis_text` from top results -> study the patterns -> write.
- **Image URLs are fresh.** The `image_url` and `image_urls` fields are resolved at query time from Baserow, so they are always valid presigned URLs. You can fetch or display them immediately.
- **For visual search, use `search_mode: "image_text"`.** Do NOT set `vector: "image_dense"` manually -- the `search_mode` param handles it. Just set `search_mode` and write a descriptive text query about the visual style you're looking for.
- **Content and analysis results include `image_urls` too.** When you search by `content_dense` or `analysis_dense`, results for content types that have images (graphics, landing pages, etc.) will include an `image_urls` array with fresh URLs for all images in that record.
