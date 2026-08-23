#!/bin/bash
# Bloom + grain. Blur radii scale with image width so a 1000px proof and a
# 3840px final get the same look.
set -euo pipefail
src="$1"; dst="$2"
w=$(magick identify -format "%w" "$src")
f=$(awk -v w="$w" 'BEGIN{printf "%.3f", w/1000.0}')
b1=$(awk -v f="$f" 'BEGIN{printf "%.1f", 22*f}')
b2=$(awk -v f="$f" 'BEGIN{printf "%.1f", 80*f}')
magick "$src" \
  \( +clone -colorspace RGB -level 42%,100% -blur 0x"$b1" -colorspace sRGB \) -compose screen -composite \
  \( +clone -colorspace RGB -level 62%,100% -blur 0x"$b2" -colorspace sRGB \) -compose screen -composite \
  -modulate 100,112,100 \
  -attenuate 0.055 +noise Gaussian \
  -quality 95 "$dst"
