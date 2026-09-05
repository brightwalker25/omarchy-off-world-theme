"""3 - Voight-Kampff: the empathy test, seen from inside the machine."""
import math, random
from palette import *

NAME = "voight-kampff"
LIGHT = "day"
OUTDOOR = False
MONO = "JetBrainsMono Nerd Font,JetBrains Mono,Noto Sans Mono,monospace"


def build(rain=True, light=LIGHT):
    rnd = random.Random(6)
    CX, CY = W * 0.5, H * 0.47
    R_PUPIL = H * 0.115
    R_IRIS = H * 0.375
    S = [svg_open(), '<defs>']

    # An interior, so daylight arrives as room light rather than as sky: the
    # backdrop lifts toward a neutral grey-violet, and the slats below put the
    # actual sun on the wall. The iris keeps its own heat and is never graded.
    ROOM = "#7d7c96"
    # A restrained lift. The frame is mostly instrument housing, and housing
    # that goes pale stops reading as metal - the light has to arrive from the
    # slats and fall off, not fill the whole box evenly.
    bg_stops = (lit_stops((("0", "#101a3d"),), light, k=0.42, haze=ROOM)
                + lit_stops((("0.5", "#080d22"),), light, k=0.30, haze=ROOM)
                + lit_stops((("1", "#02030a"),), light, k=0.14, haze=ROOM))
    S.append('<radialGradient id="bg" cx="0.5" cy="0.47" r="0.72">'
             '<stop offset="0" stop-color="%s"/><stop offset="0.5" stop-color="%s"/>'
             '<stop offset="1" stop-color="%s"/></radialGradient>'
             % tuple(c for _, c in bg_stops))
    S.append('<radialGradient id="irisfill" cx="0.5" cy="0.5" r="0.5">'
             '<stop offset="0.28" stop-color="#ff8a3d" stop-opacity="0.95"/>'
             '<stop offset="0.52" stop-color="#c9502e" stop-opacity="0.75"/>'
             '<stop offset="0.78" stop-color="#2c6a8e" stop-opacity="0.60"/>'
             '<stop offset="1" stop-color="#00e5ff" stop-opacity="0.35"/></radialGradient>')
    S.append('<radialGradient id="corona"><stop offset="0.45" stop-color="%s" stop-opacity="0"/>'
             '<stop offset="0.72" stop-color="%s" stop-opacity="0.30"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (CYAN, CYAN, CYAN))
    S.append('<radialGradient id="pupilfill"><stop offset="0" stop-color="#000206"/>'
             '<stop offset="0.75" stop-color="#04060f"/><stop offset="1" stop-color="#0d1830"/></radialGradient>')
    S.append('<filter id="glowbig" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="70"/></filter>')
    S.append('<filter id="glowmed" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="22"/></filter>')
    S.append('<filter id="glowlow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="6"/></filter>')
    S.append('<clipPath id="pupilclip"><circle cx="%.0f" cy="%.0f" r="%.0f"/></clipPath>' % (CX, CY, R_PUPIL))
    S.append('</defs>')

    S.append('<rect width="%d" height="%d" fill="url(#bg)"/>' % (W, H))

    # ---- venetian slats: the office light that dates the whole scene
    if tone(light)["lift"] > 0.2:
        slat = []
        pitch = H / 22.0
        for i in range(26):
            y = -H * 0.10 + i * pitch
            slat.append('<rect x="%d" y="%.1f" width="%d" height="%.1f"/>' % (-W, y, W * 3, pitch * 0.42))
        band = ('<g transform="rotate(-9 %.0f %.0f)">%s</g>' % (W * 0.5, H * 0.5, "".join(slat)))
        # Cut the slats off toward the right so the light has a direction and a
        # far side, which is what keeps an interior from reading as flat fog.
        S.append('<defs><linearGradient id="slatfall" x1="0" y1="0" x2="1" y2="0.3">'
                 '<stop offset="0" stop-color="#ffffff" stop-opacity="1"/>'
                 '<stop offset="0.55" stop-color="#ffffff" stop-opacity="0.35"/>'
                 '<stop offset="1" stop-color="#ffffff" stop-opacity="0"/></linearGradient>'
                 '<mask id="slatmask"><rect width="%d" height="%d" fill="url(#slatfall)"/></mask></defs>'
                 % (W, H))
        S.append('<g mask="url(#slatmask)">'
                 '<g fill="%s" opacity="0.26" filter="url(#glowbig)">%s</g>'
                 '<g fill="%s" opacity="0.17">%s</g></g>'
                 % (GOLD, band, mix(GOLD, "#ffffff", 0.5), band))

    # ---- instrument grid behind everything
    grid = []
    for gx in range(0, W + 1, 120):
        grid.append('<line x1="%d" y1="0" x2="%d" y2="%d"/>' % (gx, gx, H))
    for gy in range(0, H + 1, 120):
        grid.append('<line x1="0" y1="%d" x2="%d" y2="%d"/>' % (gy, W, gy))
    S.append('<g stroke="%s" stroke-width="1" opacity="%.3f">%s</g>' % (CYAN, 0.055 + tone(light)["lift"] * 0.06, "".join(grid)))

    S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="url(#corona)" opacity="%.2f"/>' % (CX, CY, R_IRIS * 2.4, glow(0.9, light)))
    for gx, gy, gr, gc, go in ((W * 0.10, H * 0.14, 900, GOLD, 0.17), (W * 0.90, H * 0.86, 950, MAGENTA, 0.20),
                               (W * 0.94, H * 0.16, 700, ROSE, 0.11), (W * 0.06, H * 0.88, 800, CYAN, 0.12)):
        S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="%s" opacity="%.2f" filter="url(#glowbig)"/>' % (gx, gy, gr, gc, glow(go, light)))

    # ---- iris fibres: the whole image lives or dies on these
    fib_glow, fib = [], []
    for i in range(1100):
        a = rnd.uniform(0, math.tau)
        jitter = rnd.uniform(-0.012, 0.012)
        r0 = R_PUPIL * rnd.uniform(0.98, 1.10)
        r1 = R_IRIS * rnd.uniform(0.55, 1.02)
        t = (r1 / R_IRIS)
        if t < 0.68:
            col = mix(GOLD, AMBER, rnd.uniform(0, 1))
        elif t < 0.85:
            col = mix(AMBER, ROSE, rnd.uniform(0, 1)) if rnd.random() < 0.35 else mix(AMBER, "#2c6a8e", rnd.uniform(0.2, 0.8))
        else:
            col = mix("#2c6a8e", CYAN, rnd.uniform(0.3, 1))
        x0, y0 = CX + math.cos(a) * r0, CY + math.sin(a) * r0
        x1, y1 = CX + math.cos(a + jitter) * r1, CY + math.sin(a + jitter) * r1
        line = ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f" opacity="%.2f"/>'
                % (x0, y0, x1, y1, col, rnd.uniform(1.2, 5.5), rnd.uniform(0.20, 0.85)))
        fib.append(line)
        if rnd.random() < 0.18:
            fib_glow.append(line)
    S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="url(#irisfill)"/>' % (CX, CY, R_IRIS))
    S.append('<g stroke-linecap="round" filter="url(#glowmed)" opacity="0.75">%s</g>' % "".join(fib_glow))
    S.append('<g stroke-linecap="round">%s</g>' % "".join(fib))

    # radial crypt shadows for depth
    for i in range(46):
        a0 = i * math.tau / 46 + rnd.uniform(-0.02, 0.02)
        w = rnd.uniform(0.02, 0.055)
        S.append('<path d="M %.1f %.1f L %.1f %.1f A %.0f %.0f 0 0 1 %.1f %.1f Z" fill="#120a14" opacity="%.2f"/>'
                 % (CX, CY,
                    CX + math.cos(a0) * R_IRIS, CY + math.sin(a0) * R_IRIS, R_IRIS, R_IRIS,
                    CX + math.cos(a0 + w) * R_IRIS, CY + math.sin(a0 + w) * R_IRIS, rnd.uniform(0.05, 0.22)))

    # ---- limbal ring
    S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="none" stroke="%s" stroke-width="26" opacity="0.55" filter="url(#glowmed)"/>' % (CX, CY, R_IRIS, CYAN))
    S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="none" stroke="%s" stroke-width="7" opacity="0.9"/>' % (CX, CY, R_IRIS, CYAN))
    S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="none" stroke="#0a1424" stroke-width="30" opacity="0.65"/>' % (CX, CY, R_IRIS * 1.045))

    # ---- pupil, with the city reflected in it
    S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="url(#pupilfill)"/>' % (CX, CY, R_PUPIL))
    S.append('<g clip-path="url(#pupilclip)" opacity="0.85">')
    S.append('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" fill="#0a0f26"/>'
             % (CX - R_PUPIL, CY - R_PUPIL, R_PUPIL * 2, R_PUPIL * 2))
    for _ in range(60):
        bx = CX + rnd.uniform(-R_PUPIL, R_PUPIL)
        bh = rnd.uniform(20, R_PUPIL * 0.95)
        S.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#050914"/>'
                 % (bx, CY + R_PUPIL * 0.35 - bh, rnd.uniform(6, 26), bh + 60))
    for _ in range(90):
        S.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" opacity="%.2f"/>'
                 % (CX + rnd.uniform(-R_PUPIL, R_PUPIL), CY + rnd.uniform(-R_PUPIL * 0.6, R_PUPIL * 0.5),
                    rnd.uniform(2, 9), rnd.uniform(2, 16),
                    rnd.choice([CYAN, MAGENTA, GOLD, ROSE]), rnd.uniform(0.3, 1.0)))
    S.append('</g>')
    S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="none" stroke="%s" stroke-width="4" opacity="0.75"/>' % (CX, CY, R_PUPIL, MAGENTA))
    S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="none" stroke="%s" stroke-width="16" opacity="0.45" filter="url(#glowmed)"/>' % (CX, CY, R_PUPIL, MAGENTA))

    # ---- catchlight
    S.append('<ellipse cx="%.0f" cy="%.0f" rx="%.0f" ry="%.0f" fill="#ffffff" opacity="0.55" filter="url(#glowlow)" transform="rotate(-28 %.0f %.0f)"/>'
             % (CX - R_IRIS * 0.42, CY - R_IRIS * 0.46, R_IRIS * 0.17, R_IRIS * 0.09, CX - R_IRIS * 0.42, CY - R_IRIS * 0.46))
    S.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="#dff6ff" opacity="0.35" filter="url(#glowlow)"/>'
             % (CX + R_IRIS * 0.40, CY + R_IRIS * 0.30, R_IRIS * 0.055))

    # ---- HUD
    hud = []
    for r, sw, op in ((R_IRIS * 1.20, 2, 0.30), (R_IRIS * 1.33, 1, 0.18), (R_IRIS * 1.62, 2, 0.14)):
        hud.append('<circle cx="%.0f" cy="%.0f" r="%.0f" fill="none" stroke="%s" stroke-width="%d" opacity="%.2f"/>' % (CX, CY, r, CYAN, sw, op))
    for i in range(96):
        a = i * math.tau / 96
        long_tick = (i % 8 == 0)
        r0 = R_IRIS * 1.20
        r1 = r0 + (46 if long_tick else 20)
        hud.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%d" opacity="%.2f"/>'
                   % (CX + math.cos(a) * r0, CY + math.sin(a) * r0, CX + math.cos(a) * r1, CY + math.sin(a) * r1,
                      CYAN, 4 if long_tick else 2, 0.8 if long_tick else 0.4))
    # sweep arc
    hud.append('<path d="M %.1f %.1f A %.0f %.0f 0 0 1 %.1f %.1f" fill="none" stroke="%s" stroke-width="6" opacity="0.7"/>'
               % (CX + math.cos(-0.55) * R_IRIS * 1.33, CY + math.sin(-0.55) * R_IRIS * 1.33, R_IRIS * 1.33, R_IRIS * 1.33,
                  CX + math.cos(0.62) * R_IRIS * 1.33, CY + math.sin(0.62) * R_IRIS * 1.33, MAGENTA))
    S.append('<g>%s</g>' % "".join(hud))
    S.append('<g filter="url(#glowmed)" opacity="0.5">%s</g>' % "".join(hud))

    # corner brackets
    m, L, sw = 150, 190, 5
    for px, py, dx, dy in ((m, m, 1, 1), (W - m, m, -1, 1), (m, H - m, 1, -1), (W - m, H - m, -1, -1)):
        S.append('<path d="M %d %d h %d M %d %d v %d" stroke="%s" stroke-width="%d" fill="none" opacity="0.55"/>'
                 % (px, py, dx * L, px, py, dy * L, CYAN, sw))

    labels = [
        (m + 30, m + 90, "V-K  //  NEXUS SERIES"), (m + 30, m + 150, "CAPILLARY DILATION ....... 0.0114"),
        (m + 30, m + 210, "FLUCTUATION OF PUPIL ..... UNSTABLE"), (m + 30, m + 270, "BLUSH RESPONSE ........... NEGATIVE"),
        (m + 30, H - m - 130, "TELL ME ABOUT YOUR MOTHER"), (m + 30, H - m - 60, "RESPONSE LATENCY  1.42s"),
    ]
    for lx, ly, txt in labels:
        S.append('<text x="%d" y="%d" font-family="%s" font-size="34" fill="%s" opacity="0.62" letter-spacing="3">%s</text>'
                 % (lx, ly, MONO, CYAN, txt))
    S.append('<text x="%d" y="%d" font-family="%s" font-size="34" fill="%s" opacity="0.75" letter-spacing="3" text-anchor="end">%s</text>'
             % (W - m - 30, H - m - 60, MONO, MAGENTA, "OFF-WORLD"))
    S.append('<text x="%d" y="%d" font-family="%s" font-size="34" fill="%s" opacity="0.5" letter-spacing="3" text-anchor="end">%s</text>'
             % (W - m - 30, m + 90, MONO, CYAN, "ESPER  /  FRAME 4021"))

    # ---- scanlines
    sl = "".join('<rect x="0" y="%d" width="%d" height="2" />' % (y, W) for y in range(0, H, 7))
    S.append('<g fill="#000000" opacity="%.2f">%s</g>' % (0.20 + tone(light)["lift"] * 0.14, sl))

    # ---- weather on the lens
    if rain:
        if DRAW_STREAKS: S.append('<g stroke="#cfe8ff" stroke-linecap="round">%s</g>' % "".join(
            '<line x1="%.0f" y1="%.0f" x2="%.0f" y2="%.0f" stroke-width="%.1f" opacity="%.2f"/>'
            % (x, y, x - ln * 0.12, y + ln, rnd.uniform(1.2, 3.6), rnd.uniform(0.05, 0.20))
            for x, y, ln in ((rnd.uniform(-200, W + 200), rnd.uniform(-200, H), rnd.uniform(60, 300)) for _ in range(1500))))
        for _ in range(120):
            r = rnd.uniform(5, 30)
            x, y = rnd.uniform(0, W), rnd.uniform(0, H)
            S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="none" stroke="%s" stroke-width="%.1f" opacity="%.2f"/>'
                     % (x, y, r, rnd.choice([CYAN, "#9fd8ff"]), r * 0.16, rnd.uniform(0.08, 0.26)))
            S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="#ffffff" opacity="%.2f"/>' % (x - r * 0.32, y - r * 0.32, r * 0.20, rnd.uniform(0.12, 0.38)))
    else:
        for _ in range(260):
            S.append('<circle cx="%.0f" cy="%.0f" r="%.1f" fill="%s" opacity="%.2f"/>'
                     % (rnd.uniform(0, W), rnd.uniform(0, H), rnd.uniform(1.0, 3.4),
                        rnd.choice([CYAN, "#dff6ff", GOLD]), rnd.uniform(0.08, 0.45)))

    S.append(ambient(light, haze="#c8b394", op=0.055))
    S.append(vignette(strength=vig(0.80, light), inner=0.24))
    S.append('</svg>')
    return "".join(S)
