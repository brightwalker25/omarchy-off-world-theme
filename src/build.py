"""Render every scene x weather variant at full resolution."""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene1, scene2, scene3, scene4, scene5, scene6
from palette import W, H

SCENES = [scene1, scene2, scene3, scene4, scene5, scene6]
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.expanduser(
    "~/.config/omarchy/themes/off-world/backgrounds")
RW = int(sys.argv[2]) if len(sys.argv) > 2 else W
RH = int(RW * H // W)
os.makedirs(OUT, exist_ok=True)
os.makedirs("svg", exist_ok=True)

for i, mod in enumerate(SCENES, 1):
    for rain in (False, True):
        tag = "rain" if rain else "clear"
        stem = "%d-%s-%s" % (i, mod.NAME, tag)
        svg = "svg/%s.svg" % stem
        raw = "/tmp/ow-raw-%s.png" % stem
        dst = os.path.join(OUT, "%s.jpg" % stem)
        open(svg, "w").write(mod.build(rain))
        subprocess.run(["rsvg-convert", "-w", str(RW), "-h", str(RH), svg, "-o", raw], check=True)
        subprocess.run(["./post.sh", raw, dst], check=True)
        os.remove(raw)
        print("  %-44s %6.1f MB" % (dst, os.path.getsize(dst) / 1e6))
print("done")
