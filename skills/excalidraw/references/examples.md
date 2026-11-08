# Examples Reference

## Complete 3-Tier Architecture Example

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "claude-code-excalidraw-skill",
  "elements": [
    {
      "id": "user",
      "type": "ellipse",
      "x": 540,
      "y": 50,
      "width": 120,
      "height": 80,
      "angle": 0,
      "strokeColor": "#1971c2",
      "backgroundColor": "#e7f5ff",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "roundness": { "type": 2 },
      "seed": 1,
      "version": 1,
      "versionNonce": 1,
      "isDeleted": false,
      "boundElements": [
        { "type": "text", "id": "user-text" },
        { "type": "arrow", "id": "arrow-user-frontend" }
      ],
      "updated": 1,
      "link": null,
      "locked": false
    },
    {
      "id": "user-text",
      "type": "text",
      "x": 565,
      "y": 77,
      "width": 70,
      "height": 25,
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
      "locked": false,
      "text": "Users",
      "fontSize": 20,
      "fontFamily": 1,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": "user",
      "originalText": "Users",
      "lineHeight": 1.25
    },
    {
      "id": "frontend",
      "type": "rectangle",
      "x": 500,
      "y": 200,
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
      "seed": 3,
      "version": 1,
      "versionNonce": 3,
      "isDeleted": false,
      "boundElements": [
        { "type": "text", "id": "frontend-text" },
        { "type": "arrow", "id": "arrow-user-frontend" },
        { "type": "arrow", "id": "arrow-frontend-api" }
      ],
      "updated": 1,
      "link": null,
      "locked": false
    },
    {
      "id": "frontend-text",
      "type": "text",
      "x": 505,
      "y": 215,
      "width": 190,
      "height": 50,
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
      "seed": 4,
      "version": 1,
      "versionNonce": 4,
      "isDeleted": false,
      "boundElements": null,
      "updated": 1,
      "link": null,
      "locked": false,
      "text": "React Frontend\nNext.js",
      "fontSize": 16,
      "fontFamily": 1,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": "frontend",
      "originalText": "React Frontend\nNext.js",
      "lineHeight": 1.25
    },
    {
      "id": "api-server",
      "type": "rectangle",
      "x": 500,
      "y": 380,
      "width": 200,
      "height": 80,
      "angle": 0,
      "strokeColor": "#7048e8",
      "backgroundColor": "#d0bfff",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "roundness": { "type": 3 },
      "seed": 5,
      "version": 1,
      "versionNonce": 5,
      "isDeleted": false,
      "boundElements": [
        { "type": "text", "id": "api-server-text" },
        { "type": "arrow", "id": "arrow-frontend-api" },
        { "type": "arrow", "id": "arrow-api-db" }
      ],
      "updated": 1,
      "link": null,
      "locked": false
    },
    {
      "id": "api-server-text",
      "type": "text",
      "x": 505,
      "y": 395,
      "width": 190,
      "height": 50,
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
      "seed": 6,
      "version": 1,
      "versionNonce": 6,
      "isDeleted": false,
      "boundElements": null,
      "updated": 1,
      "link": null,
      "locked": false,
      "text": "API Server\nFastAPI",
      "fontSize": 16,
      "fontFamily": 1,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": "api-server",
      "originalText": "API Server\nFastAPI",
      "lineHeight": 1.25
    },
    {
      "id": "database",
      "type": "rectangle",
      "x": 500,
      "y": 560,
      "width": 200,
      "height": 80,
      "angle": 0,
      "strokeColor": "#2f9e44",
      "backgroundColor": "#b2f2bb",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 1,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "roundness": { "type": 3 },
      "seed": 7,
      "version": 1,
      "versionNonce": 7,
      "isDeleted": false,
      "boundElements": [
        { "type": "text", "id": "database-text" },
        { "type": "arrow", "id": "arrow-api-db" }
      ],
      "updated": 1,
      "link": null,
      "locked": false
    },
    {
      "id": "database-text",
      "type": "text",
      "x": 505,
      "y": 575,
      "width": 190,
      "height": 50,
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
      "seed": 8,
      "version": 1,
      "versionNonce": 8,
      "isDeleted": false,
      "boundElements": null,
      "updated": 1,
      "link": null,
      "locked": false,
      "text": "PostgreSQL\nDatabase",
      "fontSize": 16,
      "fontFamily": 1,
      "textAlign": "center",
      "verticalAlign": "middle",
      "containerId": "database",
      "originalText": "PostgreSQL\nDatabase",
      "lineHeight": 1.25
    },
    {
      "id": "arrow-user-frontend",
      "type": "arrow",
      "x": 600,
      "y": 130,
      "width": 0,
      "height": 70,
      "angle": 0,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 0,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "roundness": null,
      "seed": 9,
      "version": 1,
      "versionNonce": 9,
      "isDeleted": false,
      "boundElements": null,
      "updated": 1,
      "link": null,
      "locked": false,
      "points": [[0, 0], [0, 70]],
      "elbowed": true,
      "startBinding": {
        "elementId": "user",
        "focus": 0,
        "gap": 1,
        "fixedPoint": [0.5, 1]
      },
      "endBinding": {
        "elementId": "frontend",
        "focus": 0,
        "gap": 1,
        "fixedPoint": [0.5, 0]
      },
      "startArrowhead": null,
      "endArrowhead": "arrow"
    },
    {
      "id": "arrow-frontend-api",
      "type": "arrow",
      "x": 600,
      "y": 280,
      "width": 0,
      "height": 100,
      "angle": 0,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 0,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "roundness": null,
      "seed": 10,
      "version": 1,
      "versionNonce": 10,
      "isDeleted": false,
      "boundElements": null,
      "updated": 1,
      "link": null,
      "locked": false,
      "points": [[0, 0], [0, 100]],
      "elbowed": true,
      "startBinding": {
        "elementId": "frontend",
        "focus": 0,
        "gap": 1,
        "fixedPoint": [0.5, 1]
      },
      "endBinding": {
        "elementId": "api-server",
        "focus": 0,
        "gap": 1,
        "fixedPoint": [0.5, 0]
      },
      "startArrowhead": null,
      "endArrowhead": "arrow"
    },
    {
      "id": "arrow-api-db",
      "type": "arrow",
      "x": 600,
      "y": 460,
      "width": 0,
      "height": 100,
      "angle": 0,
      "strokeColor": "#1e1e1e",
      "backgroundColor": "transparent",
      "fillStyle": "solid",
      "strokeWidth": 2,
      "strokeStyle": "solid",
      "roughness": 0,
      "opacity": 100,
      "groupIds": [],
      "frameId": null,
      "roundness": null,
      "seed": 11,
      "version": 1,
      "versionNonce": 11,
      "isDeleted": false,
      "boundElements": null,
      "updated": 1,
      "link": null,
      "locked": false,
      "points": [[0, 0], [0, 100]],
      "elbowed": true,
      "startBinding": {
        "elementId": "api-server",
        "focus": 0,
        "gap": 1,
        "fixedPoint": [0.5, 1]
      },
      "endBinding": {
        "elementId": "database",
        "focus": 0,
        "gap": 1,
        "fixedPoint": [0.5, 0]
      },
      "startArrowhead": null,
      "endArrowhead": "arrow"
    }
  ],
  "appState": {
    "gridSize": 20,
    "viewBackgroundColor": "#ffffff"
  },
  "files": {}
}
```

## Layout Patterns

### Vertical Flow (Architecture, Flowcharts)

```
Grid: 250px column width, 150px row height

Row 0 (y=50):   Users/Actors (ellipses)
Row 1 (y=200):  Frontend/Entry points
Row 2 (y=380):  Backend/API/Orchestration
Row 3 (y=560):  Data stores/Databases
Row 4 (y=740):  External services/APIs
Row 5 (y=920):  Infrastructure/Monitoring

Columns: center at x=200, 450, 700, 950, 1200
```

### Horizontal Flow (Pipelines, CI/CD)

```
Grid: 250px column width, 150px row height

Col 0 (x=100):  Input/Source
Col 1 (x=350):  Stage 1
Col 2 (x=600):  Stage 2
Col 3 (x=850):  Stage 3
Col 4 (x=1100): Output/Deploy

Rows: center at y=200, 400 for parallel paths
```

### Hub-and-Spoke (Concept Maps, Event-Driven)

```
Center: (600, 400)
Radius: 300px

8 positions at 45-degree increments:
  Top:         (600, 100)
  Top-Right:   (812, 188)
  Right:       (900, 400)
  Bottom-Right:(812, 612)
  Bottom:      (600, 700)
  Bottom-Left: (388, 612)
  Left:        (300, 400)
  Top-Left:    (388, 188)
```

### Nested Groups (Cloud Architecture)

```
Outer group: x=50, y=50, w=1200, h=900
  Label: x=70, y=60, "AWS Cloud"

  Inner group 1: x=90, y=100, w=1120, h=400
    Label: x=110, y=110, "VPC (10.0.0.0/16)"

    Sub-group A: x=130, y=150, w=500, h=330
      Components inside with 40px padding

    Sub-group B: x=670, y=150, w=500, h=330
      Components inside with 40px padding

  Inner group 2: x=90, y=540, w=1120, h=380
    Label: x=110, y=550, "AWS Services"
    Components at y=590+
```

## Complexity Guidelines

| Complexity | Elements | Approach |
|------------|----------|----------|
| Simple | 5-10 | Single level, no groups, direct arrows |
| Medium | 10-25 | Add grouping boxes, grid layout, legend |
| Complex | 25-50 | Nested groups, staggered arrows, multiple layers |
| Very Complex | 50+ | Split into multiple focused diagrams |
