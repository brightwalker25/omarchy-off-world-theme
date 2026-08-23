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
