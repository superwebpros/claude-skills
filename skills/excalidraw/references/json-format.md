# Excalidraw JSON Format Reference

## File Structure

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "claude-code-excalidraw-skill",
  "elements": [],
  "appState": {
    "gridSize": 20,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

## Element Types

| Type | Use For | Arrow Reliability |
|------|---------|-------------------|
| `rectangle` | Services, databases, containers, decision points, orchestrators | Excellent |
| `ellipse` | Users, external systems, start/end points | Good |
| `text` | Labels inside shapes, titles, annotations | N/A |
| `arrow` | Data flow, connections, dependencies | N/A |
| `line` | Grouping boundaries, separators | N/A |

### BANNED: Diamond Shapes

**NEVER use `type: "diamond"`.** Arrow connections are broken in raw JSON. Use styled rectangles instead:

| Semantic Meaning | Rectangle Style |
|------------------|-----------------|
| Orchestrator/Hub | Coral (`#ffa8a8`/`#c92a2a`) + strokeWidth: 3 |
| Decision Point | Orange (`#ffd8a8`/`#e8590c`) + dashed stroke |
| Central Router | Larger size + bold color |

## Required Element Properties

Every element MUST have ALL of these:

```json
{
  "id": "unique-id-string",
  "type": "rectangle",
  "x": 100,
  "y": 100,
  "width": 200,
  "height": 80,
  "angle": 0,
  "strokeColor": "#1971c2",
  "backgroundColor": "#a5d8ff",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": { "type": 3 },
  "seed": 1,
  "version": 1,
  "versionNonce": 1,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false
}
```

## Text Inside Shapes (Labels)

**Every labeled shape requires TWO elements.**

### Shape with boundElements

```json
{
  "id": "api-server",
  "type": "rectangle",
  "x": 500,
  "y": 200,
  "width": 200,
  "height": 90,
  "strokeColor": "#1971c2",
  "backgroundColor": "#a5d8ff",
  "boundElements": [
    { "type": "text", "id": "api-server-text" }
  ]
}
```

### Text with containerId

```json
{
  "id": "api-server-text",
  "type": "text",
  "x": 505,
  "y": 220,
  "width": 190,
  "height": 50,
  "text": "API Server\nExpress.js",
  "fontSize": 16,
  "fontFamily": 1,
  "textAlign": "center",
  "verticalAlign": "middle",
  "containerId": "api-server",
  "originalText": "API Server\nExpress.js",
  "lineHeight": 1.25,
  "angle": 0,
  "strokeColor": "#1e1e1e",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeWidth": 2,
  "strokeStyle": "solid",
  "roughness": 1,
  "opacity": 100,
  "groupIds": [],
  "frameId": null,
  "roundness": null,
  "seed": 2,
  "version": 1,
  "versionNonce": 2,
  "isDeleted": false,
  "boundElements": null,
  "updated": 1,
  "link": null,
  "locked": false
}
```

### DO NOT use the `label` property — it's for the JavaScript API only, not raw JSON.

### Text Positioning Rules

- Text `x` = shape `x` + 5
- Text `y` = shape `y` + (shape.height - text.height) / 2
- Text `width` = shape `width` - 10
- Use `\n` for multi-line labels
- Always: `textAlign: "center"`, `verticalAlign: "middle"`
- Text height estimate: `lines * fontSize * lineHeight`

### ID Convention

Shape: `{descriptive-name}` → Text: `{descriptive-name}-text`

## Grouping with Dashed Rectangles

For logical groupings (namespaces, VPCs, phases, layers):

```json
{
  "id": "group-backend",
  "type": "rectangle",
  "x": 100,
  "y": 500,
  "width": 1000,
  "height": 280,
  "strokeColor": "#9c36b5",
  "backgroundColor": "transparent",
  "fillStyle": "solid",
  "strokeStyle": "dashed",
  "strokeWidth": 2,
  "roughness": 0,
  "roundness": null,
  "boundElements": null
}
```

Group labels are standalone text (no containerId) positioned at top-left of group:

```json
{
  "id": "group-backend-label",
  "type": "text",
  "x": 120,
  "y": 510,
  "text": "Backend Services",
  "fontSize": 18,
  "fontFamily": 1,
  "textAlign": "left",
  "verticalAlign": "top",
  "containerId": null,
  "originalText": "Backend Services"
}
```

## Nested Groups

For diagrams like AWS architecture with nested boundaries:

1. **Outermost group first** (largest x/y/width/height)
2. **Inner groups next** — inset by 40px+ padding on all sides
3. **Components inside** — inset by 40px from inner group edges
4. Each group gets its own label at top-left
5. Use different `strokeColor` per nesting level for clarity
6. Outer groups: lighter/more muted colors. Inner groups: bolder colors.

## Legend

Place in bottom-right corner when using color-coding:

```json
// Small colored rectangle (30x20)
{
  "id": "legend-frontend",
  "type": "rectangle",
  "x": 900, "y": 700,
  "width": 30, "height": 20,
  "backgroundColor": "#a5d8ff",
  "strokeColor": "#1971c2"
}
// Label next to it
{
  "id": "legend-frontend-label",
  "type": "text",
  "x": 940, "y": 702,
  "text": "Frontend",
  "fontSize": 14,
  "containerId": null
}
```
