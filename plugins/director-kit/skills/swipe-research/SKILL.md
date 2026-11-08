---
name: swipe-research
description: Ground marketing & creative work in PROVEN, real-world examples by searching the Swipe File (a Qdrant vector DB of analyzed ads, video scripts, sales letters, landing pages, and graphics). Use whenever you're writing or designing a hook, ad, reel, brief, shot list, storyboard, landing page, email, or any creative and want what actually works — or when the user says "find proven examples", "what works for X", "swipe", "reference ads/pages", "show me winning hooks/layouts", or asks to make an ad/creative better. Pulls copy, strategy, visuals, and remixable sections.
---

# Swipe Research

Search the **Swipe File** — a Qdrant vector DB of analyzed, proven marketing content (ads, video scripts, sales letters, landing pages, graphics) — to ground creative decisions in what *actually works*, not guesses. Full how-to: `references/swipe-file-access.md`; full API: `references/swipe-file-schema.md`.

## The connector + four tools
The Swipe File MCP connector (`https://connectors.agentskillshop.com/swipe-file/mcp`) exposes four purpose-built tools — one per retrieval dimension:

| Tool | Finds | Use for |
|------|-------|---------|
| `search_swipe_content` | copy/layout patterns at the page level | topic / niche / product / industry matching |
| `search_swipe_strategy` | *how* it persuades — techniques, frameworks, funnel structure | hooks, offer mechanics, belief chains |
| `search_swipe_visuals` | visual patterns (layout, color, composition) | design direction, fal-prompt references |
| `search_swipe_sections` | remixable building blocks (hero, feature grid, CTA, testimonial…) | section-level design |

## How to use it
1. **Detect availability first.** If `search_swipe_*` tools exist in this session → use them directly. If not → tell the user: *"The Swipe File MCP isn't connected — add `https://connectors.agentskillshop.com/swipe-file/mcp` in your MCP settings,"* then fall back to the curl API in `references/swipe-file-access.md`. If neither works, proceed on framework principles and note the work isn't swipe-grounded.
2. **Run the four-parallel-query pattern** for any copy+layout+strategy task (ads, landing pages, carousels, reels): fire all four tools on the same intent and **merge** — a reference that appears in multiple is a strong signal. Weighting: section deliverables lean on `search_swipe_sections`; whole-page on content+strategy+visuals; pure visual-asset prompts on `search_swipe_visuals` only.
3. **Read the `analysis_text`** on every result — that strategic analysis is what grounds your creative decisions, not just the metadata.
4. **For visual results, view the `image_urls`** with the Read tool (Claude sees images natively) — study the actual design, then describe what you observed in your brief.

## In the director-kit pipeline
- **director-brief** (ad / short / trailer): pull proven **hooks, angles, and offer structures** before writing the beat sheet.
- **director-storyboard / director-assets**: pull **visual references** (`search_swipe_visuals`) to steer the look and the fal/nano-banana prompts.
Cite the specific references you used so the creative is traceably swipe-grounded.

See `references/swipe-file-access.md` for query routing, structured/funnel queries, the section vocabulary, and the curl fallback.
