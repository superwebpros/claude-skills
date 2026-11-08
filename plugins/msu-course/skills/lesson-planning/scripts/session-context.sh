#!/usr/bin/env bash
# session-context.sh <session-number> [course-root]
#
# Collects the mechanical context for planning one SSC 490 session:
# calendar rows, owning unit, existing files, previous retro, carried material,
# pilot-banner status, and slide deck presence.
#
# Best effort by design. If a section says "could not determine", read the vault by hand —
# the skill's reading order matters more than this tool.

set -uo pipefail

N_RAW="${1:-}"
if ! [[ "$N_RAW" =~ ^[0-9]+$ ]]; then
  echo "usage: session-context.sh <session-number 1-28> [course-root]" >&2
  exit 2
fi
N=$((10#$N_RAW))
NN=$(printf "%02d" "$N")
PREV=$((N - 1)); PREV_NN=$(printf "%02d" "$PREV")
NEXT=$((N + 1)); NEXT_NN=$(printf "%02d" "$NEXT")

# Course root: arg 2, else $COURSE_ROOT, else the current directory (run from the course repo root).
ROOT="${2:-${COURSE_ROOT:-$PWD}}"
if [ ! -f "$ROOT/course-calendar.md" ]; then
  FOUND=$(find "$ROOT/.." -maxdepth 2 -name course-calendar.md 2>/dev/null | sort | tail -1)
  [ -n "$FOUND" ] && ROOT=$(dirname "$FOUND")
fi
if [ ! -f "$ROOT/course-calendar.md" ]; then
  echo "ERROR: no course-calendar.md found. Set COURSE_ROOT or pass the course root as arg 2." >&2
  exit 1
fi
CAL="$ROOT/course-calendar.md"

hr() { printf '\n=== %s ===\n' "$1"; }

echo "SESSION $N  ·  course root: $ROOT"

# ---------------------------------------------------------------- calendar rows
hr "CALENDAR ROWS (authoritative)"
for i in "$PREV" "$N" "$NEXT"; do
  row=$(grep -E "^\| *$i \|" "$CAL" | head -1)
  if [ -n "$row" ]; then
    marker="   "; [ "$i" = "$N" ] && marker="-> "
    echo "${marker}${row}"
  fi
done
echo "   --- no-class rows in the grid ---"
grep -E "^\| *— \|" "$CAL" | sed 's/^/   /'

hr "MILESTONES"
grep -E "^\| \*\*M[0-9]" "$CAL" || echo "   none parsed"

# ---------------------------------------------------------------- owning unit
hr "OWNING UNIT"
UNIT_DIR=""
for d in "$ROOT"/units/*/; do
  ov="$d/Unit Overview.md"
  [ -f "$ov" ] || continue
  range=$(grep -m1 '^sessions:' "$ov" | sed 's/^sessions: *//' | tr -d ' ')
  lo=$(echo "$range" | sed 's/[–—-].*//')
  hi=$(echo "$range" | sed 's/.*[–—-]//')
  [[ "$lo" =~ ^[0-9]+$ && "$hi" =~ ^[0-9]+$ ]] || continue
  if [ "$N" -ge "$lo" ] && [ "$N" -le "$hi" ]; then UNIT_DIR="${d%/}"; fi
done
if [ -z "$UNIT_DIR" ]; then
  hit=$(ls -d "$ROOT"/units/*/"$NN"-*.md 2>/dev/null | head -1)
  [ -n "$hit" ] && UNIT_DIR=$(dirname "$hit")
fi
if [ -n "$UNIT_DIR" ]; then
  echo "   $UNIT_DIR"
  echo "   overview: $UNIT_DIR/Unit Overview.md"
  sed -n '2,9p' "$UNIT_DIR/Unit Overview.md" | sed 's/^/     /'
  # is the unit outcome still a stub?
  if grep -qA2 '^## Unit Outcome' "$UNIT_DIR/Unit Overview.md" && \
     sed -n '/^## Unit Outcome/,/^## /p' "$UNIT_DIR/Unit Overview.md" | grep -q '<!--'; then
    echo "     [!] Unit Outcome is still a stub — sync pass opportunity"
  fi
else
  echo "   could not determine — read units/*/Unit Overview.md by hand"
fi

# ---------------------------------------------------------------- files
hr "FILES FOR THIS SESSION"
THIS=$(ls "$ROOT"/units/*/"$NN"-*.md 2>/dev/null)
if [ -z "$THIS" ]; then
  echo "   none — writing fresh"
else
  echo "$THIS" | while IFS= read -r f; do
    banner=""
    head -1 "$f" | grep -q 'Carried from the Spring 2026 pilot' && banner="  [CARRIED PILOT BANNER — rework, don't start blank]"
    printf '   %s (%s lines)%s\n' "$f" "$(wc -l < "$f" | tr -d ' ')" "$banner"
  done
  echo "$THIS" | while IFS= read -r f; do
    if head -1 "$f" | grep -q 'Carried from the Spring 2026 pilot'; then
      echo
      echo "   --- banner: $(basename "$f") ---"
      sed -n '1,8p' "$f" | sed 's/^/   /'
    fi
  done
fi

hr "ADJACENT SESSIONS"
for i in "$PREV_NN" "$NEXT_NN"; do
  [ "$i" = "00" ] && { echo "   (no previous session — this is the first class)"; continue; }
  [ "$((10#$i))" -gt 28 ] && { echo "   (no next session — this is the last class)"; continue; }
  found=$(ls "$ROOT"/units/*/"$i"-*.md 2>/dev/null | grep -v 'retro' | head -3)
  if [ -n "$found" ]; then echo "$found" | sed 's/^/   /'; else echo "   S$i: no plan file"; fi
done

# ---------------------------------------------------------------- retro
hr "PREVIOUS SESSION RETRO  (highest-value input)"
RETRO=$(ls "$ROOT"/units/*/"$PREV_NN"-retro.md 2>/dev/null | head -1)
if [ "$PREV" -lt 1 ]; then
  echo "   n/a — session 1 has no predecessor"
elif [ -n "$RETRO" ]; then
  echo "   $RETRO"
  echo "   --- carry-forward + off-track sections ---"
  sed -n '/^## 4\./,$p' "$RETRO" | sed 's/^/   /'
else
  echo "   NO RETRO for session $PREV_NN."
  echo "   If S$PREV_NN has been taught, ask before planning — carry-forward items are the"
  echo "   single input the pilot systematically dropped. /lesson-retrospective writes it."
fi

# ---------------------------------------------------------------- carried material
hr "CARRIED PILOT MATERIAL IN THIS UNIT (reference only, not scheduled)"
if [ -n "$UNIT_DIR" ]; then
  ls "$UNIT_DIR"/CARRIED-*.md 2>/dev/null | sed 's/^/   /' || echo "   none"
else
  echo "   unit unknown"
fi
echo "   shared: $ROOT/carried-over/  (see MANIFEST.md)"

# ---------------------------------------------------------------- slides
hr "SLIDES  (flag, don't build)"
SLIDES="${SLIDES_DIR:-}"   # set SLIDES_DIR to the slide-deck markdown folder, if the course has one
if [ -z "$SLIDES" ]; then
  echo "   SLIDES_DIR not set — skipping deck check"
elif [ -d "$SLIDES" ]; then
  deck=$(ls "$SLIDES"/session-"$NN"-*.md 2>/dev/null | head -1)
  if [ -n "$deck" ]; then
    echo "   $deck"
    echo "   [!] verify this is a Fall deck — ssc-490/markdown/ still holds copies of pilot decks"
  else
    echo "   no deck at $SLIDES/session-$NN-*.md — needs building"
  fi
else
  echo "   slides dir not found: $SLIDES"
fi

# ---------------------------------------------------------------- open items
hr "OPEN ⚠️ ITEMS IN course-facts.md"
if [ -f "$ROOT/course-facts.md" ]; then
  grep -n '^- \[ \]' "$ROOT/course-facts.md" | sed 's/^/   /' | head -20
else
  echo "   course-facts.md not found"
fi

hr "TEMPLATES"
ls "$ROOT"/templates/*.md 2>/dev/null | sed 's/^/   /'

echo
echo "Now read, in order: course-calendar → Unit Overview → S${PREV_NN} retro → S${PREV_NN}/S${NEXT_NN} plans → templates."
