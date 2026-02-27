#!/usr/bin/env python3
"""Draw aligned ASCII box diagrams from a simple text format.

Usage: python3 draw-box.py <file>

Input format (one box per file):
  Title line becomes the header. Indent with 2 spaces for nesting.
  Lines starting with "- " become bullet items. Blank lines add spacing.
  Lines starting with "[ ]" become inner boxes (group consecutive ones).

Example input:
  Docker Container
  [lead] agent-lead | UID 1001 | nono Landlock | /workspace/lead
  [coder] agent-coder | UID 1002 | nono Landlock | /workspace/coder

  tps-office-supervisor (PID 1)
  - Creates per-agent Linux users
  - Starts each agent under nono sandbox
  - Drops privileges after setup

Output: perfectly aligned Unicode box diagram.
"""

import sys
import unicodedata

def display_width(s):
    return sum(2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1 for ch in s)

def pad(s, width):
    return s + " " * (width - display_width(s))

def draw_box(title, lines, inner_boxes=None, padding=2):
    """Render a box with optional inner boxes and content lines."""
    parts = []

    # Calculate inner box renders first
    rendered_inners = []
    if inner_boxes:
        max_rows = 0
        for box_lines in inner_boxes:
            w = max(display_width(l) for l in box_lines) + 2
            rendered = []
            rendered.append("┌" + "─" * w + "┐")
            for l in box_lines:
                rendered.append("│ " + pad(l, w - 2) + " │")
            rendered.append("└" + "─" * w + "┘")
            rendered_inners.append(rendered)
            max_rows = max(max_rows, len(rendered))

        # Pad shorter boxes to same height
        for r in rendered_inners:
            while len(r) < max_rows:
                w = display_width(r[0]) - 2  # minus the corners
                r.insert(-1, "│" + " " * w + "│")

    # Determine content width
    content_lines = []
    if rendered_inners:
        for row_idx in range(len(rendered_inners[0])):
            combined = " ".join(r[row_idx] for r in rendered_inners)
            content_lines.append(combined)

    if lines:
        for l in lines:
            content_lines.append(l)

    all_items = [title] + content_lines
    inner_w = max(display_width(item) for item in all_items) + padding * 2

    # Render outer box
    p = " " * padding
    parts.append("┌" + "─" * inner_w + "┐")
    parts.append("│" + p + pad(title, inner_w - padding * 2) + p + "│")

    for line in content_lines:
        if line == "":
            parts.append("│" + " " * inner_w + "│")
        else:
            parts.append("│" + p + pad(line, inner_w - padding * 2) + p + "│")

    parts.append("└" + "─" * inner_w + "┘")
    return parts

def parse_input(text):
    lines = text.strip().split("\n")
    title = lines[0].strip()
    inner_boxes = []
    content = []
    current_box = []

    for line in lines[1:]:
        stripped = line.strip()
        if stripped.startswith("[") and "]" in stripped:
            # Parse inner box: [id] col1 | col2 | col3
            tag_end = stripped.index("]")
            rest = stripped[tag_end + 1:].strip()
            cols = [c.strip() for c in rest.split("|")]
            current_box.append(cols)
        else:
            if current_box:
                # Flush accumulated box lines
                # Group into separate inner boxes by first column
                boxes = {}
                for cols in current_box:
                    key = cols[0] if cols else "box"
                    if key not in boxes:
                        boxes[key] = []
                    boxes[key] = cols
                # Each [tag] line becomes one inner box
                for cols in current_box:
                    inner_boxes.append(cols)
                current_box = []

            if stripped.startswith("- "):
                content.append("· " + stripped[2:])
            elif stripped == "":
                content.append("")
            else:
                content.append(stripped)

    if current_box:
        for cols in current_box:
            inner_boxes.append(cols)

    return title, content, inner_boxes

def main():
    if len(sys.argv) < 2:
        # Read from stdin or show usage
        print(__doc__)
        sys.exit(1)

    with open(sys.argv[1]) as f:
        text = f.read()

    title, content, inner_box_items = parse_input(text)

    # Convert inner box items to box groups
    box_groups = []
    for cols in inner_box_items:
        box_groups.append(cols)

    result = draw_box(title, content, box_groups if box_groups else None)
    print("\n".join(result))

if __name__ == "__main__":
    main()
