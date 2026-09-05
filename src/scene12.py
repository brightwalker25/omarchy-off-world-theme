"""12 - The Blaster: the gun on the table, against a wall that is giving up.

The prop was a Steyr Mannlicher receiver married to a Charter Arms Bulldog,
with amber grips, two triggers and six LEDs - four red, two green. Interior,
so it renders as a single plate.
"""
import math, random
from palette import *

NAME = "blaster"
LIGHT = "dusk"
OUTDOOR = False


def build(rain=False, light=LIGHT):
    rnd = random.Random(2019)
    TABLE = H * 0.715
    S = [svg_open(), '<defs>']

    # Noir out of grime rather than out of darkness: the wall is the subject as
    # much as the gun is, and it has to look like it is coming off in sheets.
    plaster = lit("#8c8168", light, 0.55)
    render = lit("#4e4436", light, 0.40)
    lath = lit("#241c14", light, 0.28)
    blued = lit("#20242c", light, 0.26)
    amber_grip = lit("#a8642a", light, 0.45)

    S.append('<linearGradient id="wall" x1="0.1" y1="0" x2="0.9" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="0.45" stop-color="%s"/>'
             '<stop offset="1" stop-color="%s"/></linearGradient>'
             % (lit("#8e8571", light, 0.5), lit("#5e5544", light, 0.38), lit("#241e17", light, 0.24)))
    S.append('<linearGradient id="tabletop" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="0.22" stop-color="%s"/>'
             '<stop offset="1" stop-color="%s"/></linearGradient>'
             % (lit("#7a5730", light, 0.55), lit("#3a2614", light, 0.34), lit("#120c07", light, 0.22)))
    S.append('<linearGradient id="daylight" x1="0" y1="0.1" x2="1" y2="0.5">'
             '<stop offset="0" stop-color="#ffd9a0" stop-opacity="0.55"/>'
             '<stop offset="0.42" stop-color="#ffc078" stop-opacity="0.20"/>'
             '<stop offset="1" stop-color="#ffb060" stop-opacity="0"/></linearGradient>')
    S.append('<linearGradient id="barrel" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="0.30" stop-color="%s"/>'
             '<stop offset="0.62" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
             % (lit("#6e7684", light, 0.5), lit("#333a45", light, 0.3), blued, lit("#0c0e12", light, 0.2)))
    S.append('<linearGradient id="grip" x1="0" y1="0" x2="0.6" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="0.5" stop-color="%s"/>'
             '<stop offset="1" stop-color="%s"/></linearGradient>'
             % (lit("#d99a4a", light, 0.55), amber_grip, lit("#5a2f12", light, 0.3)))
    S.append('<filter id="huge" x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="130"/></filter>')
    S.append('<filter id="big" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="44"/></filter>')
    S.append('<filter id="med" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="14"/></filter>')
    S.append('<filter id="low" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="4"/></filter>')
    S.append('<filter id="grain" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="2"/></filter>')
    S.append('</defs>')
    S.append('<rect width="%d" height="%d" fill="url(#wall)"/>' % (W, H))

    # ---- the wall: mottling, then damp, then the places it has failed
    for _ in range(150):
        S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#big)"/>'
                 % (rnd.uniform(0, W), rnd.uniform(0, TABLE + 100), rnd.uniform(90, 620), rnd.uniform(60, 340),
                    rnd.choice([lit("#5a5140", light, 0.36), lit("#847a62", light, 0.5),
                                lit("#332c22", light, 0.26), lit("#6a5c42", light, 0.42)]),
                    rnd.uniform(0.12, 0.40)))
    # a tide line where the damp has climbed the wall and stopped
    S.append('<rect x="0" y="%.0f" width="%d" height="%.0f" fill="%s" opacity="0.35" filter="url(#big)"/>'
             % (TABLE - H * 0.30, W, H * 0.30, lit("#4a3c2a", light, 0.32)))
    for _ in range(26):
        S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#med)"/>'
                 % (rnd.uniform(0, W), rnd.uniform(TABLE - H * 0.34, TABLE - H * 0.20),
                    rnd.uniform(60, 300), rnd.uniform(10, 40), lit("#3a2e1e", light, 0.28), rnd.uniform(0.10, 0.30)))

    # patches where the top coat has come away, exposing render and then lath
    for _ in range(11):
        cx0, cy0 = rnd.uniform(W * 0.02, W * 0.98), rnd.uniform(H * 0.04, TABLE - H * 0.03)
        rx0, ry0 = rnd.uniform(70, 330), rnd.uniform(60, 260)
        pts, n = [], 15
        for i in range(n):
            a = i * math.tau / n
            k = rnd.uniform(0.55, 1.25)
            pts.append("%.0f,%.0f" % (cx0 + math.cos(a) * rx0 * k, cy0 + math.sin(a) * ry0 * k))
        poly = " ".join(pts)
        S.append('<polygon points="%s" fill="%s" opacity="0.80" filter="url(#low)"/>' % (poly, render))
        # only the upper lip of the break catches light, and only faintly
        S.append('<polygon points="%s" fill="none" stroke="%s" stroke-width="4" opacity="0.28" filter="url(#low)"/>'
                 % (poly, lit("#c0b291", light, 0.55)))
        S.append('<polygon points="%s" fill="none" stroke="#000000" stroke-width="9" opacity="0.22" filter="url(#low)"/>' % poly)
        if rnd.random() < 0.55:
            S.append('<g opacity="0.7">')
            for i in range(7):
                S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s" opacity="0.55"/>'
                         % (cx0 - rx0 * 0.6, cy0 - ry0 * 0.55 + i * ry0 * 0.16, rx0 * 1.2, ry0 * 0.075, lath))
            S.append('</g>')

    # cracks, wandering down from wherever they started
    for _ in range(16):
        x, y = rnd.uniform(0, W), rnd.uniform(0, TABLE * 0.5)
        d = []
        for _ in range(rnd.randint(8, 22)):
            d.append("%.0f,%.0f" % (x, y))
            x += rnd.uniform(-42, 42); y += rnd.uniform(14, 68)
            if y > TABLE:
                break
        S.append('<polyline points="%s" fill="none" stroke="#1c160e" stroke-width="%.1f" opacity="%.2f"/>'
                 % (" ".join(d), rnd.uniform(1.6, 5.0), rnd.uniform(0.25, 0.62)))
        S.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%.1f" opacity="0.25"/>'
                 % (" ".join(d), lit("#d0c2a2", light, 0.6), rnd.uniform(1.0, 2.2)))

    # ---- last of the day, coming in from a window off to the left
    S.append('<rect width="%d" height="%.0f" fill="url(#daylight)"/>' % (W, TABLE + 60))
    slats = "".join('<rect x="%.0f" y="%.1f" width="%d" height="%.1f"/>'
                    % (-W, -H * 0.10 + i * H * 0.086, W * 3, H * 0.040) for i in range(16))
    S.append('<defs><linearGradient id="fall" x1="0" y1="0" x2="1" y2="0.2">'
             '<stop offset="0" stop-color="#ffffff" stop-opacity="0.95"/>'
             '<stop offset="0.62" stop-color="#ffffff" stop-opacity="0.20"/>'
             '<stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>'
             '<mask id="fallmask"><rect width="%d" height="%.0f" fill="url(#fall)"/></mask></defs>' % (W, TABLE + 60))
    S.append('<g mask="url(#fallmask)"><g fill="#ffcf92" opacity="0.20" transform="rotate(-6 %.0f %.0f)">%s</g></g>'
             % (W * 0.5, H * 0.4, slats))

    # ---- the table
    S.append('<rect x="0" y="%.0f" width="%d" height="%.0f" fill="url(#tabletop)"/>' % (TABLE, W, H - TABLE))
    S.append('<rect x="0" y="%.0f" width="%d" height="7" fill="%s" opacity="0.8"/>'
             % (TABLE, W, lit("#b8874e", light, 0.6)))
    # the front edge of the table, and the drop past it into nothing
    S.append('<rect x="0" y="%.0f" width="%d" height="%.0f" fill="%s"/>'
             % (H * 0.945, W, H * 0.055, lit("#0d0906", light, 0.16)))
    S.append('<rect x="0" y="%.0f" width="%d" height="6" fill="%s" opacity="0.55"/>'
             % (H * 0.945, W, lit("#9a7040", light, 0.55)))
    for _ in range(70):
        yy = rnd.uniform(TABLE + 10, H)
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="2" fill="#000000" opacity="%.2f"/>'
                 % (rnd.uniform(-200, W), yy, rnd.uniform(240, 1500), rnd.uniform(0.05, 0.20)))

    # ---- the blaster. Local space is 1000 x 430, muzzle at x=0, grip base at y=430.
    GS = (W * 0.615) / 1000.0
    GX, GY = W * 0.185, TABLE - 430 * GS + H * 0.014
    # Pivot on the grip base, not on the origin: rotating about the muzzle
    # lifts the butt off the table and the gun floats.
    S.append('<g transform="translate(%.1f,%.1f) rotate(-5 %.1f %.1f) scale(%.5f)">'
             % (GX, GY, 780 * GS, 424 * GS, GS))

    def R(x, y, w, h, fill, rx=0, op=1.0, extra=""):
        S.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s" opacity="%.2f"%s/>'
                 % (x, y, w, h, rx, fill, op, extra))

    # cast shadow on the table
    S.append('<ellipse cx="520" cy="452" rx="470" ry="40" fill="#000000" opacity="0.50" filter="url(#med)"/>')
    S.append('<ellipse cx="770" cy="432" rx="120" ry="20" fill="#000000" opacity="0.80" filter="url(#low)"/>')

    # barrel assembly and the vented shroud over it
    R(6, 150, 330, 62, "url(#barrel)", 10)
    for i in range(6):
        R(52 + i * 44, 162, 20, 38, "#07090c", 6, 0.85)
    R(0, 158, 26, 46, lit("#0a0c10", light, 0.2), 4)
    # receiver
    R(300, 118, 430, 118, "url(#barrel)", 14)
    R(300, 118, 430, 16, lit("#8d97a6", light, 0.55), 8, 0.85)
    # bolt and its handle, sitting proud on top
    R(352, 84, 210, 44, lit("#2b323c", light, 0.3), 12)
    R(352, 84, 210, 10, lit("#98a2b0", light, 0.55), 5, 0.8)
    S.append('<path d="M 540 104 L 620 60 L 646 76 L 566 122 Z" fill="%s"/>' % lit("#3a424e", light, 0.32))
    S.append('<circle cx="632" cy="68" r="21" fill="%s"/>' % lit("#4a535f", light, 0.35))
    # the side cover plate over the cylinder, with its rivets
    R(392, 140, 232, 88, lit("#2a3038", light, 0.3), 10)
    R(392, 140, 232, 88, "none", 10, 0.55, ' stroke="%s" stroke-width="5"' % lit("#7d8794", light, 0.5))
    for i in range(6):
        S.append('<circle cx="%.0f" cy="%.0f" r="7" fill="%s" opacity="0.9"/>'
                 % (412 + (i % 3) * 100, 160 + (i // 3) * 50, lit("#8e98a6", light, 0.5)))
    # rear sight and the receiver tang
    R(700, 100, 46, 34, lit("#333b46", light, 0.3), 6)
    R(716, 82, 14, 26, lit("#48515e", light, 0.35), 4)

    # trigger guard, and the two triggers inside it
    S.append('<path d="M 560 236 L 560 268 Q 610 322 668 268 L 668 236 Z" fill="%s"/>' % lit("#252b34", light, 0.28))
    S.append('<path d="M 578 240 L 578 262 Q 612 300 650 262 L 650 240 Z" fill="#05070a"/>')
    for tx in (596, 626):
        S.append('<path d="M %d 244 Q %d 276 %d 288 Q %d 274 %d 244 Z" fill="%s"/>'
                 % (tx, tx + 4, tx + 2, tx - 8, tx - 12, lit("#5c6672", light, 0.4)))

    # the grip: amber, raked back, the warmest thing in the frame
    S.append('<path d="M 668 214 L 806 214 L 858 418 L 726 430 Z" fill="url(#grip)"/>')
    S.append('<path d="M 668 214 L 806 214 L 858 418 L 726 430 Z" fill="none" stroke="%s" stroke-width="6" opacity="0.55"/>'
             % lit("#f0b060", light, 0.6))
    for i in range(7):   # checkering
        S.append('<path d="M %d 240 L %d 412" stroke="#5a2f12" stroke-width="4" opacity="0.35" fill="none"/>'
                 % (700 + i * 20, 726 + i * 20))
    S.append('<path d="M 806 214 Q 852 300 858 418 L 812 424 Q 806 306 772 220 Z" fill="%s" opacity="0.9"/>'
             % lit("#6b3c16", light, 0.32))
    S.append('<ellipse cx="754" cy="300" rx="46" ry="92" fill="#ffd9a0" opacity="0.16" filter="url(#med)" transform="rotate(9 754 300)"/>')
    R(676, 208, 148, 14, lit("#2a3038", light, 0.28), 6)

    # ---- the LEDs: four red, two green, and the only saturated colour here
    for lx, ly, col in ((424, 200, ROSE), (472, 200, ROSE), (520, 200, ROSE), (568, 200, ROSE),
                        (338, 132, MINT), (676, 132, MINT)):
        S.append('<circle cx="%d" cy="%d" r="34" fill="%s" opacity="%.2f" filter="url(#med)"/>' % (lx, ly, col, glow(0.85, light)))
        S.append('<circle cx="%d" cy="%d" r="11" fill="%s"/>' % (lx, ly, col))
        S.append('<circle cx="%d" cy="%d" r="5" fill="#ffffff" opacity="0.85"/>' % (lx - 2, ly - 3))
        S.append('<circle cx="%d" cy="%d" r="13" fill="none" stroke="%s" stroke-width="4" opacity="0.7"/>'
                 % (lx, ly, lit("#8a94a2", light, 0.5)))
    S.append('</g>')

    # ---- what the LEDs put back into the varnish, and into the wall behind
    for fx, col in ((0.455, ROSE), (0.482, ROSE), (0.509, ROSE), (0.536, ROSE),
                    (0.404, MINT), (0.594, MINT)):
        S.append('<ellipse cx="%.0f" cy="%.0f" rx="26" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#med)"/>'
                 % (W * fx, TABLE + H * 0.055, H * 0.058, col, glow(0.30, light)))
    S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#huge)"/>'
             % (W * 0.50, TABLE - H * 0.045, W * 0.20, H * 0.10, ROSE, glow(0.22, light)))
    S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#huge)"/>'
             % (W * 0.36, TABLE - H * 0.02, W * 0.12, H * 0.07, GOLD, glow(0.18, light)))

    # ---- dust in what is left of the light
    for _ in range(420):
        S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="#fff0d4" opacity="%.2f"/>'
                 % (rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(0.9, 3.4), rnd.uniform(0.05, 0.34)))

    S.append(ambient(light, haze="#6a4c33", op=0.04))
    S.append(vignette(strength=vig(1.05, light), inner=0.18, color="#080506"))
    S.append('</svg>')
    return "".join(S)
