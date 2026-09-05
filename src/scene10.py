"""10 - Tyrell's Office: the hall at first light, and the owl that watches it.

Interior, so it renders as a single plate.
"""
import math, random
from palette import *

NAME = "tyrell-office"
LIGHT = "dawn"
OUTDOOR = False


def build(rain=False, light=LIGHT):
    rnd = random.Random(2021)
    FLOOR = H * 0.720
    S = [svg_open(), '<defs>']

    # The room is enormous and nearly empty. All of the light comes in flat and
    # low from the right, so everything reads as silhouette plus one rim.
    sun = lit("#ffbf72", light, 0.35)
    stone = lit("#2a2434", light, 0.35)
    S.append('<linearGradient id="hall" x1="1" y1="0.15" x2="0" y2="0.9">'
             '<stop offset="0" stop-color="%s"/><stop offset="0.35" stop-color="%s"/>'
             '<stop offset="1" stop-color="%s"/></linearGradient>'
             % (lit("#6a4a52", light, 0.55), lit("#241d33", light, 0.35), lit("#08060f", light, 0.20)))
    S.append('<linearGradient id="win" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#ffe2b0" stop-opacity="0.98"/>'
             '<stop offset="0.45" stop-color="%s" stop-opacity="0.92"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0.55"/></linearGradient>' % (sun, ROSE))
    S.append('<linearGradient id="beam" x1="1" y1="0.2" x2="0" y2="0.8">'
             '<stop offset="0" stop-color="#ffdaa6" stop-opacity="0.50"/>'
             '<stop offset="0.55" stop-color="%s" stop-opacity="0.14"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient>' % (sun, sun))
    S.append('<linearGradient id="polish" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="0.4" stop-color="%s"/>'
             '<stop offset="1" stop-color="%s"/></linearGradient>'
             % (lit("#3a2c3a", light, 0.4), lit("#140f1c", light, 0.26), lit("#05040a", light, 0.18)))
    S.append('<filter id="huge" x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="150"/></filter>')
    S.append('<filter id="big" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="52"/></filter>')
    S.append('<filter id="med" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="16"/></filter>')
    S.append('<filter id="low" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="5"/></filter>')
    S.append('<filter id="smear" x="-30%" y="-10%" width="160%" height="130%"><feGaussianBlur stdDeviation="20 70"/></filter>')
    S.append('</defs>')
    S.append('<rect width="%d" height="%d" fill="url(#hall)"/>' % (W, H))

    # ---- the window wall: full-height bays down the right-hand side
    bays = 5
    for i in range(bays):
        t0 = i / float(bays)
        # bays recede to the left, so both edges and the top converge
        x0 = W * (0.995 - t0 * 0.62) - W * 0.115 * (1 - t0 * 0.55)
        x1 = W * (0.995 - t0 * 0.62)
        ytop = H * (0.045 + t0 * 0.115)
        ybot = FLOOR - (FLOOR - H * 0.62) * t0 * 0.45
        S.append('<polygon points="%.0f,%.0f %.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="url(#win)" opacity="%.2f"/>'
                 % (x0, ytop, x1, ytop, x1, ybot, x0, ybot, 0.95 - t0 * 0.32))
        # mullions
        for k in range(1, 4):
            mx = x0 + (x1 - x0) * k / 4.0
            S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s" opacity="0.9"/>'
                     % (mx, ytop, max(4.0, 11 * (1 - t0 * 0.5)), ybot - ytop, lit("#120d1a", light, 0.24)))
        for k in range(1, 6):
            my = ytop + (ybot - ytop) * k / 6.0
            S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s" opacity="0.85"/>'
                     % (x0, my, x1 - x0, max(3.0, 8 * (1 - t0 * 0.5)), lit("#120d1a", light, 0.24)))
        # the pier between this bay and the next
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s"/>'
                 % (x0 - W * 0.030 * (1 - t0 * 0.5), ytop - H * 0.02, W * 0.030 * (1 - t0 * 0.5),
                    ybot - ytop + H * 0.04, lit("#0e0a16", light, 0.20)))
    S.append('<rect x="%.0f" y="0" width="%.0f" height="%.0f" fill="%s" opacity="%.2f" filter="url(#huge)"/>'
             % (W * 0.38, W * 0.64, FLOOR, sun, glow(0.30, light)))

    # ---- the colonnade marching away down the left
    for i in range(5):
        t = i / 4.0
        # spaced so daylight gets between them; overlapping columns read as one wall
        cw = W * (0.088 - t * 0.056)
        cx0 = W * (0.000 + t * 0.400)
        ctop = H * (0.0 + t * 0.105)
        cbot = FLOOR + (H - FLOOR) * (1 - t) * 0.30
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s"/>'
                 % (cx0, ctop, cw, cbot - ctop, mix(stone, "#05040a", 0.30 + t * 0.45)))
        # the one rim the sun gets around the right-hand edge of each column
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s" opacity="%.2f"/>'
                 % (cx0 + cw - max(4.0, 16 * (1 - t)), ctop, max(4.0, 16 * (1 - t)), cbot - ctop,
                    sun, 0.65 - t * 0.35))
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s" opacity="%.2f" filter="url(#med)"/>'
                 % (cx0 + cw - 6, ctop, 44 * (1 - t * 0.6), cbot - ctop, sun, glow(0.30 - t * 0.15, light)))

    # ---- the light itself, lying across the room in flat bars
    for i in range(bays):
        t0 = i / float(bays)
        x1 = W * (0.995 - t0 * 0.62)
        S.append('<polygon points="%.0f,%.0f %.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="url(#beam)" filter="url(#big)" opacity="%.2f"/>'
                 % (x1, H * (0.05 + t0 * 0.10), x1, FLOOR * (0.62 + t0 * 0.10),
                    -W * 0.05, H * (0.78 - t0 * 0.06), -W * 0.05, H * (0.30 + t0 * 0.10),
                    glow(0.80 - t0 * 0.12, light)))

    # ---- the floor, polished enough to give the window back
    S.append('<rect x="0" y="%.0f" width="%d" height="%.0f" fill="url(#polish)"/>' % (FLOOR, W, H - FLOOR))
    S.append('<rect x="0" y="%.0f" width="%d" height="8" fill="%s" opacity="0.5"/>' % (FLOOR, W, sun))
    S.append('<g filter="url(#smear)" opacity="%.2f">' % glow(0.55, light))
    for i in range(bays):
        t0 = i / float(bays)
        x1 = W * (0.995 - t0 * 0.62)
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s"/>'
                 % (x1 - W * 0.100 * (1 - t0 * 0.5), FLOOR, W * 0.100 * (1 - t0 * 0.5), H - FLOOR, sun))
    S.append('</g>')
    for i in range(1, 12):
        t = (i / 11.0) ** 2.0
        S.append('<line x1="0" y1="%.1f" x2="%d" y2="%.1f" stroke="#000000" stroke-width="2" opacity="0.20"/>'
                 % (FLOOR + (H - FLOOR) * t, W, FLOOR + (H - FLOOR) * t))

    # ---- the owl, on its perch, left of centre, watching the frame
    ox, oy = W * 0.292, FLOOR - H * 0.330
    oh = H * 0.330
    ow = oh * 0.46
    S.append('<rect x="%.0f" y="%.0f" width="14" height="%.0f" fill="%s"/>'
             % (ox - 7, oy + oh * 0.86, oh * 0.62, lit("#0d0a14", light, 0.22)))
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="16" rx="8" fill="%s"/>'
             % (ox - ow * 0.60, oy + oh * 0.84, ow * 1.2, lit("#171224", light, 0.26)))
    # body: a heavy teardrop, wings folded
    S.append('<path d="M %.1f %.1f Q %.1f %.1f %.1f %.1f Q %.1f %.1f %.1f %.1f Q %.1f %.1f %.1f %.1f Z" fill="%s"/>'
             % (ox, oy,
                ox + ow * 0.62, oy + oh * 0.10, ox + ow * 0.50, oy + oh * 0.88,
                ox, oy + oh * 0.98, ox - ow * 0.50, oy + oh * 0.88,
                ox - ow * 0.62, oy + oh * 0.10, ox, oy,
                lit("#0a0810", light, 0.18)))
    # the rim the window puts down its right side
    S.append('<path d="M %.1f %.1f Q %.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="9" opacity="0.75"/>'
             % (ox + ow * 0.05, oy + oh * 0.02, ox + ow * 0.62, oy + oh * 0.10,
                ox + ow * 0.50, oy + oh * 0.88, sun))
    S.append('<path d="M %.1f %.1f Q %.1f %.1f %.1f %.1f" fill="none" stroke="%s" stroke-width="34" opacity="%.2f" filter="url(#med)"/>'
             % (ox + ow * 0.05, oy + oh * 0.02, ox + ow * 0.62, oy + oh * 0.10,
                ox + ow * 0.50, oy + oh * 0.88, sun, glow(0.40, light)))
    # feather texture, just enough to break the silhouette
    for _ in range(90):
        a = rnd.uniform(0, math.tau); r = rnd.uniform(0, 1) ** 0.6
        fx = ox + math.cos(a) * ow * 0.46 * r
        fy = oy + oh * 0.52 + math.sin(a) * oh * 0.40 * r
        S.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s" opacity="%.2f"/>'
                 % (fx, fy, rnd.uniform(4, 13), rnd.uniform(2, 6), lit("#2a2028", light, 0.22), rnd.uniform(0.04, 0.13)))
    # ear tufts
    for sgn in (-1, 1):
        S.append('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f Z" fill="%s"/>'
                 % (ox + sgn * ow * 0.30, oy + oh * 0.050, ox + sgn * ow * 0.47, oy + oh * 0.012,
                    ox + sgn * ow * 0.50, oy + oh * 0.105, lit("#0a0810", light, 0.18)))
    # the eyes, which are the only thing in the room that is switched on
    for sgn in (-1, 1):
        ex0 = ox + sgn * ow * 0.215
        ey0 = oy + oh * 0.185
        er = oh * 0.042
        S.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" opacity="%.2f" filter="url(#med)"/>'
                 % (ex0, ey0, er * 2.6, AMBER, glow(0.55, light)))
        S.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (ex0, ey0, er, GOLD))
        S.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (ex0, ey0, er * 0.62, AMBER))
        S.append('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="#1a0a04"/>' % (ex0, ey0, er * 0.20, er * 0.44))
        S.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#fff4d8" opacity="0.9"/>' % (ex0 - er * 0.28, ey0 - er * 0.30, er * 0.16))
    S.append('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f Z" fill="%s"/>'
             % (ox, oy + oh * 0.215, ox - oh * 0.026, oy + oh * 0.275, ox + oh * 0.026, oy + oh * 0.275,
                lit("#6a4a20", light, 0.4)))
    # the owl's own reflection, standing in the polished floor
    S.append('<g filter="url(#smear)" opacity="%.2f"><rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s"/></g>'
             % (glow(0.30, light), ox - ow * 0.5, FLOOR, ow, H * 0.14, lit("#160f18", light, 0.24)))

    # ---- dust, which is the whole reason the beams are visible
    for _ in range(900):
        x = rnd.uniform(0, W); y = rnd.uniform(0, H)
        w8 = 1.0 - abs(x - W * 0.72) / W        # thickest where the light is
        S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="#fff0cc" opacity="%.2f"/>'
                 % (x, y, rnd.uniform(0.9, 3.6), rnd.uniform(0.04, 0.42) * max(0.15, w8)))

    S.append(ambient(light, haze="#5e5470", op=0.05))
    S.append(vignette(strength=vig(0.86, light), inner=0.24, color="#06050e"))
    S.append('</svg>')
    return "".join(S)
