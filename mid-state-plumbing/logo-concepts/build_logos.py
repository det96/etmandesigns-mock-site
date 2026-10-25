#!/usr/bin/env python3
"""Build outlined Mid-State Plumbing logo concepts.

Wordmarks are converted to paths from Inter (SIL Open Font License)
so the SVGs render the same way offline, without the font installed.
"""

import os
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = os.path.dirname(os.path.abspath(__file__))
FONT_SEMI = "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"
FONT_MED = "/usr/share/fonts/truetype/macos/Inter-Medium.ttf"

NAVY = "#1a4a61"
BLUE = "#2c5f7c"
ORANGE = "#E85D04"
MIST = "#e8f4f8"
WHITE = "#ffffff"
INK = "#1a4a61"

# Simplified Florida shoreline, west tip to west tip, clockwise from the north.
# Drawn as a logo silhouette, not a navigation chart.
FLORIDA = [
    (-87.55, 30.42),
    (-86.20, 30.55),
    (-84.90, 30.38),
    (-83.60, 30.28),
    (-82.85, 30.48),
    (-82.05, 30.70),
    (-81.48, 30.58),
    (-81.40, 29.85),
    (-81.15, 29.10),
    (-80.85, 28.20),
    (-80.55, 27.30),
    (-80.20, 26.40),
    (-80.05, 25.70),
    (-80.25, 25.20),
    (-80.85, 25.05),
    (-81.45, 24.68),
    (-81.15, 24.95),
    (-80.55, 25.35),
    (-81.15, 25.95),
    (-81.70, 26.75),
    (-82.15, 27.55),
    (-82.55, 28.35),
    (-82.80, 29.05),
    (-83.30, 29.55),
    (-84.15, 29.72),
    (-85.40, 29.68),
    (-86.60, 30.05),
    (-87.35, 30.28),
]


def shape(font_path, text, size):
    blob = hb.Blob.from_file_path(font_path)
    face = hb.Face(blob)
    hbfont = hb.Font(face)
    hbfont.scale = (face.upem, face.upem)
    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(hbfont, buf)

    tt = TTFont(font_path)
    gs = tt.getGlyphSet()
    upem = tt["head"].unitsPerEm
    scale = size / upem
    parts = []
    cursor_x = 0.0
    cursor_y = 0.0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = tt.getGlyphName(info.codepoint)
        pen = SVGPathPen(gs)
        svg_x = (cursor_x + pos.x_offset) * scale
        svg_base = -(cursor_y + pos.y_offset) * scale
        gs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, svg_x, svg_base)))
        cmd = pen.getCommands()
        if cmd:
            parts.append(cmd)
        cursor_x += pos.x_advance
        cursor_y += pos.y_advance
    os2 = tt["OS/2"]
    return {
        "d": " ".join(parts),
        "width": cursor_x * scale,
        "ascent": os2.sTypoAscender * scale,
        "descent": -os2.sTypoDescender * scale,
    }


def move_path(d, dx, dy):
    """Translate an SVG path whose commands use absolute coordinates only."""
    # SVGPathPen emits absolute M/L/C/Q/Z. Apply a translate by rewriting numbers
    # is fragile. Wrap in a group instead.
    return d


def text_path(font_path, text, size, x, baseline, fill):
    shaped = shape(font_path, text, size)
    return (
        f'<path fill="{fill}" transform="translate({x:.2f} {baseline:.2f})" d="{shaped["d"]}"/>',
        shaped,
    )


def florida_path(x, y, w, h):
    lons = [p[0] for p in FLORIDA]
    lats = [p[1] for p in FLORIDA]
    minlon, maxlon = min(lons), max(lons)
    minlat, maxlat = min(lats), max(lats)
    s = min(w / (maxlon - minlon), h / (maxlat - minlat))
    used_w = (maxlon - minlon) * s
    used_h = (maxlat - minlat) * s
    ox = x + (w - used_w) / 2
    oy = y + (h - used_h) / 2
    pts = []
    for lon, lat in FLORIDA:
        pts.append((ox + (lon - minlon) * s, oy + (maxlat - lat) * s))
    d = "M " + " L ".join(f"{px:.2f} {py:.2f}" for px, py in pts) + " Z"
    return d, pts, s


def elbow(cx, cy, arm, thick):
    """Square pipe elbow opening up and to the right, centered on the corner."""
    h = thick / 2
    # vertical leg going up from the corner, horizontal leg going right
    d = (
        f"M {cx - h:.2f} {cy - arm:.2f} "
        f"L {cx + h:.2f} {cy - arm:.2f} "
        f"L {cx + h:.2f} {cy - h:.2f} "
        f"L {cx + arm:.2f} {cy - h:.2f} "
        f"L {cx + arm:.2f} {cy + h:.2f} "
        f"L {cx - h:.2f} {cy + h:.2f} Z"
    )
    return d


def symbol_a(ox, oy, size, fg, hot):
    """Florida silhouette with an orange coupling on the panhandle."""
    d, pts, s = florida_path(ox, oy, size, size)
    # West tip of the panhandle is the minimum x among the northern third.
    north = [p for p in pts if p[1] < oy + size * 0.42]
    tip = min(north, key=lambda p: p[0])
    # Coupling: a short orange bar set into the west end, thick enough to survive 16px.
    thick = size * 0.115
    length = size * 0.20
    cy = tip[1] + size * 0.012
    cx = tip[0] + length * 0.15
    bar = (
        f"M {cx:.2f} {cy - thick / 2:.2f} "
        f"h {length:.2f} v {thick:.2f} h {-length:.2f} Z"
    )
    # Keep the bar inside the state.
    return f'''<g>
      <path fill="{fg}" d="{d}"/>
      <path fill="{hot}" clip-path="url(#fl-clip-{id(d)})" d="{bar}"/>
    </g>''', d


def svg_symbol_a(ox, oy, size, fg, hot, clip_id):
    d, pts, _ = florida_path(ox, oy, size, size)
    north = [p for p in pts if p[1] < oy + size * 0.45]
    tip = min(north, key=lambda p: p[0])
    thick = size * 0.125
    length = size * 0.22
    cy = tip[1] + thick * 0.05
    cx = tip[0] - thick * 0.05
    bar = (
        f"M {cx:.2f} {cy - thick / 2:.2f} "
        f"H {cx + length:.2f} V {cy + thick / 2:.2f} H {cx:.2f} Z"
    )
    return (
        f'<clipPath id="{clip_id}"><path d="{d}"/></clipPath>'
        f'<path fill="{fg}" d="{d}"/>'
        f'<path fill="{hot}" clip-path="url(#{clip_id})" d="{bar}"/>'
    )


def svg_symbol_b(ox, oy, size, fg, hot, joint):
    """Orthogonal pipe runs. One run is the safety-orange main."""
    u = size / 64
    x = ox
    y = oy

    def p(px, py):
        return f"{x + px * u:.2f} {y + py * u:.2f}"

    cool = f"M {p(8, 16)} H {p(30, 16)[len(str(int(x))):]}" 
    # build explicitly
    def X(px):
        return x + px * u

    def Y(py):
        return y + py * u

    cool_d = f"M {X(9):.2f} {Y(16):.2f} H {X(30):.2f} V {Y(40):.2f} H {X(54):.2f}"
    hot_d = f"M {X(16):.2f} {Y(28):.2f} H {X(40):.2f} V {Y(54):.2f}"
    sw = 7.2 * u
    joints = [(30, 16), (40, 28), (54, 40)]
    circles = "".join(
        f'<circle cx="{X(cx):.2f}" cy="{Y(cy):.2f}" r="{3.4 * u:.2f}" fill="{joint}"/>'
        for cx, cy in joints
    )
    return (
        f'<path fill="none" stroke="{fg}" stroke-width="{sw:.2f}" stroke-linejoin="miter" stroke-linecap="square" d="{cool_d}"/>'
        f'<path fill="none" stroke="{hot}" stroke-width="{sw:.2f}" stroke-linejoin="miter" stroke-linecap="square" d="{hot_d}"/>'
        f"{circles}"
    )


def svg_symbol_c(ox, oy, size, fg, hot):
    """Condensed MSP. The S is a pipe bend in safety orange."""
    u = size / 64

    def X(px):
        return ox + px * u

    def Y(py):
        return oy + py * u

    m = (
        f"M {X(3.5):.2f} {Y(54):.2f} L {X(3.5):.2f} {Y(10):.2f} "
        f"L {X(10):.2f} {Y(10):.2f} L {X(16.2):.2f} {Y(26):.2f} "
        f"L {X(22.4):.2f} {Y(10):.2f} L {X(28.9):.2f} {Y(10):.2f} "
        f"L {X(28.9):.2f} {Y(54):.2f} L {X(22.6):.2f} {Y(54):.2f} "
        f"L {X(22.6):.2f} {Y(28):.2f} L {X(16.2):.2f} {Y(42):.2f} "
        f"L {X(9.8):.2f} {Y(28):.2f} L {X(9.8):.2f} {Y(54):.2f} Z"
    )
    # Orthogonal S, same stroke weight as the letter stems.
    sw = 6.4 * u
    s = (
        f"M {X(45.2):.2f} {Y(13.2):.2f} H {X(33.4):.2f} "
        f"V {Y(30.2):.2f} H {X(45.2):.2f} V {Y(50.8):.2f} H {X(32.2):.2f}"
    )
    p = (
        f"M {X(48.6):.2f} {Y(10):.2f} H {X(56.4):.2f} "
        f"Q {X(61.6):.2f} {Y(10):.2f} {X(61.6):.2f} {Y(19.4):.2f} "
        f"Q {X(61.6):.2f} {Y(28.6):.2f} {X(56.4):.2f} {Y(28.6):.2f} "
        f"H {X(54.8):.2f} V {Y(54):.2f} H {X(48.6):.2f} Z "
        f"M {X(54.8):.2f} {Y(15.8):.2f} V {Y(22.8):.2f} H {X(56):.2f} "
        f"Q {X(57.8):.2f} {Y(22.8):.2f} {X(57.8):.2f} {Y(19.3):.2f} "
        f"Q {X(57.8):.2f} {Y(15.8):.2f} {X(56):.2f} {Y(15.8):.2f} Z"
    )
    return (
        f'<path fill="{fg}" fill-rule="evenodd" d="{m} {p}"/>'
        f'<path fill="none" stroke="{hot}" stroke-width="{sw:.2f}" stroke-linejoin="miter" stroke-linecap="square" d="{s}"/>'
    )


def svg_symbol_d(ox, oy, size, fg, hot):
    """Chamfered field badge with a pipe elbow inside."""
    u = size / 64

    def X(px):
        return ox + px * u

    def Y(py):
        return oy + py * u

    plate = (
        f"M {X(14):.2f} {Y(6):.2f} H {X(50):.2f} L {X(58):.2f} {Y(14):.2f} "
        f"V {Y(50):.2f} L {X(50):.2f} {Y(58):.2f} H {X(14):.2f} "
        f"L {X(6):.2f} {Y(50):.2f} V {Y(14):.2f} Z"
    )
    inner = (
        f"M {X(18):.2f} {Y(12):.2f} H {X(46):.2f} L {X(52):.2f} {Y(18):.2f} "
        f"V {Y(46):.2f} L {X(46):.2f} {Y(52):.2f} H {X(18):.2f} "
        f"L {X(12):.2f} {Y(46):.2f} V {Y(18):.2f} Z"
    )
    # Elbow centered in the badge. Corner sits near the middle.
    arm = 18 * u
    thick = 8.2 * u
    cx = X(29)
    cy = Y(38)
    h = thick / 2
    bend = (
        f"M {cx - h:.2f} {cy - arm:.2f} L {cx + h:.2f} {cy - arm:.2f} "
        f"L {cx + h:.2f} {cy - h:.2f} L {cx + arm:.2f} {cy - h:.2f} "
        f"L {cx + arm:.2f} {cy + h:.2f} L {cx - h:.2f} {cy + h:.2f} Z"
    )
    return (
        f'<path fill="none" stroke="{fg}" stroke-width="{3.6 * u:.2f}" d="{plate}"/>'
        f'<path fill="{hot}" d="{bend}"/>'
        f'<circle cx="{cx:.2f}" cy="{cy:.2f}" r="{2.5 * u:.2f}" fill="{fg}"/>'
    )


def wordmark(x, baseline_adjust, fg, hot):
    """Two-line name. Returns svg, width, height used, top y."""
    line1 = "Mid-State"
    line2 = "Plumbing, Inc."
    s1 = 58
    s2 = 40
    gap = 12
    t1, m1 = text_path(FONT_SEMI, line1, s1, 0, 0, fg)
    t2, m2 = text_path(FONT_SEMI, line2, s2, 0, 0, fg)
    width = max(m1["width"], m2["width"])
    # Baselines: line1 ascent starts at y of the block.
    top = 0
    base1 = m1["ascent"]
    base2 = base1 + m1["descent"] + gap + m2["ascent"]
    block_h = base2 + m2["descent"]
    rule_w = min(78, m1["width"] * 0.42)
    rule_y = base1 + m1["descent"] + gap * 0.45
    # Reposition. text_path already baked baseline 0, we translate.
    t1, _ = text_path(FONT_SEMI, line1, s1, x, base1, fg)
    t2, _ = text_path(FONT_SEMI, line2, s2, x, base2, fg)
    rule = f'<rect x="{x:.2f}" y="{rule_y:.2f}" width="{rule_w:.2f}" height="5" fill="{hot}"/>'
    svg = t1 + rule + t2
    return svg, width, block_h, base1


def lockup(symbol_fn, ground, fg, hot, joint, plate):
    """Full logo. plate True draws the navy icon tile behind the symbol (light version)."""
    # Canvas
    mark = 168
    pad = 28
    gap = 36
    sym_x = pad
    sym_y = 36
    text_x = pad + mark + gap
    # Wordmark block vertical center against the mark.
    wm_svg, wm_w, wm_h, _ = wordmark(0, 0, fg, hot)
    canvas_h = mark + pad * 2
    text_y = (canvas_h - wm_h) / 2
    # Rebuild wordmark at text_x, shifted by text_y. wordmark() uses y starting at 0.
    # Easiest: wrap wordmark in a translate group.
    wm_inner, wm_w, wm_h, _ = wordmark(0, 0, fg, hot)
    canvas_w = text_x + wm_w + pad
    if plate:
        symbol_bg = f'<rect x="{sym_x}" y="{sym_y}" width="{mark}" height="{mark}" fill="{NAVY}"/>'
        # Symbol art is the reversed (light on navy) drawing inside the tile.
        art = symbol_fn(sym_x, sym_y, mark, MIST, ORANGE, MIST)
    else:
        symbol_bg = ""
        art = symbol_fn(sym_x, sym_y, mark, fg, hot, joint)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w:.2f} {canvas_h:.2f}" width="1200" height="{1200 * canvas_h / canvas_w:.2f}" role="img" aria-label="Mid-State Plumbing, Inc.">
  <rect width="100%" height="100%" fill="{ground}"/>
  {symbol_bg}
  {art}
  <g transform="translate(0 {text_y:.2f})">{wm_inner}</g>
</svg>
'''


def icon_svg(symbol_fn):
    size = 64
    art = symbol_fn(0, 0, size, MIST, ORANGE, MIST)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="512" height="512" role="img" aria-label="Mid-State Plumbing, Inc.">
  <rect width="64" height="64" fill="{NAVY}"/>
  {art}
</svg>
'''


def header_svg(symbol_fn):
    """Reversed art, no background plate, for the navy site header."""
    mark = 168
    pad_y = 8
    gap = 26
    sym_x = 0
    sym_y = pad_y
    text_x = mark + gap
    wm_inner, wm_w, wm_h, _ = wordmark(0, 0, WHITE, ORANGE)
    canvas_h = max(mark + pad_y * 2, wm_h + pad_y * 2)
    text_y = (canvas_h - wm_h) / 2
    sym_y = (canvas_h - mark) / 2
    art = symbol_fn(sym_x, sym_y, mark, MIST, ORANGE, MIST)
    canvas_w = text_x + wm_w
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_w:.2f} {canvas_h:.2f}" role="img" aria-label="Mid-State Plumbing, Inc.">
  {art}
  <g transform="translate({text_x:.2f} {text_y:.2f})">{wm_inner}</g>
</svg>
'''


def adapt(fn):
    """Symbols use (ox, oy, size, fg, hot, joint) or without joint."""

    def call(ox, oy, size, fg, hot, joint):
        try:
            return fn(ox, oy, size, fg, hot, joint)
        except TypeError:
            return fn(ox, oy, size, fg, hot)

    return call


CONCEPTS = [
    ("a-state-line", adapt(lambda ox, oy, size, fg, hot, joint: svg_symbol_a(ox, oy, size, fg, hot, f"fl-{ox:.0f}-{oy:.0f}"))),
    ("b-schematic", adapt(svg_symbol_b)),
    ("c-monogram", adapt(svg_symbol_c)),
    ("d-field-badge", adapt(svg_symbol_d)),
]


def main():
    for folder, fn in CONCEPTS:
        dest = os.path.join(ROOT, folder)
        os.makedirs(dest, exist_ok=True)
        files = {
            "logo-light.svg": lockup(fn, WHITE, INK, ORANGE, WHITE, plate=False),
            "logo-navy.svg": lockup(fn, NAVY, WHITE, ORANGE, MIST, plate=False),
            "icon.svg": icon_svg(fn),
            "logo-header.svg": header_svg(fn),
        }
        # Clip ids must be unique within a file. They're based on coordinates, OK.
        for name, svg in files.items():
            path = os.path.join(dest, name)
            with open(path, "w", encoding="utf-8") as f:
                f.write(svg)
            print("wrote", path)


if __name__ == "__main__":
    main()
