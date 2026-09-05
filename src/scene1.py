"""1 - Spinner Descent: rain-drowned megacity under an advertising sky."""
import random
from palette import *

NAME = "spinner-descent"
LIGHT = "night"
OUTDOOR = True
HORIZON = int(H * 0.735)
GLOWLINE = int(H * 0.60)
HAZE = "#b04a80"
NEON = [CYAN, MAGENTA, AMBER, GOLD, MINT, ROSE, BLUE, VIOLET]


def build(rain=True, light=LIGHT):
    rnd = random.Random(2019)
    S = [svg_open(), '<defs>']

    # The upper sky takes the full grade; the band just above the horizon takes
    # less, so the city's own glow still reads as the brightest thing in it.
    sky_stops = lit_stops((("0", "#02030a"), ("0.14", "#070b22"), ("0.32", "#141a4a"),
                           ("0.47", "#33206b")), light)
    sky_stops += lit_stops((("0.60", "#6b2472"), ("0.72", "#a83a6b"),
                            ("0.80", "#4a1c52")), light, k=0.55)
    sky_stops += lit_stops((("1", "#0a0a1e"),), light)
    S.append('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">%s</linearGradient>'
             % "".join('<stop offset="%s" stop-color="%s"/>' % st for st in sky_stops))
    haze = lit(HAZE, light, k=0.55)
    for n, c in (("gm", MAGENTA), ("gc", CYAN), ("ga", AMBER), ("gv", VIOLET), ("gr", ROSE)):
        S.append('<radialGradient id="%s"><stop offset="0" stop-color="%s" stop-opacity="0.95"/>'
                 '<stop offset="0.38" stop-color="%s" stop-opacity="0.34"/>'
                 '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (n, c, c, c))
    S.append('<linearGradient id="fog" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s" stop-opacity="0"/>'
             '<stop offset="0.55" stop-color="%s" stop-opacity="0.33"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0.88"/></linearGradient>'
             % (lit("#8e3a86", light, k=0.55), lit("#8e3a86", light, k=0.55), lit("#bd5684", light, k=0.55)))
    S.append('<linearGradient id="beam" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#e6f7ff" stop-opacity="%.2f"/>'
             '<stop offset="0.55" stop-color="#7fd4ff" stop-opacity="%.2f"/>'
             '<stop offset="1" stop-color="#7fd4ff" stop-opacity="0"/></linearGradient>'
             % (0.30 if rain else 0.17, 0.09 if rain else 0.05))
    # wet asphalt when it rains, dry and much darker when it does not
    if rain:
        gs = lit_stops((("0", "#a83a6b"), ("0.16", "#2a1240"), ("0.6", "#0a0c22"),
                        ("1", "#04060f")), light, k=0.7)
        S.append('<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">'
                 '<stop offset="0" stop-color="%s" stop-opacity="0.34"/>'
                 '<stop offset="0.16" stop-color="%s" stop-opacity="0.92"/>'
                 '<stop offset="0.6" stop-color="%s"/>'
                 '<stop offset="1" stop-color="%s"/></linearGradient>'
                 % tuple(c for _, c in gs))
    else:
        gs = lit_stops((("0", "#6b2452"), ("0.14", "#160c26"), ("0.5", "#080a1a"),
                        ("1", "#03050d")), light, k=0.7)
        S.append('<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">'
                 '<stop offset="0" stop-color="%s" stop-opacity="0.22"/>'
                 '<stop offset="0.14" stop-color="%s" stop-opacity="0.96"/>'
                 '<stop offset="0.5" stop-color="%s"/>'
                 '<stop offset="1" stop-color="%s"/></linearGradient>'
                 % tuple(c for _, c in gs))
    S.append('<filter id="bigblur" x="-45%" y="-45%" width="190%" height="190%"><feGaussianBlur stdDeviation="110"/></filter>')
    S.append('<filter id="medblur" x="-45%" y="-45%" width="190%" height="190%"><feGaussianBlur stdDeviation="30"/></filter>')
    S.append('<filter id="lowblur" x="-45%" y="-45%" width="190%" height="190%"><feGaussianBlur stdDeviation="8"/></filter>')
    S.append('<filter id="tinyblur" x="-45%" y="-45%" width="190%" height="190%"><feGaussianBlur stdDeviation="3"/></filter>')
    S.append('<filter id="softband" x="-30%" y="-200%" width="160%" height="500%"><feGaussianBlur stdDeviation="70"/></filter>')
    S.append('<filter id="smear" x="-25%" y="-10%" width="150%" height="125%"><feGaussianBlur stdDeviation="20 60"/></filter>')
    S.append('</defs>')

    S.append('<rect width="%d" height="%d" fill="url(#sky)"/>' % (W, H))

    # a clear night lets the starfield through
    if not rain:
        for _ in range(stars(420, light)):
            y = rnd.uniform(0, H * 0.46)
            S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="#dfeaff" opacity="%.2f"/>'
                     % (rnd.uniform(0, W), y, rnd.uniform(0.8, 2.9),
                        rnd.uniform(0.10, 0.75) * (1 - y / (H * 0.55))))

    for cx, cy, rx, ry, g, op in (
            (0.20 * W, GLOWLINE + 130, 1350, 780, "gm", 0.85),
            (0.63 * W, GLOWLINE + 60,  1500, 860, "gc", 0.62),
            (0.44 * W, GLOWLINE + 190, 900,  520, "ga", 0.55),
            (0.92 * W, GLOWLINE + 150, 1050, 600, "gv", 0.60),
            (0.05 * W, GLOWLINE + 200, 800,  480, "gr", 0.50)):
        S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="url(#%s)" opacity="%.2f"/>'
                 % (cx, cy, rx, ry, g, glow(op * (1.0 if rain else 0.82), light)))

    # ---- the off-world advertisement hanging in the smog
    ax, ay, aw, ah = int(0.055 * W), int(0.075 * H), int(0.30 * W), int(0.26 * H)
    S.append('<rect x="%d" y="%d" width="%d" height="%d" rx="26" fill="%s" opacity="%.2f" filter="url(#bigblur)"/>'
             % (ax, ay, aw, ah, MAGENTA, glow(0.60 if rain else 0.42, light)))
    S.append('<rect x="%d" y="%d" width="%d" height="%d" rx="14" fill="#1a0a30" opacity="0.88"/>' % (ax, ay, aw, ah))
    # broadcast content: a haloed disc over a horizon bar - an advert, not a UI card
    cx, cy = ax + aw * 0.5, ay + ah * 0.44
    S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="%s" opacity="0.30" filter="url(#medblur)"/>' % (cx, cy, ah * 0.30, ROSE))
    S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="none" stroke="%s" stroke-width="7" opacity="0.9"/>' % (cx, cy, ah * 0.24, GOLD))
    S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="%s" opacity="0.85"/>' % (cx, cy, ah * 0.12, ROSE))
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="7" rx="3" fill="%s" opacity="0.8"/>'
             % (ax + aw * 0.12, ay + ah * 0.70, aw * 0.76, CYAN))
    for i, frac in enumerate((0.20, 0.42, 0.30)):
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="6" fill="%s" opacity="%.2f"/>'
                 % (ax + aw * (0.5 - frac / 2), ay + ah * (0.78 + i * 0.055), aw * frac, ah * 0.030,
                    (MAGENTA, GOLD, CYAN)[i], 0.85 - i * 0.18))
    # scan bands across the screen face
    for i in range(28):
        S.append('<rect x="%d" y="%.0f" width="%d" height="3" fill="#000000" opacity="0.28"/>' % (ax, ay + i * ah / 28.0, aw))
    S.append('<rect x="%d" y="%d" width="%d" height="%d" rx="14" fill="none" stroke="%s" stroke-width="5" opacity="0.8"/>' % (ax, ay, aw, ah, MAGENTA))
    S.append('<g filter="url(#medblur)" opacity="0.45"><rect x="%d" y="%d" width="%d" height="%d" rx="14" fill="none" stroke="%s" stroke-width="16"/></g>' % (ax, ay, aw, ah, MAGENTA))

    S.append('<g filter="url(#medblur)">')
    for x0, spread, tilt, op in ((0.34 * W, 240, -620, 0.9), (0.66 * W, 300, 760, 0.7), (0.88 * W, 190, -380, 0.55)):
        S.append('<polygon points="%.0f,-300 %.0f,-300 %.0f,%d %.0f,%d" fill="url(#beam)" opacity="%.2f"/>'
                 % (x0 - 70, x0 + 70, x0 + tilt + spread, HORIZON, x0 + tilt - spread, HORIZON, op))
    S.append('</g>')

    signs = []

    def skyline(base, hmin, hmax, wmin, wmax, gmin, gmax, fill, op, windows, wsz, sc, collect):
        body, wins = [], []
        x = -300
        while x < W + 300:
            w = rnd.randint(wmin, wmax); h = rnd.randint(hmin, hmax); top = base - h
            body.append('<rect x="%d" y="%d" width="%d" height="%d"/>' % (x, top, w, base - top + 500))
            if rnd.random() < 0.5:
                iw = int(w * rnd.uniform(0.3, 0.7)); ih = rnd.randint(int(h * .05), int(h * .20) + 8)
                body.append('<rect x="%d" y="%d" width="%d" height="%d"/>' % (x + (w - iw) // 2, top - ih, iw, ih + 24))
                top -= ih
            if rnd.random() < 0.34:
                a = rnd.randint(70, 340)
                body.append('<rect x="%d" y="%d" width="%d" height="%d"/>' % (x + w // 2 - max(2, w // 44), top - a, max(4, w // 22), a + 20))
            if windows > 0:
                cols = max(1, w // (wsz * 4)); rows = max(1, h // (wsz * 6))
                for c in range(cols):
                    for r in range(rows):
                        if rnd.random() > windows: continue
                        wins.append('<rect x="%.0f" y="%.0f" width="%d" height="%d" fill="%s" opacity="%.2f"/>'
                                    % (x + 14 + c * (w - 28) / cols + rnd.uniform(0, wsz), base - h + 26 + r * (h - 46) / rows,
                                       wsz, int(wsz * 1.7), rnd.choice([GOLD, GOLD, AMBER, CYAN, MAGENTA, "#dfe9ff"]),
                                       rnd.uniform(0.28, 0.95)))
            if collect and rnd.random() < sc:
                col = rnd.choice(NEON)
                if rnd.random() < 0.6:
                    sw = max(16, int(w * rnd.uniform(0.09, 0.18))); sh = int(h * rnd.uniform(0.25, 0.55))
                    sx = x + int(w * rnd.uniform(0.08, 0.82)); sy = base - h + int(h * rnd.uniform(0.08, 0.32))
                else:
                    sw = int(w * rnd.uniform(0.45, 0.92)); sh = max(14, int(h * rnd.uniform(0.022, 0.05)))
                    sx = x + int((w - sw) * rnd.uniform(0.1, 0.9)); sy = base - h + int(h * rnd.uniform(0.15, 0.6))
                signs.append((sx, sy, sw, sh, col))
            x += w + rnd.randint(gmin, gmax)
        return '<g fill="%s" opacity="%.2f">%s</g>' % (fill, op, "".join(body)), "".join(wins)

    fogscale = 1.0 if rain else 0.62
    for base, hmin, hmax, wmin, wmax, gmin, gmax, fill, op, win, wsz, sc, fogop in [
        (HORIZON - 120, 180,  620,  50, 140, -20,  30, lit(mix(DEEP, HAZE, 0.62), light, 0.9), 0.90, 0.00,  5, 0.00, 0.55),
        (HORIZON - 60,  280,  900,  65, 175, -16,  44, lit(mix(DEEP, HAZE, 0.42), light, 0.7), 0.95, 0.03,  6, 0.06, 0.40),
        (HORIZON,       380, 1130,  90, 235, -12,  66, lit(mix(DEEP, HAZE, 0.24), light, 0.5), 1.00, 0.07,  8, 0.18, 0.26),
        (HORIZON + 70,  520, 1380, 125, 320,  14, 130, lit("#07091a", light, 0.3),             1.00, 0.10, 11, 0.34, 0.00),
    ]:
        body, wins = skyline(base, hmin, hmax, wmin, wmax, gmin, gmax, fill, op, win, wsz, sc, sc > 0)
        S.append(body)
        if wins:
            S.append('<g filter="url(#tinyblur)" opacity="0.8">%s</g>' % wins)
            S.append(wins)
        if fogop:
            S.append('<rect x="0" y="%d" width="%d" height="%d" fill="url(#fog)" opacity="%.2f"/>'
                     % (int(H * 0.20), W, HORIZON + 120 - int(H * 0.20), fogop * fogscale))

    sign_svg = "".join('<rect x="%d" y="%d" width="%d" height="%d" rx="%d" fill="%s"/>'
                       % (sx, sy, sw, sh, min(sw, sh) // 3, c) for sx, sy, sw, sh, c in signs)
    S.append('<g filter="url(#medblur)" opacity="%.2f">%s</g>' % (glow(0.9 if rain else 0.62, light), sign_svg))
    S.append('<g opacity="0.96">%s</g>' % sign_svg)

    for _ in range(18):
        x = rnd.uniform(0, W); y = rnd.uniform(H * 0.05, GLOWLINE - 160)
        ln = rnd.uniform(50, 240); col = rnd.choice([CYAN, GOLD, ROSE, "#e8f4ff"])
        S.append('<g opacity="%.2f"><rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="5" fill="%s" filter="url(#lowblur)"/>'
                 '<rect x="%.0f" y="%.0f" width="%.0f" height="4" fill="#ffffff" opacity="0.9"/></g>'
                 % (rnd.uniform(0.35, 0.9), x, y, ln, rnd.uniform(6, 13), col, x, y + 3, ln * 0.45))

    # ---- ground
    S.append('<rect x="0" y="%d" width="%d" height="%d" fill="url(#ground)"/>' % (HORIZON + 60, W, H - HORIZON - 60))
    S.append('<rect x="0" y="%d" width="%d" height="120" fill="%s" opacity="%.2f" filter="url(#softband)"/>'
             % (HORIZON + 10, W, haze, glow(0.30 if rain else 0.16, light)))
    if rain:
        refl = ['<rect x="%d" y="%d" width="%d" height="%d" fill="%s" opacity="%.2f"/>'
                % (sx + rnd.randint(-50, 50), HORIZON + 70, max(sw, 30), rnd.randint(340, 1000), c, rnd.uniform(0.12, 0.34))
                for sx, sy, sw, sh, c in signs]
        S.append('<g filter="url(#smear)">%s</g>' % "".join(refl))
    ripples = 260 if rain else 70
    for _ in range(ripples):
        y = rnd.uniform(HORIZON + 80, H)
        d = (y - HORIZON - 80) / max(1.0, (H - HORIZON - 80))
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="2" fill="%s" opacity="%.2f"/>'
                 % (rnd.uniform(0, W), y, rnd.uniform(40, 300) * (0.35 + d), 2 + d * 5,
                    rnd.choice([CYAN, MAGENTA, GOLD, ROSE, "#cfe6ff"]),
                    rnd.uniform(0.05, 0.30) * (1.0 if rain else 0.55)))

    # ---- weather
    if rain:
        drops = ['<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke-width="%.1f" opacity="%.2f"/>'
                 % (x, y, x - ln * 0.15, y + ln, rnd.uniform(1.0, 3.0), rnd.uniform(0.04, 0.22))
                 for x, y, ln in ((rnd.uniform(-250, W + 250), rnd.uniform(-250, H), rnd.uniform(50, 230)) for _ in range(2000))]
        if DRAW_STREAKS: S.append('<g stroke="#dcefff" stroke-linecap="round">%s</g>' % "".join(drops))
        near = ['<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke-width="%.1f" opacity="%.2f"/>'
                % (x, y, x - ln * 0.15, y + ln, rnd.uniform(4, 10), rnd.uniform(0.05, 0.16))
                for x, y, ln in ((rnd.uniform(-250, W + 250), rnd.uniform(-250, H), rnd.uniform(200, 620)) for _ in range(90))]
        if DRAW_STREAKS: S.append('<g stroke="#ffffff" stroke-linecap="round" filter="url(#lowblur)">%s</g>' % "".join(near))
    else:
        # dry night: drifting smog and ember motes instead of rain
        for _ in range(9):
            S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#bigblur)"/>'
                     % (rnd.uniform(0, W), rnd.uniform(H * 0.30, H * 0.80), rnd.uniform(500, 1200),
                        rnd.uniform(90, 220), lit(rnd.choice([HAZE, VIOLET, "#3a2a6b"]), light, 0.6), rnd.uniform(0.06, 0.16)))
        for _ in range(260):
            S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="%s" opacity="%.2f"/>'
                     % (rnd.uniform(0, W), rnd.uniform(H * 0.25, H), rnd.uniform(1.2, 4.2),
                        rnd.choice([GOLD, AMBER, "#ffe6c0"]), rnd.uniform(0.10, 0.5)))

    S.append(ambient(light))
    S.append(vignette(strength=vig(0.70, light), inner=0.30))
    S.append('</svg>')
    return "".join(S)
