# Super Web Pros - Claude Code Skills

Shared [Claude Code](https://claude.ai/claude-code) skills for the Super Web Pros team.

## What are Skills?

Skills are reusable prompt templates that extend Claude Code with specialized capabilities. They live in `~/.claude/skills/` and are automatically available as `/slash-commands` in any project.

## Available Skills

| Skill | Description | Trigger |
|-------|-------------|---------|
| [excalidraw](./excalidraw/) | Generate Excalidraw diagrams (architecture, flowcharts, concept maps, process flows) from text prompts | `/excalidraw` or ask Claude to create a diagram |

## Installation

### Quick Install (all skills)

```bash
# Clone the repo
git clone git@github.com:superwebpros/claude-skills.git /tmp/claude-skills-repo

# Symlink each skill into your Claude skills directory
for skill in /tmp/claude-skills-repo/*/; do
  skill_name=$(basename "$skill")
  [ "$skill_name" = "." ] && continue
  [ -f "$skill/SKILL.md" ] || continue
  ln -sf "$skill" ~/.claude/skills/"$skill_name"
  echo "Installed: $skill_name"
done
```

### Install a single skill

```bash
git clone git@github.com:superwebpros/claude-skills.git /tmp/claude-skills-repo
ln -sf /tmp/claude-skills-repo/excalidraw ~/.claude/skills/excalidraw
```

### Manual install

Copy the skill folder directly into `~/.claude/skills/`:

```bash
cp -r excalidraw ~/.claude/skills/excalidraw
```

## Adding a New Skill

1. Create a new folder: `my-skill/`
2. Add a `SKILL.md` with frontmatter:
   ```yaml
   ---
   name: my-skill
   description: What this skill does. When to trigger it.
   allowed-tools: Read, Write, Edit, Bash(command:*)
   ---
   ```
3. Add any reference files in `my-skill/references/`
4. Update this README
5. Push and have teammates pull/re-symlink

## Team Usage

After installing, skills are available in Claude Code across all projects. Use them by:
- Typing `/excalidraw` followed by your prompt
- Or just asking Claude to create a diagram naturally -- it will detect the skill automatically
