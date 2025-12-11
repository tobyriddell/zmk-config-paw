#!/usr/bin/env python3
"""
Post-process a keymap-drawer SVG to thicken strokes and text.

Usage:
    python3 thicken_svg.py [input_svg] [output_svg]

Defaults:
    input_svg:  /build/paw.svg
    output_svg: /build/paw_thick.svg
"""
import pathlib
import re
import sys


def patch_svg(text: str) -> str:
    """Insert a style block after the existing style block to override styles."""
    # More specific selectors with !important to override existing styles
    style = (
        "<style>\n"
        "  /* Override stroke widths and colors with !important */\n"
        "  rect.key, rect.combo, rect.combo-separate { stroke-width: 3px !important; stroke: #555555 !important; }\n"
        "  path.combo { stroke-width: 3px !important; stroke: #555555 !important; }\n"
        "  path, line, polyline { stroke-width: 3px !important; stroke: #555555 !important; }\n"
        "  text { font-weight: 1000 !important; stroke: #000000 !important; stroke-width: 0.5px !important; paint-order: stroke !important; }\n"
        "</style>\n"
    )
    # Find the closing </style> tag and insert our style after it
    match = re.search(r"</style>", text, flags=re.IGNORECASE)
    if match:
        pos = match.end()
        return text[:pos] + "\n" + style + text[pos:]
    # Fallback: if no style tag found, insert after opening svg tag
    match = re.search(r"<svg[^>]*>", text, flags=re.IGNORECASE)
    if match:
        pos = match.end()
        return text[:pos] + "\n" + style + text[pos:]
    return text


def main() -> int:
    args = sys.argv[1:]
    input_path = pathlib.Path(args[0]) if len(args) > 0 else pathlib.Path("/build/paw.svg")
    output_path = pathlib.Path(args[1]) if len(args) > 1 else pathlib.Path("/build/paw_thick.svg")

    if not input_path.exists():
        raise SystemExit(f"Input SVG not found: {input_path}")

    text = input_path.read_text()
    patched = patch_svg(text)
    output_path.write_text(patched)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

