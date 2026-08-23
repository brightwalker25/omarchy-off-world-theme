#!/usr/bin/env python3
"""Add the Off-World animated rain to your copy of the Omarchy background plugin.

Omarchy's background plugin is packaged read-only, so this clones it into your
own config (`omarchy plugin clone`) and injects a particle layer into the clone.
Re-running is safe. Re-run after an Omarchy update if the rain disappears: the
clone is a snapshot, so `--reclone` takes a fresh copy and re-injects.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGINS = os.path.expanduser("~/.config/omarchy/plugins")
SOURCE_ID = "omarchy.background"
MARKER = "Off-World animated rain"

# Where the two snippets are spliced in. Both are matched loosely so small
# upstream edits to Background.qml do not break the install.
PROP_ANCHOR = re.compile(r"^(\s*property real revealProgress:.*)$", re.M)
LAYER_ANCHOR = re.compile(r"^(\s*)(Connections\s*\{\s*\n\s*target:\s*root)", re.M)


def die(msg, code=1):
    print("install-rain: " + msg, file=sys.stderr)
    sys.exit(code)


def find_clone():
    if not os.path.isdir(PLUGINS):
        return None
    for name in sorted(os.listdir(PLUGINS)):
        qml = os.path.join(PLUGINS, name, "Background.qml")
        if name.endswith(".background") and os.path.isfile(qml):
            return os.path.join(PLUGINS, name)
    return None


def clone():
    print("==> cloning %s" % SOURCE_ID)
    r = subprocess.run(["omarchy", "plugin", "clone", SOURCE_ID],
                       capture_output=True, text=True)
    sys.stdout.write(r.stdout)
    if r.returncode != 0:
        sys.stderr.write(r.stderr)
        die("`omarchy plugin clone %s` failed" % SOURCE_ID)
    d = find_clone()
    if not d:
        die("clone reported success but no *.background plugin appeared in %s" % PLUGINS)
    return d


def inject(plugin_dir):
    qml_path = os.path.join(plugin_dir, "Background.qml")
    src = open(qml_path).read()

    if MARKER in src:
        print("    rain layer already present, refreshing it")
        src = strip(src)

    prop = open(os.path.join(HERE, "rain-property.qml")).read().rstrip("\n")
    layer = open(os.path.join(HERE, "rain-layer.qml")).read().rstrip("\n")

    if "import QtQuick.Particles" not in src:
        if "import QtQuick\n" not in src:
            die("Background.qml has no `import QtQuick` line to anchor to")
        src = src.replace("import QtQuick\n", "import QtQuick\nimport QtQuick.Particles\n", 1)

    m = PROP_ANCHOR.search(src)
    if not m:
        die("could not find the `property real revealProgress` line in Background.qml.\n"
            "            Omarchy's plugin has changed; open an issue with your omarchy version.")
    src = src[:m.end()] + "\n\n" + prop + src[m.end():]

    m = LAYER_ANCHOR.search(src)
    if not m:
        die("could not find the `Connections { target: root }` block in Background.qml.\n"
            "            Omarchy's plugin has changed; open an issue with your omarchy version.")
    src = src[:m.start()] + layer + "\n\n" + src[m.start():]

    open(qml_path, "w").write(src)

    assets = os.path.join(plugin_dir, "assets")
    os.makedirs(assets, exist_ok=True)
    for png in ("raindrop.png", "raindrop-near.png"):
        shutil.copy2(os.path.join(HERE, "assets", png), os.path.join(assets, png))
    return qml_path


def strip(src):
    """Remove a previously injected layer so re-running does not stack copies."""
    src = re.sub(r"\n*[ \t]*// ---- Off-World animated rain.*?(?=\n[ \t]*function imageUrl)",
                 "", src, flags=re.S)
    src = re.sub(r"\n*[ \t]*// ---- animated rain -+\n.*?(?=\n[ \t]*Connections \{)",
                 "", src, flags=re.S)
    return src


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--reclone", action="store_true",
                    help="discard the existing clone and take a fresh copy first")
    ap.add_argument("--remove", action="store_true",
                    help="strip the rain layer, leaving the clone otherwise intact")
    args = ap.parse_args()

    if not shutil.which("omarchy"):
        die("this needs Omarchy on PATH")

    plugin_dir = find_clone()

    if args.remove:
        if not plugin_dir:
            die("no cloned background plugin found; nothing to remove")
        qml_path = os.path.join(plugin_dir, "Background.qml")
        src = open(qml_path).read()
        if MARKER not in src:
            print("no rain layer present")
            return
        open(qml_path, "w").write(strip(src))
        print("removed the rain layer from %s" % qml_path)
        print("run: omarchy restart shell")
        return

    if args.reclone and plugin_dir:
        print("==> removing existing clone %s" % os.path.basename(plugin_dir))
        shutil.rmtree(plugin_dir)
        plugin_dir = None

    if not plugin_dir:
        plugin_dir = clone()
    else:
        print("==> using existing clone %s" % os.path.basename(plugin_dir))

    qml_path = inject(plugin_dir)
    print("==> rain layer installed in %s" % qml_path)
    print()
    print("Restart the shell to see it:  omarchy restart shell")
    print("Tune it: `density` and `speed` near the top of the rain block.")


if __name__ == "__main__":
    main()
