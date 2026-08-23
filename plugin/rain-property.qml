  // ---- Off-World animated rain -------------------------------------------
  // The wallpaper filename is the signal: *-rain.jpg means it is raining, so
  // omarchy-off-world-bg, `omarchy theme bg next` and the picker all drive this
  // without a separate state file. Other themes never match, so they stay dry.
  readonly property bool raining: /-rain\.(jpe?g|png|webp)$/i.test(displayedBackground)
