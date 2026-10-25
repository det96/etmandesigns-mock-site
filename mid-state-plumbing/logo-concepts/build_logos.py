#!/usr/bin/env python3
"""Build outlined Mid-State Plumbing logo concepts.

Wordmarks are converted to paths from Inter (SIL Open Font License)
so the SVGs render the same way offline, without the font installed.

The Florida silhouette is a Douglas-Peucker simplification (tolerance
0.10 degrees) of the outer ring of a public Florida boundary
(usstatesgeojson / florida.geojson). Longitude is scaled by cos(latitude)
so the panhandle and the peninsula keep the state's real proportions.
The sawtooth where Tampa Bay meets the gulf is eased into one curve so
the mark stays a silhouette. The orange band is a pipe coupling set into
the panhandle, clear of the west tip.
"""

import math
import os

import uharfbuzz as hb
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.abspath(__file__))
FONT_SEMI = "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"

NAVY = "#1a4a61"
ORANGE = "#E85D04"
MIST = "#e8f4f8"
WHITE = "#ffffff"
INK = "#1a4a61"

# Outer ring, west tip of the panhandle, around the peninsula, and back.
# Not closed; the path adds Z.
FLORIDA = [
    (-83.30945, 30.63442),
    (-82.21438, 30.56696),
    (-82.16519, 30.35804),
    (-82.05007, 30.36234),
    (-82.02321, 30.78199),
    (-81.42742, 30.69802),
    (-81.24092, 29.73922),
    (-80.57487, 28.58517),
    (-80.56643, 28.09563),
    (-80.03136, 26.79634),
    (-80.15497, 25.66549),
    (-80.24038, 25.72421),
    (-80.49534, 25.19946),
    (-81.09452, 25.12705),
    (-81.35273, 25.82202),
    (-81.72709, 25.90721),
    (-81.86898, 26.37865),
    (-82.18157, 26.68171),
    (-82.06313, 26.95021),
    (-82.25987, 26.71740),
    (-82.78000, 27.45000),
    (-82.50000, 27.95000),
    (-82.86000, 28.35000),
    (-82.64486, 28.88925),
    (-82.80474, 29.14662),
    (-83.05321, 29.13084),
    (-83.63798, 29.88607),
    (-84.25644, 30.10379),
    (-84.34907, 29.89681),
    (-85.34477, 29.65479),
    (-85.40505, 29.93849),
    (-86.22256, 30.34359),
    (-87.51832, 30.28044),
    (-87.39422, 30.64170),
    (-87.63494, 30.86589),
    (-87.59893, 30.99746),
    (-85.00237, 31.00068),
    (-84.86469, 30.71154),
]

_CLIP = 0


def _union(a, b):
    if a is None:
        return b
    if b is None:
        return a
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[2], b[2]), max(a[3], b[3]))


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
    names = []
    bounds = None
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = tt.getGlyphName(info.codepoint)
        names.append(name)
        pen = SVGPathPen(gs)
        svg_x = (cursor_x + pos.x_offset) * scale
        svg_base = -(cursor_y + pos.y_offset) * scale
        matrix = (scale, 0, 0, -scale, svg_x, svg_base)
        gs[name].draw(TransformPen(pen, matrix))
        cmd = pen.getCommands()
        if cmd:
            parts.append(cmd)
        bp = BoundsPen(gs)
        gs[name].draw(TransformPen(bp, matrix))
        if bp.bounds:
            bounds = _union(bounds, bp.bounds)
        cursor_x += pos.x_advance
        cursor_y += pos.y_advance
    return {
        "d": " ".join(parts),
        "width": cursor_x * scale,
        "bounds": bounds,
        "names": names,
    }


def path_from(shaped, baseline, fill):
    return (
        f'<path fill="{fill}" transform="translate(0 {baseline:.2f})" d="{shaped["d"]}"/>'
    )


def wordmark(fg, hot):
    """Two-line name. Local origin is the top-left of the ink."""
    line1 = "Mid-State"
    line2 = "Plumbing, Inc."
    m1 = shape(FONT_SEMI, line1, 54)
    m2 = shape(FONT_SEMI, line2, 36)
    if "comma" not in m2["names"] or "period" not in m2["names"]:
        raise SystemExit(f"wordmark is missing comma or period: {m2['names']}")
    b1 = m1["bounds"]
    b2 = m2["bounds"]
    base1 = -b1[1]
    line1_bottom = base1 + b1[3]
    air = 16.0
    base2 = line1_bottom + air - b2[1]
    line2_top = base2 + b2[1]
    line2_bottom = base2 + b2[3]
    rule_h = 4.2
    rule_y = (line1_bottom + line2_top - rule_h) / 2.0
    rule_x = b1[0]
    rule_w = 76.0
    rule = (
        f'<rect x="{rule_x:.2f}" y="{rule_y:.2f}" width="{rule_w:.2f}" '
        f'height="{rule_h:.2f}" fill="{hot}"/>'
    )
    bb = _union(
        (b1[0], base1 + b1[1], b1[2], line1_bottom),
        (b2[0], line2_top, b2[2], line2_bottom),
    )
    bb = _union(bb, (rule_x, rule_y, rule_x + rule_w, rule_y + rule_h))
    return path_from(m1, base1, fg) + rule + path_from(m2, base2, fg), bb


def florida_geometry(x, y, w, h):
    """Project the state into the box. Returns path data and points."""
    lons = [p[0] for p in FLORIDA]
    lats = [p[1] for p in FLORIDA]
    minlon, maxlon = min(lons), max(lons)
    minlat, maxlat = min(lats), max(lats)
    kx = math.cos(math.radians((minlat + maxlat) / 2.0))
    xs = [(lon - minlon) * kx for lon in lons]
    ys = [(maxlat - lat) for lat in lats]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    scale = min(w / (maxx - minx), h / (maxy - miny))
    used_w = (maxx - minx) * scale
    used_h = (maxy - miny) * scale
    ox = x + (w - used_w) / 2.0
    oy = y + (h - used_h) / 2.0
    pts = [(ox + (px - minx) * scale, oy + (py - miny) * scale) for px, py in zip(xs, ys)]
    d = "M " + " L ".join(f"{px:.2f} {py:.2f}" for px, py in pts) + " Z"
    return d, pts


def svg_symbol_a(ox, oy, size, fg, hot, joint):
    """Florida silhouette. Orange coupling crosses the panhandle, inset from the tip."""
    global _CLIP
    _CLIP += 1
    cid = f"flc{_CLIP}"
    d, pts = florida_geometry(ox, oy, size, size)
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)
    width = maxx - minx
    # A collar on the shaft of the panhandle, not a cap on the west tip.
    band_w = width * 0.105
    band_cx = minx + width * 0.20
    bar = (
        f"M {band_cx - band_w / 2:.2f} {miny - size:.2f} "
        f"H {band_cx + band_w / 2:.2f} "
        f"V {miny + (maxy - miny) * 0.32:.2f} "
        f"H {band_cx - band_w / 2:.2f} Z"
    )
    art = (
        f'<clipPath id="{cid}"><path d="{d}"/></clipPath>'
        f'<path fill="{fg}" d="{d}"/>'
        f'<path fill="{hot}" clip-path="url(#{cid})" d="{bar}"/>'
    )
    return art, (minx, miny, maxx, maxy)


def _stroke_bbox(polylines, sw):
    half = sw / 2.0
    minx = miny = 1e9
    maxx = maxy = -1e9
    for pts in polylines:
        for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
            dx, dy = x2 - x1, y2 - y1
            length = math.hypot(dx, dy) or 1.0
            nx, ny = -dy / length * half, dx / length * half
            for x, y in ((x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x2 + nx, y2 + ny), (x2 - nx, y2 - ny)):
                minx, maxx = min(minx, x), max(maxx, x)
                miny, maxy = min(miny, y), max(maxy, y)
    return (minx, miny, maxx, maxy)


def svg_symbol_b(ox, oy, size, fg, hot, joint):
    """Two right-angle pipe runs. Same stroke. The orange run does not cross the other."""
    u = size / 64.0
    sw = 6.6 * u

    def P(px, py):
        return (ox + px * u, oy + py * u)

    # Shifted so the stroked bounds sit on the center of the 64 tile.
    cool = [P(11, 13.6), P(32, 13.6), P(32, 31.6), P(53, 31.6)]
    warm = [P(18, 44.6), P(40, 44.6), P(40, 53.6)]
    joints = [cool[1], cool[2], warm[1]]

    def d_of(pts):
        return "M " + " L ".join(f"{x:.2f} {y:.2f}" for x, y in pts)

    dots = "".join(
        f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{2.35 * u:.2f}" fill="{joint}"/>'
        for x, y in joints
    )
    art = (
        f'<path fill="none" stroke="{fg}" stroke-width="{sw:.2f}" '
        f'stroke-linejoin="miter" stroke-linecap="butt" d="{d_of(cool)}"/>'
        f'<path fill="none" stroke="{hot}" stroke-width="{sw:.2f}" '
        f'stroke-linejoin="miter" stroke-linecap="butt" d="{d_of(warm)}"/>'
        f"{dots}"
    )
    return art, _stroke_bbox([cool, warm], sw)


def _offset_down(a, b, dist):
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    n1 = (-dy / length, dx / length)
    n2 = (dy / length, -dx / length)
    normal = n1 if n1[1] > n2[1] else n2
    return (a[0] + normal[0] * dist, a[1] + normal[1] * dist), (
        b[0] + normal[0] * dist,
        b[1] + normal[1] * dist,
    )


def _at_x(p, q, x):
    t = (x - p[0]) / (q[0] - p[0])
    return (x, p[1] + t * (q[1] - p[1]))


def _intersect(p1, p2, p3, p4):
    den = (p1[0] - p2[0]) * (p3[1] - p4[1]) - (p1[1] - p2[1]) * (p3[0] - p4[0])
    t = ((p1[0] - p3[0]) * (p3[1] - p4[1]) - (p1[1] - p3[1]) * (p3[0] - p4[0])) / den
    return (p1[0] + t * (p2[0] - p1[0]), p1[1] + t * (p2[1] - p1[1]))


def svg_symbol_c(ox, oy, size, fg, hot, joint):
    """MSP. Shared cap height and stem weight. S is an open pipe bend."""
    u = size / 64.0
    top, bot = 10.0, 54.0
    stem = 5.8

    def X(px):
        return ox + px * u

    def Y(py):
        return oy + py * u

    def xy(p):
        return (X(p[0]), Y(p[1]))

    # M. Diagonals are parallel offsets of the stems so the valley stays open.
    m_l, m_r = 2.2, 25.0
    mid = (m_l + m_r) / 2.0
    valley = (mid, top + (bot - top) * 0.36)
    left_top = (m_l + stem, top)
    right_top = (m_r - stem, top)
    i_left_a, i_left_b = _offset_down(left_top, valley, stem)
    i_right_a, i_right_b = _offset_down(right_top, valley, stem)
    peel_l = _at_x(i_left_a, i_left_b, m_l + stem)
    peel_r = _at_x(i_right_a, i_right_b, m_r - stem)
    inner_v = _intersect(i_left_a, i_left_b, i_right_a, i_right_b)
    if not (top + 8 < inner_v[1] < bot - 4):
        raise SystemExit(f"M valley is out of the letter: {inner_v}")
    m_pts = [
        (m_l, bot),
        (m_l, top),
        left_top,
        valley,
        right_top,
        (m_r, top),
        (m_r, bot),
        (m_r - stem, bot),
        peel_r,
        inner_v,
        peel_l,
        (m_l + stem, bot),
    ]
    m = "M " + " L ".join(f"{X(px):.2f} {Y(py):.2f}" for px, py in m_pts) + " Z"

    # S centerline. Round caps land on the same cap line and baseline as M and P.
    s_left = m_r + 3.4
    s_width = 14.2
    s_l = s_left + stem / 2.0
    s_r = s_left + s_width - stem / 2.0
    s_top = top + stem / 2.0
    s_bot = bot - stem / 2.0
    s_mid = (s_top + s_bot) / 2.0
    s = (
        f"M {X(s_r):.2f} {Y(s_top):.2f} "
        f"H {X(s_l):.2f} V {Y(s_mid):.2f} "
        f"H {X(s_r):.2f} V {Y(s_bot):.2f} "
        f"H {X(s_l):.2f}"
    )

    # P. Bowl wall matches the stem; the counter stays open.
    p_l = s_left + s_width + 3.4
    p_r = 61.6
    bowl_bot = top + (bot - top) * 0.50
    mid_y = (top + bowl_bot) / 2.0
    shoulder = p_l + stem + 1.2
    p = (
        f"M {X(p_l):.2f} {Y(bot):.2f} "
        f"V {Y(top):.2f} H {X(shoulder):.2f} "
        f"Q {X(p_r):.2f} {Y(top):.2f} {X(p_r):.2f} {Y(mid_y):.2f} "
        f"Q {X(p_r):.2f} {Y(bowl_bot):.2f} {X(shoulder):.2f} {Y(bowl_bot):.2f} "
        f"H {X(p_l + stem):.2f} V {Y(bot):.2f} Z "
        f"M {X(p_l + stem):.2f} {Y(top + 4.0):.2f} "
        f"H {X(p_l + stem + 1.0):.2f} "
        f"Q {X(p_r - 4.0):.2f} {Y(top + 4.0):.2f} {X(p_r - 4.0):.2f} {Y(mid_y):.2f} "
        f"Q {X(p_r - 4.0):.2f} {Y(bowl_bot - 3.4):.2f} {X(p_l + stem + 1.0):.2f} {Y(bowl_bot - 3.4):.2f} "
        f"H {X(p_l + stem):.2f} Z"
    )
    art = (
        f'<path fill="{fg}" fill-rule="evenodd" d="{m} {p}"/>'
        f'<path fill="none" stroke="{hot}" stroke-width="{stem * u:.2f}" '
        f'stroke-linejoin="round" stroke-linecap="round" d="{s}"/>'
    )
    return art, (X(m_l), Y(top), X(p_r), Y(bot))


def _elbow_centroid_shift(arm, thick):
    """How far the area centroid sits from the elbow corner, in (x, y-down)."""
    half = thick / 2.0
    v_area = thick * (arm + half)
    h_area = (arm + half) * thick
    o_area = thick * thick
    # Vertical bar center is above the corner (negative y) by (arm - half) / 2.
    v_cy = -(arm - half) / 2.0
    h_cx = (arm - half) / 2.0
    area = v_area + h_area - o_area
    cx = (h_area * h_cx) / area
    cy = (v_area * v_cy) / area
    return cx, cy


def svg_symbol_d(ox, oy, size, fg, hot, joint):
    """Chamfered stamp. The elbow's weight is centered in the plate."""
    u = size / 64.0

    def X(px):
        return ox + px * u

    def Y(py):
        return oy + py * u

    plate_sw = 4.6
    plate = (
        f"M {X(18):.2f} {Y(6):.2f} H {X(46):.2f} L {X(58):.2f} {Y(18):.2f} "
        f"V {Y(46):.2f} L {X(46):.2f} {Y(58):.2f} H {X(18):.2f} "
        f"L {X(6):.2f} {Y(46):.2f} V {Y(18):.2f} Z"
    )
    arm = 15.0
    thick = 7.2
    half = thick / 2.0
    shift_x, shift_y = _elbow_centroid_shift(arm, thick)
    # Corner sits so the filled L is centered on the plate (32, 32).
    cx = 32.0 - shift_x
    cy = 32.0 - shift_y
    bend = (
        f"M {X(cx - half):.2f} {Y(cy - arm):.2f} "
        f"L {X(cx + half):.2f} {Y(cy - arm):.2f} "
        f"L {X(cx + half):.2f} {Y(cy - half):.2f} "
        f"L {X(cx + arm):.2f} {Y(cy - half):.2f} "
        f"L {X(cx + arm):.2f} {Y(cy + half):.2f} "
        f"L {X(cx - half):.2f} {Y(cy + half):.2f} Z"
    )
    art = (
        f'<path fill="none" stroke="{fg}" stroke-width="{plate_sw * u:.2f}" '
        f'stroke-linejoin="miter" d="{plate}"/>'
        f'<path fill="{hot}" d="{bend}"/>'
        f'<circle cx="{X(cx):.2f}" cy="{Y(cy):.2f}" r="{2.15 * u:.2f}" fill="{joint}"/>'
    )
    outer = plate_sw / 2.0
    return art, (X(6 - outer), Y(6 - outer), X(58 + outer), Y(58 + outer))


def compose(symbol_fn, ground, fg, hot, joint, pad, include_ground):
    """Mark on the left of the name. Padding is measured from the ink."""
    sym, sb = symbol_fn(0, 0, 168, fg, hot, joint)
    wm, wb = wordmark(fg, hot)
    sw = sb[2] - sb[0]
    sh = sb[3] - sb[1]
    ww = wb[2] - wb[0]
    wh = wb[3] - wb[1]
    gap = 36.0
    block_h = max(sh, wh)
    sym_tx = pad - sb[0]
    sym_ty = pad + (block_h - sh) / 2.0 - sb[1]
    wm_tx = pad + sw + gap - wb[0]
    wm_ty = pad + (block_h - wh) / 2.0 - wb[1]
    vb_w = wm_tx + wb[2] + pad
    vb_h = pad + block_h + pad
    sym_right = sym_tx + sb[2]
    wm_left = wm_tx + wb[0]
    if sym_right > wm_left - 8:
        raise SystemExit(f"mark overlaps the wordmark ({sym_right:.1f} vs {wm_left:.1f})")
    ground_rect = f'<rect width="100%" height="100%" fill="{ground}"/>' if include_ground else ""
    width_attr = ""
    if include_ground:
        width_attr = f' width="1200" height="{1200 * vb_h / vb_w:.2f}"'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w:.2f} {vb_h:.2f}"{width_attr} role="img" aria-label="Mid-State Plumbing, Inc.">
  {ground_rect}
  <g transform="translate({sym_tx:.2f} {sym_ty:.2f})">{sym}</g>
  <g transform="translate({wm_tx:.2f} {wm_ty:.2f})">{wm}</g>
</svg>
'''
    return svg, {
        "gap": wm_left - sym_right,
        "pad": pad,
        "vb": (vb_w, vb_h),
    }


def icon_svg(symbol_fn):
    art, bb = symbol_fn(0, 0, 64, MIST, ORANGE, NAVY)
    bw = bb[2] - bb[0]
    bh = bb[3] - bb[1]
    inner = 52.0
    scale = inner / max(bw, bh)
    tw = bw * scale
    th = bh * scale
    tx = (64.0 - tw) / 2.0 - bb[0] * scale
    ty = (64.0 - th) / 2.0 - bb[1] * scale
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" width="512" height="512" role="img" aria-label="Mid-State Plumbing, Inc.">
  <rect width="64" height="64" fill="{NAVY}"/>
  <g transform="translate({tx:.3f} {ty:.3f}) scale({scale:.5f})">{art}</g>
</svg>
'''


CONCEPTS = [
    ("a-state-line", svg_symbol_a),
    ("b-schematic", svg_symbol_b),
    ("c-monogram", svg_symbol_c),
    ("d-field-badge", svg_symbol_d),
]


def main():
    for folder, fn in CONCEPTS:
        dest = os.path.join(ROOT, folder)
        os.makedirs(dest, exist_ok=True)
        light, info = compose(fn, WHITE, INK, ORANGE, WHITE, pad=32, include_ground=True)
        navy, _ = compose(fn, NAVY, WHITE, ORANGE, NAVY, pad=32, include_ground=True)
        header, _ = compose(fn, "none", MIST, ORANGE, NAVY, pad=6, include_ground=False)
        files = {
            "logo-light.svg": light,
            "logo-navy.svg": navy,
            "logo-header.svg": header,
            "icon.svg": icon_svg(fn),
        }
        for name, svg in files.items():
            path = os.path.join(dest, name)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(svg)
        print(
            f"{folder}: viewBox {info['vb'][0]:.1f} x {info['vb'][1]:.1f}, "
            f"ink gap {info['gap']:.1f}"
        )


if __name__ == "__main__":
    main()
