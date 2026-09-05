"""Regenerate docs/thumbs and GALLERY.md from the scene register.

Nineteen images is too many to keep in step by hand, and the scene docstrings
already say what every scene is, so the gallery is derived rather than written.
"""
import os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scenes import SCENES, title_and_blurb

PHASES = ("dawn", "day", "dusk", "night")
PHASE_TITLE = {"dawn": "Dawn", "day": "Day", "dusk": "Dusk", "night": "Night"}
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BG = os.path.join(ROOT, "backgrounds")
THUMBS = os.path.join(ROOT, "docs", "thumbs")

HEADER = """# Off-World - gallery

Every image here is generated: drawn as SVG by the scripts in [`src/`](src),
rendered with `rsvg-convert`, then given a bloom and grain pass. Nothing is
taken from any film.

Thumbnails are 1000px. Click one for the full 3840x2400 original.

Twelve scenes, three for each phase of the day. Each scene is authored and
rendered for its own phase, so the day scenes are genuinely lit and the night
scenes keep their blacks.

The seven outdoor scenes ship as a **dry** and a **wet** plate. The wet plates
below carry the wet ground, reflections and heavy haze - but no painted
raindrops, because when one is on screen the live particle layer supplies the
falling kind. That is why they look still here.

The five interiors have a single plate. Rain you could only see through a
window is not worth a second 2 MB image, and the falling-rain layer keys off the
`-rain` suffix, so an interior never drizzles indoors.

If you would rather not spend the CPU on falling rain, `./rain-mode.sh static`
swaps in a second set with the drops rendered into the image. Same scenes, rain
that holds still. See [rain, falling or painted](README.md#rain-falling-or-painted).

---
"""


FOOTER = """
---

## Palette

![Off-World palette](docs/palette.png)

Cyan is the accent, magenta the counterweight, amber the warm note. Window
borders run a magenta-to-cyan gradient, and the Omarchy shell reuses it for
popups, notifications, the launcher and the lock screen. The full definition is
[`colors.toml`](colors.toml).

## Icons

![Off-World icons](docs/icons.png)

Twenty-three neon-noir folders with a magenta-to-cyan edge and colour-coded
glyphs, inheriting `Yaru-magenta-dark` so anything not overridden still
resolves. Drawn by [`src/gen_icons.py`](src/gen_icons.py).

## The desktop

![Off-World desktop preview](preview.png)

---

Back to the [README](README.md) for install and configuration.
"""


def thumb(name):
    src = os.path.join(BG, name + ".jpg")
    dst = os.path.join(THUMBS, name + ".jpg")
    if not os.path.exists(src):
        print("  missing %s" % src, file=sys.stderr)
        return False
    subprocess.run(["magick", src, "-resize", "1000x", "-quality", "88", dst], check=True)
    return True


def main():
    os.makedirs(THUMBS, exist_ok=True)
    keep = set()
    out = [HEADER]
    for phase in PHASES:
        for n, mod in SCENES:
            if mod.LIGHT != phase:
                continue
            title, blurb = title_and_blurb(mod)
            stem = "%d-%s" % (n, mod.NAME)
            out.append("\n## %s - %s\n\n%s.\n" % (PHASE_TITLE[phase], title, blurb[0].upper() + blurb[1:]))
            if mod.OUTDOOR:
                names = [stem + "-clear", stem + "-rain"]
                out.append("\n| Dry | Wet |\n|:---:|:---:|\n| %s | %s |\n" % tuple(
                    "[![%s, %s](docs/thumbs/%s.jpg)](backgrounds/%s.jpg)" % (title, lab, nm, nm)
                    for nm, lab in zip(names, ("dry", "wet"))))
            else:
                names = [stem]
                out.append("\n| Interior - one plate |\n|:---:|\n| %s |\n"
                           % ("[![%s](docs/thumbs/%s.jpg)](backgrounds/%s.jpg)" % (title, stem, stem)))
            for nm in names:
                if thumb(nm):
                    keep.add(nm + ".jpg")
                    print("  %s" % nm, flush=True)

    out.append(FOOTER)

    for stale in sorted(set(os.listdir(THUMBS)) - keep):
        os.remove(os.path.join(THUMBS, stale))
        print("  dropped stale thumb %s" % stale)

    with open(os.path.join(ROOT, "GALLERY.md"), "w") as fh:
        fh.write("".join(out))
    print("GALLERY.md: %d scenes, %d images" % (len(SCENES), len(keep)))


if __name__ == "__main__":
    main()
