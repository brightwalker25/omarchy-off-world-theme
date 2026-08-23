"""Off-World icon theme: neon-noir folders over a Yaru-magenta-dark base."""
import os

CYAN, MAGENTA, ROSE, GOLD, MINT, VIOLET, BLUE, AMBER = (
    "#00e5ff", "#ff5cf0", "#ff3d6e", "#ffc233", "#2bf5a0", "#8b5cff", "#4d8cff", "#ff8a3d")

# folder outline: tabbed, 5..43 x 9..39 in a 48 box
BODY = ("M 8 9 h 9 l 4 4.5 h 19 a 3 3 0 0 1 3 3 V 36 a 3 3 0 0 1 -3 3 H 8 "
        "a 3 3 0 0 1 -3 -3 V 12 a 3 3 0 0 1 3 -3 Z")
# front panel of the folder, sitting proud of the back
FRONT = "M 5 18 h 38 v 18 a 3 3 0 0 1 -3 3 H 8 a 3 3 0 0 1 -3 -3 Z"


def head(accent):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48">
<defs>
<linearGradient id="back" x1="0" y1="0" x2="0" y2="1">
<stop offset="0" stop-color="#182247"/><stop offset="1" stop-color="#0a1026"/></linearGradient>
<linearGradient id="front" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#101835"/><stop offset="1" stop-color="#070b1c"/></linearGradient>
<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="{MAGENTA}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="lip" x1="0" y1="0" x2="1" y2="0">
<stop offset="0" stop-color="{accent}" stop-opacity="0.25"/>
<stop offset="0.5" stop-color="{accent}"/>
<stop offset="1" stop-color="{accent}" stop-opacity="0.25"/></linearGradient>
</defs>'''


def folder(accent=CYAN, glyph="", open_=False, accept=False):
    s = [head(accent)]
    s.append(f'<path d="{BODY}" fill="url(#back)" stroke="url(#edge)" stroke-width="1.4" stroke-opacity="0.85"/>')
    if open_:
        # front panel skewed forward, as if the folder is spilling light
        s.append('<g transform="translate(0,1.5) skewX(-6)">')
        s.append(f'<path d="{FRONT}" fill="url(#front)" stroke="url(#edge)" stroke-width="1.2" stroke-opacity="0.7"/>')
        s.append(f'<path d="M 5 18 h 38" stroke="url(#lip)" stroke-width="1.6" fill="none"/>')
        s.append('</g>')
        s.append(f'<path d="M 7 17 h 34" stroke="{accent}" stroke-width="1" opacity="0.35" fill="none"/>')
    else:
        s.append(f'<path d="{FRONT}" fill="url(#front)" stroke="url(#edge)" stroke-width="1.2" stroke-opacity="0.7"/>')
        s.append(f'<path d="M 5 18 h 38" stroke="url(#lip)" stroke-width="1.8" fill="none"/>')
    if accept:
        s.append(f'<path d="M 24 22 v 9 m 0 0 l -4 -4 m 4 4 l 4 -4" stroke="{MINT}" stroke-width="2.4" '
                 f'fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    elif glyph:
        s.append(f'<g transform="translate(24,28.5)" fill="none" stroke="{accent}" stroke-width="1.8" '
                 f'stroke-linecap="round" stroke-linejoin="round" opacity="0.95">{glyph}</g>')
    s.append('</svg>')
    return "\n".join(s)


G = {
    "documents": '<path d="M -5 -5 h 10 M -5 -1 h 10 M -5 3 h 6"/>',
    "download":  '<path d="M 0 -6 v 8 m 0 0 l -3.5 -3.5 M 0 2 l 3.5 -3.5 M -6 5 h 12"/>',
    "music":     '<path d="M -2 4 a 2.6 2.6 0 1 0 0.1 -0.1 M 0.6 3.6 V -5 l 6 -1.6 v 8"/>'
                 '<circle cx="4" cy="4" r="2.6"/>',
    "pictures":  '<rect x="-6.5" y="-5.5" width="13" height="11" rx="1.5"/>'
                 '<circle cx="-2.6" cy="-2" r="1.6"/><path d="M -6.5 3.5 l 4.5 -4 l 3.5 3 l 2.5 -2 l 2.5 3"/>',
    "videos":    '<rect x="-6.5" y="-5" width="13" height="10" rx="1.6"/><path d="M -1.8 -1.8 l 4 1.8 l -4 1.8 Z"/>',
    "home":      '<path d="M -6.5 0 L 0 -6 L 6.5 0 M -4.5 -1.6 V 5.5 h 9 V -1.6"/>',
    "desktop":   '<rect x="-7" y="-5.5" width="14" height="9.5" rx="1.4"/><path d="M -3.5 6.5 h 7"/>',
    "public":    '<circle cx="-4.5" cy="-2.5" r="2.2"/><circle cx="4.5" cy="-2.5" r="2.2"/>'
                 '<circle cx="0" cy="4" r="2.2"/><path d="M -2.6 -1 L -1 2.2 M 2.6 -1 L 1 2.2"/>',
    "templates": '<path d="M -5 -6 h 6.5 L 5.5 -2 V 6 h -10.5 Z M 1.5 -6 v 4 h 4"/>',
    "remote":    '<circle cx="0" cy="0" r="6.2"/><path d="M -6.2 0 h 12.4 M 0 -6.2 c 3 3 3 9.4 0 12.4 '
                 'c -3 -3 -3 -9.4 0 -12.4"/>',
    "search":    '<circle cx="-1.2" cy="-1.2" r="4.6"/><path d="M 2.4 2.4 L 6.4 6.4"/>',
    "trash":     '<path d="M -6 -3.5 h 12 M -4 -3.5 v 9 h 8 v -9 M -2 -3.5 v -2 h 4 v 2 M -1.5 -0.5 v 5 M 1.5 -0.5 v 5"/>',
    "code":      '<path d="M -2.5 -5 l -4.5 5 l 4.5 5 M 2.5 -5 l 4.5 5 l -4.5 5"/>',
}

# name -> (accent, glyph key, is_open, is_accept)
ICONS = {
    "folder":                 (CYAN,    None,        False, False),
    "folder-open":            (CYAN,    None,        True,  False),
    "folder-visiting":        (CYAN,    None,        True,  False),
    "folder-drag-accept":     (MINT,    None,        True,  True),
    "folder-documents":       (CYAN,    "documents", False, False),
    "folder-download":        (MINT,    "download",  False, False),
    "folder-downloads":       (MINT,    "download",  False, False),
    "folder-music":           (VIOLET,  "music",     False, False),
    "folder-pictures":        (MAGENTA, "pictures",  False, False),
    "folder-videos":          (ROSE,    "videos",    False, False),
    "folder-publicshare":     (BLUE,    "public",    False, False),
    "folder-templates":       (GOLD,    "templates", False, False),
    "folder-remote":          (BLUE,    "remote",    False, False),
    "folder-saved-search":    (GOLD,    "search",    False, False),
    "folder-recent":          (GOLD,    "search",    False, False),
    "folder-development":     (MINT,    "code",      False, False),
    "user-home":              (CYAN,    "home",      False, False),
    "user-desktop":           (CYAN,    "desktop",   False, False),
    "user-trash":             (ROSE,    "trash",     False, False),
    "user-trash-full":        (ROSE,    "trash",     False, False),
    "folder-trash":           (ROSE,    "trash",     False, False),
    "network-workgroup":      (BLUE,    "remote",    False, False),
}

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
places = os.path.join(ROOT, "icons/Off-World/scalable/places")
mimes = os.path.join(ROOT, "icons/Off-World/scalable/mimetypes")
for d in (places, mimes):
    os.makedirs(d, exist_ok=True)

for name, (accent, gk, op, acc) in ICONS.items():
    svg = folder(accent, G.get(gk, ""), op, acc)
    open(os.path.join(places, name + ".svg"), "w").write(svg)

# file managers ask for inode-directory as a mimetype
open(os.path.join(mimes, "inode-directory.svg"), "w").write(folder(CYAN, "", False, False))

open(os.path.join(ROOT, "icons/Off-World/index.theme"), "w").write("""[Icon Theme]
Name=Off-World
Comment=Neon-noir folders for the Off-World Omarchy theme
Inherits=Yaru-magenta-dark,Yaru-dark,Adwaita,hicolor
Directories=scalable/places,scalable/mimetypes
Example=folder

[scalable/places]
Size=48
MinSize=8
MaxSize=512
Context=Places
Type=Scalable

[scalable/mimetypes]
Size=48
MinSize=8
MaxSize=512
Context=MimeTypes
Type=Scalable
""")
print("wrote %d place icons + 1 mimetype" % len(ICONS))
