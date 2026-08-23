"""Re-render the rain variants as WET PLATES: wet ground, reflections and heavy
haze, but no painted falling drops - the shell plugin supplies those live."""
import os, subprocess, sys
os.environ["OW_STREAKS"] = "0"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scene1, scene2, scene3, scene4, scene5, scene6
from palette import W, H, DRAW_STREAKS

assert not DRAW_STREAKS, "OW_STREAKS did not take effect"
OUT = os.path.expanduser("~/.config/omarchy/themes/off-world/backgrounds")
RW = 3840; RH = int(RW * H // W)
for i, mod in enumerate([scene1, scene2, scene3, scene4, scene5, scene6], 1):
    stem = "%d-%s-rain" % (i, mod.NAME)
    svg = "svg/%s.svg" % stem
    raw = "/tmp/ow-plate-%s.png" % stem
    dst = os.path.join(OUT, "%s.jpg" % stem)
    os.makedirs("svg", exist_ok=True)
    open(svg, "w").write(mod.build(True))
    subprocess.run(["rsvg-convert", "-w", str(RW), "-h", str(RH), svg, "-o", raw], check=True)
    subprocess.run(["./post.sh", raw, dst], check=True)
    os.remove(raw)
    print("  %s  %.1f MB" % (os.path.basename(dst), os.path.getsize(dst) / 1e6), flush=True)
print("done")
