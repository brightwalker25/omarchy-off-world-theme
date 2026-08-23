"""6 - Joi: a hologram the size of a building, standing over the rain."""
import math, random
from palette import *

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

    # ---- the hologram: a standing figure abstracted to light
    top, bot = H * 0.075, HZ + H * 0.015
    hh = bot - top
    hw = W * 0.082
    hd = hw * 0.36                       # head radius
    sy = top + hd * 1.95                 # shoulder line
    wy = top + hh * 0.40                 # waist

    figure = (
        'M %.1f %.1f '
        'C %.1f %.1f %.1f %.1f %.1f %.1f '          # shoulder -> waist, left
        'C %.1f %.1f %.1f %.1f %.1f %.1f '          # waist -> hem, left
        'L %.1f %.1f '
        'C %.1f %.1f %.1f %.1f %.1f %.1f '          # hem -> waist, right
        'C %.1f %.1f %.1f %.1f %.1f %.1f Z'         # waist -> shoulder, right
        % (HX - hw * 0.62, sy,
           HX - hw * 0.70, sy + hh * 0.10, HX - hw * 0.46, sy + hh * 0.14, HX - hw * 0.40, wy,
           HX - hw * 0.62, wy + hh * 0.22, HX - hw * 0.78, bot - hh * 0.16, HX - hw * 1.18, bot,
           HX + hw * 0.94, bot,
           HX + hw * 0.78, bot - hh * 0.16, HX + hw * 0.62, wy + hh * 0.22, HX + hw * 0.40, wy,
           HX + hw * 0.46, sy + hh * 0.14, HX + hw * 0.70, sy + hh * 0.10, HX + hw * 0.62, sy))

    fig = ('<path d="%s"/><circle cx="%.1f" cy="%.1f" r="%.1f"/>'
           '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>'
           % (figure, HX, top + hd, hd, HX - hd * 0.34, top + hd * 1.5, hd * 0.68, hd * 1.2))
    # arms held close, drawn as tapered strokes
    arms = ('<path d="M %.1f %.1f C %.1f %.1f %.1f %.1f %.1f %.1f" fill="none" stroke-width="%.1f" stroke-linecap="round"/>'
            '<path d="M %.1f %.1f C %.1f %.1f %.1f %.1f %.1f %.1f" fill="none" stroke-width="%.1f" stroke-linecap="round"/>'
            % (HX - hw * 0.60, sy + hh * 0.02, HX - hw * 0.92, sy + hh * 0.12,
               HX - hw * 0.80, wy + hh * 0.02, HX - hw * 0.52, wy + hh * 0.10, hw * 0.16,
               HX + hw * 0.60, sy + hh * 0.02, HX + hw * 0.92, sy + hh * 0.12,
               HX + hw * 0.80, wy + hh * 0.02, HX + hw * 0.52, wy + hh * 0.10, hw * 0.16))

    S.append('<defs><clipPath id="figclip"><path d="%s"/><circle cx="%.1f" cy="%.1f" r="%.1f"/>'
             '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></clipPath></defs>'
             % (figure, HX, top + hd, hd, HX - hd * 0.34, top + hd * 1.5, hd * 0.68, hd * 1.2))

    S.append('<g fill="url(#holo)" opacity="0.85" filter="url(#big)">%s</g>' % fig)
    S.append('<g fill="url(#holo)" opacity="0.60" filter="url(#med)">%s</g>' % fig)
    S.append('<g stroke="url(#holo)" opacity="0.32" filter="url(#med)">%s</g>' % arms)
    S.append('<g fill="url(#holo)" opacity="0.45">%s</g>' % fig)
    S.append('<g stroke="%s" opacity="0.22">%s</g>' % (mix(MAGENTA, "#ffffff", 0.3), arms))
    # rim light along the silhouette
    S.append('<g fill="none" stroke="%s" stroke-width="4" opacity="0.55" filter="url(#low)">'
             '<path d="%s"/></g>' % (mix(MAGENTA, "#ffffff", 0.55), figure))

    # scan structure, clipped so it never overhangs her
    S.append('<g clip-path="url(#figclip)">')
    S.append('<g fill="#04040e" opacity="0.42">%s</g>' % "".join(
        '<rect x="%.0f" y="%.1f" width="%.0f" height="%.1f"/>'
        % (HX - hw * 1.6, top + i * (hh / 110.0), hw * 3.2, (hh / 110.0) * 0.45) for i in range(110)))
    for _ in range(6):
        y = top + hh * rnd.uniform(0.04, 0.96)
        S.append('<rect x="%.0f" y="%.1f" width="%.0f" height="%.1f" fill="%s" opacity="%.2f"/>'
                 % (HX - hw * 1.6, y, hw * 3.2, rnd.uniform(5, 16), mix(MAGENTA, "#ffffff", 0.75), rnd.uniform(0.18, 0.40)))
    S.append('</g>')
    # one glitch slice offset sideways, outside the clip, sells the projection
    gy = top + hh * 0.52
    S.append('<g opacity="0.35" transform="translate(%.0f,0)"><g clip-path="url(#figclip)">'
             '<rect x="%.0f" y="%.1f" width="%.0f" height="%.1f" fill="%s"/></g></g>'
             % (hw * 0.22, HX - hw * 1.6, gy, hw * 3.2, hh * 0.035, CYAN))

    # projector shafts rising past her
    for dx in (-1, 1):
        S.append('<polygon points="%.0f,%.0f %.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="url(#shaft)" opacity="0.45" filter="url(#big)"/>'
                 % (HX + dx * hw * 0.2, top, HX + dx * hw * 1.5, top, HX + dx * hw * 2.6, bot, HX + dx * hw * 0.5, bot))

    # ---- ground
    S.append('<rect x="0" y="%d" width="%d" height="%d" fill="url(#ground)"/>' % (HZ + 60, W, H - HZ - 60))
    S.append('<rect x="0" y="%d" width="%d" height="140" fill="%s" opacity="0.30" filter="url(#huge)"/>' % (HZ, W, MAGENTA))
    S.append('<g filter="url(#smear)" opacity="%.2f">'
             '<rect x="%.0f" y="%d" width="%.0f" height="%d" fill="%s"/></g>'
             % (0.75 if rain else 0.35, HX - hw * 1.3, HZ + 60, hw * 2.6, int(H * 0.22), MAGENTA))
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
