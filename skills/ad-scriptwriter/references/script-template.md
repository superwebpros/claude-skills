# Ad Script Template & Formatting Specification

Use this canonical template when authoring direct-response video ad scripts and accompanying Meta/social ad copy.

---

## 1. Markdown Frontmatter Schema

Every script file must start with this frontmatter:

```yaml
---
type: ad-script
campaign: roadmap-quiz
hook_id: 1 # 1 (Start from Zero), 2 (Wasting Time), 3 (Reason Not Working)
variant: "1.1 (The Champion)"
angle: "Internal talent vs outside hires"
target_icp: "Owner/Operator ($1M–$50M, 10–200 employees) with a curious team member"
target_duration: "~45s"
word_count: 122 # strictly 115–135 words
proof_anchor: "MSU SSC 490 Case Study"
destination_url: "https://aiprocesspros.com/roadmap"
cta_button: "LEARN_MORE"
status: draft
owner: <script-owner>
---
```

---

## 2. Teleprompter & Video Script Structure

```markdown
# Script [Variant Number]: [Angle Name]

**[VISUAL: Medium Shot (MS). Plain-speaking founder to camera in clean office/workspace. Text overlay: "[PUNCHY HOOK SUMMARY]"]**

**HOOK (0:00 - 0:04):**
[Exact hook sentence from the hook matrix. Punchy, scroll-stopping, no greeting.]

**AGITATE (0:04 - 0:13):**
[Dismantle the false consensus or mistake. Name the pain or bad alternative plainly.]

**SHIFT / MECHANISM (0:13 - 0:26):**
**[VISUAL: Cut to close-up (MCU) or punch-in zoom. Clear hand gesture / on-screen graphic: 1, 2, 3]**
[Introduce the practical alternative. Break down the 2-step or 3-step operational framework.]

**PROOF ANCHOR (0:26 - 0:38):**
**[VISUAL: B-roll cut or text overlay citing verified proof point]**
[Verified proof: MSU SSC 490 students or 400+ production automations running in-house.]

**DIAGNOSTIC CTA (0:38 - 0:48):**
**[VISUAL: Screen preview of /roadmap assessment UI. Headline: "Get Your Custom AI Roadmap"]**
[Low-friction bridge: Free 2-minute diagnostic assessment quiz. Call to click the link below.]
```

---

## 3. Companion Meta Ad Copy Block

Append this block directly below the video script in the markdown deliverable:

```markdown
---

## Accompanying Meta Ad Copy

**Headline (max 5–6 words):**
[Punchy, high curiosity, e.g. "Start with the person you already have"]

**Primary Text:**
[Paragraph 1 — Hook & Agitate: The contrarian premise from the video]

[Paragraph 2 — The Reframe: The internal champion or operational inventory concept]

[Paragraph 3 — The Proof: MSU non-coder students or 400+ production automations]

[Paragraph 4 — The Diagnostic CTA: Free 2-minute assessment quiz + roadmap promise]

**Description:**
Free 2-minute assessment

**CTA Button:**
LEARN_MORE (`https://aiprocesspros.com/roadmap`)
```

---

## 4. Script Quality Checklist

Before finalizing any script:
1. **Word count audit:** Is the spoken text strictly between 115 and 135 words?
2. **Pacing check:** Does the hook land within the first 4 seconds?
3. **No IT jargon:** Did you remove terms like "vector", "LangGraph", "MCP", "pipeline", "endpoint"?
4. **Natural cadence:** When read aloud, do the transitions sound like natural speech rather than bulleted captions?
5. **No inflated claims:** Are guarantees omitted? Is proof tied to MSU or 400+ automations?
6. **Free vs. Paid clarity:** Does the CTA offer a method roadmap, without promising a ranked opportunity list?
