"""Render every scene at full resolution.

Outdoor scenes render twice, wet and dry, as `N-name-clear.jpg` and
`N-name-rain.jpg`. Interiors render once, as `N-name.jpg`: weather you could
only see through a window is not worth a second plate, and the falling-rain
layer keys off the `-rain` suffix, so a single-plate interior never drizzles.
"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scenes import SCENES, variants
from palette import W, H

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
    "~/.config/omarchy/themes/off-world/backgrounds")
RW = int(sys.argv[2]) if len(sys.argv) > 2 else W
RH = int(RW * H // W)
os.makedirs(OUT, exist_ok=True)
os.makedirs("svg", exist_ok=True)

for stem, mod, rain in variants(SCENES):
    svg = "svg/%s.svg" % stem
    raw = "/tmp/ow-raw-%s.png" % stem
    dst = os.path.join(OUT, "%s.jpg" % stem)
    open(svg, "w").write(mod.build(rain))
    subprocess.run(["rsvg-convert", "-w", str(RW), "-h", str(RH), svg, "-o", raw], check=True)
    subprocess.run(["./post.sh", raw, dst], check=True)
    os.remove(raw)
    print("  %-46s %6.1f MB" % (dst, os.path.getsize(dst) / 1e6), flush=True)
print("done")
