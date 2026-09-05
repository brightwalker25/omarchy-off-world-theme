"""The scene register: which module is which, and when each one is shown.

`light` is the time of day a scene is authored and rendered for, and it is the
same value the wallpaper picker uses to group them. A scene renders at exactly
one light level, which is why twelve scenes cost nineteen images rather than
ninety-six.
"""
import scene1, scene2, scene3, scene4, scene5, scene6
import scene7, scene8, scene9, scene10, scene11, scene12

# (number, module) in file-name order
SCENES = [
    (1, scene1), (2, scene2), (3, scene3), (4, scene4), (5, scene5), (6, scene6),
    (7, scene7), (8, scene8), (9, scene9), (10, scene10), (11, scene11), (12, scene12),
]


def variants(scenes):
    """Yield (stem, module, rain) for every image that needs rendering."""
    for n, mod in scenes:
        if mod.OUTDOOR:
            yield "%d-%s-clear" % (n, mod.NAME), mod, False
            yield "%d-%s-rain" % (n, mod.NAME), mod, True
        else:
            yield "%d-%s" % (n, mod.NAME), mod, False


def by_light():
    """{light level: [stem-prefix, ...]} - what the picker groups on."""
    out = {}
    for n, mod in SCENES:
        out.setdefault(mod.LIGHT, []).append("%d-%s" % (n, mod.NAME))
    return out


def title_and_blurb(mod):
    """Pull the scene's name and one-line description out of its docstring.

    Every scene opens with `N - Title: what it is.`, so the docstring is the
    single source of truth and the gallery cannot drift from the code.
    """
    line = (mod.__doc__ or "").strip().split("\n")[0]
    _, _, rest = line.partition(" - ")
    title, _, blurb = rest.partition(": ")
    return title.strip(), blurb.strip().rstrip(".")
