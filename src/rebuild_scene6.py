"""Re-render scene 6 in all three forms after the unicorn change."""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from palette import W, H
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RW = 3840; RH = int(RW * H // W)
os.makedirs("svg", exist_ok=True)

def render(svg_text, dst):
    svg = "/tmp/s6-%s.svg" % os.path.basename(dst).replace(".jpg", "")
    raw = svg.replace(".svg", ".png")
    open(svg, "w").write(svg_text)
    subprocess.run(["rsvg-convert", "-w", str(RW), "-h", str(RH), svg, "-o", raw], check=True)
    subprocess.run(["./post.sh", raw, dst], check=True)
    os.remove(raw)
    print("  %s  %.1f MB" % (dst.replace(ROOT + "/", ""), os.path.getsize(dst) / 1e6), flush=True)

for streaks, targets in ((False, [(True, "backgrounds/6-hologram-rain.jpg"),
                                  (True, "plates/animated-rain/6-hologram-rain.jpg"),
                                  (False, "backgrounds/6-hologram-clear.jpg")]),
                         (True,  [(True, "plates/static-rain/6-hologram-rain.jpg")])):
    os.environ["OW_STREAKS"] = "1" if streaks else "0"
    for mod in list(sys.modules):
        if mod in ("palette", "scene6", "origami"):
            del sys.modules[mod]
    import scene6
    for rain, rel in targets:
        render(scene6.build(rain), os.path.join(ROOT, rel))
print("done")
