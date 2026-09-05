#!/bin/bash
# Install the Off-World extras: icon theme, dynamic wallpaper switcher, timer,
# theme-set hook and the animated rain layer.
#
# The theme itself (palette, wallpapers, previews) is this directory. If you got
# here via `omarchy theme install` you are already in the right place and this
# script only adds the parts that live outside a theme directory.
#
#   ./install.sh                everything, with rain that falls
#   ./install.sh --static-rain  painted rain in the wallpaper, no shell plugin
#   ./install.sh --no-rain      no rain at all
set -euo pipefail
src="$(cd "$(dirname "$0")" && pwd)"

RAIN_MODE=animated
for a in "$@"; do
  case "$a" in
    --no-rain) RAIN_MODE=none ;;
    --static-rain) RAIN_MODE=static ;;
    -h|--help) sed -n '2,10p' "$0" | sed 's/^# \?//'; exit 0 ;;
    *) echo "unknown option: $a" >&2; exit 2 ;;
  esac
done

THEME_DIR="$HOME/.config/omarchy/themes/off-world"
ICON_DIR="$HOME/.local/share/icons/Off-World"
BIN_DIR="$HOME/.local/bin"
UNIT_DIR="$HOME/.config/systemd/user"
CONF="$HOME/.config/omarchy/off-world.conf"

command -v omarchy >/dev/null || { echo "This needs Omarchy on PATH." >&2; exit 1; }

# ---- theme payload -------------------------------------------------------
if [[ $src -ef $THEME_DIR ]]; then
  echo "==> theme    already installed at $THEME_DIR"
else
  echo "==> theme    -> $THEME_DIR"
  mkdir -p "$THEME_DIR/backgrounds"
  cp "$src"/backgrounds/*.jpg "$THEME_DIR/backgrounds/"
  for f in colors.toml icons.theme shell.bar.toml preview.png preview-unlock.png unlock.png; do
    cp "$src/$f" "$THEME_DIR/"
  done
fi
echo "             $(find "$THEME_DIR/backgrounds" -name '*.jpg' | wc -l) wallpapers"

echo "==> icons    -> $ICON_DIR"
rm -rf "$ICON_DIR"
mkdir -p "$(dirname "$ICON_DIR")"
cp -r "$src/icons/Off-World" "$ICON_DIR"
command -v gtk-update-icon-cache >/dev/null && gtk-update-icon-cache -qf "$ICON_DIR" 2>/dev/null || true

echo "==> switcher -> $BIN_DIR/omarchy-off-world-bg"
mkdir -p "$BIN_DIR"
install -m 755 "$src/bin/omarchy-off-world-bg" "$BIN_DIR/omarchy-off-world-bg"

if [[ -f $CONF ]]; then
  echo "==> config   $CONF already exists, keeping your settings"
else
  echo "==> config   -> $CONF"
  mkdir -p "$(dirname "$CONF")"
  install -m 644 "$src/config/off-world.conf" "$CONF"
fi

echo "==> hook     -> theme-set"
omarchy hook install theme-set "$src/hooks/off-world-wallpaper-hook" >/dev/null

echo "==> timer    -> off-world-wallpaper.timer"
mkdir -p "$UNIT_DIR"
install -m 644 "$src/units/off-world-wallpaper.service" "$UNIT_DIR/"
install -m 644 "$src/units/off-world-wallpaper.timer" "$UNIT_DIR/"
systemctl --user daemon-reload
systemctl --user enable --now off-world-wallpaper.timer

case "$RAIN_MODE" in
  animated)
    echo "==> rain     falling (particle layer over still wet plates)"
    cp "$src"/plates/animated-rain/*.jpg "$THEME_DIR/backgrounds/"
    python3 "$src/plugin/install-rain.py"
    omarchy restart shell >/dev/null 2>&1 || true
    ;;
  static)
    echo "==> rain     painted into the wallpaper, no plugin, no CPU cost"
    cp "$src"/plates/static-rain/*.jpg "$THEME_DIR/backgrounds/"
    python3 "$src/plugin/install-rain.py" --remove >/dev/null 2>&1 || true
    ;;
  none)
    echo "==> rain     skipped (--no-rain); wet plates will look still"
    ;;
esac

echo
echo "Done. Apply it with:  omarchy theme set off-world"
echo "Check the picker:     omarchy-off-world-bg --status"
echo
echo "The wallpaper follows the clock by default. To change that:"
echo "  omarchy-off-world-bg --mode weather   real conditions pick the scene"
echo "  omarchy-off-world-bg --mode manual    nothing moves unless you move it"
echo
echo "To step through them by hand, bind these in ~/.config/hypr/bindings.lua:"
echo "  omarchy-off-world-bg --next          next scene in this phase"
echo "  omarchy-off-world-bg --prev          previous scene"
echo "  omarchy-off-world-bg --toggle-rain   flip the wet and dry plate"
echo "  omarchy-off-world-bg --auto          back to automatic"
echo "A pick made by hand is held until the light changes."
