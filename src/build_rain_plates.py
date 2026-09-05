"""Render the ANIMATED rain plates into plates/animated-rain.

Wet ground, reflections and heavy haze, but no painted falling drops: the shell
plugin supplies those live. Only outdoor scenes have a rain variant at all.
"""
import os, subprocess, sys
os.environ["OW_STREAKS"] = "0"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scenes import SCENES
from palette import W, H, DRAW_STREAKS

assert not DRAW_STREAKS, "OW_STREAKS did not take effect"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "plates", "animated-rain")
os.makedirs(OUT, exist_ok=True)
os.makedirs("svg", exist_ok=True)
RW = 3840; RH = int(RW * H // W)

for n, mod in SCENES:
    if not mod.OUTDOOR:
        continue
    stem = "%d-%s-rain" % (n, mod.NAME)
    svg = "svg/plate-%s.svg" % stem
    raw = "/tmp/ow-plate-%s.png" % stem
    dst = os.path.join(OUT, "%s.jpg" % stem)
    open(svg, "w").write(mod.build(True))
    subprocess.run(["rsvg-convert", "-w", str(RW), "-h", str(RH), svg, "-o", raw], check=True)
    subprocess.run(["./post.sh", raw, dst], check=True)
    os.remove(raw)
    print("  %s  %.1f MB" % (os.path.basename(dst), os.path.getsize(dst) / 1e6), flush=True)
print("done")
