# Validation Reference

## Pre-Flight Validation Algorithm

Run BEFORE writing the file:

```
FUNCTION validateDiagram(elements):
  errors = []

  // 1. Validate shape-text bindings
  FOR each shape IN elements WHERE shape.boundElements != null:
    FOR each binding IN shape.boundElements:
      textElement = findById(elements, binding.id)
      IF textElement == null:
        errors.append("Shape {shape.id} references missing text {binding.id}")
      ELSE IF textElement.containerId != shape.id:
        errors.append("Text containerId doesn't match shape")

  // 2. Validate arrow connections
  FOR each arrow IN elements WHERE arrow.type == "arrow":
    sourceShape = findShapeNear(elements, arrow.x, arrow.y)
    IF sourceShape == null:
      errors.append("Arrow {arrow.id} doesn't start from shape edge")

    finalPoint = arrow.points[arrow.points.length - 1]
    endX = arrow.x + finalPoint[0]
    endY = arrow.y + finalPoint[1]
    targetShape = findShapeNear(elements, endX, endY)
    IF targetShape == null:
      errors.append("Arrow {arrow.id} doesn't end at shape edge")

    IF arrow.points.length > 2:
      IF arrow.elbowed != true:
        errors.append("Arrow {arrow.id} missing elbowed:true")
      IF arrow.roundness != null:
        errors.append("Arrow {arrow.id} should have roundness:null")

  // 3. Validate unique IDs
  ids = [el.id for el in elements]
  duplicates = findDuplicates(ids)
  IF duplicates.length > 0:
    errors.append("Duplicate IDs: {duplicates}")

  // 4. Validate bounding boxes
  FOR each arrow IN elements WHERE arrow.type == "arrow":
    maxX = max(abs(p[0]) for p in arrow.points)
    maxY = max(abs(p[1]) for p in arrow.points)
    IF arrow.width < maxX OR arrow.height < maxY:
      errors.append("Arrow {arrow.id} bounding box too small")

  RETURN errors
```

## Checklists

### Before Generating

- [ ] Identified all components
- [ ] Mapped all connections/data flows
- [ ] Chose layout pattern (vertical, horizontal, hub-and-spoke, nested)
- [ ] Selected color palette
- [ ] Planned grid positions
- [ ] Created ID naming scheme

### During Generation

- [ ] Every labeled shape has BOTH shape AND text elements
- [ ] Shape has `boundElements: [{ "type": "text", "id": "{id}-text" }]`
- [ ] Text has `containerId: "{shape-id}"`
- [ ] Multi-point arrows have `elbowed: true`, `roundness: null`, `roughness: 0`
- [ ] Arrows have `startBinding` and `endBinding`
- [ ] No diamond shapes used
- [ ] Applied staggering formula for multiple arrows from same edge
- [ ] Shapes connected by arrows list arrows in their `boundElements`

### Arrow Validation (Every Arrow)

- [ ] Arrow `x,y` calculated from source shape edge
- [ ] Final point offset = `targetEdge - sourceEdge`
- [ ] Arrow `width` = `max(abs(point[0]))` for all points
- [ ] Arrow `height` = `max(abs(point[1]))` for all points
- [ ] U-turn arrows have 40-60px clearance

### After Generation

- [ ] All `boundElements` IDs reference existing text elements
- [ ] All `containerId` values reference existing shapes
- [ ] All arrows start within 15px of a shape edge
- [ ] All arrows end within 15px of a shape edge
- [ ] No duplicate IDs
- [ ] Arrow bounding boxes match points
- [ ] File is valid JSON

## Common Bugs and Fixes

### Bug: Arrow appears disconnected/floating

**Cause**: Arrow `x,y` not calculated from shape edge.
**Fix**: `arrow_x = shape.x + shape.width/2`, `arrow_y = shape.y + shape.height`

### Bug: Arrow endpoint doesn't reach target

**Cause**: Final point offset wrong.
**Fix**: `offset_x = target_edge.x - arrow.x`, `offset_y = target_edge.y - arrow.y`

### Bug: Multiple arrows overlap from same source

**Cause**: All arrows start from same point.
**Fix**: Stagger — spread across 20%-80% of the edge.

### Bug: Labels don't appear inside shapes

**Cause**: Using `label` property instead of two elements.
**Fix**: Shape with `boundElements` + Text with `containerId`.

### Bug: Arrows are curved, not 90-degree

**Cause**: Missing elbow properties.
**Fix**: `roughness: 0`, `roundness: null`, `elbowed: true` — all three required.

### Bug: Callback/return arrow loops incorrectly

**Cause**: U-turn path lacks clearance.
**Fix**: 4-point path with 40-60px clearance: `[[0,0], [clearance,0], [clearance,-vert], [final_x,-vert]]`
