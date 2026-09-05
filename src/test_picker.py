"""Check the picker's tables against the scene register.

The picker deliberately does not import src/, so that it keeps working from
~/.local/bin with the theme repo deleted. The cost is a table it has to keep in
step by hand, which is exactly the thing worth testing.

    python3 src/test_picker.py
"""
import importlib.machinery
import importlib.util
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scenes import SCENES

PICKER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                      "bin", "omarchy-off-world-bg")

fails = []
checks = 0


def eq(got, want, what):
    global checks
    checks += 1
    if got != want:
        fails.append("%s: got %r want %r" % (what, got, want))


def ok(cond, what):
    global checks
    checks += 1
    if not cond:
        fails.append(what)


def load(path):
    loader = importlib.machinery.SourceFileLoader("owbg", path)
    spec = importlib.util.spec_from_loader("owbg", loader)
    mod = importlib.util.module_from_spec(spec)
    loader.exec_module(mod)
    return mod


def main():
    m = load(PICKER)

    # ---- the picker's table has to match src/scenes.py exactly
    want = {"%d-%s" % (n, s.NAME): (s.LIGHT, s.OUTDOOR) for n, s in SCENES}
    got = {n: (p, o) for n, p, o in m.SCENES}
    eq(got, want, "picker table matches src/scenes.py")

    # ---- three scenes per phase, at least one of them outdoors so that
    # weather mode can always show rain whatever the hour
    for p in m.PHASES:
        eq(len(m.IN_PHASE[p]), 3, "phase %s has three scenes" % p)
        ok(any(m.OUTDOOR[n] for n in m.IN_PHASE[p]), "phase %s has no outdoor scene" % p)

    # ---- file names round-trip, both shapes
    eq(m.scene_of_path("/x/4-neon-signage-rain.jpg"), ("4-neon-signage", True), "outdoor wet")
    eq(m.scene_of_path("/x/4-neon-signage-clear.jpg"), ("4-neon-signage", False), "outdoor dry")
    eq(m.scene_of_path("/x/12-blaster.jpg"), ("12-blaster", False), "interior")
    eq(m.scene_of_path("/x/10-tyrell-office.jpg"), ("10-tyrell-office", False), "two-digit interior")
    eq(m.scene_of_path("/x/something-else.jpg"), (None, False), "foreign file ignored")
    eq(m.scene_of_path(""), (None, False), "empty path ignored")
    eq(os.path.basename(m.path_for("/b", "7-sea-wall", True)), "7-sea-wall-rain.jpg", "outdoor wet path")
    eq(os.path.basename(m.path_for("/b", "9-vk-machine", True)), "9-vk-machine.jpg", "interior ignores wet")

    # ---- phase boundaries either side of a known sunrise and sunset
    sun = (datetime(2026, 9, 5, 6, 20), datetime(2026, 9, 5, 19, 40))
    for hh, mm, expect in ((5, 0, "night"), (5, 30, "dawn"), (7, 0, "dawn"), (8, 0, "day"),
                           (15, 0, "day"), (18, 30, "dusk"), (20, 0, "dusk"), (23, 0, "night")):
        eq(m.phase_of(datetime(2026, 9, 5, hh, mm), sun), expect, "phase at %02d:%02d" % (hh, mm))

    # ---- weather mode: the condition names candidates, the hour breaks the tie
    eq(m.scene_for_weather(95, "night")[0], "1-spinner-descent", "thunderstorm at night")
    eq(m.scene_for_weather(95, "dusk")[0], "7-sea-wall", "thunderstorm at dusk")
    eq(m.scene_for_weather(95, "dawn")[0], "11-spinner-ascent", "thunderstorm at dawn")
    eq(m.scene_for_weather(0, "day")[0], "2-off-world-colonies", "clear by day")
    eq(m.scene_for_weather(0, "night")[0], "1-spinner-descent", "clear at night")
    eq(m.scene_for_weather(3, "day")[0], "8-bradbury-atrium", "overcast by day")

    for _, label, names in m.BY_CONDITION:
        for n in names:
            ok(n in m.PHASE_OF, "condition %r names unknown scene %s" % (label, n))
    # anything counted as wet must land on a condition, or the scene would be
    # chosen by the clock while the plate says it is raining
    for c in sorted(m.WET_CODES):
        ok(any(t(c) for t, _, _ in m.BY_CONDITION), "wet code %d matches no condition" % c)
    # and every wet condition must actually offer an outdoor scene to get wet
    for test, label, names in m.BY_CONDITION:
        if any(test(c) for c in m.WET_CODES):
            ok(any(m.OUTDOOR[n] for n in names), "wet condition %r has no outdoor scene" % label)

    # ---- the rotation visits every scene in a phase over a day
    for p in m.PHASES:
        seen = {m.scene_for_phase(p, datetime(2026, 9, 5, h)) for h in range(24)}
        eq(len(seen), 3, "phase %s rotation covers all three in a day" % p)

    if fails:
        print("\n".join(fails))
        print("\n%d of %d checks failed" % (len(fails), checks))
        return 1
    print("all %d checks passed" % checks)
    return 0


if __name__ == "__main__":
    sys.exit(main())
