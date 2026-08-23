#!/bin/bash
# Switch how rain is drawn.
#
#   ./rain-mode.sh animated   still wet plates + a live particle layer (default)
#   ./rain-mode.sh static     painted drops baked into the wallpaper, no plugin
#   ./rain-mode.sh status     report which is active
#
# Animated costs about 13% of one CPU core while it is raining and nothing when
# it is dry. Static costs nothing at all, but the rain does not move.
set -euo pipefail
src="$(cd "$(dirname "$0")" && pwd)"
mode="${1:-status}"

BG="$src/backgrounds"
ANIM="$src/plates/animated-rain"
STATIC="$src/plates/static-rain"

for d in "$ANIM" "$STATIC"; do
  [[ -d $d ]] || { echo "missing $d — is this a complete checkout?" >&2; exit 1; }
done

current() {
  local probe
  probe=$(find "$BG" -name '*-rain.jpg' | sort | head -1)
  [[ -n $probe ]] || { echo unknown; return; }
  local name; name=$(basename "$probe")
  if cmp -s "$probe" "$STATIC/$name"; then echo static
  elif cmp -s "$probe" "$ANIM/$name"; then echo animated
  else echo modified; fi
}

apply() {
  cp "$1"/*-rain.jpg "$BG/"
  # The live theme reads from a staged copy, so re-apply to pick the new plates up.
  omarchy theme set off-world >/dev/null 2>&1 || true
}

case "$mode" in
  status)
    echo "rain plates : $(current)"
    if grep -qs "Off-World animated rain" "$HOME"/.config/omarchy/plugins/*.background/Background.qml 2>/dev/null; then
      echo "rain layer  : installed"
    else
      echo "rain layer  : not installed"
    fi
    ;;
  animated)
    echo "==> still wet plates + live particle layer"
    apply "$ANIM"
    python3 "$src/plugin/install-rain.py"
    omarchy restart shell >/dev/null 2>&1 || true
    echo "done — rain now falls."
    ;;
  static)
    echo "==> painted plates, no particle layer"
    apply "$STATIC"
    python3 "$src/plugin/install-rain.py" --remove || true
    omarchy restart shell >/dev/null 2>&1 || true
    echo "done — rain is now part of the image, and costs no CPU."
    ;;
  -h|--help)
    sed -n '2,10p' "$0" | sed 's/^# \?//'
    ;;
  *)
    echo "unknown mode: $mode (want animated, static or status)" >&2
    exit 2
    ;;
esac
