# Working on Off-World

An Omarchy theme. The palette and the icons are ordinary theme files; the
interesting part is that the wallpapers are generated and the one on screen is
chosen by a picker on a timer.

## Layout

```
backgrounds/       the 19 wallpapers actually in use
plates/            the two rain treatments, swapped in by rain-mode.sh
bin/               omarchy-off-world-bg, the picker
src/               the generators, the register, the tests
config/ units/ hooks/   the parts install.sh puts outside the theme directory
```

## The two rules that matter

**1. The scene table exists twice, and a test holds them together.**

`src/scenes.py` is the register: which module is which scene, which phase it
belongs to, whether it is outdoors. `bin/omarchy-off-world-bg` keeps its own
copy of that table, deliberately — the picker is installed to `~/.local/bin`
and has to keep working with this repo deleted, so it must not import `src/`.

Change one and you must change the other. `src/test_picker.py` compares them,
along with the invariants that make the picker sane: three scenes per phase, at
least one of them outdoors so weather mode can always show rain, the rotation
visiting all three, and every weather code counted as wet landing on a
condition that can actually offer a wet plate.

```bash
python3 src/test_picker.py
```

Run it after touching either table. It has already caught a real bug.

**2. The build must stay byte-reproducible.**

Rebuilding an unchanged scene has to produce the identical file, or `git status`
comes back dirty for no reason and history gains a set of 2 MB JPEGs that can
never be pruned. Git cannot delta-compress these, so every non-reproducible
build costs about 60 MB, permanently.

Three things keep it deterministic, and all three are load-bearing:

- fixed `random.Random(...)` seeds at the top of each `sceneN.py`
- `rsvg-convert`, which is deterministic already
- `post.sh`, which seeds ImageMagick's film grain from the output filename

That last one is easy to lose. `+noise` without `-seed` draws fresh noise every
run. If you add any randomised step to the pipeline, seed it from something
stable, and check:

```bash
python3 src/build.py && git status --short backgrounds
```

Clean means reproducible.

## Adding a scene

Write `src/sceneN.py` exporting:

```python
NAME = "short-slug"          # the file stem, after the number
LIGHT = "dawn"               # dawn | day | dusk | night
OUTDOOR = True               # False means one plate and no weather variant
def build(rain=True, light=LIGHT) -> str:   # returns SVG
```

Then list it in `src/scenes.py`, add the matching row to `SCENES` in
`bin/omarchy-off-world-bg`, and run the test.

Keep three scenes per phase. The picker's rotation and the key bindings both
assume it, and the test enforces it.

## Lighting

Each scene is authored and rendered for exactly one time of day, which is why
twelve scenes cost nineteen images rather than ninety-six. The grade lives in
`src/palette.py`:

- `lift` pulls colours toward an atmospheric haze — what daylight does to shadow
- `sink` pulls them toward black — what deepens a night
- `stars`, `glow`, `ambient` and `vig` scale the rest

Use `lit()`, `lit_stops()`, `stars()`, `glow()`, `ambient()` and `vig()` rather
than grading the finished image. Lifting a night-black frame in post makes it
grey, not daylit. The point is that only the shadows move: highlights stay put,
so contrast is redistributed rather than flattened and the result stays noir.

A scene with its own strong colour cast should pass its own `haze=` — scene 2
grades against warm dust, not the cold default, or the sun goes out.

## Interiors

An interior gets one plate. Rain you could only see through a window is not
worth a second 2 MB image, and the animated rain layer keys off the `-rain`
filename suffix, so a single-plate scene never drizzles indoors. Set
`OUTDOOR = False` and the build scripts, the picker and the gallery all follow.

## Regenerating

```bash
cd src
python3 build.py                  # all nineteen, ~13 min
python3 build_rain_plates.py      # wet plates, no painted drops (animated)
python3 build_static_rain.py      # wet plates with painted drops (static)
python3 gen_icons.py
python3 gen_gallery.py            # docs/thumbs and GALLERY.md, from the register
```

`GALLERY.md` is generated. Do not hand-edit it; edit the scene docstrings, which
are where its titles and one-line descriptions come from.

## Image cost

`plates/animated-rain` is free: byte-identical to the `-rain` files in
`backgrounds/`, so git stores one blob for both paths. `plates/static-rain` is
the only duplicated set, about 16 MB, and it buys instant `rain-mode.sh`
switching instead of a five-minute re-render. Everything else is one copy.
