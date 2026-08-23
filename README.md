# Off-World

A neon-noir theme for [Omarchy](https://omarchy.org/), with wallpapers that
follow the time of day and rain that actually falls.

![Off-World](preview.png)

**[See the full gallery →](GALLERY.md)** — all twelve wallpapers wet and dry, the
palette, and the icon set.

Every image is generated. The wallpapers are drawn as SVG by the scripts in
`src/`, rendered with `rsvg-convert`, then given a bloom and grain pass. Nothing
is taken from any film.

## Install

```bash
omarchy theme install https://github.com/brightwalker25/omarchy-off-world-theme
cd ~/.config/omarchy/themes/off-world && ./install.sh
```

The first command installs and applies the palette and wallpapers. The second
adds the parts that live outside a theme directory: the icon set, the wallpaper
switcher, its timer, and the animated rain. Use `./install.sh --no-rain` to skip
the rain.

## What's in it

**Palette.** Rain-dark blue surfaces, electric cyan, hologram magenta, Vegas
amber. Window borders run a magenta-to-cyan gradient, which the Omarchy shell
reuses for popups, notifications, the launcher and the lock screen. Alacritty,
foot, kitty, ghostty, btop, neovim, VSCode and Chromium all follow.

**Twelve wallpapers**, six scenes in a wet and a dry plate, rendered at
3840x2400. They are all in the [gallery](GALLERY.md):

| Scene | |
|---|---|
| Spinner Descent | rain-drowned megacity under a colossal advertising screen |
| Off-World Colonies | the sun over the dust, a ziggurat, a figure for scale |
| Voight-Kampff | the empathy test seen from inside the machine |
| Neon Signage | an alley of light through wet glass |
| Tyrell Approach | a wireframe ziggurat over a light grid |
| Hologram | a projected figure standing over the city |

**Twenty-three icons.** A GTK icon theme of neon-noir folders with a
magenta-to-cyan edge and colour-coded glyphs, inheriting `Yaru-magenta-dark` so
everything it does not override still resolves.

## The wallpaper picks itself

Time of day chooses the scene:

| Time | Scene |
|---|---|
| Dawn | Tyrell Approach |
| Day | Off-World Colonies |
| Dusk | Hologram |
| Night | rotates Spinner Descent, Neon Signage, Voight-Kampff |

Sunrise and sunset are computed locally from your coordinates, so dawn and dusk
track the real sky with no network call. Verified against Open-Meteo: within two
minutes.

Rain is a weighted coin held steady for three hours at a stretch, so the weather
has a mood instead of flickering every time the timer runs. Fifty-fifty by
default. A systemd user timer re-checks every fifteen minutes.

```
omarchy-off-world-bg --status          # what it picked, and why
omarchy-off-world-bg --list            # the twelve wallpapers
omarchy-off-world-bg --rain            # force the wet plate, now
omarchy-off-world-bg --clear           # force the dry one
omarchy-off-world-bg --at 06:30        # pretend it is dawn
omarchy-off-world-bg --scene 3         # jump to a scene, 1-6
omarchy-off-world-bg --dry-run --at 23:00 --rain
```

Overrides apply the wallpaper so you can look at it. The timer puts things back
within fifteen minutes, or run it with no arguments to restore at once.

### Configuration

`~/.config/omarchy/off-world.conf`:

```
RAIN=random        # random | live | always | never
RAIN_CHANCE=0.5    # chance per spell, random mode only
RAIN_SPELL_HOURS=3 # how long one spell of weather lasts
LAT=               # blank derives from your timezone, offline
LON=
```

`RAIN=live` swaps the coin for real precipitation where you are, via Open-Meteo
(no account, no key). That is the only mode that touches the network. Location
comes from your system timezone via `/usr/share/zoneinfo/zone.tab` — the nearest
listed city, resolved on your machine, never IP geolocation.

## Rain that falls

When a wet plate is on screen, a particle layer drizzles over it. The wet plates
carry the wet ground, reflections and heavy haze but no painted drops, so the
only rain you see is the moving kind.

It is a small addition to Omarchy's own background plugin. Because that plugin
ships read-only, `plugin/install-rain.py` clones it into your config with
`omarchy plugin clone` and injects the layer into the clone. Re-running is safe.

```bash
python3 plugin/install-rain.py            # install or refresh
python3 plugin/install-rain.py --reclone  # after an Omarchy update
python3 plugin/install-rain.py --remove   # take it back out
omarchy restart shell
```

**Cost.** Measured on a 2880x1800 display: about 13% of one CPU core while it is
raining, and exactly zero when it is dry, because the particle system is stopped
rather than hidden. No measurable memory, and no growth over time. On a laptop
that is a real battery consideration — tune or disable it if you would rather
have the hours back.

Tuning lives at the top of the rain block in your cloned
`~/.config/omarchy/plugins/*.background/Background.qml`:

```qml
property real density: 1.0    // how much falls
property real speed: 1.0      // how fast
```

Both hot-reload on save. `density: 0.5` roughly halves the CPU cost.

## Turning things off

```bash
systemctl --user disable --now off-world-wallpaper.timer   # stop the rotation
python3 plugin/install-rain.py --remove                    # stop the rain
omarchy theme set tokyo-night                              # leave the theme
```

The theme keeps working with the timer off; backgrounds then cycle manually with
`omarchy theme bg next` like any other theme.

## Rebuilding the art

```bash
cd src
python3 build.py                  # all twelve, ~7 min
python3 build_rain_plates.py      # just the wet plates, no painted drops
python3 gen_icons.py              # the icon theme
```

Scene seeds are fixed, so a rebuild reproduces the same images. Change the
`random.Random(...)` seed at the top of a `sceneN.py` for a different layout of
the same design. `build.py` writes straight into the installed theme.

## See also

- [GALLERY.md](GALLERY.md) — every wallpaper, the palette, the icons

## License

MIT. Omarchy is MIT too; `plugin/install-rain.py` modifies a copy of its
background plugin in your own config and never touches the packaged original.
