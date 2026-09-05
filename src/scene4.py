"""4 - Neon Signage: an alley of light seen through wet glass."""
import random
from palette import *

NAME = "neon-signage"
LIGHT = "night"
OUTDOOR = True
# weighted so the frame reads cyan/magenta first, amber as the accent
NEON = [CYAN, CYAN, CYAN, BLUE, MAGENTA, MAGENTA, ROSE, VIOLET, AMBER, GOLD, MINT]


def build(rain=True, light=LIGHT):
    rnd = random.Random(77)
    FLOOR = int(H * 0.855)
    S = [svg_open(), '<defs>']
    S.append('<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="0.42" stop-color="%s"/>'
             '<stop offset="0.74" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
             % tuple(c for _, c in lit_stops((("0", "#04061a"), ("0.42", "#0a0d2e"),
                                              ("0.74", "#170e36"), ("1", "#04060f")), light)))
    S.append('<linearGradient id="floor" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s" stop-opacity="0.85"/>'
             '<stop offset="0.5" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
             % tuple(c for _, c in lit_stops((("0", "#1c1240"), ("0.5", "#0a0a1e"),
                                              ("1", "#03050e")), light, k=0.75)))
    S.append('<filter id="huge" x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="170"/></filter>')
    S.append('<filter id="bokeh" x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="90"/></filter>')
    S.append('<filter id="big" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="55"/></filter>')
    S.append('<filter id="med" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="18"/></filter>')
    S.append('<filter id="far" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="9"/></filter>')
    S.append('<filter id="smear" x="-30%" y="-10%" width="160%" height="130%"><feGaussianBlur stdDeviation="24 80"/></filter>')
    S.append('<filter id="softedge" x="-30%" y="-300%" width="160%" height="700%"><feGaussianBlur stdDeviation="60"/></filter>')
    S.append('</defs>')
    S.append('<rect width="%d" height="%d" fill="url(#bg)"/>' % (W, H))

    # ---- distant light haze
    for _ in range(46):
        S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="%s" opacity="%.2f" filter="url(#huge)"/>'
                 % (rnd.uniform(0, W), rnd.uniform(0, FLOOR), rnd.uniform(150, 520),
                    rnd.choice(NEON), glow(rnd.uniform(0.10, 0.30) * (1.0 if rain else 0.78), light)))

    # ---- facades: the signs need walls to hang on
    fac = []
    facade = lit("#070a1c", light, 0.5)
    x = -200
    while x < W + 200:
        w = rnd.uniform(180, 520)
        top = rnd.uniform(-100, H * 0.30)
        fac.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s" opacity="%.2f"/>'
                   % (x, top, w, FLOOR - top + 40, facade, rnd.uniform(0.55, 0.9)))
        x += w * rnd.uniform(0.55, 0.95)
    S.append("".join(fac))
    S.append('<rect x="0" y="0" width="%d" height="%d" fill="%s" opacity="0.35"/>' % (W, FLOOR, lit("#0d0a2a", light, 0.8)))

    def glyphs(x, y, w, h, col, op):
        out, n = [], rnd.randint(2, 4)
        for _ in range(n):
            if rnd.random() < 0.55:
                out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" opacity="%.2f"/>'
                           % (x + w * rnd.uniform(0.08, 0.35), y + h * rnd.uniform(0.10, 0.80),
                              w * rnd.uniform(0.30, 0.84), max(2.5, h * 0.075), col, op))
            else:
                out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" opacity="%.2f"/>'
                           % (x + w * rnd.uniform(0.15, 0.72), y + h * rnd.uniform(0.08, 0.30),
                              max(2.5, w * 0.09), h * rnd.uniform(0.35, 0.78), col, op))
        return "".join(out)

    def sign(x, y, w, h, col, alpha):
        sw = max(3.0, w * 0.085)
        parts = ['<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="%.0f" fill="none" stroke="%s" '
                 'stroke-width="%.1f" opacity="%.2f"/>' % (x, y, w, h, w * 0.20, col, sw, alpha),
                 '<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="%.0f" fill="none" stroke="%s" '
                 'stroke-width="%.1f" opacity="%.2f"/>' % (x, y, w, h, w * 0.20, mix(col, "#ffffff", 0.62),
                                                           sw * 0.38, alpha * 0.9)]
        cells = max(2, int(h / (w * 1.3)))
        for c in range(cells):
            cy = y + h * 0.06 + c * (h * 0.88) / cells
            parts.append(glyphs(x + w * 0.16, cy, w * 0.68, (h * 0.88) / cells * 0.82, col, alpha * rnd.uniform(0.6, 1.0)))
        if rnd.random() < 0.35:
            mw = w * rnd.uniform(1.6, 3.0); mh = max(8.0, w * 0.26)
            parts.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="%.0f" fill="%s" opacity="%.2f"/>'
                         % (x - mw * 0.28, y + h * rnd.uniform(0.2, 0.8), mw, mh, mh * 0.5, rnd.choice(NEON), alpha * 0.9))
        return "".join(parts)

    # ---- FAR plane: small, dim, softened
    farsigns = "".join(sign(rnd.uniform(0, W - 40), rnd.uniform(H * 0.02, H * 0.55),
                            rnd.uniform(16, 38), rnd.uniform(110, 300), rnd.choice(NEON), 0.5) for _ in range(40))
    S.append('<g filter="url(#far)" opacity="%.2f">%s</g>' % (glow(0.55, light), farsigns))

    # ---- MID plane: the readable middle distance
    mid = "".join(sign(rnd.uniform(-40, W - 60), rnd.uniform(H * 0.03, H * 0.52),
                       rnd.uniform(52, 105), rnd.uniform(300, 780), rnd.choice(NEON), 0.85) for _ in range(20))
    S.append('<g filter="url(#med)" opacity="%.2f">%s</g>' % (glow(0.9, light), mid))
    S.append('<g opacity="0.95">%s</g>' % mid)

    # ---- NEAR plane: big enough to run off the frame
    near = "".join(sign(x, y, w, h, rnd.choice(NEON), 1.0) for x, y, w, h in (
        (rnd.uniform(-140, W - 120), rnd.uniform(-H * 0.06, H * 0.36),
         rnd.uniform(150, 300), rnd.uniform(700, 1700)) for _ in range(8)))
    S.append('<g filter="url(#big)" opacity="%.2f">%s</g>' % (glow(0.80 if rain else 0.55, light), near))
    S.append('<g filter="url(#med)" opacity="0.95">%s</g>' % near)
    S.append('<g opacity="0.98">%s</g>' % near)

    # ---- FOREGROUND bokeh signs, thrown right out of focus
    fg = "".join(sign(x, y, w, h, rnd.choice(NEON), 1.0) for x, y, w, h in (
        (rnd.choice([-260.0, W - 200.0, W * 0.5]) + rnd.uniform(-160, 160), rnd.uniform(-H * 0.25, H * 0.15),
         rnd.uniform(320, 560), rnd.uniform(1400, 2600)) for _ in range(3)))
    S.append('<g filter="url(#bokeh)" opacity="%.2f">%s</g>' % (glow(0.55, light), fg))

    # ---- the street
    S.append('<rect x="0" y="%d" width="%d" height="%d" fill="url(#floor)"/>' % (FLOOR, W, H - FLOOR))
    S.append('<rect x="0" y="%d" width="%d" height="60" fill="%s" opacity="%.2f" filter="url(#softedge)"/>' % (FLOOR - 30, W, VIOLET, glow(0.35, light)))
    refl = ['<rect x="%.0f" y="%d" width="%.0f" height="%.0f" fill="%s" opacity="%.2f"/>'
            % (rnd.uniform(0, W), FLOOR, rnd.uniform(40, 220), rnd.uniform(180, 560),
               rnd.choice(NEON), rnd.uniform(0.14, 0.45) * (1.0 if rain else 0.42)) for _ in range(60)]
    S.append('<g filter="url(#smear)">%s</g>' % "".join(refl))
    for _ in range(240 if rain else 70):
        y = rnd.uniform(FLOOR, H); d = (y - FLOOR) / max(1.0, H - FLOOR)
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="2" fill="%s" opacity="%.2f"/>'
                 % (rnd.uniform(0, W), y, rnd.uniform(50, 340) * (0.35 + d), 2 + d * 6,
                    rnd.choice(NEON + ["#dfeaff"]), rnd.uniform(0.06, 0.32)))

    # ---- weather
    if rain:
        if DRAW_STREAKS: S.append('<g stroke="#e2f1ff" stroke-linecap="round">%s</g>' % "".join(
            '<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke-width="%.1f" opacity="%.2f"/>'
            % (x, y, x - ln * 0.14, y + ln, rnd.uniform(1.2, 3.4), rnd.uniform(0.05, 0.22))
            for x, y, ln in ((rnd.uniform(-250, W + 250), rnd.uniform(-250, H), rnd.uniform(70, 330)) for _ in range(2000))))
        # fewer, larger beads - each one lensing the sign behind it
        for _ in range(48):
            r = rnd.uniform(22, 78); x, y = rnd.uniform(0, W), rnd.uniform(0, H)
            col = rnd.choice(NEON)
            S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="%s" opacity="%.2f"/>' % (x, y, r, col, rnd.uniform(0.06, 0.18)))
            S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="none" stroke="#ffffff" stroke-width="%.1f" opacity="%.2f"/>'
                     % (x, y, r * 0.90, r * 0.07, rnd.uniform(0.10, 0.26)))
            S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="#ffffff" opacity="%.2f"/>' % (x - r * 0.35, y - r * 0.35, r * 0.16, rnd.uniform(0.15, 0.40)))
        for _ in range(26):   # runnels tracking down the glass
            x = rnd.uniform(0, W); y = rnd.uniform(0, H * 0.7)
            S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="%.0f" fill="#cfe6ff" opacity="%.2f" filter="url(#far)"/>'
                     % (x, y, rnd.uniform(8, 22), rnd.uniform(200, 900), 10, rnd.uniform(0.04, 0.12)))
    else:
        for _ in range(12):
            S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#huge)"/>'
                     % (rnd.uniform(0, W), rnd.uniform(H * 0.2, H * 0.9), rnd.uniform(500, 1400),
                        rnd.uniform(80, 220), rnd.choice([VIOLET, BLUE, MAGENTA]), rnd.uniform(0.06, 0.15)))
        for _ in range(300):
            S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="%s" opacity="%.2f"/>'
                     % (rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(1.2, 4.0), rnd.choice(NEON), rnd.uniform(0.10, 0.48)))

    S.append(ambient(light))
    S.append(vignette(strength=vig(0.78, light), inner=0.24))
    S.append('</svg>')
    return "".join(S)
