# Arrow Routing Reference

## Critical: Elbow Arrow Properties

Three required properties for clean 90-degree corners:

```json
{
  "type": "arrow",
  "roughness": 0,
  "roundness": null,
  "elbowed": true
}
```

Without ALL THREE, arrows will be curved instead of 90-degree elbows.

## Edge Calculation Formulas

| Shape Type | Edge | Formula |
|------------|------|---------|
| Rectangle | Top | `(x + width/2, y)` |
| Rectangle | Bottom | `(x + width/2, y + height)` |
| Rectangle | Left | `(x, y + height/2)` |
| Rectangle | Right | `(x + width, y + height/2)` |
| Ellipse | Top | `(x + width/2, y)` |
| Ellipse | Bottom | `(x + width/2, y + height)` |

## Arrow Routing Algorithm

```
FUNCTION createArrow(source, target, sourceEdge, targetEdge):
  sourcePoint = getEdgePoint(source, sourceEdge)
  targetPoint = getEdgePoint(target, targetEdge)

  dx = targetPoint.x - sourcePoint.x
  dy = targetPoint.y - sourcePoint.y

  IF sourceEdge == "bottom" AND targetEdge == "top":
    IF abs(dx) < 10:  // Nearly aligned
      points = [[0, 0], [0, dy]]
    ELSE:  // L-shape
      points = [[0, 0], [dx, 0], [dx, dy]]

  ELSE IF sourceEdge == "right" AND targetEdge == "left":
    IF abs(dy) < 10:
      points = [[0, 0], [dx, 0]]
    ELSE:
      points = [[0, 0], [0, dy], [dx, dy]]

  ELSE IF sourceEdge == targetEdge:  // U-turn
    clearance = 50
    IF sourceEdge == "right":
      points = [[0, 0], [clearance, 0], [clearance, dy], [dx, dy]]
    ELSE IF sourceEdge == "bottom":
      points = [[0, 0], [0, clearance], [dx, clearance], [dx, dy]]

  width = max(abs(p[0]) for p in points)
  height = max(abs(p[1]) for p in points)

  RETURN {x: sourcePoint.x, y: sourcePoint.y, points, width, height}
```

## Arrow Patterns

| Pattern | Points | Use Case |
|---------|--------|----------|
| Down | `[[0,0], [0,h]]` | Vertical connection |
| Right | `[[0,0], [w,0]]` | Horizontal connection |
| L-left-down | `[[0,0], [-w,0], [-w,h]]` | Go left, then down |
| L-right-down | `[[0,0], [w,0], [w,h]]` | Go right, then down |
| L-down-left | `[[0,0], [0,h], [-w,h]]` | Go down, then left |
| L-down-right | `[[0,0], [0,h], [w,h]]` | Go down, then right |
| S-shape | `[[0,0], [0,h1], [w,h1], [w,h2]]` | Navigate around obstacles |
| U-turn | `[[0,0], [w,0], [w,-h], [0,-h]]` | Callback/return arrows |

## Worked Examples

### Vertical (Bottom to Top)

```
Source: x=500, y=200, w=180, h=90
Target: x=500, y=400, w=180, h=90

source_bottom = (590, 290)
target_top = (590, 400)

Arrow: x=590, y=290, points=[[0,0], [0,110]], width=0, height=110
```

### Fan-out (One to Many)

```
Source: x=570, y=400, w=140, h=80
Target: x=120, y=550, w=160, h=80

source_bottom = (640, 480)
target_top = (200, 550)

Arrow: x=640, y=480, points=[[0,0], [-440,0], [-440,70]], width=440, height=70
```

### U-turn (Callback)

```
Source right: (710, 440)
Target right: (730, 315)

Arrow: x=710, y=440
points=[[0,0], [50,0], [50,-125], [20,-125]]
// Right 50px clearance, up 125px, left to target
```

## Staggering Multiple Arrows

When N arrows leave from same edge, spread evenly across 20%-80% of the edge:

```
For i in 0..N-1:
  percentage = 0.2 + (0.6 * i / (N - 1))

  If bottom/top edge: x = shape.x + shape.width * percentage
  If left/right edge: y = shape.y + shape.height * percentage
```

Examples: 2 arrows → 20%, 80%. 3 arrows → 20%, 50%, 80%.

## Arrow Bindings

For visual attachment to shapes:

```json
{
  "id": "arrow-api-to-db",
  "type": "arrow",
  "x": 600,
  "y": 290,
  "width": 0,
  "height": 110,
  "points": [[0, 0], [0, 110]],
  "roughness": 0,
  "roundness": null,
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
```

### fixedPoint Values

- Top center: `[0.5, 0]`
- Bottom center: `[0.5, 1]`
- Left center: `[0, 0.5]`
- Right center: `[1, 0.5]`

### Update Shape boundElements for Arrows

Shapes connected by arrows must list them:

```json
{
  "id": "api-server",
  "boundElements": [
    { "type": "text", "id": "api-server-text" },
    { "type": "arrow", "id": "arrow-api-to-db" }
  ]
}
```

## Bidirectional Arrows

```json
{
  "startArrowhead": "arrow",
  "endArrowhead": "arrow"
}
```

Options: `null`, `"arrow"`, `"bar"`, `"dot"`, `"triangle"`

## Arrow Labels

Standalone text near arrow midpoint:

```json
{
  "id": "arrow-api-db-label",
  "type": "text",
  "x": 605,
  "y": 340,
  "text": "SQL",
  "fontSize": 12,
  "containerId": null,
  "backgroundColor": "#ffffff"
}
```

Positioning: place at midpoint of longest arrow segment.

## Width/Height = Bounding Box

```
points = [[0,0], [-440,0], [-440,70]]
width = 440, height = 70

points = [[0,0], [50,0], [50,-125], [20,-125]]
width = 50, height = 125
```
