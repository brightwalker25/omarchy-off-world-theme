# Off-World — gallery

Every image here is generated: drawn as SVG by the scripts in [`src/`](src),
rendered with `rsvg-convert`, then given a bloom and grain pass. Nothing is
taken from any film.

Thumbnails are 1000px. Click one for the full 3840x2400 original.

Each scene ships as a **dry** and a **wet** plate. The wet plates carry the wet
ground, reflections and heavy haze — but no painted raindrops, because when one
is on screen the [animated rain](README.md#rain-that-falls) supplies the falling
kind. That is why the wet plates look still on their own.

---

## Dawn — Tyrell Approach

A wireframe ziggurat over a light grid, the hour before the city wakes.

| Dry | Wet |
|:---:|:---:|
| [![Tyrell Approach, dry](docs/thumbs/5-tyrell-approach-clear.jpg)](backgrounds/5-tyrell-approach-clear.jpg) | [![Tyrell Approach, wet](docs/thumbs/5-tyrell-approach-rain.jpg)](backgrounds/5-tyrell-approach-rain.jpg) |

## Day — Off-World Colonies

The sun over the dust, a ziggurat on the right, and a single figure for scale.

| Dry | Wet |
|:---:|:---:|
| [![Off-World Colonies, dry](docs/thumbs/2-off-world-colonies-clear.jpg)](backgrounds/2-off-world-colonies-clear.jpg) | [![Off-World Colonies, wet](docs/thumbs/2-off-world-colonies-rain.jpg)](backgrounds/2-off-world-colonies-rain.jpg) |

## Dusk — Hologram

A projected figure the size of a building, standing over the skyline.

| Dry | Wet |
|:---:|:---:|
| [![Hologram, dry](docs/thumbs/6-hologram-clear.jpg)](backgrounds/6-hologram-clear.jpg) | [![Hologram, wet](docs/thumbs/6-hologram-rain.jpg)](backgrounds/6-hologram-rain.jpg) |

## Night

Three scenes, rotating every couple of hours so it is not the same view all night.

### Spinner Descent

A rain-drowned megacity under a colossal advertising screen.

| Dry | Wet |
|:---:|:---:|
| [![Spinner Descent, dry](docs/thumbs/1-spinner-descent-clear.jpg)](backgrounds/1-spinner-descent-clear.jpg) | [![Spinner Descent, wet](docs/thumbs/1-spinner-descent-rain.jpg)](backgrounds/1-spinner-descent-rain.jpg) |

### Neon Signage

An alley of light seen through wet glass, three depth planes deep.

| Dry | Wet |
|:---:|:---:|
| [![Neon Signage, dry](docs/thumbs/4-neon-signage-clear.jpg)](backgrounds/4-neon-signage-clear.jpg) | [![Neon Signage, wet](docs/thumbs/4-neon-signage-rain.jpg)](backgrounds/4-neon-signage-rain.jpg) |

### Voight-Kampff

The empathy test, seen from inside the machine. Eleven hundred iris fibres.

| Dry | Wet |
|:---:|:---:|
| [![Voight-Kampff, dry](docs/thumbs/3-voight-kampff-clear.jpg)](backgrounds/3-voight-kampff-clear.jpg) | [![Voight-Kampff, wet](docs/thumbs/3-voight-kampff-rain.jpg)](backgrounds/3-voight-kampff-rain.jpg) |

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
