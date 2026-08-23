"""Overlay for the theme-switcher preview: a mock desktop over a wallpaper."""
import sys
from palette import *

MONO = "JetBrainsMono Nerd Font,JetBrains Mono,Noto Sans Mono,monospace"
PW, PH = 1800, 1012

SWATCHES = [
    ("red", ROSE), ("orange", AMBER), ("yellow", GOLD), ("green", MINT),
    ("cyan", CYAN), ("blue", BLUE), ("magenta", MAGENTA), ("fg", "#c5d4f2"),
    ("br red", "#ff6f92"), ("br orange", "#ffab6e"), ("br yellow", "#ffd75e"), ("br green", "#74ffc4"),
    ("br cyan", "#7af2ff"), ("br blue", "#87b4ff"), ("br magenta", "#ff92f5"), ("br fg", "#f0f6ff"),
]

TERM = [
    [("#5c6d96", "user"), ("#00e5ff", "@"), ("#ff5cf0", "nexus"), ("#5c6d96", " ~/work "), ("#ffc233", "main"), ("#c5d4f2", " $ ")],
    [("#c5d4f2", "omarchy theme set off-world")],
    [("#2bf5a0", "  applied "), ("#c5d4f2", "Off-World"), ("#5c6d96", "  ->  12 backgrounds, 23 icons")],
    [],
    [("#5c6d96", "user"), ("#00e5ff", "@"), ("#ff5cf0", "nexus"), ("#5c6d96", " ~/work "), ("#ffc233", "main"), ("#c5d4f2", " $ ")],
    [("#c5d4f2", "omarchy-off-world-bg --status")],
    [("#5c6d96", "  rain     : "), ("#4d8cff", "yes"), ("#5c6d96", "  (random 50% in 3h spells)")],
    [("#5c6d96", "  time     : "), ("#ff8a3d", "night"), ("#5c6d96", " (23:41)")],
    [("#5c6d96", "  wallpaper: "), ("#ff5cf0", "1-spinner-descent-rain.jpg")],
    [],
    [("#5c6d96", "user"), ("#00e5ff", "@"), ("#ff5cf0", "nexus"), ("#5c6d96", " ~/work "), ("#ffc233", "main"), ("#c5d4f2", " $ "), ("#f0f6ff", "█")],
]

S = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (PW, PH, PW, PH)]
S.append('<defs><linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">'
         '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
         '<filter id="sh" x="-30%%" y="-30%%" width="160%%" height="160%%">'
         '<feGaussianBlur stdDeviation="22"/></filter></defs>' % (MAGENTA, CYAN))

# ---- bar
BH = 38
S.append('<rect x="0" y="0" width="%d" height="%d" fill="#070b18" opacity="0.93"/>' % (PW, BH))
for i, (lab, col) in enumerate((("1", CYAN), ("2", "#3c4c78"), ("3", "#3c4c78"), ("4", "#3c4c78"))):
    S.append('<rect x="%d" y="9" width="30" height="20" rx="6" fill="%s" opacity="%.2f"/>'
             % (18 + i * 36, col, 0.9 if i == 0 else 0.30))
S.append('<text x="%d" y="26" font-family="%s" font-size="17" fill="%s" opacity="0.85">%s</text>'
         % (186, MONO, "#c5d4f2", "off-world — nexus"))
right = [(" 87%", MINT), ("", CYAN), ("", "#c5d4f2"), ("23:41", "#f0f6ff")]
x = PW - 24
for txt, col in reversed(right):
    w = len(txt) * 11 + 14
    x -= w
    S.append('<text x="%d" y="26" font-family="%s" font-size="17" fill="%s">%s</text>' % (x, MONO, col, txt))

def window(x, y, w, h, title, accent=CYAN):
    o = ['<rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="#04060f" opacity="0.55" filter="url(#sh)"/>' % (x + 6, y + 10, w, h),
         '<rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="#0b1020" opacity="0.96"/>' % (x, y, w, h),
         '<rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="none" stroke="url(#edge)" stroke-width="2.5"/>' % (x, y, w, h),
         '<rect x="%d" y="%d" width="%d" height="34" fill="#070b18" opacity="0.9"/>' % (x + 2, y + 2, w - 4),
         '<text x="%d" y="%d" font-family="%s" font-size="16" fill="%s" opacity="0.8">%s</text>' % (x + 18, y + 25, MONO, accent, title)]
    return "".join(o)

# ---- terminal
TX, TY, TW, TH = 74, 132, 1000, 720
S.append(window(TX, TY, TW, TH, "  user@nexus: ~/work"))
ly = TY + 78
for line in TERM:
    lx = TX + 26
    for col, txt in line:
        S.append('<text x="%d" y="%d" font-family="%s" font-size="24" fill="%s" xml:space="preserve">%s</text>'
                 % (lx, ly, MONO, col, txt))
        lx += len(txt) * 14.45
    ly += 44

# ---- palette card
PX, PY, PWD, PHT = 1132, 132, 596, 396
S.append(window(PX, PY, PWD, PHT, "  palette"))
for i, (lab, col) in enumerate(SWATCHES):
    r, c = divmod(i, 4)
    sx = PX + 28 + c * 138
    sy = PY + 66 + r * 82
    S.append('<rect x="%d" y="%d" width="120" height="46" rx="8" fill="%s"/>' % (sx, sy, col))
    S.append('<text x="%d" y="%d" font-family="%s" font-size="15" fill="#5c6d96">%s</text>' % (sx + 2, sy + 66, MONO, col))

# ---- identity card
IX, IY, IW, IH = 1132, 560, 596, 292
S.append(window(IX, IY, IW, IH, "  theme", MAGENTA))
S.append('<text x="%d" y="%d" font-family="%s" font-size="62" fill="%s" letter-spacing="6">OFF-WORLD</text>'
         % (IX + 30, IY + 118, MONO, CYAN))
S.append('<text x="%d" y="%d" font-family="%s" font-size="21" fill="%s" opacity="0.85" letter-spacing="2">a new life awaits you</text>'
         % (IX + 32, IY + 162, MONO, MAGENTA))
for i, (txt, col) in enumerate((("12 wallpapers  ·  wet + dry plates", "#c5d4f2"),
                                ("time of day picks the scene", "#5c6d96"),
                                ("rain that actually falls", "#5c6d96"))):
    S.append('<text x="%d" y="%d" font-family="%s" font-size="19" fill="%s">%s</text>'
             % (IX + 32, IY + 208 + i * 30, MONO, col, txt))
S.append('</svg>')
open(sys.argv[1] if len(sys.argv) > 1 else "svg/preview-overlay.svg", "w").write("".join(S))
print("overlay written")
