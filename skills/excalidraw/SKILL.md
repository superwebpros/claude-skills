---
name: excalidraw
description: Generate Excalidraw diagrams (architecture, flowcharts, concept maps, process flows) from detailed text prompts. Use when the user wants to create or update .excalidraw diagram files.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash(npx:*), Bash(node:*)
---

# Excalidraw Diagram Generator

Generate `.excalidraw` JSON files from detailed text descriptions. Supports architecture diagrams, flowcharts, concept maps, and process flows.

## When to Use This Skill

Use when the user asks to:
- Create any kind of diagram (architecture, flowchart, concept map, process flow)
- Generate an `.excalidraw` file
- Visualize a system, process, or concept
- Create diagram content for social media, videos, or presentations

## Diagram Types Supported

| Type | Layout | Best For |
|------|--------|----------|
| Architecture Diagram | Vertical flow with nested groups | System design, infrastructure, cloud stacks |
| Flowchart | Top-to-bottom or left-to-right | Decision trees, algorithms, user journeys |
| Concept Map | Hub-and-spoke or clustered | Teaching concepts, brainstorming, relationships |
| Process Flow | Horizontal pipeline or swimlanes | Workflows, CI/CD, data pipelines |

## Workflow

### Step 1: Understand the Request

Parse the user's prompt for:
- **Diagram type** (architecture, flowchart, concept map, process flow)
- **Components** — what nodes/shapes to include
- **Connections** — how components relate (data flow, dependencies, sequence)
- **Groupings** — logical clusters (services, layers, teams, phases)
- **Style preferences** — color palette, complexity level
- **Output location** — where to save (default: `docs/diagrams/` or project root)

If the prompt is vague, ask clarifying questions before generating.

### Step 2: Plan the Layout

Choose layout based on diagram type:

**Vertical Flow** (architecture, flowcharts):
- Grid: 250px column width, 150px row height
- Top-to-bottom: users → frontend → backend → data → external
- Center the main flow, branch out for side components

**Horizontal Flow** (process flows, pipelines):
- Grid: 250px column width, 150px row height
- Left-to-right: input → processing stages → output
- Stack parallel paths vertically

**Hub-and-Spoke** (concept maps):
- Central concept at (600, 400)
- Spokes radiate outward at equal angles
- Secondary concepts branch from spokes

**Nested Groups** (cloud architecture like AWS/K8s):
- Outermost group = cloud/environment boundary
- Inner groups = VPC, subnets, namespaces
- Components inside groups with proper padding (40px from group edges)

### Step 3: Generate Elements

For EVERY component, create elements following these rules:

#### Critical Rules

1. **Labels require TWO elements**: Every labeled shape needs a shape element with `boundElements` AND a separate text element with `containerId`. The `label` property does NOT work in raw JSON.

2. **NEVER use diamond shapes**: Diamond arrow connections are broken in raw Excalidraw JSON. Use styled rectangles instead.

3. **Elbow arrows need THREE properties**: `elbowed: true`, `roundness: null`, `roughness: 0`

4. **Arrow edge calculations**: Arrows must originate from shape edges using the formulas in `references/arrows.md`

5. **Unique IDs**: Every element must have a unique string ID. Use descriptive kebab-case: `api-server`, `api-server-text`, `arrow-api-to-db`

#### Element Generation Order

1. **Group boundaries first** (dashed rectangles, back-to-front)
2. **Group labels** (standalone text, no containerId)
3. **Shapes** (rectangles, ellipses) with boundElements
4. **Shape labels** (text with containerId)
5. **Arrows** (with bindings and edge calculations)
6. **Arrow labels** (standalone text near midpoints)
7. **Legend** (if needed — small rectangles + text in bottom-right)

### Step 4: Apply Colors

Use the color palette from `references/colors.md`. Select based on context:
- **Default palette** for general diagrams
- **AWS/Azure/GCP palettes** for cloud architecture
- **K8s palette** for container orchestration
- Use consistent colors within component types
- Use distinct colors between different types for visual clarity

### Step 5: Validate

Before writing the file, run through the validation checklist from `references/validation.md`:

- [ ] Every shape with a label has BOTH shape (with `boundElements`) AND text (with `containerId`)
- [ ] Every `boundElements` ID references an existing text element
- [ ] Every `containerId` references an existing shape
- [ ] Multi-point arrows have `elbowed: true`, `roundness: null`, `roughness: 0`
- [ ] Arrow `x,y` is calculated from source shape edge
- [ ] Arrow final point offset reaches target shape edge
- [ ] Arrow `width` = max(abs(point[0])), `height` = max(abs(point[1]))
- [ ] No duplicate IDs
- [ ] No diamond shapes
- [ ] File is valid JSON
- [ ] Shapes bound to arrows list them in `boundElements`

### Step 6: Write the File

Save as `.excalidraw` JSON file. Default location: `docs/diagrams/` or user-specified path.

File structure:
```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "claude-code-excalidraw-skill",
  "elements": [ ... ],
  "appState": {
    "gridSize": 20,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

### Step 7: Report Results

After writing, tell the user:
- File path and name
- How to open it (excalidraw.com, VS Code Excalidraw extension, or Obsidian Excalidraw plugin)
- Component count and diagram dimensions
- Suggest tweaks they might want

## Reference Files

Consult these for detailed specs. Read them when generating diagrams:

| File | When to Read |
|------|-------------|
| `~/.claude/skills/excalidraw/references/json-format.md` | Always — element structure, required properties, text binding |
| `~/.claude/skills/excalidraw/references/arrows.md` | Always — arrow routing, edge calculations, bindings |
| `~/.claude/skills/excalidraw/references/colors.md` | When choosing colors — palettes by platform/type |
| `~/.claude/skills/excalidraw/references/examples.md` | For layout patterns and complete JSON examples |
| `~/.claude/skills/excalidraw/references/validation.md` | Before writing — validation checklist and common bugs |

## Prompt Examples

Users can trigger this skill with prompts like:

### Architecture Diagram
```
/excalidraw Create an architecture diagram showing:
- Users connect to a Next.js frontend
- Frontend calls a FastAPI backend
- Backend connects to PostgreSQL and Redis
- Backend also calls OpenAI API and S3 for file storage
- Everything runs on AWS with a VPC boundary
- Use AWS color palette
```

### Flowchart
```
/excalidraw Create a flowchart for our content approval process:
1. Author submits draft
2. Editor reviews → approve or request changes
3. If changes requested → back to author
4. If approved → legal review
5. Legal approves → publish
6. Legal flags issues → back to editor
```

### Concept Map
```
/excalidraw Create a concept map showing how AI models work:
- Central concept: "AI Model"
- Connected to: Training Data, Parameters, Inference, Fine-tuning
- Training Data connects to: Tokens, Embeddings, Datasets
- Inference connects to: Prompt, Context Window, Output
- Use purple/blue tones for AI concepts
```

### Process Flow
```
/excalidraw Create a horizontal process flow for our CI/CD pipeline:
Source Code → Build → Unit Tests → Integration Tests → Staging Deploy → E2E Tests → Production Deploy
- Add a rollback arrow from Production back to Staging
- Group Build+Tests as "CI" and Deploys as "CD"
```

## Output Locations

- Default: `docs/diagrams/[descriptive-name].excalidraw`
- If user specifies a path, use that
- For course slides: `[course-id]/assets/[diagram-name].excalidraw`

## Complexity Guidelines

| Complexity | Elements | Recommendation |
|------------|----------|----------------|
| Simple | 5-10 | Single-level, no groups |
| Medium | 10-25 | Add grouping boxes, use grid layout |
| Complex | 25-50 | Multiple layers, nested groups, legend |
| Very Complex | 50+ | Split into multiple focused diagrams |

## Social Media / Video Tips

When the user mentions social media or video content:
- Use **larger font sizes** (20-24px for labels, 28-32px for titles)
- Use **high contrast** colors (avoid pastels on white)
- Add a **title element** at the top (large text, bold)
- Keep diagrams **focused** — one clear message per diagram
- Use **generous spacing** between elements (300px+ columns)
- Consider a **dark background** (`viewBackgroundColor: "#1e1e1e"`) with light text for video
