import os

# The shell plugin draws live falling rain over the wallpaper, so the painted
# streaks are switched off when rendering plates for it (OW_STREAKS=0). The wet
# ground, reflections and heavy haze stay - only the falling drops go.
DRAW_STREAKS = os.environ.get("OW_STREAKS", "1") != "0"

# Off-World palette - shared by every generator
W, H = 3840, 2400

NIGHT   = "#04060f"
DEEP    = "#0b1020"
NAVY    = "#161d38"
SLATE   = "#1d2a4f"
FG      = "#c5d4f2"

CYAN    = "#00e5ff"
MAGENTA = "#ff5cf0"
ROSE    = "#ff3d6e"
AMBER   = "#ff8a3d"
GOLD    = "#ffc233"
MINT    = "#2bf5a0"
BLUE    = "#4d8cff"
VIOLET  = "#8b5cff"

def hex2rgb(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def rgb2hex(t):
    return '#%02x%02x%02x' % tuple(max(0, min(255, int(round(c)))) for c in t)

def mix(c1, c2, t):
    a, b = hex2rgb(c1), hex2rgb(c2)
    return rgb2hex([a[i] + (b[i] - a[i]) * t for i in range(3)])

def svg_open(w=W, h=H):
    return ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
            'viewBox="0 0 %d %d">' % (w, h, w, h))

def vignette(w=W, h=H, strength=0.62, inner=0.42, color=NIGHT):
    """Radial darkening toward the frame edge."""
    return (
      '<defs><radialGradient id="vig" cx="0.5" cy="0.5" r="0.78">'
      '<stop offset="%.2f" stop-color="%s" stop-opacity="0"/>'
      '<stop offset="0.75" stop-color="%s" stop-opacity="%.2f"/>'
      '<stop offset="1" stop-color="%s" stop-opacity="%.2f"/>'
      '</radialGradient></defs>'
      '<rect width="%d" height="%d" fill="url(#vig)"/>'
      % (inner, color, color, strength * 0.45, color, strength, w, h))


# ---- light levels --------------------------------------------------------
# Every scene is authored for one time of day, and renders only at that level,
# so the wallpaper count stays at two per scene rather than eight.
#
# The table below is what makes a day scene read as daylight instead of as a
# brightened night. It lifts the darkest tones toward an atmospheric haze,
# thins or removes the starfield, pulls the neon glow back so it stops
# carrying the frame, lays an ambient scrim over the whole image and opens the
# vignette up. Noir survives the lift because only the shadows move: the
# highlights stay where they were, so contrast is redistributed rather than
# flattened, and the grade stays desaturated and cold.

LIGHTS = ("dawn", "day", "dusk", "night")

# lift  pulls colours toward `haze`, which is what daylight does to shadow
# sink  pulls them toward black afterwards, which is what deepens a night
# The two are not opposites: dusk uses a little of each, so the air keeps a
# violet cast while the ground drops away.
SINK = "#000206"

_TONE = {
    "night": dict(lift=0.00, sink=0.16, haze="#0a1024", stars=1.00, glow=1.06,
                  fill=None, fill_op=0.00, vig=1.06),
    "dawn": dict(lift=0.13, sink=0.03, haze="#2b2d5c", stars=0.45, glow=0.90,
                 fill="#4c4f92", fill_op=0.06, vig=0.94),
    "day": dict(lift=0.44, sink=0.00, haze="#93a6c6", stars=0.00, glow=0.48,
                fill="#b3c4dc", fill_op=0.17, vig=0.62),
    "dusk": dict(lift=0.07, sink=0.11, haze="#4d2450", stars=0.28, glow=1.08,
                 fill="#5a2748", fill_op=0.05, vig=0.98),
}


def tone(light):
    try:
        return _TONE[light]
    except KeyError:
        raise ValueError("unknown light level %r, want one of %s" % (light, ", ".join(LIGHTS)))


def lit(color, light, k=1.0, haze=None):
    """Grade one colour to the level. k scales the effect locally: k=0 pins a
    colour where it was, k>1 pushes it further. Lift first, then sink, so a
    dusk colour picks up the violet in the air before the frame darkens."""
    t = tone(light)
    c = mix(color, haze or t["haze"], max(0.0, min(1.0, t["lift"] * k)))
    return mix(c, SINK, max(0.0, min(1.0, t["sink"] * k)))


def lit_stops(stops, light, k=1.0, haze=None):
    """Lift a gradient's stop list. Near stops are usually further from the
    viewer's eye than far ones, so callers scale k per band where it matters."""
    return tuple((off, lit(c, light, k, haze)) for off, c in stops)


def stars(n, light):
    """Starfield population. Zero by day, which is the point."""
    return int(round(n * tone(light)["stars"]))


def glow(op, light, k=1.0):
    """Scale a neon glow opacity. Daylight washes neon out; dusk lifts it."""
    return max(0.0, min(1.0, op * (1.0 + (tone(light)["glow"] - 1.0) * k)))


def ambient(light, haze=None, op=None):
    """A flat scrim of atmospheric light over the finished frame. Empty at
    night, where there is nothing in the air to catch the light. Interiors
    pass a smaller `op`: a room has far less air between you and the subject
    than a city block does, so the same scrim there just reads as fog."""
    t = tone(light)
    fill = haze or t["fill"]
    o = t["fill_op"] if op is None else op * (1.0 if t["fill_op"] else 0.0)
    if not fill or o <= 0:
        return ""
    return '<rect width="%d" height="%d" fill="%s" opacity="%.3f"/>' % (W, H, fill, o)


def vig(strength, light):
    """Vignettes close the frame down hard at night and open up by day."""
    return strength * tone(light)["vig"]
