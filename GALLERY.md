# Off-World - gallery

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

## Dawn - Tyrell Approach

A wireframe ziggurat over a light grid at first light.

| Dry | Wet |
|:---:|:---:|
| [![Tyrell Approach, dry](docs/thumbs/5-tyrell-approach-clear.jpg)](backgrounds/5-tyrell-approach-clear.jpg) | [![Tyrell Approach, wet](docs/thumbs/5-tyrell-approach-rain.jpg)](backgrounds/5-tyrell-approach-rain.jpg) |

## Dawn - Tyrell's Office

The hall at first light, and the owl that watches it.

| Interior - one plate |
|:---:|
| [![Tyrell's Office](docs/thumbs/10-tyrell-office.jpg)](backgrounds/10-tyrell-office.jpg) |

## Dawn - Spinner Ascent

A police spinner climbing into first light.

| Dry | Wet |
|:---:|:---:|
| [![Spinner Ascent, dry](docs/thumbs/11-spinner-ascent-clear.jpg)](backgrounds/11-spinner-ascent-clear.jpg) | [![Spinner Ascent, wet](docs/thumbs/11-spinner-ascent-rain.jpg)](backgrounds/11-spinner-ascent-rain.jpg) |

## Day - Off-World Colonies

A colossal sun over the dust, monoliths, a ziggurat.

| Dry | Wet |
|:---:|:---:|
| [![Off-World Colonies, dry](docs/thumbs/2-off-world-colonies-clear.jpg)](backgrounds/2-off-world-colonies-clear.jpg) | [![Off-World Colonies, wet](docs/thumbs/2-off-world-colonies-rain.jpg)](backgrounds/2-off-world-colonies-rain.jpg) |

## Day - Voight-Kampff

The empathy test, seen from inside the machine.

| Interior - one plate |
|:---:|
| [![Voight-Kampff](docs/thumbs/3-voight-kampff.jpg)](backgrounds/3-voight-kampff.jpg) |

## Day - Bradbury Atrium

Iron stairs under a rotting glass roof, at noon.

| Interior - one plate |
|:---:|
| [![Bradbury Atrium](docs/thumbs/8-bradbury-atrium.jpg)](backgrounds/8-bradbury-atrium.jpg) |

## Dusk - Unicorn

Gaff's folded unicorn, projected over the city.

| Dry | Wet |
|:---:|:---:|
| [![Unicorn, dry](docs/thumbs/6-hologram-clear.jpg)](backgrounds/6-hologram-clear.jpg) | [![Unicorn, wet](docs/thumbs/6-hologram-rain.jpg)](backgrounds/6-hologram-rain.jpg) |

## Dusk - Sea Wall Flares

The refinery plain at last light.

| Dry | Wet |
|:---:|:---:|
| [![Sea Wall Flares, dry](docs/thumbs/7-sea-wall-clear.jpg)](backgrounds/7-sea-wall-clear.jpg) | [![Sea Wall Flares, wet](docs/thumbs/7-sea-wall-rain.jpg)](backgrounds/7-sea-wall-rain.jpg) |

## Dusk - The Blaster

The gun on the table, against a wall that is giving up.

| Interior - one plate |
|:---:|
| [![The Blaster](docs/thumbs/12-blaster.jpg)](backgrounds/12-blaster.jpg) |

## Night - Spinner Descent

Rain-drowned megacity under an advertising sky.

| Dry | Wet |
|:---:|:---:|
| [![Spinner Descent, dry](docs/thumbs/1-spinner-descent-clear.jpg)](backgrounds/1-spinner-descent-clear.jpg) | [![Spinner Descent, wet](docs/thumbs/1-spinner-descent-rain.jpg)](backgrounds/1-spinner-descent-rain.jpg) |

## Night - Neon Signage

An alley of light seen through wet glass.

| Dry | Wet |
|:---:|:---:|
| [![Neon Signage, dry](docs/thumbs/4-neon-signage-clear.jpg)](backgrounds/4-neon-signage-clear.jpg) | [![Neon Signage, wet](docs/thumbs/4-neon-signage-rain.jpg)](backgrounds/4-neon-signage-rain.jpg) |

## Night - The Machine

The Voight-Kampff apparatus itself, on the desk, after dark.

| Interior - one plate |
|:---:|
| [![The Machine](docs/thumbs/9-vk-machine.jpg)](backgrounds/9-vk-machine.jpg) |

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
