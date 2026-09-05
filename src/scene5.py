"""5 - Tyrell Approach: a wireframe ziggurat over a light grid at first light."""
import math, random
from palette import *

NAME = "tyrell-approach"
LIGHT = "dawn"
OUTDOOR = True


def build(rain=True, light=LIGHT):
    rnd = random.Random(101)
    HZ = int(H * 0.585)
    S = [svg_open(), '<defs>']
    if rain:
        stops = (("0", "#050718"), ("0.24", "#101034"), ("0.44", "#2a1550"),
                 ("0.62", "#5c1f63"), ("0.80", "#8e2f6b"), ("1", "#22143c"))
    else:
        stops = (("0", "#03040f"), ("0.22", "#0d1240"), ("0.42", "#2e1663"),
                 ("0.60", "#7a2178"), ("0.78", "#d94a7a"), ("1", "#2a1642"))
    # First light belongs to the sky here, so the zenith takes the whole grade
    # and the sunrise band near the horizon is left alone to stay the hottest
    # part of the frame.
    stops = (lit_stops(stops[:3], light)
             + lit_stops(stops[3:5], light, k=0.35)
             + lit_stops(stops[5:], light, k=0.8))
    S.append('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">%s</linearGradient>'
             % "".join('<stop offset="%s" stop-color="%s"/>' % s for s in stops))
    gs = lit_stops((("0", "#2a1046"), ("0.35", "#0d0a26"), ("1", "#04050f")), light, k=0.7)
    S.append('<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s" stop-opacity="0.95"/>'
             '<stop offset="0.35" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
             % tuple(c for _, c in gs))
    S.append('<radialGradient id="hzglow"><stop offset="0" stop-color="%s" stop-opacity="0.9"/>'
             '<stop offset="0.45" stop-color="%s" stop-opacity="0.30"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (CYAN, MAGENTA, MAGENTA))
    S.append('<radialGradient id="disc"><stop offset="0" stop-color="#ffd9f2" stop-opacity="0.95"/>'
             '<stop offset="0.35" stop-color="%s" stop-opacity="0.75"/>'
             '<stop offset="0.7" stop-color="%s" stop-opacity="0.25"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (MAGENTA, ROSE, ROSE))
    S.append('<filter id="huge" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="140"/></filter>')
    S.append('<filter id="big" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="46"/></filter>')
    S.append('<filter id="med" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="16"/></filter>')
    S.append('<filter id="low" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="5"/></filter>')
    S.append('</defs>')
    S.append('<rect width="%d" height="%d" fill="url(#sky)"/>' % (W, H))

    # ---- stars, thinned out by cloud when it rains
    for _ in range(stars(300 if rain else 700, light)):
        y = rnd.uniform(0, HZ * 0.92)
        S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="#e6f0ff" opacity="%.2f"/>'
                 % (rnd.uniform(0, W), y, rnd.uniform(0.9, 3.0), rnd.uniform(0.08, 0.85) * (1 - y / HZ) * (0.5 if rain else 1.0)))

    VPX, VPY = W * 0.5, float(HZ)

    # ---- the disc sitting on the horizon behind everything
    S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="url(#disc)"/>' % (W * 0.30, HZ - H * 0.055, H * 0.20))
    S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="url(#hzglow)" opacity="%.2f"/>'
             % (VPX, VPY, W * 0.62, H * 0.20, glow(0.85, light)))

    # ---- distant city, low and dark, so the ziggurat dominates
    x = -200
    city = []
    while x < W + 200:
        w = rnd.uniform(40, 150); h = rnd.uniform(20, 190)
        city.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f"/>' % (x, HZ - h, w, h + 40))
        x += w * rnd.uniform(0.9, 1.7)
    S.append('<g fill="#0b0820" opacity="0.9">%s</g>' % "".join(city))

    # ---- wireframe ziggurat
    ZX, ZTOP, ZBASE, ZHALF = W * 0.5, HZ - H * 0.40, float(HZ), W * 0.21
    steps = 9
    edges, faces = [], []
    for i in range(steps + 1):
        t = i / float(steps)
        y = ZTOP + (ZBASE - ZTOP) * t
        hw = ZHALF * (0.07 + 0.93 * t)
        dep = hw * 0.30
        # front rail + the receding top face of each terrace
        edges.append('<path d="M %.1f %.1f L %.1f %.1f" />' % (ZX - hw, y, ZX + hw, y))
        edges.append('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f" />'
                     % (ZX - hw, y, ZX - hw * 0.72, y - dep, ZX + hw * 0.72, y - dep))
        edges.append('<path d="M %.1f %.1f L %.1f %.1f" />' % (ZX + hw, y, ZX + hw * 0.72, y - dep))
        if i:
            faces.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f"/>'
                         % (ZX - hw, y, ZX + hw, y, ZX + prev_hw, prev_y, ZX - prev_hw, prev_y))
        prev_hw, prev_y = hw, y
    for k in range(9):   # the two raked slopes
        t = k / 8.0
        edges.append('<path d="M %.1f %.1f L %.1f %.1f"/>'
                     % (ZX - ZHALF * 0.07 - t * 6, ZTOP, ZX - ZHALF * (0.07 + 0.93 * 1.0) * (0.35 + t * 0.65), ZBASE))
        edges.append('<path d="M %.1f %.1f L %.1f %.1f"/>'
                     % (ZX + ZHALF * 0.07 + t * 6, ZTOP, ZX + ZHALF * (0.07 + 0.93 * 1.0) * (0.35 + t * 0.65), ZBASE))
    S.append('<g fill="%s" opacity="0.55">%s</g>' % (lit("#0a0620", light, 0.6), "".join(faces)))
    S.append('<g fill="none" stroke="%s" stroke-width="9" opacity="%.2f" filter="url(#big)">%s</g>' % (CYAN, glow(0.5, light), "".join(edges)))
    S.append('<g fill="none" stroke="%s" stroke-width="5" opacity="%.2f" filter="url(#med)">%s</g>' % (CYAN, glow(0.75, light), "".join(edges)))
    S.append('<g fill="none" stroke="%s" stroke-width="2.5" opacity="0.95">%s</g>' % (mix(CYAN, "#ffffff", 0.5), "".join(edges)))
    S.append('<circle cx="%.0f" cy="%.0f" r="14" fill="%s"/>' % (ZX, ZTOP - 6, ROSE))
    S.append('<circle cx="%.0f" cy="%.0f" r="70" fill="%s" opacity="0.8" filter="url(#med)"/>' % (ZX, ZTOP - 6, ROSE))

    # ---- ground plane and the grid running to the vanishing point
    S.append('<rect x="0" y="%d" width="%d" height="%d" fill="url(#ground)"/>' % (HZ, W, H - HZ))
    grid = []
    rows = 34
    for i in range(1, rows + 1):
        t = (i / float(rows)) ** 2.35
        grid.append('<line x1="0" y1="%.1f" x2="%d" y2="%.1f"/>' % (VPY + (H - VPY) * t, W, VPY + (H - VPY) * t))
    for j in range(-30, 31):
        grid.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%d"/>' % (VPX, VPY, VPX + j * (W * 0.115), H))
    S.append('<g stroke="%s" stroke-width="7" opacity="%.2f" filter="url(#big)">%s</g>' % (MAGENTA, glow(0.30, light), "".join(grid)))
    S.append('<g stroke="%s" stroke-width="3" opacity="%.2f" filter="url(#low)">%s</g>' % (MAGENTA, glow(0.55, light), "".join(grid)))
    S.append('<g stroke="%s" stroke-width="1.6" opacity="0.75">%s</g>' % (mix(MAGENTA, CYAN, 0.35), "".join(grid)))

    # ---- horizon haze sitting on the grid
    S.append('<rect x="0" y="%d" width="%d" height="150" fill="%s" opacity="%.2f" filter="url(#huge)"/>' % (HZ - 75, W, MAGENTA, glow(0.55, light)))
    for _ in range(11):
        S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#huge)"/>'
                 % (rnd.uniform(0, W), rnd.uniform(HZ - H * 0.14, HZ + H * 0.10), rnd.uniform(500, 1500),
                    rnd.uniform(40, 130), rnd.choice([MAGENTA, VIOLET, CYAN]), rnd.uniform(0.10, 0.26)))

    # ---- traffic threading toward the structure
    for _ in range(14):
        t = rnd.uniform(0.05, 0.9)
        y = VPY + (H - VPY) * (t ** 2.0)
        ln = 20 + t * 260
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="4" fill="%s" opacity="%.2f" filter="url(#low)"/>'
                 % (rnd.uniform(0, W), y, ln, 3 + t * 9, rnd.choice([CYAN, GOLD, "#ffffff"]), rnd.uniform(0.3, 0.85)))

    if rain:
        if DRAW_STREAKS: S.append('<g stroke="#dcecff" stroke-linecap="round">%s</g>' % "".join(
            '<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke-width="%.1f" opacity="%.2f"/>'
            % (x, y, x - ln * 0.16, y + ln, rnd.uniform(1.1, 3.2), rnd.uniform(0.05, 0.22))
            for x, y, ln in ((rnd.uniform(-250, W + 250), rnd.uniform(-250, H), rnd.uniform(60, 300)) for _ in range(1900))))
        for _ in range(8):
            S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="#1a1030" opacity="%.2f" filter="url(#huge)"/>'
                     % (rnd.uniform(0, W), rnd.uniform(0, HZ * 0.8), rnd.uniform(700, 1800), rnd.uniform(120, 300), rnd.uniform(0.18, 0.4)))
    else:
        for _ in range(240):
            S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="%s" opacity="%.2f"/>'
                     % (rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(1.0, 3.6),
                        rnd.choice([CYAN, MAGENTA, "#ffffff"]), rnd.uniform(0.10, 0.5)))

    S.append(ambient(light))
    S.append(vignette(strength=vig(0.72, light), inner=0.28))
    S.append('</svg>')
    return "".join(S)
