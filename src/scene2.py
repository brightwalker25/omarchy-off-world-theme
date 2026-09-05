"""2 - Off-World Colonies: a colossal sun over the dust, monoliths, a ziggurat."""
import random
from palette import *

NAME = "off-world-colonies"
LIGHT = "day"
OUTDOOR = True
GROUND = int(H * 0.795)


def build(rain=True, light=LIGHT):
    rnd = random.Random(2049)
    # rain cools and mutes the whole grade; clear is full furnace amber
    if rain:
        sky_stops = (("0", "#1d0a18"), ("0.20", "#43141f"), ("0.42", "#7d2a1c"),
                     ("0.62", "#c2521f"), ("0.79", "#e8823a"), ("1", "#8c4a2e"))
        sun, sun2, dust = "#ffc98a", "#ff6f2e", "#cf8a56"
        ground_top, ground_bot = "#43241a", "#120a0e"
    else:
        sky_stops = (("0", "#2a0d08"), ("0.20", "#5c1c0c"), ("0.42", "#9c3a10"),
                     ("0.62", "#e0691a"), ("0.78", "#ffab3d"), ("1", "#ffd07a"))
        sun, sun2, dust = "#fff0c0", "#ff9b2e", "#e8a45c"
        ground_top, ground_bot = "#7a3a18", "#1a0b06"

    # This scene is already the furnace of the set, so it grades against its own
    # warm haze rather than the cold default. The sky barely moves - lifting it
    # toward blue would put out the sun - and almost all of the daylight goes
    # into the shadows on the ground, which is where a lit frame differs from a
    # dark one anyway.
    WARM = "#f0c288"
    sky_stops = lit_stops(sky_stops, light, k=0.22, haze=WARM)
    ground_top = lit(ground_top, light, k=0.85, haze=dust)
    ground_bot = lit(ground_bot, light, k=0.70, haze=dust)

    S = [svg_open(), '<defs>']
    S.append('<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">%s</linearGradient>'
             % "".join('<stop offset="%s" stop-color="%s"/>' % s for s in sky_stops))
    S.append('<radialGradient id="sundisc"><stop offset="0" stop-color="%s" stop-opacity="1"/>'
             '<stop offset="0.30" stop-color="%s" stop-opacity="0.95"/>'
             '<stop offset="0.62" stop-color="%s" stop-opacity="0.35"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (sun, sun2, sun2, sun2))
    S.append('<radialGradient id="halo"><stop offset="0" stop-color="%s" stop-opacity="0.55"/>'
             '<stop offset="0.5" stop-color="%s" stop-opacity="0.18"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (sun2, sun2, sun2))
    S.append('<linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="0.45" stop-color="%s"/>'
             '<stop offset="1" stop-color="%s"/></linearGradient>'
             % (ground_top, mix(ground_top, ground_bot, 0.6), ground_bot))
    S.append('<linearGradient id="dustveil" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s" stop-opacity="0"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0.85"/></linearGradient>' % (dust, dust))
    S.append('<filter id="bigblur" x="-45%" y="-45%" width="190%" height="190%"><feGaussianBlur stdDeviation="120"/></filter>')
    S.append('<filter id="medblur" x="-45%" y="-45%" width="190%" height="190%"><feGaussianBlur stdDeviation="34"/></filter>')
    S.append('<filter id="lowblur" x="-45%" y="-45%" width="190%" height="190%"><feGaussianBlur stdDeviation="9"/></filter>')
    S.append('<filter id="smear" x="-25%" y="-10%" width="150%" height="125%"><feGaussianBlur stdDeviation="14 54"/></filter>')
    S.append('</defs>')

    S.append('<rect width="%d" height="%d" fill="url(#sky)"/>' % (W, H))

    # ---- the sun: a furnace sitting just above the dust line
    sx, sy, sr = W * 0.285, GROUND - H * 0.335, H * 0.255
    S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="url(#halo)"/>' % (sx, sy, sr * 2.6))
    S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="url(#sundisc)"/>' % (sx, sy, sr))
    S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="%s" opacity="%.2f"/>' % (sx, sy, sr * 0.40, sun, 0.75 if rain else 0.95))

    # ---- dust strata, drawn across the sun to sell the haze
    for i in range(16):
        y = GROUND - H * 0.60 + i * H * 0.040 + rnd.uniform(-16, 16)
        S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#medblur)"/>'
                 % (rnd.uniform(W * 0.1, W * 0.9), y, rnd.uniform(900, 2400), rnd.uniform(16, 58), dust, rnd.uniform(0.06, 0.24)))

    # ---- silhouettes, far to near, each dimmed by the dust between it and us
    def band(depth, base_y, n, wmin, wmax, hmin, hmax, kind):
        """depth 0 = furthest. Colour lerps from dust toward near-black."""
        col = lit(mix(dust, "#160a06", 0.30 + depth * 0.24), light, k=0.65 - depth * 0.15, haze=dust)
        op = 0.52 + depth * 0.15
        out = []
        for _ in range(n):
            x = rnd.uniform(-200, W); w = rnd.uniform(wmin, wmax); h = rnd.uniform(hmin, hmax)
            if kind == "block":
                out.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f"/>' % (x, base_y - h, w, h + 400))
                if rnd.random() < 0.5:   # setback crown
                    out.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f"/>'
                               % (x + w * 0.2, base_y - h - h * 0.18, w * 0.6, h * 0.2))
            else:                        # colossus: a standing figure abstracted to slabs
                bw = w * 0.55
                out.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f"/>' % (x, base_y - h * 0.62, bw, h * 0.62 + 400))
                out.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f"/>'
                           % (x - w * 0.10, base_y - h, bw * 1.35, h * 0.42))
                out.append('<circle cx="%.0f" cy="%.0f" r="%.0f"/>' % (x + bw * 0.5, base_y - h - w * 0.14, w * 0.20))
        return '<g fill="%s" opacity="%.2f">%s</g>' % (col, op, "".join(out))

    S.append(band(0, GROUND - H * 0.035, 22, 60, 190, 120, 460, "block"))
    S.append('<rect x="0" y="%d" width="%d" height="%d" fill="url(#dustveil)" opacity="0.55"/>' % (int(H * 0.35), W, GROUND - int(H * 0.35)))
    S.append(band(1, GROUND - H * 0.015, 14, 90, 260, 200, 700, "block"))
    S.append(band(1, GROUND - H * 0.015, 5, 150, 300, 420, 900, "colossus"))
    S.append('<rect x="0" y="%d" width="%d" height="%d" fill="url(#dustveil)" opacity="0.40"/>' % (int(H * 0.40), W, GROUND - int(H * 0.40)))

    # ---- the ziggurat: the one structure that dominates the frame
    zx, zw = W * 0.80, W * 0.40
    zt, zb = GROUND - H * 0.62, GROUND + 60
    steps = 7
    zig = []
    for i in range(steps):
        t0, t1 = i / float(steps), (i + 1) / float(steps)
        y0 = zt + (zb - zt) * t0
        hw0 = zw * 0.5 * (0.16 + 0.84 * t0)
        hw1 = zw * 0.5 * (0.16 + 0.84 * t1)
        zig.append('<polygon points="%.0f,%.0f %.0f,%.0f %.0f,%.0f %.0f,%.0f"/>'
                   % (zx - hw0, y0, zx + hw0, y0, zx + hw1, zt + (zb - zt) * t1, zx - hw1, zt + (zb - zt) * t1))
        zig.append('<rect x="%.0f" y="%.0f" width="%.0f" height="14"/>' % (zx - hw1 - 12, zt + (zb - zt) * t1 - 8, hw1 * 2 + 24))
    S.append('<g fill="%s" opacity="0.95">%s</g>' % (lit("#1a0b07", light, 0.5, haze=dust), "".join(zig)))
    # rim light where the sun grazes the left face
    S.append('<polygon points="%.0f,%.0f %.0f,%.0f %.0f,%.0f" fill="%s" opacity="%.2f" filter="url(#lowblur)"/>'
             % (zx - zw * 0.08, zt, zx - zw * 0.5, zb, zx - zw * 0.42, zb, sun, 0.30 if rain else 0.5))
    # beacon
    S.append('<circle cx="%.0f" cy="%.0f" r="16" fill="%s"/>' % (zx, zt - 10, ROSE))
    S.append('<circle cx="%.0f" cy="%.0f" r="60" fill="%s" opacity="0.7" filter="url(#medblur)"/>' % (zx, zt - 10, ROSE))

    S.append(band(2, GROUND + H * 0.01, 9, 130, 340, 260, 820, "block"))

    # ---- ground
    S.append('<rect x="0" y="%d" width="%d" height="%d" fill="url(#ground)"/>' % (GROUND, W, H - GROUND))
    S.append('<rect x="0" y="%d" width="%d" height="200" fill="%s" opacity="%.2f" filter="url(#bigblur)"/>'
             % (GROUND - 100, W, dust, 0.34 if rain else 0.42))
    # long shadows thrown toward the viewer by the low sun
    S.append('<g filter="url(#medblur)">')
    for _ in range(18):
        bx = rnd.uniform(-200, W + 200)
        skew = (bx - sx) * 0.30
        sw_ = rnd.uniform(90, 340)
        S.append('<polygon points="%.0f,%d %.0f,%d %.0f,%d %.0f,%d" fill="#170a06" opacity="%.2f"/>'
                 % (bx, GROUND, bx + sw_, GROUND, bx + sw_ + skew, H, bx + skew, H, rnd.uniform(0.07, 0.18)))
    S.append('</g>')
    # dust drifts and debris scattered across the plain
    for _ in range(34):
        y = rnd.uniform(GROUND, H)
        d = (y - GROUND) / max(1.0, H - GROUND)
        S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#medblur)"/>'
                 % (rnd.uniform(0, W), y, rnd.uniform(200, 900) * (0.5 + d), rnd.uniform(10, 40) * (0.5 + d),
                    rnd.choice([dust, ground_top, sun]), rnd.uniform(0.05, 0.20)))
    for _ in range(120):
        y = rnd.uniform(GROUND + 20, H)
        d = (y - GROUND) / max(1.0, H - GROUND)
        S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="#1c0d07" opacity="%.2f"/>'
                 % (rnd.uniform(0, W), y, rnd.uniform(4, 26) * (0.4 + d), rnd.uniform(2, 9) * (0.4 + d), rnd.uniform(0.15, 0.5)))
    # sun glare smeared down the wet or dusty plain
    S.append('<rect x="%.0f" y="%d" width="%.0f" height="%d" fill="%s" opacity="%.2f" filter="url(#smear)"/>'
             % (sx - 160, GROUND, 320, int(H * 0.18), sun, 0.45 if rain else 0.22))
    S.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s" opacity="%.2f" filter="url(#bigblur)"/>'
             % (GROUND - 20, W, int((H - GROUND) * 0.75), dust, 0.22 if rain else 0.28))
    # scale figure
    fx, fy, fh = W * 0.155, GROUND + H * 0.052, H * 0.055
    S.append('<g fill="#0d0604" opacity="0.92">'
             '<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="%.0f"/>'
             '<circle cx="%.0f" cy="%.0f" r="%.0f"/></g>'
             % (fx, fy - fh * 0.72, fh * 0.30, fh * 0.72, fh * 0.10,
                fx + fh * 0.15, fy - fh * 0.86, fh * 0.145))
    S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="9" fill="#0d0604" opacity="0.5" filter="url(#lowblur)"/>' % (fx + fh * 0.15, fy + 4, fh * 0.5))

    # ---- traffic in the sky
    for _ in range(11):
        x = rnd.uniform(0, W); y = rnd.uniform(H * 0.06, GROUND - H * 0.30); ln = rnd.uniform(30, 150)
        S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="4" fill="#20100a" opacity="%.2f"/>'
                 % (x, y, ln, rnd.uniform(5, 12), rnd.uniform(0.35, 0.8)))

    # ---- weather
    if rain:
        drops = ['<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke-width="%.1f" opacity="%.2f"/>'
                 % (x, y, x - ln * 0.13, y + ln, rnd.uniform(1.2, 3.4), rnd.uniform(0.05, 0.24))
                 for x, y, ln in ((rnd.uniform(-250, W + 250), rnd.uniform(-250, H), rnd.uniform(60, 280)) for _ in range(1900))]
        if DRAW_STREAKS: S.append('<g stroke="#ffe0c0" stroke-linecap="round">%s</g>' % "".join(drops))
        for _ in range(7):
            S.append('<rect x="%.0f" y="0" width="%.0f" height="%d" fill="%s" opacity="%.2f" filter="url(#bigblur)"/>'
                     % (rnd.uniform(-200, W), rnd.uniform(300, 900), H, dust, rnd.uniform(0.06, 0.18)))
        S.append('<g filter="url(#smear)" opacity="0.55">')
        for _ in range(40):
            S.append('<rect x="%.0f" y="%d" width="%.0f" height="%.0f" fill="%s" opacity="%.2f"/>'
                     % (rnd.uniform(0, W), GROUND, rnd.uniform(60, 300), rnd.uniform(200, 700),
                        rnd.choice([sun, dust, "#2a1410"]), rnd.uniform(0.10, 0.35)))
        S.append('</g>')
        for _ in range(170):
            y = rnd.uniform(GROUND, H)
            d = (y - GROUND) / max(1.0, H - GROUND)
            S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f"/>'
                     % (rnd.uniform(0, W), y, rnd.uniform(20, 150) * (0.4 + d), 2 + d * 4, sun, rnd.uniform(0.08, 0.30)))
    else:
        for _ in range(900):
            S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="%s" opacity="%.2f"/>'
                     % (rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(1.0, 4.5),
                        rnd.choice([sun, dust, "#ffd9a0"]), rnd.uniform(0.06, 0.42)))
        for _ in range(10):
            S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="%s" opacity="%.2f" filter="url(#bigblur)"/>'
                     % (rnd.uniform(0, W), rnd.uniform(H * 0.25, H * 0.9), rnd.uniform(600, 1600),
                        rnd.uniform(80, 240), dust, rnd.uniform(0.08, 0.22)))

    S.append(ambient(light, haze="#e6c49b"))
    S.append(vignette(strength=vig(0.66, light), inner=0.30, color=lit("#14070a", light, 0.5, haze=dust)))
    S.append('</svg>')
    return "".join(S)
