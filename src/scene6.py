"""6 - Unicorn: Gaff's folded unicorn, projected over the city."""
import math, random
from palette import *
import origami

NAME = "hologram"


def build(rain=True):
    rnd = random.Random(2022)
    HZ = int(H * 0.80)
    S = [svg_open(), '<defs>']
    S.append('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#03040e"/><stop offset="0.30" stop-color="#0a0c2a"/>'
             '<stop offset="0.56" stop-color="#1e1046" stop-opacity="1"/>'
             '<stop offset="0.78" stop-color="#4a1550"/><stop offset="1" stop-color="#0c0a20"/></linearGradient>')
    S.append('<linearGradient id="holo" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s" stop-opacity="0.05"/>'
             '<stop offset="0.18" stop-color="%s" stop-opacity="0.55"/>'
             '<stop offset="0.55" stop-color="%s" stop-opacity="0.85"/>'
             '<stop offset="0.88" stop-color="%s" stop-opacity="0.45"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0.05"/></linearGradient>' % (MAGENTA, MAGENTA, ROSE, MAGENTA, MAGENTA))
    S.append('<linearGradient id="shaft" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s" stop-opacity="0.42"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0"/></linearGradient>' % (MAGENTA, MAGENTA))
    S.append('<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="#3a1246" stop-opacity="0.85"/>'
             '<stop offset="0.4" stop-color="#0c0a22"/><stop offset="1" stop-color="#03040e"/></linearGradient>')
    S.append('<radialGradient id="bloom"><stop offset="0" stop-color="%s" stop-opacity="0.55"/>'
             '<stop offset="0.5" stop-color="%s" stop-opacity="0.16"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (MAGENTA, MAGENTA, MAGENTA))
    S.append('<filter id="huge" x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="150"/></filter>')
    S.append('<filter id="big" x="-70%" y="-70%" width="240%" height="240%"><feGaussianBlur stdDeviation="55"/></filter>')
    S.append('<filter id="med" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="18"/></filter>')
    S.append('<filter id="low" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6"/></filter>')
    S.append('<filter id="smear" x="-30%" y="-10%" width="160%" height="130%"><feGaussianBlur stdDeviation="26 80"/></filter>')
    S.append('</defs>')
    S.append('<rect width="%d" height="%d" fill="url(#sky)"/>' % (W, H))

    if not rain:
        for _ in range(380):
            y = rnd.uniform(0, H * 0.5)
            S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="#e0ecff" opacity="%.2f"/>'
                     % (rnd.uniform(0, W), y, rnd.uniform(0.9, 2.8), rnd.uniform(0.08, 0.7) * (1 - y / (H * 0.6))))

    # cyan counter-light from the left keeps the frame from going all magenta
    S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="0.30" filter="url(#huge)"/>'
             % (W * 0.06, H * 0.62, 900, 700, CYAN))

    HX = W * 0.615
    S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="url(#bloom)"/>' % (HX, H * 0.44, H * 0.62))

    # ---- far skyline, dwarfed
    for depth, (base, hmin, hmax, wmin, wmax, col, op) in enumerate((
            (HZ - 40, 120, 520, 50, 150, "#14103a", 0.75),
            (HZ + 10, 220, 820, 80, 220, "#0b0a24", 0.9),
            (HZ + 90, 320, 1050, 120, 300, "#060616", 1.0))):
        x = -250; body = []
        while x < W + 250:
            w = rnd.uniform(wmin, wmax); h = rnd.uniform(hmin, hmax)
            body.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f"/>' % (x, base - h, w, h + 500))
            if rnd.random() < 0.3:
                body.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f"/>' % (x + w * 0.45, base - h - rnd.uniform(40, 200), max(4.0, w * 0.05), 220))
            for _ in range(int(h / 55)):
                if rnd.random() < 0.45:
                    body.append('<rect x="%.0f" y="%.0f" width="6" height="10" fill="%s" opacity="%.2f"/>'
                                % (x + rnd.uniform(6, max(7.0, w - 10)), base - rnd.uniform(10, h),
                                   rnd.choice([GOLD, CYAN, "#dfe9ff"]), rnd.uniform(0.25, 0.9)))
            x += w * rnd.uniform(0.95, 1.5)
        S.append('<g fill="%s" opacity="%.2f">%s</g>' % (col, op, "".join(body)))

    # ---- the hologram: a folded unicorn, rearing, projected over the skyline
    top, bot = H * 0.055, HZ + H * 0.02
    uh = bot - top
    k = uh / 112.0                      # unit space runs y -10..100
    ux = HX - 56.0 * k                  # unit x spans ~13..99, centre 56
    uy = top + 10.0 * k
    XF = 'translate(%.2f,%.2f) scale(%.4f)' % (ux, uy, k)

    fig = origami.facets_svg(body=MAGENTA, edge=mix(MAGENTA, "#ffffff", 0.65), edge_w=0.5)
    sil = origami.silhouette()

    S.append('<defs><clipPath id="uniclip" clipPathUnits="userSpaceOnUse">'
             '<g transform="%s"><path d="%s"/></g></clipPath></defs>' % (XF, sil))

    # bloom passes, then the crisp folds
    S.append('<g transform="%s" filter="url(#big)" opacity="0.85"><path d="%s" fill="%s" opacity="0.9"/></g>'
             % (XF, sil, MAGENTA))
    S.append('<g transform="%s" filter="url(#med)" opacity="0.55"><path d="%s" fill="%s"/></g>'
             % (XF, sil, ROSE))
    S.append('<g transform="%s" opacity="0.92">%s</g>' % (XF, fig))
    # rim light along the folded edge
    S.append('<g transform="%s" filter="url(#low)" opacity="0.5">'
             '<path d="%s" fill="none" stroke="%s" stroke-width="0.7"/></g>'
             % (XF, sil, mix(MAGENTA, "#ffffff", 0.7)))

    # scan structure, clipped to the unicorn so it never overhangs
    S.append('<g clip-path="url(#uniclip)">')
    S.append('<g fill="#04040e" opacity="0.40">%s</g>' % "".join(
        '<rect x="0" y="%.1f" width="%d" height="%.1f"/>' % (top + i * (uh / 120.0), W, (uh / 120.0) * 0.45)
        for i in range(120)))
    for _ in range(6):
        y = top + uh * rnd.uniform(0.04, 0.96)
        S.append('<rect x="0" y="%.1f" width="%d" height="%.1f" fill="%s" opacity="%.2f"/>'
                 % (y, W, rnd.uniform(5, 16), mix(MAGENTA, "#ffffff", 0.75), rnd.uniform(0.18, 0.40)))
    S.append('</g>')
    # a slice offset sideways: the projection stuttering
    S.append('<g opacity="0.32" transform="translate(%.0f,0)"><g clip-path="url(#uniclip)">'
             '<rect x="0" y="%.1f" width="%d" height="%.1f" fill="%s"/></g></g>'
             % (uh * 0.02, top + uh * 0.52, W, uh * 0.03, CYAN))

    # projector shafts rising past it
    for dx in (-1, 1):
        S.append('<polygon points="%.0f,%.0f %.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="url(#shaft)" opacity="0.42" filter="url(#big)"/>'
                 % (HX + dx * W * 0.020, top, HX + dx * W * 0.075, top,
                    HX + dx * W * 0.130, bot, HX + dx * W * 0.030, bot))

    # ---- ground
    S.append('<rect x="0" y="%d" width="%d" height="%d" fill="url(#ground)"/>' % (HZ + 60, W, H - HZ - 60))
    S.append('<rect x="0" y="%d" width="%d" height="140" fill="%s" opacity="0.30" filter="url(#huge)"/>' % (HZ, W, MAGENTA))
    S.append('<g filter="url(#smear)" opacity="%.2f">'
             '<rect x="%.0f" y="%d" width="%.0f" height="%d" fill="%s"/></g>'
             % (0.75 if rain else 0.35, HX - uh * 0.22, HZ + 60, uh * 0.44, int(H * 0.22), MAGENTA))
    for _ in range(260 if rain else 80):
        y = rnd.uniform(HZ + 70, H); d = (y - HZ - 70) / max(1.0, H - HZ - 70)
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="2" fill="%s" opacity="%.2f"/>'
                 % (rnd.uniform(0, W), y, rnd.uniform(40, 300) * (0.35 + d), 2 + d * 5,
                    rnd.choice([MAGENTA, ROSE, CYAN, "#dfe9ff"]), rnd.uniform(0.06, 0.32)))

    if rain:
        if DRAW_STREAKS: S.append('<g stroke="#e4f1ff" stroke-linecap="round">%s</g>' % "".join(
            '<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke-width="%.1f" opacity="%.2f"/>'
            % (x, y, x - ln * 0.15, y + ln, rnd.uniform(1.1, 3.2), rnd.uniform(0.05, 0.24))
            for x, y, ln in ((rnd.uniform(-250, W + 250), rnd.uniform(-250, H), rnd.uniform(60, 300)) for _ in range(2200))))
        if DRAW_STREAKS: S.append('<g stroke="#ffffff" stroke-linecap="round" filter="url(#low)">%s</g>' % "".join(
            '<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke-width="%.1f" opacity="%.2f"/>'
            % (x, y, x - ln * 0.15, y + ln, rnd.uniform(4, 11), rnd.uniform(0.05, 0.15))
            for x, y, ln in ((rnd.uniform(-250, W + 250), rnd.uniform(-250, H), rnd.uniform(200, 650)) for _ in range(80))))
    else:
        for _ in range(10):
            S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#huge)"/>'
                     % (rnd.uniform(0, W), rnd.uniform(H * 0.3, H * 0.9), rnd.uniform(600, 1500),
                        rnd.uniform(80, 220), rnd.choice([MAGENTA, VIOLET]), rnd.uniform(0.06, 0.16)))
        for _ in range(300):
            S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="%s" opacity="%.2f"/>'
                     % (rnd.uniform(0, W), rnd.uniform(H * 0.15, H), rnd.uniform(1.2, 4.0),
                        rnd.choice([MAGENTA, ROSE, GOLD, "#ffd9f2"]), rnd.uniform(0.10, 0.5)))

    S.append(vignette(strength=0.74, inner=0.28))
    S.append('</svg>')
    return "".join(S)
