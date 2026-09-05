"""8 - Bradbury Atrium: iron stairs under a rotting glass roof, at noon."""
import math, random
from palette import *

NAME = "bradbury-atrium"
LIGHT = "day"
OUTDOOR = False


def build(rain=True, light=LIGHT):
    rnd = random.Random(1893)
    ROOF = H * 0.170                    # underside of the glass
    FLOOR = H * 0.845                   # where the back wall meets the tile
    XB = W * 0.330                      # side wall meets back wall
    S = [svg_open(), '<defs>']

    # Grime is what keeps this noir. The light is enormous and the building is
    # rotting underneath it, so the palette is warm dust over cold iron.
    if rain:
        glass, air, iron = "#c9cfd8", "#5d6478", "#14121a"
    else:
        glass, air, iron = "#f2e6cc", "#7b7a86", "#17131b"
    glass = lit(glass, light, 0.22)
    air = lit(air, light, 0.34)
    iron = lit(iron, light, 0.10)

    S.append('<linearGradient id="vol" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="0.42" stop-color="%s"/>'
             '<stop offset="1" stop-color="%s"/></linearGradient>'
             % (lit("#b8ac97", light, 0.35), air, lit("#0e0b14", light, 0.18)))
    S.append('<linearGradient id="roofglass" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#ffffff" stop-opacity="0.96"/>'
             '<stop offset="0.55" stop-color="%s" stop-opacity="0.82"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0.30"/></linearGradient>' % (glass, glass))
    S.append('<linearGradient id="shaft" x1="0.2" y1="0" x2="0.8" y2="1">'
             '<stop offset="0" stop-color="#fffaf0" stop-opacity="0.46"/>'
             '<stop offset="0.45" stop-color="%s" stop-opacity="0.30"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient>' % (glass, glass))
    S.append('<linearGradient id="tile" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
             % (lit("#3a3340", light, 0.30), lit("#0c0a11", light, 0.15)))
    S.append('<filter id="huge" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="150"/></filter>')
    S.append('<filter id="big" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="55"/></filter>')
    S.append('<filter id="med" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="17"/></filter>')
    S.append('<filter id="low" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="5"/></filter>')
    S.append('<filter id="smear" x="-30%" y="-10%" width="160%" height="130%"><feGaussianBlur stdDeviation="18 60"/></filter>')
    S.append('</defs>')
    S.append('<rect width="%d" height="%d" fill="url(#vol)"/>' % (W, H))

    # One-point perspective. u runs 0 at the frame edge to 1 at the back wall;
    # v runs 0 at the ceiling to 1 at the floor of whichever wall we are on.
    def ytop(u):
        return u * ROOF

    def ybot(u):
        return H + u * (FLOOR - H)

    def why(u, v):
        return ytop(u) + v * (ybot(u) - ytop(u))

    def ex(u, side):
        return (u * XB) if side < 0 else (W - u * XB)

    # ---- back wall: brick, with a tall window letting the day in
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s"/>'
             % (XB, ROOF, W - 2 * XB, FLOOR - ROOF, lit("#2a2229", light, 0.24)))
    for i in range(46):
        yy = ROOF + i * (FLOOR - ROOF) / 46.0
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="2" fill="#000000" opacity="0.10"/>'
                 % (XB, yy, W - 2 * XB))
    # water staining down the brick, which is the whole point of the building
    for _ in range(22):
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s" opacity="%.2f" filter="url(#med)"/>'
                 % (rnd.uniform(XB, W - XB), ROOF, rnd.uniform(20, 130), rnd.uniform(200, FLOOR - ROOF),
                    lit("#2e2118", light, 0.3), rnd.uniform(0.10, 0.34)))

    # ---- the glass roof, blown out
    S.append('<rect x="0" y="0" width="%d" height="%.0f" fill="url(#roofglass)"/>' % (W, ROOF))
    ribs = []
    for i in range(19):
        rx = i * W / 18.0
        ribs.append('<path d="M %.0f 0 L %.0f %.0f"/>' % (rx, XB + (rx / W) * (W - 2 * XB), ROOF))
    for i in range(5):
        ry = i * ROOF / 4.0
        ribs.append('<path d="M 0 %.0f L %d %.0f"/>' % (ry, W, ry))
    S.append('<g stroke="%s" stroke-width="7" fill="none" opacity="0.85">%s</g>' % (iron, "".join(ribs)))
    # broken and grimed panes
    for _ in range(30):
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s" opacity="%.2f"/>'
                 % (rnd.uniform(0, W), rnd.uniform(0, ROOF), rnd.uniform(40, 190), rnd.uniform(20, 70),
                    rnd.choice([iron, "#8a7c62"]), rnd.uniform(0.10, 0.42)))
    S.append('<rect x="0" y="%.0f" width="%d" height="%.0f" fill="%s" opacity="0.7" filter="url(#big)"/>'
             % (ROOF - 60, W, 150, glass))

    # ---- the side walls, and three storeys of cast-iron balustrade on each
    for side in (-1, 1):
        S.append('<polygon points="%.0f,%.0f %.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="%s" opacity="0.92"/>'
                 % (ex(0, side), 0, ex(1, side), ROOF, ex(1, side), FLOOR, ex(0, side), H,
                    lit("#161220", light, 0.16)))
        # arched openings along each storey read as the rooms behind the rail
        for v in (0.30, 0.52, 0.74):
            n = 9
            for i in range(n):
                u0 = 1 - (1 - i / float(n)) ** 1.85
                u1 = 1 - (1 - (i + 0.62) / float(n)) ** 1.85
                S.append('<polygon points="%.0f,%.0f %.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="#0b0810" opacity="0.55"/>'
                         % (ex(u0, side), why(u0, v - 0.14), ex(u1, side), why(u1, v - 0.14),
                            ex(u1, side), why(u1, v), ex(u0, side), why(u0, v)))
            # a few rooms are lit from inside, which is what stops the tiers
            # reading as one flat repeated stamp
            for i in range(n):
                if rnd.random() > 0.22:
                    continue
                u0 = 1 - (1 - i / float(n)) ** 1.85
                u1 = 1 - (1 - (i + 0.62) / float(n)) ** 1.85
                S.append('<polygon points="%.0f,%.0f %.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="%s" opacity="%.2f" filter="url(#low)"/>'
                         % (ex(u0, side), why(u0, v - 0.14), ex(u1, side), why(u1, v - 0.14),
                            ex(u1, side), why(u1, v), ex(u0, side), why(u0, v),
                            rnd.choice([GOLD, AMBER, "#e8d8a8"]), rnd.uniform(0.10, 0.34)))
        for v in (0.32, 0.54, 0.76):
            # the rail itself
            S.append('<polygon points="%.0f,%.0f %.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="%s"/>'
                     % (ex(0, side), why(0, v), ex(1, side), why(1, v),
                        ex(1, side), why(1, v) + 9, ex(0, side), why(0, v) + 26, iron))
            # balusters, compressing toward the back wall
            n = 34
            for i in range(n):
                u = 1 - (1 - i / float(n)) ** 1.85
                bx = ex(u, side)
                by = why(u, v)
                bh = (why(u, v + 0.075) - by)
                bw = max(2.0, 13 * (1 - u * 0.80))
                S.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>' % (bx, by, bw, bh, iron))
                S.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (bx + bw / 2, by + bh * 0.45, bw * 0.85, iron))
            # the floor slab under the rail
            S.append('<polygon points="%.0f,%.0f %.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="%s" opacity="0.9"/>'
                     % (ex(0, side), why(0, v + 0.085), ex(1, side), why(1, v + 0.085),
                        ex(1, side), why(1, v + 0.105), ex(0, side), why(0, v + 0.135), lit("#0a0810", light, 0.14)))

    # ---- the open-cage lift, dead centre, stopped between floors
    lx, lw = W * 0.5, W * 0.070
    ltop, lbot = ROOF + H * 0.045, FLOOR - H * 0.010
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="none" stroke="%s" stroke-width="9" opacity="0.9"/>'
             % (lx - lw, ltop, lw * 2, lbot - ltop, iron))
    for i in range(16):
        yy = ltop + i * (lbot - ltop) / 16.0
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="4" fill="%s" opacity="0.75"/>' % (lx - lw, yy, lw * 2, iron))
    cy0 = ltop + (lbot - ltop) * 0.42
    ch = H * 0.115
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s" opacity="0.96"/>'
             % (lx - lw * 0.86, cy0, lw * 1.72, ch, iron))
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s" opacity="0.34" filter="url(#low)"/>'
             % (lx - lw * 0.62, cy0 + ch * 0.16, lw * 1.24, ch * 0.44, GOLD))
    S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#big)"/>'
             % (lx, cy0 + ch * 0.38, lw * 1.6, ch * 0.7, GOLD, glow(0.30, light)))
    for i in range(9):
        S.append('<rect x="%.0f" y="%.0f" width="3" height="%.0f" fill="%s"/>'
                 % (lx - lw * 0.62 + i * lw * 1.24 / 8.0, cy0 + ch * 0.16, ch * 0.44, iron))

    # ---- shafts falling out of the roof, over everything they cross. They are
    # drawn late on purpose: light that goes behind the architecture lights
    # nothing, and the shafts are the only reason this room reads as noon.
    SHAFTS = ((0.13, 0.085, 0.34), (0.37, 0.050, 0.18), (0.66, 0.095, -0.15), (0.89, 0.055, -0.30))
    for sx0, sw0, lean in SHAFTS:
        x0, w0 = W * sx0, W * sw0
        pts = (x0, ROOF, x0 + w0, ROOF,
               x0 + w0 + lean * W * 0.34, H, x0 + lean * W * 0.34 - w0 * 0.5, H)
        S.append('<polygon points="%.0f,%.0f %.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="url(#shaft)" filter="url(#big)" opacity="%.2f"/>'
                 % (pts + (glow(0.50, light),)))
        S.append('<polygon points="%.0f,%.0f %.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="url(#shaft)" filter="url(#med)" opacity="%.2f"/>'
                 % (pts + (glow(0.40, light),)))

    # ---- the floor, and the pool of light standing on it
    S.append('<rect x="0" y="%.0f" width="%d" height="%.0f" fill="url(#tile)"/>' % (FLOOR, W, H - FLOOR))
    for i in range(1, 15):
        t = (i / 14.0) ** 2.1
        S.append('<line x1="0" y1="%.1f" x2="%d" y2="%.1f" stroke="#000000" stroke-width="2" opacity="0.22"/>'
                 % (FLOOR + (H - FLOOR) * t, W, FLOOR + (H - FLOOR) * t))
    for j in range(-14, 15):
        S.append('<line x1="%.1f" y1="%.0f" x2="%.1f" y2="%d" stroke="#000000" stroke-width="2" opacity="0.18"/>'
                 % (W * 0.5 + j * W * 0.030, FLOOR, W * 0.5 + j * W * 0.145, H))
    for sx0, sw0, lean in SHAFTS:
        S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="#fff6e2" opacity="%.2f" filter="url(#big)"/>'
                 % (W * sx0 + lean * W * 0.30, FLOOR + (H - FLOOR) * 0.34, W * (sw0 + 0.055),
                    (H - FLOOR) * 0.34, glow(0.26, light)))

    # ---- dust, which is the only thing that makes a shaft visible
    for _ in range(700):
        x = rnd.uniform(0, W)
        y = rnd.uniform(ROOF * 0.4, H)
        S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="#fff4dc" opacity="%.2f"/>'
                 % (x, y, rnd.uniform(0.9, 3.6), rnd.uniform(0.06, 0.42)))

    if rain:
        # weather stays outside: it runs down the glass and drips through
        if DRAW_STREAKS:
            S.append('<g stroke="#cfd8e6" stroke-linecap="round">%s</g>' % "".join(
                '<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke-width="%.1f" opacity="%.2f"/>'
                % (x, y, x - ln * 0.10, y + ln, rnd.uniform(1.0, 2.8), rnd.uniform(0.06, 0.26))
                for x, y, ln in ((rnd.uniform(0, W), rnd.uniform(-60, ROOF), rnd.uniform(30, 120))
                                 for _ in range(700))))
            S.append('<g stroke="#e8eef7" stroke-linecap="round">%s</g>' % "".join(
                '<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke-width="%.1f" opacity="%.2f"/>'
                % (x, y, x - ln * 0.06, y + ln, rnd.uniform(1.4, 3.4), rnd.uniform(0.05, 0.18))
                for x, y, ln in ((rnd.uniform(0, W), rnd.uniform(ROOF, H), rnd.uniform(120, 420))
                                 for _ in range(240))))
        for _ in range(14):
            S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#smear)"/>'
                     % (rnd.uniform(0, W), rnd.uniform(FLOOR, H), rnd.uniform(90, 330), rnd.uniform(10, 34),
                        glass, rnd.uniform(0.10, 0.34)))
    else:
        for _ in range(9):
            S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#huge)"/>'
                     % (rnd.uniform(0, W), rnd.uniform(ROOF, H * 0.85), rnd.uniform(400, 1100),
                        rnd.uniform(70, 190), glass, rnd.uniform(0.06, 0.16)))

    S.append(ambient(light, haze="#cdbfa4", op=0.045))
    S.append(vignette(strength=vig(0.86, light), inner=0.26, color="#0b0812"))
    S.append('</svg>')
    return "".join(S)
