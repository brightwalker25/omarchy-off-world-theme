"""7 - Sea Wall Flares: the refinery plain at last light."""
import math, random
from palette import *

NAME = "sea-wall"
LIGHT = "dusk"
OUTDOOR = True


def build(rain=True, light=LIGHT):
    rnd = random.Random(2027)
    HZ = int(H * 0.610)                 # plain meets sky
    WALL = int(H * 0.775)               # top of the concrete barrier
    S = [svg_open(), '<defs>']

    if rain:
        stops = (("0", "#080a1c"), ("0.26", "#170f2e"), ("0.48", "#3d1636"),
                 ("0.68", "#78292c"), ("0.86", "#b8541f"), ("1", "#4e1d10"))
        flame, smog, water = "#ffb44a", "#3a1a2e", "#150f22"
    else:
        stops = (("0", "#05060f"), ("0.24", "#120e30"), ("0.46", "#3a1240"),
                 ("0.66", "#8c2c2a"), ("0.84", "#e0761c"), ("1", "#6d2810"))
        flame, smog, water = "#ffd06a", "#341629", "#100d1b"

    # The burn band above the horizon keeps most of its heat. It is the last
    # light in the sky, and grading it away would leave the flares with nothing
    # to sit against.
    stops = (lit_stops(stops[:3], light)
             + lit_stops(stops[3:5], light, k=0.30)
             + lit_stops(stops[5:], light, k=0.70))
    S.append('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">%s</linearGradient>'
             % "".join('<stop offset="%s" stop-color="%s"/>' % st for st in stops))

    ws = lit_stops((("0", "#5a2a1c"), ("0.30", water), ("1", "#04050c")), light, k=0.75)
    S.append('<linearGradient id="water" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s" stop-opacity="0.75"/>'
             '<stop offset="0.30" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
             % tuple(c for _, c in ws))
    S.append('<linearGradient id="plume" x1="0" y1="1" x2="0.25" y2="0">'
             '<stop offset="0" stop-color="#fff6dc" stop-opacity="0.95"/>'
             '<stop offset="0.28" stop-color="%s" stop-opacity="0.85"/>'
             '<stop offset="0.66" stop-color="%s" stop-opacity="0.40"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient>' % (flame, AMBER, ROSE))
    S.append('<radialGradient id="flareglow"><stop offset="0" stop-color="%s" stop-opacity="0.85"/>'
             '<stop offset="0.42" stop-color="%s" stop-opacity="0.26"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (flame, AMBER, AMBER))
    S.append('<linearGradient id="smogveil" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s" stop-opacity="0"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0.80"/></linearGradient>'
             % (lit(smog, light, 0.6), lit(smog, light, 0.6)))
    S.append('<filter id="huge" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="150"/></filter>')
    S.append('<filter id="big" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="52"/></filter>')
    S.append('<filter id="med" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="17"/></filter>')
    S.append('<filter id="low" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="5"/></filter>')
    S.append('<filter id="smear" x="-30%" y="-10%" width="160%" height="130%"><feGaussianBlur stdDeviation="22 78"/></filter>')
    S.append('</defs>')
    S.append('<rect width="%d" height="%d" fill="url(#sky)"/>' % (W, H))

    for _ in range(stars(420, light)):
        y = rnd.uniform(0, HZ * 0.55)
        S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="#e2ecff" opacity="%.2f"/>'
                 % (rnd.uniform(0, W), y, rnd.uniform(0.8, 2.6),
                    rnd.uniform(0.06, 0.6) * (1 - y / (HZ * 0.7))))

    # ---- smog strata, drawn before the plant so the plant cuts through them
    for _ in range(18):
        S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#huge)"/>'
                 % (rnd.uniform(0, W), rnd.uniform(HZ - H * 0.30, HZ + H * 0.02),
                    rnd.uniform(700, 2100), rnd.uniform(30, 120),
                    rnd.choice([smog, VIOLET, "#5a2038"]), rnd.uniform(0.10, 0.30)))

    # ---- the plant: tanks, stacks and pipe racks, in three depths
    def plant(base, scale, fill, op, lattice_odds):
        out = []
        x = -220.0
        while x < W + 220:
            kind = rnd.random()
            if kind < 0.34:                       # storage tank
                w = rnd.uniform(120, 320) * scale
                h = rnd.uniform(40, 90) * scale
                out.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f"/>' % (x, base - h, w, h + 400))
                out.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f"/>' % (x + w / 2, base - h, w / 2, h * 0.22))
                x += w * rnd.uniform(1.05, 1.4)
            elif kind < 0.62:                     # stack
                w = rnd.uniform(14, 34) * scale
                h = rnd.uniform(150, 420) * scale
                out.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f"/>' % (x, base - h, w, h + 400))
                if rnd.random() < 0.5:
                    out.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f"/>'
                               % (x - w * 0.5, base - h - w * 0.6, w * 2, w * 0.7))
                x += w * rnd.uniform(2.4, 7.0)
            elif kind < lattice_odds:             # lattice tower
                w = rnd.uniform(40, 95) * scale
                h = rnd.uniform(180, 430) * scale
                for leg in (0.0, 1.0):
                    out.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f"/>'
                               % (x + leg * w, base - h, max(3.0, 5 * scale), h + 400))
                rungs = max(3, int(h / (34 * scale)))
                for r in range(rungs):
                    yy = base - h + r * h / rungs
                    out.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f"/>'
                               % (x, yy, w, max(2.0, 3 * scale)))
                x += w * rnd.uniform(1.4, 2.6)
            else:                                 # pipe rack / low shed
                w = rnd.uniform(180, 460) * scale
                h = rnd.uniform(18, 46) * scale
                out.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f"/>' % (x, base - h, w, h + 400))
                x += w * rnd.uniform(1.0, 1.3)
        return '<g fill="%s" opacity="%.2f">%s</g>' % (fill, op, "".join(out))

    S.append(plant(HZ - H * 0.020, 0.95, lit("#2a1428", light, 0.9), 0.85, 0.86))
    # The veil has to die away below the horizon rather than stop on it, or it
    # lays a grey bar straight across the plant.
    S.append('<rect x="0" y="%d" width="%d" height="%d" fill="url(#smogveil)" opacity="0.34"/>'
             % (int(H * 0.26), W, HZ - int(H * 0.26)))
    S.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s" opacity="0.18" filter="url(#huge)"/>'
             % (HZ - 90, W, 150, lit("#3a1a2e", light, 0.6)))
    S.append(plant(HZ + H * 0.016, 1.55, lit("#150a1c", light, 0.5), 0.96, 0.84))

    # ---- flare stacks: the only real light left out here
    for fx, fh, fs, tilt in ((0.175, 0.300, 1.00, -0.16), (0.395, 0.215, 0.72, 0.10),
                             (0.655, 0.345, 1.18, -0.07), (0.875, 0.245, 0.86, 0.20)):
        sx = W * fx
        top = HZ - H * fh
        # The stack: a braced column with a ladder up one side, so it reads as
        # plant rather than as a lamp post holding the flame up.
        col = lit("#120817", light, 0.4)
        sw = 19 * fs
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s"/>'
                 % (sx - sw, top, sw * 2, HZ - top + 300, col))
        rungs = int((HZ - top) / (46 * fs))
        S.append('<g fill="%s">%s</g>' % (col, "".join(
            '<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f"/>'
            % (sx + sw, top + r * (HZ - top) / max(1, rungs), 15 * fs, 4 * fs)
            for r in range(max(1, rungs)))))
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s"/>'
                 % (sx + sw, top, 4 * fs, HZ - top, col))
        # flare tip: a wider crown the flame actually leaves from
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s"/>'
                 % (sx - sw * 1.7, top - 16 * fs, sw * 3.4, 20 * fs, col))

        # the plume: a torn tongue, tall and narrow, raked over by the wind
        ph = H * 0.235 * fs
        pw = W * 0.0135 * fs
        tip = top - 16 * fs
        def edge(sign):
            pts = []
            for t in (0.0, 0.12, 0.26, 0.42, 0.58, 0.74, 0.88, 1.0):
                # the tongue swells just off the nozzle, then tears into nothing
                swell = math.sin(min(1.0, t * 1.55) * math.pi * 0.62) * 1.35 + 0.25
                spread = pw * swell * (1.0 - t * 0.55) * rnd.uniform(0.55, 1.5)
                lean = tilt * ph * (t ** 1.55) * 2.1
                pts.append((sx + lean + sign * spread, tip - ph * t))
            return pts
        pts = edge(1.0) + list(reversed(edge(-1.0)))
        poly = "".join("%.1f,%.1f " % pt for pt in pts)
        S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="url(#flareglow)" opacity="%.2f"/>'
                 % (sx + tilt * ph * 0.5, tip - ph * 0.30, ph * 0.75, ph * 0.62, glow(0.70, light)))
        S.append('<polygon points="%s" fill="url(#plume)" filter="url(#big)" opacity="%.2f"/>' % (poly, glow(0.55, light)))
        S.append('<polygon points="%s" fill="url(#plume)" filter="url(#med)" opacity="%.2f"/>' % (poly, glow(0.85, light)))
        S.append('<polygon points="%s" fill="url(#plume)" filter="url(#low)" opacity="%.2f"/>' % (poly, glow(0.55, light)))
        # the incandescent root sitting on the nozzle
        S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="#fff8e4" opacity="%.2f" filter="url(#low)"/>'
                 % (sx + tilt * 8 * fs, tip - 13 * fs, pw * 0.85, 17 * fs, glow(0.95, light)))
        # sparks torn off the top of the plume
        for _ in range(int(34 * fs)):
            t = rnd.uniform(0.55, 1.7)
            S.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="%.2f"/>'
                     % (sx + tilt * ph * (t ** 1.55) * 2.1 + rnd.uniform(-pw, pw) * 3.4, tip - ph * t,
                        rnd.uniform(1.4, 4.6), rnd.choice([flame, GOLD, "#fff0c8"]), rnd.uniform(0.12, 0.62)))

    # ---- spinner traffic threading the smog
    for _ in range(13):
        x = rnd.uniform(0, W); y = rnd.uniform(H * 0.08, HZ - H * 0.16); ln = rnd.uniform(40, 190)
        S.append('<g opacity="%.2f"><rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="4" fill="%s" filter="url(#low)"/>'
                 '<rect x="%.0f" y="%.0f" width="%.0f" height="3" fill="#ffffff" opacity="0.85"/></g>'
                 % (rnd.uniform(0.30, 0.85), x, y, ln, rnd.uniform(5, 11),
                    rnd.choice([CYAN, GOLD, ROSE]), x, y + 3, ln * 0.42))

    # ---- the sea wall itself, and the channel of water in front of it
    S.append('<linearGradient id="wallface" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
             % (lit("#160b1c", light, 0.35), lit("#040309", light, 0.15)))
    S.append('<rect x="0" y="%d" width="%d" height="%d" fill="url(#wallface)"/>' % (HZ, W, WALL - HZ))
    # form lines down the poured bays, and rust staining under each one
    for i in range(int(W / 168) + 1):
        bx = i * 168
        S.append('<rect x="%d" y="%d" width="3" height="%d" fill="#000000" opacity="0.40"/>' % (bx, HZ, WALL - HZ))
        if rnd.random() < 0.45:
            S.append('<rect x="%.0f" y="%d" width="%.0f" height="%d" fill="%s" opacity="%.2f" filter="url(#low)"/>'
                     % (bx + rnd.uniform(8, 120), HZ, rnd.uniform(6, 26), WALL - HZ,
                        lit("#5a2a14", light, 0.5), rnd.uniform(0.06, 0.20)))
    S.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s" opacity="%.2f" filter="url(#huge)"/>'
             % (HZ - 30, W, 110, flame, glow(0.16, light)))
    # wall coping and the bays cast into it
    S.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s"/>'
             % (WALL - 26, W, 26, lit("#241432", light, 0.7)))
    for i in range(int(W / 168) + 1):
        S.append('<rect x="%d" y="%d" width="8" height="%d" fill="#05040c" opacity="0.55"/>'
                 % (i * 168, WALL - 26, H - WALL + 26))

    S.append('<rect x="0" y="%d" width="%d" height="%d" fill="url(#water)"/>' % (WALL, W, H - WALL))
    # the flares smeared down the water
    S.append('<g filter="url(#smear)" opacity="%.2f">' % glow(0.75 if rain else 0.55, light))
    for fx, fs in ((0.175, 1.0), (0.395, 0.72), (0.655, 1.18), (0.875, 0.86)):
        S.append('<rect x="%.0f" y="%d" width="%.0f" height="%d" fill="%s"/>'
                 % (W * fx - 70 * fs, WALL, 140 * fs, int(H * 0.20), flame))
    S.append('</g>')
    for _ in range(280 if rain else 90):
        y = rnd.uniform(WALL, H)
        d = (y - WALL) / max(1.0, H - WALL)
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="2" fill="%s" opacity="%.2f"/>'
                 % (rnd.uniform(0, W), y, rnd.uniform(40, 280) * (0.35 + d), 2 + d * 5,
                    rnd.choice([flame, AMBER, ROSE, "#cfe0ff"]), rnd.uniform(0.05, 0.30)))

    if rain:
        if DRAW_STREAKS:
            S.append('<g stroke="#e8dcc8" stroke-linecap="round">%s</g>' % "".join(
                '<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke-width="%.1f" opacity="%.2f"/>'
                % (x, y, x - ln * 0.17, y + ln, rnd.uniform(1.1, 3.2), rnd.uniform(0.05, 0.22))
                for x, y, ln in ((rnd.uniform(-250, W + 250), rnd.uniform(-250, H), rnd.uniform(60, 300))
                                 for _ in range(2000))))
        for _ in range(9):
            S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#huge)"/>'
                     % (rnd.uniform(0, W), rnd.uniform(0, HZ), rnd.uniform(700, 1900),
                        rnd.uniform(110, 280), smog, rnd.uniform(0.14, 0.34)))
    else:
        for _ in range(320):
            S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="%s" opacity="%.2f"/>'
                     % (rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(1.0, 4.2),
                        rnd.choice([flame, GOLD, AMBER]), rnd.uniform(0.08, 0.45)))
        for _ in range(11):
            S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#huge)"/>'
                     % (rnd.uniform(0, W), rnd.uniform(HZ - H * 0.2, H * 0.92), rnd.uniform(600, 1600),
                        rnd.uniform(70, 210), rnd.choice([smog, VIOLET]), rnd.uniform(0.06, 0.18)))

    S.append(ambient(light))
    S.append(vignette(strength=vig(0.72, light), inner=0.28, color="#0b0616"))
    S.append('</svg>')
    return "".join(S)
