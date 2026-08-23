"""Render the STATIC rain plates: the wet scenes with painted falling drops.

These are for anyone not running the animated rain layer - install.sh --static-rain,
or `./rain-mode.sh static`. The default backgrounds/ set omits the painted drops
because the shell plugin draws them live.
"""
import os, subprocess, sys
os.environ["OW_STREAKS"] = "1"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene1, scene2, scene3, scene4, scene5, scene6
from palette import W, H, DRAW_STREAKS

assert DRAW_STREAKS, "these plates need the painted drops switched on"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "plates", "static-rain")
os.makedirs(OUT, exist_ok=True)
os.makedirs("svg", exist_ok=True)
RW = 3840; RH = int(RW * H // W)

for i, mod in enumerate([scene1, scene2, scene3, scene4, scene5, scene6], 1):
    stem = "%d-%s-rain" % (i, mod.NAME)
    svg = "svg/static-%s.svg" % stem
    raw = "/tmp/ow-static-%s.png" % stem
    dst = os.path.join(OUT, "%s.jpg" % stem)
    open(svg, "w").write(mod.build(True))
    subprocess.run(["rsvg-convert", "-w", str(RW), "-h", str(RH), svg, "-o", raw], check=True)
    subprocess.run(["./post.sh", raw, dst], check=True)
    os.remove(raw)
    print("  %s  %.1f MB" % (os.path.basename(dst), os.path.getsize(dst) / 1e6), flush=True)
print("done")
