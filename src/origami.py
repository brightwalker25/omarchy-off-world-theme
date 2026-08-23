"""Gaff's unicorn, folded from light. Rearing, facing left. Ground at y=100."""

# Each facet is a flat plane of folded paper. Shade = how it catches the light.
FACETS = [
    # name,            points,                                                   shade
    ("horn",     [(31.0, 11.5), (35.0, 9.0), (13.0, -10.0)],                      1.00),
    ("ear",      [(35.5, 8.5), (40.0, 1.0), (42.0, 10.5)],                        0.86),
    ("head",     [(19.0, 23.5), (21.5, 27.5), (34.5, 20.0), (33.0, 10.5)],        0.94),
    ("muzzle",   [(19.0, 23.5), (21.5, 27.5), (24.5, 25.0)],                      0.66),
    ("jaw",      [(21.5, 27.5), (34.5, 20.0), (32.0, 26.5)],                      0.62),
    ("neck",     [(33.0, 10.5), (34.5, 20.0), (58.0, 46.0), (62.0, 33.0)],        0.82),
    ("neck lo",  [(34.5, 20.0), (32.0, 26.5), (54.0, 50.0), (58.0, 46.0)],        0.60),
    ("mane a",   [(34.0, 10.0), (44.0, 13.0), (40.0, 20.0)],                      1.00),
    ("mane b",   [(40.0, 20.0), (50.0, 22.0), (46.0, 29.0)],                      0.92),
    ("mane c",   [(46.0, 29.0), (57.0, 31.0), (53.0, 38.0)],                      0.86),
    ("mane d",   [(53.0, 38.0), (63.0, 40.0), (60.0, 46.0)],                      0.78),
    ("back",     [(62.0, 33.0), (84.0, 56.0), (79.0, 68.0), (58.0, 46.0)],        0.88),
    ("belly",    [(58.0, 46.0), (79.0, 68.0), (73.0, 74.0), (54.0, 50.0)],        0.58),
    ("chest",    [(54.0, 50.0), (58.0, 46.0), (60.5, 52.0)],                      0.70),
    ("rump",     [(84.0, 56.0), (89.0, 67.0), (78.0, 66.0)],                      0.74),
    ("tail",     [(84.0, 54.0), (97.0, 60.0), (90.0, 65.0), (99.0, 78.0),
                  (88.0, 70.0), (91.0, 90.0), (80.0, 64.0)],                      0.96),
    # hind legs
    ("hind f u", [(66.0, 59.0), (74.0, 60.0), (78.0, 78.0), (71.0, 79.0)],        0.50),
    ("hind f l", [(71.0, 79.0), (78.0, 78.0), (75.0, 99.0), (69.0, 99.0)],        0.44),
    ("hind n u", [(74.0, 62.0), (82.0, 63.0), (86.0, 80.0), (79.0, 81.0)],        0.90),
    ("hind n l", [(79.0, 81.0), (86.0, 80.0), (83.0, 99.0), (77.0, 99.0)],        0.80),
    # forelegs, folded and raised
    ("fore f u", [(56.0, 39.0), (58.5, 47.5), (38.0, 54.0), (34.0, 47.5)],        0.48),
    ("fore f l", [(34.0, 47.5), (38.0, 54.0), (24.0, 42.0), (22.0, 35.5)],        0.42),
    ("fore n u", [(58.0, 43.5), (60.5, 52.0), (42.0, 62.0), (38.0, 55.5)],        0.98),
    ("fore n l", [(38.0, 55.5), (42.0, 62.0), (27.5, 52.0), (25.5, 45.5)],        0.88),
]

def poly(pts):
    return "M " + " L ".join("%.2f %.2f" % p for p in pts) + " Z"


def facets_svg(body="#ff5cf0", edge="#ffd9f2", edge_w=0.45):
    """Flat planes plus their fold lines, in the 0..100 unit space."""
    out = []
    for _name, pts, shade in FACETS:
        out.append('<path d="%s" fill="%s" opacity="%.2f"/>' % (poly(pts), body, shade))
    out.append('<g fill="none" stroke="%s" stroke-width="%.2f" opacity="0.55" stroke-linejoin="round">'
               % (edge, edge_w))
    for _name, pts, _shade in FACETS:
        out.append('<path d="%s"/>' % poly(pts))
    out.append('</g>')
    return "".join(out)


def silhouette():
    """Every facet as one path - used as a clip for scan lines."""
    return "".join(poly(pts) for _n, pts, _s in FACETS)


if __name__ == "__main__":
    W, H, PAD = 900, 1000, 60
    sx = (W - 2 * PAD) / 100.0
    sy = (H - 2 * PAD) / 100.0
    S = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H)]
    S.append('<rect width="%d" height="%d" fill="#0b1020"/>' % (W, H))
    S.append('<g transform="translate(%d,%d) scale(%f,%f)">%s</g>' % (PAD, PAD, sx, sy, facets_svg()))
    S.append('<line x1="0" y1="%.0f" x2="%d" y2="%.0f" stroke="#00e5ff" stroke-width="2" opacity="0.4"/>'
             % (PAD + sy * 100, W, PAD + sy * 100))
    S.append('</svg>')
    open("origami.svg", "w").write("".join(S))
    print("ok")
