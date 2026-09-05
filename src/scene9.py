"""9 - The Machine: the Voight-Kampff apparatus itself, on the desk, after dark.

Scene 3 is what the machine sees. This is the machine. Interior, so it renders
as a single plate with no weather variant.
"""
import math, random
from palette import *

NAME = "vk-machine"
LIGHT = "night"
OUTDOOR = False
MONO = "JetBrainsMono Nerd Font,JetBrains Mono,Noto Sans Mono,monospace"


def build(rain=False, light=LIGHT):
    rnd = random.Random(1982)
    DESK = H * 0.780
    S = [svg_open(), '<defs>']

    # Brass and bakelite in a room with no light of its own. Every colour here
    # is emitted by the instrument or thrown by the one lamp.
    brass = lit("#9a763a", light, 0.4)
    steel = lit("#1a1c1f", light, 0.3)
    S.append('<radialGradient id="room" cx="0.34" cy="0.10" r="1.00">'
             '<stop offset="0" stop-color="%s"/><stop offset="0.40" stop-color="%s"/>'
             '<stop offset="1" stop-color="%s"/></radialGradient>'
             % (lit("#2e2740", light, 0.55), lit("#0e0c1a", light, 0.30), lit("#030308", light, 0.18)))
    S.append('<linearGradient id="desk" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="0.30" stop-color="%s"/>'
             '<stop offset="1" stop-color="%s"/></linearGradient>'
             % (lit("#4a3320", light, 0.5), lit("#1c1209", light, 0.3), lit("#070505", light, 0.2)))
    S.append('<linearGradient id="lampcone" x1="0.1" y1="0" x2="0.7" y2="1">'
             '<stop offset="0" stop-color="#fff2d4" stop-opacity="0.42"/>'
             '<stop offset="0.45" stop-color="%s" stop-opacity="0.14"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient>' % (GOLD, GOLD))
    S.append('<linearGradient id="lid" x1="0" y1="0" x2="0.3" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="0.45" stop-color="%s"/>'
             '<stop offset="1" stop-color="%s"/></linearGradient>'
             % (lit("#4e4a3e", light, 0.55), lit("#22211d", light, 0.32), lit("#0e0e10", light, 0.22)))
    S.append('<radialGradient id="lenscore"><stop offset="0" stop-color="#fffaf0" stop-opacity="0.98"/>'
             '<stop offset="0.18" stop-color="%s" stop-opacity="0.92"/>'
             '<stop offset="0.48" stop-color="%s" stop-opacity="0.55"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (AMBER, ROSE, ROSE))
    S.append('<radialGradient id="crtface" cx="0.5" cy="0.42" r="0.72">'
             '<stop offset="0" stop-color="%s" stop-opacity="0.42"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0.04"/></radialGradient>' % (MINT, MINT))
    S.append('<filter id="huge" x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="140"/></filter>')
    S.append('<filter id="big" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="46"/></filter>')
    S.append('<filter id="med" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="15"/></filter>')
    S.append('<filter id="low" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="4"/></filter>')
    S.append('<filter id="smear" x="-30%" y="-10%" width="160%" height="130%"><feGaussianBlur stdDeviation="14 58"/></filter>')
    S.append('</defs>')
    S.append('<rect width="%d" height="%d" fill="url(#room)"/>' % (W, H))

    # ---- the window, high on the right, and the city a long way below it
    wx, wy, ww, wh = W * 0.700, H * 0.055, W * 0.255, H * 0.400
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s"/>'
             % (wx, wy, ww, wh, lit("#0c1128", light, 0.75)))
    for _ in range(150):
        yy = rnd.uniform(wy + wh * 0.25, wy + wh)
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s" opacity="%.2f"/>'
                 % (rnd.uniform(wx, wx + ww), yy, rnd.uniform(2, 8), rnd.uniform(2, 14),
                    rnd.choice([GOLD, CYAN, MAGENTA, ROSE, "#dfe9ff"]), rnd.uniform(0.25, 0.95)))
    for _ in range(7):
        S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#big)"/>'
                 % (rnd.uniform(wx, wx + ww), rnd.uniform(wy + wh * 0.4, wy + wh),
                    rnd.uniform(90, 240), rnd.uniform(40, 110),
                    rnd.choice([MAGENTA, CYAN, GOLD]), rnd.uniform(0.14, 0.34)))
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="none" stroke="%s" stroke-width="13"/>'
             % (wx, wy, ww, wh, lit("#0e0b12", light, 0.28)))
    for i in range(1, 3):
        S.append('<rect x="%.0f" y="%.0f" width="8" height="%.0f" fill="%s"/>'
                 % (wx + i * ww / 3.0, wy, wh, lit("#0e0b12", light, 0.28)))
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s" opacity="%.2f" filter="url(#huge)"/>'
             % (wx - 90, wy - 70, ww + 180, wh + 140, CYAN, glow(0.20, light)))

    # ---- venetian shadow, cast on the wall only, falling away to the right
    S.append('<defs><linearGradient id="slatfall" x1="0" y1="0" x2="1" y2="0.25">'
             '<stop offset="0" stop-color="#ffffff" stop-opacity="0"/>'
             '<stop offset="0.30" stop-color="#ffffff" stop-opacity="0.9"/>'
             '<stop offset="1" stop-color="#ffffff" stop-opacity="0.15"/></linearGradient>'
             '<mask id="slatmask"><rect width="%d" height="%.0f" fill="url(#slatfall)"/></mask></defs>'
             % (W, DESK))
    slats = "".join('<rect x="0" y="%.1f" width="%d" height="%.1f"/>'
                    % (-H * 0.06 + i * H * 0.052, W, H * 0.024) for i in range(20))
    S.append('<g mask="url(#slatmask)" filter="url(#med)">'
             '<g fill="%s" opacity="0.12" transform="rotate(-7 %.0f %.0f)">%s</g></g>'
             % (GOLD, W * 0.5, H * 0.4, slats))

    # ---- the task lamp cone, from off-frame upper left
    S.append('<polygon points="%.0f,%.0f %.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="url(#lampcone)" filter="url(#big)"/>'
             % (W * 0.02, -60, W * 0.18, -60, W * 0.80, DESK + 140, W * 0.16, DESK + 140))

    # ---- the desk
    S.append('<rect x="0" y="%.0f" width="%d" height="%.0f" fill="url(#desk)"/>' % (DESK, W, H - DESK))
    S.append('<rect x="0" y="%.0f" width="%d" height="9" fill="%s" opacity="0.8"/>'
             % (DESK, W, lit("#7d5a2c", light, 0.55)))
    for _ in range(60):
        yy = rnd.uniform(DESK + 12, H)
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="2" fill="#000000" opacity="%.2f"/>'
                 % (rnd.uniform(-200, W), yy, rnd.uniform(200, 1400), rnd.uniform(0.06, 0.22)))

    # ---- the case
    bx, by = W * 0.255, DESK - H * 0.275
    bw, bh = W * 0.485, H * 0.275
    S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="#000000" opacity="0.60" filter="url(#big)"/>'
             % (bx + bw * 0.56, DESK + 30, bw * 0.60, 52))
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="12" fill="url(#lid)"/>' % (bx, by, bw, bh))
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="16" rx="7" fill="%s" opacity="0.9"/>'
             % (bx, by, bw, lit("#8a8270", light, 0.55)))
    S.append('<rect x="%.0f" y="%.0f" width="16" height="%.0f" fill="%s" opacity="0.6"/>'
             % (bx, by, bh, lit("#6e6858", light, 0.55)))
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="12" fill="none" stroke="#000000" stroke-width="5" opacity="0.5"/>'
             % (bx, by, bw, bh))
    for cx0, cy0 in ((bx + 20, by + 28), (bx + bw - 40, by + 28),
                     (bx + 20, by + bh - 46), (bx + bw - 40, by + bh - 46)):
        S.append('<rect x="%.0f" y="%.0f" width="20" height="20" rx="4" fill="%s" opacity="0.92"/>' % (cx0, cy0, brass))
        S.append('<circle cx="%.0f" cy="%.0f" r="4" fill="#000000" opacity="0.6"/>' % (cx0 + 10, cy0 + 10))

    # bellows folded into the left third
    pleats = 15
    for i in range(pleats):
        px = bx + bw * 0.045 + i * (bw * 0.245) / pleats
        t = i / float(pleats - 1)
        inset = math.sin(t * math.pi) * bh * 0.045
        S.append('<polygon points="%.0f,%.0f %.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="%s"/>'
                 % (px, by + bh * 0.19 + inset, px + bw * 0.0115, by + bh * 0.19 + inset,
                    px + bw * 0.0115, by + bh * 0.88 - inset, px, by + bh * 0.88 - inset,
                    lit("#231e18", light, 0.30)))
        S.append('<rect x="%.0f" y="%.0f" width="3" height="%.0f" fill="%s" opacity="%.2f"/>'
                 % (px + bw * 0.0115, by + bh * 0.19 + inset, bh * 0.69 - inset * 2,
                    lit("#8a7650", light, 0.55), 0.22 + 0.50 * (1 - t)))

    # ---- dials
    for i, (dx, dr) in enumerate(((0.400, 0.034), (0.487, 0.034), (0.567, 0.024))):
        cx0, cy0, r = W * dx, by + bh * 0.42, W * dr
        S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="%s"/>' % (cx0, cy0, r * 1.14, lit("#151310", light, 0.28)))
        S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="#08080a"/>' % (cx0, cy0, r))
        S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="%s" opacity="0.20"/>' % (cx0, cy0, r * 0.94, GOLD))
        S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="none" stroke="%s" stroke-width="6"/>' % (cx0, cy0, r * 1.07, brass))
        for t in range(21):
            a = math.radians(-210 + t * 240 / 20.0)
            r0 = r * (0.68 if t % 5 else 0.56)
            S.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#e2d6bc" stroke-width="%d" opacity="0.85"/>'
                     % (cx0 + math.cos(a) * r0, cy0 + math.sin(a) * r0,
                        cx0 + math.cos(a) * r * 0.86, cy0 + math.sin(a) * r * 0.86, 3 if t % 5 else 2))
        a = math.radians(-210 + (0.30 + i * 0.24) * 240)
        S.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="6" stroke-linecap="round"/>'
                 % (cx0, cy0, cx0 + math.cos(a) * r * 0.76, cy0 + math.sin(a) * r * 0.76, ROSE))
        S.append('<circle cx="%.0f" cy="%.0f" r="7" fill="%s"/>' % (cx0, cy0, brass))
        S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="#ffffff" opacity="0.13" filter="url(#low)" transform="rotate(-30 %.0f %.0f)"/>'
                 % (cx0 - r * 0.30, cy0 - r * 0.38, r * 0.52, r * 0.24, cx0 - r * 0.30, cy0 - r * 0.38))

    # ---- the CRT
    sx0, sy0 = W * 0.612, by + bh * 0.17
    sw0, sh0 = W * 0.112, bh * 0.50
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="16" fill="#04060a"/>' % (sx0, sy0, sw0, sh0))
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="16" fill="url(#crtface)"/>' % (sx0, sy0, sw0, sh0))
    trace = []
    for i in range(140):
        t = i / 139.0
        yy = sy0 + sh0 * (0.52 - 0.32 * math.sin(t * 14.0) * math.exp(-abs(t - 0.40) * 3.2)
                          - 0.045 * math.sin(t * 51.0))
        trace.append("%.1f,%.1f" % (sx0 + sw0 * t, yy))
    tr = " ".join(trace)
    S.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="12" opacity="%.2f" filter="url(#med)"/>' % (tr, MINT, glow(0.60, light)))
    S.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="4" opacity="0.95" filter="url(#low)"/>' % (tr, MINT))
    S.append('<polyline points="%s" fill="none" stroke="#f0fff6" stroke-width="1.8" opacity="0.85"/>' % tr)
    for i in range(int(sh0 / 7)):
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="2" fill="#000000" opacity="0.32"/>' % (sx0, sy0 + i * 7, sw0))
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="16" fill="none" stroke="%s" stroke-width="8"/>'
             % (sx0, sy0, sw0, sh0, brass))
    # the screen throws green back onto the lid around it
    S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#big)"/>'
             % (sx0 + sw0 / 2, sy0 + sh0 / 2, sw0 * 1.15, sh0 * 1.05, MINT, glow(0.26, light)))

    # ---- toggles and lamps along the front edge
    for i in range(10):
        tx = bx + bw * 0.275 + i * bw * 0.048
        ty = by + bh * 0.815
        S.append('<rect x="%.0f" y="%.0f" width="16" height="28" rx="7" fill="%s"/>' % (tx, ty, lit("#312d25", light, 0.35)))
        S.append('<rect x="%.0f" y="%.0f" width="9" height="18" rx="4" fill="%s"/>' % (tx + 3, ty - (12 if i % 3 else -2), brass))
    for i, c in enumerate((ROSE, GOLD, MINT, CYAN)):
        lx0 = bx + bw * 0.770 + i * bw * 0.050
        ly0 = by + bh * 0.805
        S.append('<circle cx="%.0f" cy="%.0f" r="34" fill="%s" opacity="%.2f" filter="url(#med)"/>' % (lx0, ly0, c, glow(0.60, light)))
        S.append('<circle cx="%.0f" cy="%.0f" r="12" fill="%s"/>' % (lx0, ly0, c))
        S.append('<circle cx="%.0f" cy="%.0f" r="12" fill="none" stroke="%s" stroke-width="4"/>' % (lx0, ly0, brass))
    S.append('<text x="%.0f" y="%.0f" font-family="%s" font-size="30" fill="%s" opacity="0.55" letter-spacing="5">%s</text>'
             % (bx + bw * 0.28, by + bh * 0.15, MONO, lit("#c8bda4", light, 0.5), "V-K  MK IV"))

    # ---- the arm, reaching out toward whoever is in the chair
    j1 = (bx + bw * 0.155, by + 10)
    j2 = (W * 0.185, H * 0.300)
    j3 = (W * 0.150, H * 0.470)
    S.append('<path d="M %.0f %.0f L %.0f %.0f L %.0f %.0f" fill="none" stroke="%s" stroke-width="30" stroke-linecap="round" stroke-linejoin="round"/>'
             % (j1[0], j1[1], j2[0], j2[1], j3[0], j3[1], lit("#191715", light, 0.26)))
    S.append('<path d="M %.0f %.0f L %.0f %.0f L %.0f %.0f" fill="none" stroke="%s" stroke-width="8" stroke-linecap="round" stroke-linejoin="round" opacity="0.6"/>'
             % (j1[0] - 5, j1[1] - 7, j2[0] - 6, j2[1] - 7, j3[0] - 6, j3[1], brass))
    for jx, jy in (j1, j2):
        S.append('<circle cx="%.0f" cy="%.0f" r="27" fill="%s"/>' % (jx, jy, lit("#262220", light, 0.3)))
        S.append('<circle cx="%.0f" cy="%.0f" r="27" fill="none" stroke="%s" stroke-width="4" opacity="0.7"/>' % (jx, jy, brass))
        S.append('<circle cx="%.0f" cy="%.0f" r="10" fill="%s"/>' % (jx, jy, brass))

    # ---- the lens head, turned three-quarters toward the frame
    hx, hy = j3
    LR = W * 0.070
    S.append('<g transform="rotate(-16 %.0f %.0f)">' % (hx, hy))
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="18" fill="%s"/>'
             % (hx - LR * 1.05, hy - LR * 1.05, LR * 2.1, LR * 2.1, lit("#1c1a17", light, 0.26)))
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="12" rx="6" fill="%s" opacity="0.75"/>'
             % (hx - LR * 1.05, hy - LR * 1.05, LR * 2.1, lit("#7a7160", light, 0.5)))
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="18" fill="none" stroke="#000000" stroke-width="5" opacity="0.5"/>'
             % (hx - LR * 1.05, hy - LR * 1.05, LR * 2.1, LR * 2.1))
    # barrel rings, stepping in toward the glass
    S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="#0a0a0d"/>' % (hx, hy, LR * 1.02))
    for k, (rr, sw, col) in enumerate(((1.00, 13, lit("#c49a4e", light, 0.5)), (0.86, 10, "#08080a"),
                                       (0.73, 8, lit("#b08a44", light, 0.5)), (0.62, 6, "#08080a"))):
        S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="none" stroke="%s" stroke-width="%d"/>' % (hx, hy, LR * rr, col, sw))
    S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="#04040a"/>' % (hx, hy, LR * 0.54))
    S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="url(#lenscore)"/>' % (hx, hy, LR * 0.54))
    # the iris blades, just readable inside the glass
    for k in range(9):
        a = k * math.tau / 9
        S.append('<path d="M %.1f %.1f L %.1f %.1f L %.1f %.1f Z" fill="#1a0d06" opacity="0.45"/>'
                 % (hx + math.cos(a) * LR * 0.52, hy + math.sin(a) * LR * 0.52,
                    hx + math.cos(a + 0.7) * LR * 0.52, hy + math.sin(a + 0.7) * LR * 0.52,
                    hx + math.cos(a + 0.35) * LR * 0.20, hy + math.sin(a + 0.35) * LR * 0.20))
    S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="url(#lenscore)" opacity="%.2f" filter="url(#med)"/>'
             % (hx, hy, LR * 0.95, glow(0.55, light)))
    S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="#ffffff" opacity="0.45" filter="url(#low)" transform="rotate(-34 %.0f %.0f)"/>'
             % (hx - LR * 0.26, hy - LR * 0.28, LR * 0.20, LR * 0.09, hx - LR * 0.26, hy - LR * 0.28))
    S.append('</g>')

    # ---- the paper trace spilling off the front onto the desk
    px0 = bx + bw * 0.62
    top_pts, bot_pts = [], []
    for i in range(28):
        t = i / 27.0
        xx = px0 + t * W * 0.255
        yy = DESK - H * 0.020 + math.sin(t * 3.3) * H * 0.018 + t * H * 0.055
        top_pts.append((xx, yy)); bot_pts.append((xx, yy + H * 0.055))
    S.append('<polygon points="%s" fill="%s" opacity="0.94"/>'
             % (" ".join("%.1f,%.1f" % q for q in top_pts + list(reversed(bot_pts))),
                lit("#c4b89c", light, 0.65)))
    S.append('<polyline points="%s" fill="none" stroke="#5a1822" stroke-width="4" opacity="0.8"/>'
             % " ".join("%.1f,%.1f" % (q[0], q[1] + H * 0.028 + math.sin(q[0] * 0.021) * H * 0.010) for q in top_pts))
    for i in range(26):
        S.append('<rect x="%.0f" y="%.0f" width="2" height="%.0f" fill="#000000" opacity="0.16"/>'
                 % (px0 + i * W * 0.0098, DESK - H * 0.020 + i * 0.5, H * 0.053))

    # ---- what the instrument throws back into the desk varnish
    S.append('<g filter="url(#smear)" opacity="%.2f">' % glow(0.42, light))
    for cx0, c, wd in ((bx + bw * 0.795, ROSE, 44), (bx + bw * 0.845, GOLD, 44),
                       (bx + bw * 0.895, MINT, 44), (bx + bw * 0.945, CYAN, 44),
                       (sx0 + sw0 * 0.5, MINT, 170), (hx, AMBER, 150)):
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="%s"/>' % (cx0 - wd / 2, DESK, wd, H * 0.13, c))
    S.append('</g>')

    # ---- smoke through the lamp cone, and dust everywhere
    for _ in range(15):
        S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#huge)"/>'
                 % (rnd.uniform(W * 0.10, W * 0.72), rnd.uniform(H * 0.08, DESK),
                    rnd.uniform(200, 660), rnd.uniform(60, 210),
                    rnd.choice([GOLD, "#6a5a48", VIOLET]), rnd.uniform(0.05, 0.14)))
    for _ in range(340):
        S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="#ffeccc" opacity="%.2f"/>'
                 % (rnd.uniform(W * 0.05, W * 0.85), rnd.uniform(H * 0.03, DESK),
                    rnd.uniform(0.9, 3.2), rnd.uniform(0.05, 0.34)))

    S.append(ambient(light))
    S.append(vignette(strength=vig(0.88, light), inner=0.20, color="#04030a"))
    S.append('</svg>')
    return "".join(S)
