"""11 - Spinner Ascent: a police spinner climbing into first light.

Looking up between two towers. The street is still night; only the crowns have
the sun on them yet.
"""
import math, random
from palette import *

NAME = "spinner-ascent"
LIGHT = "dawn"
OUTDOOR = True


def build(rain=True, light=LIGHT):
    rnd = random.Random(2032)
    VPY = H * 1.28                       # vanishing point below the frame
    S = [svg_open(), '<defs>']

    if rain:
        stops = (("0", "#7d5162"), ("0.24", "#57436e"), ("0.44", "#2d3568"),
                 ("0.70", "#16214e"), ("1", "#070a20"))
        sun, wet = "#ffb887", 1.0
    else:
        stops = (("0", "#b4657a"), ("0.22", "#5a4076"), ("0.45", "#25336b"),
                 ("0.70", "#101d4e"), ("1", "#04060f"))
        sun, wet = "#ffd0a0", 0.0
    # We are looking up, so the sun is at the top of the frame and the canyon
    # under us keeps its night. The warm band holds most of its heat.
    stops = lit_stops(stops[:2], light, k=0.40) + lit_stops(stops[2:], light)
    S.append('<linearGradient id="sky" x1="0.30" y1="0" x2="0.70" y2="1">%s</linearGradient>'
             % "".join('<stop offset="%s" stop-color="%s"/>' % st for st in stops))
    S.append('<linearGradient id="face" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="0.30" stop-color="%s"/>'
             '<stop offset="1" stop-color="%s"/></linearGradient>'
             % (lit("#4e3a52", light, 0.5), lit("#171436", light, 0.32), lit("#05050f", light, 0.18)))
    S.append('<radialGradient id="lamp"><stop offset="0" stop-color="#ffffff" stop-opacity="0.95"/>'
             '<stop offset="0.3" stop-color="%s" stop-opacity="0.65"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (CYAN, CYAN))
    S.append('<radialGradient id="burn"><stop offset="0" stop-color="#fff2d0" stop-opacity="0.95"/>'
             '<stop offset="0.35" stop-color="%s" stop-opacity="0.60"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (AMBER, ROSE))
    S.append('<filter id="huge" x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="150"/></filter>')
    S.append('<filter id="big" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="50"/></filter>')
    S.append('<filter id="med" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="16"/></filter>')
    S.append('<filter id="low" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="5"/></filter>')
    S.append('</defs>')
    S.append('<rect width="%d" height="%d" fill="url(#sky)"/>' % (W, H))

    for _ in range(stars(560, light)):
        y = rnd.uniform(0, H * 0.62)
        S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="#e6eeff" opacity="%.2f"/>'
                 % (rnd.uniform(0, W), y, rnd.uniform(0.8, 2.8),
                    rnd.uniform(0.08, 0.7) * (y / (H * 0.62)) * (0.5 if rain else 1.0)))

    # ---- the towers, leaning in toward a vanishing point under the frame
    def tower(xin, xout, crown, depth, col_k):
        """One tower face, drawn as a trapezoid converging downward."""
        def px(x, t):
            return x + (W * 0.5 - x) * t
        out = []
        top = crown
        bot = H + 200
        t_top, t_bot = 0.0, (bot - top) / (VPY - top)
        out.append('<polygon points="%.0f,%.0f %.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="url(#face)" opacity="%.2f"/>'
                   % (px(xin, t_top), top, px(xout, t_top), top,
                      px(xout, t_bot), bot, px(xin, t_bot), bot, 0.94))
        # window grid, compressing as it recedes downward
        rows = 34
        for r in range(rows):
            t = t_bot * (r / float(rows)) ** 1.25
            yy = top + (VPY - top) * t
            if yy > H:
                break
            for c in range(9):
                u = (c + 0.5) / 9.0
                wx = px(xin + (xout - xin) * u, t)
                lit_win = rnd.random() < (0.30 if r > rows * 0.35 else 0.14)
                ww = max(2.0, (xout - xin) * 0.055 * (1 - t))
                hh = max(2.0, H * 0.016 * (1 - t))
                out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" opacity="%.2f"/>'
                           % (wx, yy, ww, hh,
                              rnd.choice([GOLD, AMBER, CYAN, "#dfe9ff"]) if lit_win else "#05060f",
                              rnd.uniform(0.35, 0.95) if lit_win else 0.55))
        # the crown, which is the only part with sun on it
        out.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s" opacity="%.2f"/>'
                   % (xin, crown, xout - xin, H * 0.030, sun, 0.55 * col_k))
        out.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s" opacity="%.2f" filter="url(#med)"/>'
                   % (xin, crown - H * 0.012, xout - xin, H * 0.055, sun, glow(0.40 * col_k, light)))
        return "".join(out)

    S.append(tower(-W * 0.12, W * 0.235, H * 0.075, 0, 1.0))
    S.append(tower(W * 0.760, W * 1.10, H * 0.135, 0, 0.75))
    S.append(tower(W * 0.215, W * 0.320, H * 0.290, 1, 0.55))
    S.append(tower(W * 0.690, W * 0.790, H * 0.335, 1, 0.45))

    # haze filling the canyon between them
    for _ in range(14):
        S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#huge)"/>'
                 % (rnd.uniform(W * 0.2, W * 0.8), rnd.uniform(H * 0.30, H * 0.80),
                    rnd.uniform(350, 1000), rnd.uniform(80, 240),
                    rnd.choice([VIOLET, "#3a2650", BLUE]), rnd.uniform(0.07, 0.17)))

    # ---- the street, a very long way down, still in the dark
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="#02030a"/>'
             % (W * 0.26, H * 0.83, W * 0.48, H * 0.17))
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="#02030a" opacity="0.75" filter="url(#big)"/>'
             % (W * 0.24, H * 0.80, W * 0.52, H * 0.20))
    for _ in range(70):
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="2" fill="%s" opacity="%.2f"/>'
                 % (rnd.uniform(W * 0.31, W * 0.69), rnd.uniform(H * 0.87, H),
                    rnd.uniform(4, 22), rnd.uniform(2, 5),
                    rnd.choice([GOLD, ROSE, CYAN]), rnd.uniform(0.20, 0.75)))

    # ---- the spinner, climbing, seen from below and behind
    sx, sy = W * 0.487, H * 0.530
    SW = W * 0.225
    SH = SW * 0.40
    S.append('<g transform="rotate(-9 %.0f %.0f)">' % (sx, sy))
    # thruster wash under it
    for k, (rr, op) in enumerate(((1.15, 0.16), (0.80, 0.30), (0.52, 0.60))):
        S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="url(#burn)" opacity="%.2f" filter="url(#big)"/>'
                 % (sx - SW * 0.20, sy + SH * (0.8 + k * 0.42), SW * 0.30 * rr, SH * 0.55 * rr, glow(op, light)))
        S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="url(#burn)" opacity="%.2f" filter="url(#big)"/>'
                 % (sx + SW * 0.22, sy + SH * (0.8 + k * 0.42), SW * 0.30 * rr, SH * 0.55 * rr, glow(op, light)))
    # hull
    S.append('<path d="M %.1f %.1f Q %.1f %.1f %.1f %.1f L %.1f %.1f Q %.1f %.1f %.1f %.1f Z" fill="%s"/>'
             % (sx - SW * 0.52, sy + SH * 0.30,
                sx - SW * 0.30, sy - SH * 0.62, sx + SW * 0.10, sy - SH * 0.58,
                sx + SW * 0.52, sy - SH * 0.10,
                sx + SW * 0.56, sy + SH * 0.52, sx - SW * 0.52, sy + SH * 0.30,
                lit("#12131c", light, 0.24)))
    # canopy
    S.append('<path d="M %.1f %.1f Q %.1f %.1f %.1f %.1f L %.1f %.1f Z" fill="%s" opacity="0.95"/>'
             % (sx - SW * 0.24, sy - SH * 0.30, sx - SW * 0.05, sy - SH * 0.66,
                sx + SW * 0.30, sy - SH * 0.36, sx + SW * 0.20, sy - SH * 0.06,
                lit("#2a4a66", light, 0.45)))
    S.append('<path d="M %.1f %.1f Q %.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="7" opacity="0.8"/>'
             % (sx - SW * 0.24, sy - SH * 0.30, sx - SW * 0.05, sy - SH * 0.66,
                sx + SW * 0.30, sy - SH * 0.36, mix(CYAN, "#ffffff", 0.5)))
    # the sun catching the top of the hull
    S.append('<path d="M %.1f %.1f Q %.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="9" opacity="0.75"/>'
             % (sx - SW * 0.44, sy + SH * 0.12, sx - SW * 0.24, sy - SH * 0.60,
                sx + SW * 0.50, sy - SH * 0.14, sun))
    # skids and fins
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="6" fill="%s"/>'
             % (sx - SW * 0.40, sy + SH * 0.52, SW * 0.86, SH * 0.13, lit("#0c0d14", light, 0.2)))
    S.append('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f Z" fill="%s"/>'
             % (sx + SW * 0.40, sy - SH * 0.16, sx + SW * 0.70, sy - SH * 0.62,
                sx + SW * 0.56, sy + SH * 0.10, lit("#141520", light, 0.24)))
    # LAPD strobes
    for lx, ly, c in ((-0.44, -0.16, ROSE), (0.46, -0.24, CYAN), (-0.10, 0.44, GOLD)):
        S.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="url(#lamp)" opacity="%.2f"/>'
                 % (sx + SW * lx, sy + SH * ly, SW * 0.16, glow(0.85, light)))
        S.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (sx + SW * lx, sy + SH * ly, SW * 0.024, c))
    S.append('</g>')
    # the beam it is throwing down the canyon ahead of itself
    S.append('<polygon points="%.0f,%.0f %.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="%s" opacity="%.2f" filter="url(#big)"/>'
             % (sx - SW * 0.30, sy + SH * 0.4, sx + SW * 0.10, sy + SH * 0.4,
                sx + SW * 0.80, H, sx - SW * 0.95, H, CYAN, glow(0.10, light)))

    # ---- other traffic, small, threading the canyon
    for _ in range(9):
        x = rnd.uniform(W * 0.30, W * 0.70); y = rnd.uniform(H * 0.30, H * 0.86)
        ln = rnd.uniform(24, 90)
        S.append('<g opacity="%.2f"><rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="4" fill="%s" filter="url(#low)"/>'
                 '<rect x="%.0f" y="%.0f" width="%.0f" height="3" fill="#ffffff" opacity="0.8"/></g>'
                 % (rnd.uniform(0.30, 0.80), x, y, ln, rnd.uniform(4, 9),
                    rnd.choice([CYAN, GOLD, ROSE]), x, y + 2, ln * 0.4))

    if rain:
        if DRAW_STREAKS:
            S.append('<g stroke="#dceaff" stroke-linecap="round">%s</g>' % "".join(
                '<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke-width="%.1f" opacity="%.2f"/>'
                % (x, y, x - ln * 0.14, y + ln, rnd.uniform(1.1, 3.2), rnd.uniform(0.05, 0.24))
                for x, y, ln in ((rnd.uniform(-250, W + 250), rnd.uniform(-250, H), rnd.uniform(60, 300))
                                 for _ in range(2100))))
        for _ in range(8):
            S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="#1c1430" opacity="%.2f" filter="url(#huge)"/>'
                     % (rnd.uniform(0, W), rnd.uniform(0, H * 0.7), rnd.uniform(600, 1700),
                        rnd.uniform(100, 260), rnd.uniform(0.14, 0.34)))
    else:
        for _ in range(300):
            S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="%s" opacity="%.2f"/>'
                     % (rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(1.0, 3.6),
                        rnd.choice([sun, CYAN, "#ffe0c0"]), rnd.uniform(0.07, 0.40)))

    S.append(ambient(light))
    S.append(vignette(strength=vig(0.76, light), inner=0.28))
    S.append('</svg>')
    return "".join(S)
