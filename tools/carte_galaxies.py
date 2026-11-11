# -*- coding: utf-8 -*-
"""Génère galaxies/carte_1.svg, carte_2.svg, carte_3.svg (carte de Lodenn, bible v3 § 7)."""
import math, random, sys, os

OUT = sys.argv[1]
random.seed(11)

try:
    from PIL import ImageFont
    _F = ImageFont.truetype('/System/Library/Fonts/Supplemental/Georgia Italic.ttf', 100)
    def adv(ch):
        return _F.getlength(ch) / 100.0
except Exception:
    def adv(ch):
        return 0.28 if ch in " .,'" else 0.5

INK = '#3b2616'
RED = '#a5281c'
PX0, PY0, PX1, PY1 = 60, 40, 1140, 760
FONT = 'font-family="Georgia, \'Times New Roman\', serif"'


# ------------------------------------------------------------------ géométrie
def catmull(pts, closed=False, n=14):
    out = []
    L = len(pts)
    rng = range(L) if closed else range(L - 1)
    for i in rng:
        if closed:
            p0, p1, p2, p3 = pts[(i - 1) % L], pts[i], pts[(i + 1) % L], pts[(i + 2) % L]
        else:
            p0 = pts[i - 1] if i > 0 else pts[0]
            p1, p2 = pts[i], pts[i + 1]
            p3 = pts[i + 2] if i + 2 < L else pts[-1]
        for k in range(n):
            t = k / n
            t2, t3 = t * t, t * t * t
            out.append(tuple(
                0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2
                       + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    if not closed:
        out.append(tuple(pts[-1]))
    return out


def cumlen(pts):
    c = [0.0]
    for a, b in zip(pts, pts[1:]):
        c.append(c[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    return c


def at(pts, cl, s):
    """point + tangente unitaire à l'abscisse curviligne s"""
    s = max(0, min(cl[-1], s))
    lo, hi = 0, len(cl) - 1
    while hi - lo > 1:
        m = (lo + hi) // 2
        if cl[m] <= s:
            lo = m
        else:
            hi = m
    a, b = pts[lo], pts[hi]
    d = cl[hi] - cl[lo] or 1
    t = (s - cl[lo]) / d
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t), ((b[0] - a[0]) / d, (b[1] - a[1]) / d)


def path(pts, closed=False):
    return 'M' + ' L'.join('%.1f,%.1f' % p for p in pts) + ('Z' if closed else '')


def seg_hit(a, b, c, d):
    r = (b[0] - a[0], b[1] - a[1]); s = (d[0] - c[0], d[1] - c[1])
    den = r[0] * s[1] - r[1] * s[0]
    if abs(den) < 1e-12:
        return None
    t = ((c[0] - a[0]) * s[1] - (c[1] - a[1]) * s[0]) / den
    u = ((c[0] - a[0]) * r[1] - (c[1] - a[1]) * r[0]) / den
    if 0 <= t <= 1 and 0 <= u <= 1:
        return t
    return None


def hits(a, b, poly):
    hs = []
    for c, d in zip(poly, poly[1:]):
        t = seg_hit(a, b, c, d)
        if t is not None:
            hs.append(t)
    return sorted(hs)


def inside(p, poly):
    x, y = p; c = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]; x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
            c = not c
    return c


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


# ------------------------------------------------------------------ points clés
K = (240.0, 360.0)            # clocher de la chapelle (l'œil)
Pm = (480.0, 562.0)           # bout du Môle (point rouge)
G = (953.0, 422.0)            # Corps de garde, sur la Miette
C = (385.0, 503.0)            # la cale
R = (245.0, 668.0)            # rose des vents


def on_line(a, b, x):
    return (x, a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0]))


X = on_line(K, Pm, 310.0)     # la Croix, exactement sur clocher -> bout du Môle
M = on_line(Pm, G, 1072.0)    # milieu des deux Sœurs, exactement sur bout du Môle -> Corps de garde
SA = (M[0] - 11, M[1] - 17)   # pied de la Sœur nord
SB = (M[0] + 11, M[1] + 17)   # pied de la Sœur sud

# la découpe : ligne médiane (haut -> bas)
CUT_CTRL = [(570, 26), (566, 120), (571, 210), (565, 300), (569, 390), (566, 470), (566, 518), (562, 542),
            (546, 554), (522, 551), (480, 538), (430, 531), (398, 527), (374, 537), (352, 560), (300, 613),
            (245, 668), (190, 723), (150, 763), (136, 777)]
cut = catmull(CUT_CTRL, n=24)
ccl = cumlen(cut)
AMP, STEP = 7.0, 12.0
zig = []
i = 0
s = 0.0
while s <= ccl[-1]:
    p, t = at(cut, ccl, s)
    nx, ny = t[1], -t[0]          # normale côté est
    sg = 1 if i % 2 == 0 else -1
    zig.append((p[0] + nx * AMP * sg, p[1] + ny * AMP * sg))
    i += 1
    s += STEP
WEST = zig + [(-300, 1000), (-300, -200), (zig[0][0], -200)]
EAST = zig + [(1500, 1000), (1500, -200), (zig[0][0], -200)]

# le Môle
MOLE_CTRL = [C, (388, 530), (393, 558), (408, 583), (432, 596), (458, 591), (474, 579), Pm]
mole = catmull(MOLE_CTRL, n=20)
mcl = cumlen(mole)
MOLE_LEN = mcl[-1]
BAR = MOLE_LEN / 3.0            # « cent pas de mousse » : le Môle en fait trois cents

# l'île (sens horaire depuis le nez)
ISLAND_CTRL = [(128, 398), (160, 362), (215, 326), (300, 297), (400, 282), (500, 277), (590, 285), (670, 308),
               (730, 336), (770, 352), (802, 338), (832, 308), (851, 289), (847, 322), (833, 360), (846, 395),
               (866, 427), (830, 418), (798, 406), (768, 402), (730, 430), (680, 462), (620, 485), (560, 497),
               (480, 503), (400, 504), (320, 492), (250, 470), (190, 443), (150, 420)]
isl = catmull(ISLAND_CTRL, closed=True, n=12)
area = sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(isl, isl[1:] + isl[:1])) / 2
SG = 1 if area > 0 else -1


def inward(i):
    a, b = isl[i - 1], isl[(i + 1) % len(isl)]
    tx, ty = b[0] - a[0], b[1] - a[1]
    d = math.hypot(tx, ty) or 1
    return (-ty / d * SG, tx / d * SG)


def offset(d):
    return [(p[0] - inward(i)[0] * d, p[1] - inward(i)[1] * d) for i, p in enumerate(isl)]


# ------------------------------------------------------------------ vérifications
def side(p):
    return 'O' if inside(p, WEST) else 'E'


h1 = hits(K, Pm, zig)
h2 = hits(M, Pm, zig)
assert h1 and h2, 'les traits doivent rencontrer la découpe avant le bout du Môle'
E1 = lerp(K, Pm, h1[0])
E2 = lerp(M, Pm, h2[0])
d1 = math.hypot(Pm[0] - E1[0], Pm[1] - E1[1])
d2 = math.hypot(Pm[0] - E2[0], Pm[1] - E2[1])
mh = []
for a, b in zip(mole, mole[1:]):
    mh += hits(a, b, zig)
report = {
    'K': side(K), 'X': side(X), 'C': side(C), 'P': side(Pm), 'G': side(G), 'M': side(M),
    'N': side((R[0], R[1] - 66)), 'Ouest': side((R[0] - 66, R[1])), 'S': side((R[0], R[1] + 66)),
    'Est': side((R[0] + 66, R[1])),
    'fin trait 1': E1, 'reste 1': round(d1, 1), 'fin trait 2': E2, 'reste 2': round(d2, 1),
    'coupes du Mole': len(mh), 'long. Mole': round(MOLE_LEN, 1), 'barre': round(BAR, 1),
    'X': X, 'M': M,
}
for k, v in report.items():
    print(k, v)
assert side(K) == 'O' and side(C) == 'O' and side(Pm) == 'E' and side(G) == 'E' and side(M) == 'E'
assert side((R[0], R[1] - 66)) == 'O' and side((R[0] - 66, R[1])) == 'O'
assert side((R[0], R[1] + 66)) == 'E' and side((R[0] + 66, R[1])) == 'E'
assert len(mh) == 1 and d1 > 15 and d2 > 15
# la ligne de visée du bout du Môle vers la Miette ne touche pas l'île
assert not hits(Pm, G, isl + isl[:1]), 'la visée Môle -> Miette coupe la côte'
# alignements exacts
for a, b, c in ((K, X, Pm), (M, G, Pm)):
    cr = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    assert abs(cr) < 1e-6

# abscisse du Môle à la découpe (pour le bout « tache »)
for idx, (a, b) in enumerate(zip(mole, mole[1:])):
    if hits(a, b, zig):
        MOLE_CUT_S = mcl[idx]
        break
print('bout ouest du Mole (px):', round(MOLE_CUT_S, 1))


# ------------------------------------------------------------------ dessins élémentaires
def wavy_rect():
    pts = []
    def edge(a, b, n):
        for k in range(n):
            t = k / n
            x = a[0] + (b[0] - a[0]) * t; y = a[1] + (b[1] - a[1]) * t
            pts.append((x + random.uniform(-2.2, 2.2), y + random.uniform(-2.2, 2.2)))
    c = 10
    edge((PX0 + c, PY0), (PX1 - c, PY0), 36)
    edge((PX1, PY0 + c), (PX1, PY1 - c), 24)
    edge((PX1 - c, PY1), (PX0 + c, PY1), 36)
    edge((PX0, PY1 - c), (PX0, PY0 + c), 24)
    # deux petites entailles
    for j, p in enumerate(pts):
        if abs(p[0] - 820) < 12 and p[1] > 700:
            pts[j] = (p[0], p[1] - 9)
        if abs(p[1] - 300) < 12 and p[0] > 1100:
            pts[j] = (p[0] - 8, p[1])
    return catmull(pts, closed=True, n=4)


PAPER = wavy_rect()


def chapel(k):
    x, y = k
    return f'''<g fill="#eedfb6" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round">
<path d="M{x-30},{y+7} L{x-30},{y-6} L{x-24},{y-14} L{x-5},{y-14} L{x-5},{y+7} Z"/>
<path d="M{x-30},{y-6} L{x-5},{y-6}" fill="none" stroke-width="1"/>
<path d="M{x-5.5},{y+7} L{x-5.5},{y-22} L{x},{y-36} L{x+5.5},{y-22} L{x+5.5},{y+7} Z"/>
<path d="M{x-5.5},{y-22} L{x+5.5},{y-22}" fill="none" stroke-width="1"/>
<path d="M{x},{y-36} L{x},{y-45} M{x-3.5},{y-41.5} L{x+3.5},{y-41.5}" fill="none" stroke-width="1.5"/>
<path d="M{x-2},{y-12} L{x-2},{y-17} L{x+2},{y-17} L{x+2},{y-12} Z" fill="{INK}" stroke="none"/>
<path d="M{x-20},{y+7} L{x-20},{y} Q{x-17.5},{y-4} {x-15},{y} L{x-15},{y+7}" fill="{INK}" fill-opacity=".55" stroke-width="1"/>
</g>'''


def croix(p):
    x, y = p
    return f'''<g fill="none" stroke="{INK}" stroke-width="2.2" stroke-linecap="round">
<path d="M{x:.1f},{y-12:.1f} L{x:.1f},{y+8:.1f} M{x-6.5:.1f},{y-5:.1f} L{x+6.5:.1f},{y-5:.1f}"/>
<path d="M{x-5:.1f},{y+8:.1f} L{x+5:.1f},{y+8:.1f} M{x-8:.1f},{y+11.5:.1f} L{x+8:.1f},{y+11.5:.1f}" stroke-width="1.8"/>
</g>'''


def house(bx, by, w=13):
    h = w / 2
    return (f'<path d="M{bx-h},{by} L{bx-h},{by-8} L{bx},{by-15.5} L{bx+h},{by-8} L{bx+h},{by} Z" fill="#eedfb6" '
            f'stroke="{INK}" stroke-width="1.5" stroke-linejoin="round"/>'
            f'<path d="M{bx-h},{by-8} L{bx+h},{by-8}" stroke="{INK}" stroke-width="1" fill="none"/>'
            f'<rect x="{bx-1.5}" y="{by-5}" width="3" height="5" fill="{INK}" fill-opacity=".7"/>')


def anchor(x, y, ident):
    return f'''<g class="ancre" id="{ident}" transform="translate({x},{y})">
<circle class="halo" r="13" fill="#f6c93c" filter="url(#lueur)"/>
<g class="trait" fill="none" stroke="{INK}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
<circle cx="0" cy="-8.2" r="2.1"/><path d="M0,-6 L0,7.5 M-4.2,-3.6 L4.2,-3.6"/>
<path d="M-6.6,1.6 Q-5.6,7.8 0,7.8 Q5.6,7.8 6.6,1.6"/><path d="M-8.2,3.6 L-6.6,1.2 L-4.6,3.4 M8.2,3.6 L6.6,1.2 L4.6,3.4" stroke-width="1.3"/>
</g></g>'''


def tower(p):
    x, y = p
    return (f'<path d="M{x-6.5:.1f},{y:.1f} L{x-5.5:.1f},{y-19:.1f} L{x-2.5:.1f},{y-25:.1f} L{x+2.5:.1f},{y-26:.1f} '
            f'L{x+5.5:.1f},{y-20:.1f} L{x+6.5:.1f},{y:.1f} Z" fill="#d9cfb4" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round"/>'
            f'<path d="M{x+2:.1f},{y-22:.1f} L{x+3:.1f},{y-3:.1f} M{x-0.5:.1f},{y-12:.1f} L{x:.1f},{y-2:.1f} M{x-3:.1f},{y-18:.1f} L{x-3.2:.1f},{y-10:.1f}" '
            f'fill="none" stroke="{INK}" stroke-width=".9" stroke-opacity=".8"/>'
            f'<path d="M{x-10:.1f},{y+1.5:.1f} q4,-3 8,0 q4,3 8,0 q3,-2 5,0" fill="none" stroke="{INK}" stroke-width="1" stroke-opacity=".7"/>')


def wave(x, y, s=1.0):
    return f'<path d="M{x},{y} q{4*s},{-4*s} {8*s},0 q{4*s},{4*s} {8*s},0 q{4*s},{-4*s} {8*s},0"/>'


def rose():
    x, y = R
    o = [f'<g transform="translate({x},{y})">']
    o.append(f'<circle r="40" fill="#efe2bb" fill-opacity=".55" stroke="{INK}" stroke-width="1.3"/>')
    o.append(f'<circle r="35.5" fill="none" stroke="{INK}" stroke-width=".8"/>')
    for a in range(0, 360, 15):
        r1 = 35.5 if a % 45 else 31
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        o.append(f'<path d="M{r1*ca:.1f},{r1*sa:.1f} L{40*ca:.1f},{40*sa:.1f}" stroke="{INK}" stroke-width=".8"/>')
    for a in (45, 135, 225, 315):  # pointes courtes
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        px, py = -sa, ca
        o.append(f'<path d="M{30*ca:.1f},{30*sa:.1f} L{6*px:.1f},{6*py:.1f} L{-6*px:.1f},{-6*py:.1f} Z" fill="#cdb98a" stroke="{INK}" stroke-width="1"/>')
        o.append(f'<path d="M{30*ca:.1f},{30*sa:.1f} L{6*px:.1f},{6*py:.1f} L0,0 Z" fill="{INK}" fill-opacity=".75"/>')
    for a, L in ((270, 56), (0, 50), (90, 50), (180, 50)):  # N, E, S, O
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        px, py = -sa, ca
        o.append(f'<path d="M{L*ca:.1f},{L*sa:.1f} L{8*px:.1f},{8*py:.1f} L{-8*px:.1f},{-8*py:.1f} Z" fill="#efe2bb" stroke="{INK}" stroke-width="1.2" stroke-linejoin="round"/>')
        o.append(f'<path d="M{L*ca:.1f},{L*sa:.1f} L{8*px:.1f},{8*py:.1f} L0,0 Z" fill="{INK}" fill-opacity=".85"/>')
    o.append(f'<circle r="3" fill="#efe2bb" stroke="{INK}" stroke-width="1.2"/>')
    o.append('</g>')
    o.append(f'<g {FONT} font-size="21" font-weight="bold" fill="{INK}" text-anchor="middle">'
             f'<text x="{x}" y="{y-61}">N</text><text x="{x+65}" y="{y+7}">E</text>'
             f'<text x="{x}" y="{y+74}">S</text><text x="{x-66}" y="{y+7}">O</text></g>')
    return '\n'.join(o)


def ship(x, y):
    o = [f'<g transform="translate({x},{y})" stroke="{INK}" stroke-linejoin="round" stroke-linecap="round">']
    o.append('<path d="M-30,-2 Q-27,10 -14,11 L16,11 Q27,9 33,-4 L20,-1 L-22,-1 Z" fill="#b9935a" stroke-width="1.6"/>')
    o.append('<path d="M-24,4 L26,4" fill="none" stroke-width=".8"/>')
    o.append('<path d="M33,-4 L47,-11 M-13,-1 L-13,-40 M3,-1 L3,-50 M18,-1 L18,-38" fill="none" stroke-width="1.4"/>')
    for mx, tops in ((-13, (-37, -20)), (3, (-47, -28, -11)), (18, (-35, -19))):
        for k, ty in enumerate(tops):
            w = 7.5 + k * 1.6
            hh = 14 if k < len(tops) - 1 or len(tops) == 2 else 9
            o.append(f'<path d="M{mx-w+1},{ty} L{mx+w-1},{ty} Q{mx+w+3},{ty+hh/2} {mx+w},{ty+hh} L{mx-w},{ty+hh} Q{mx-w+3},{ty+hh/2} {mx-w+1},{ty} Z" fill="#f2e8c8" stroke-width="1.1"/>')
    o.append('<path d="M47,-11 L20,-30 L22,-6 Z" fill="#f2e8c8" stroke-width="1"/>')
    o.append(f'<path d="M3,-50 L3,-57 L12,-54.5 L3,-52" fill="{RED}" fill-opacity="0" stroke-width="1"/>')
    o.append('<path d="M-42,15 q5,-4 10,0 q5,4 10,0 q5,-4 10,0 q5,4 10,0 q5,-4 10,0 q5,4 10,0 q5,-4 10,0 q5,4 10,0" fill="none" stroke-width="1"/>')
    o.append('<path d="M-56,22 q5,-4 10,0 q5,4 10,0 q5,-4 10,0 M10,23 q5,-4 10,0 q5,4 10,0 q5,-4 10,0" fill="none" stroke-width=".9" stroke-opacity=".7"/>')
    o.append('</g>')
    return '\n'.join(o)


def scale_bar(x0, y0):
    b = BAR
    o = [f'<g stroke="{INK}" fill="none" stroke-linecap="round">']
    o.append(f'<rect x="{x0:.1f}" y="{y0}" width="{b:.1f}" height="6" stroke-width="1.3" fill="#efe2bb"/>')
    for k in range(4):
        if k % 2 == 0:
            o.append(f'<rect x="{x0+k*b/4:.1f}" y="{y0}" width="{b/4:.1f}" height="6" fill="{INK}" fill-opacity=".8" stroke="none"/>')
    for k in range(5):
        xx = x0 + k * b / 4
        o.append(f'<path d="M{xx:.1f},{y0+6} L{xx:.1f},{y0+(11 if k in (0,4) else 9)}" stroke-width="1.1"/>')
    # le tout petit bonhomme : un enfant (grosse tête, bonnet, jambes courtes) qui marche sur la barre
    bx = x0 + b * 0.36
    o.append(f'<g transform="translate({bx:.1f},{y0})" stroke-width="1.5">'
             f'<circle cx="0" cy="-15.5" r="3.6" fill="#efe2bb"/>'
             f'<path d="M-3.6,-17 Q0,-23.5 3.8,-17.2 M3.2,-19.5 L6.2,-20.4" stroke-width="1.3"/>'
             f'<path d="M0,-11.8 L0,-5.2 M0,-5.2 L-3.6,-0.4 M0,-5.2 L3.8,-0.4 M3.8,-0.4 L5.6,-0.6 M0,-10 L-4,-6.6 M0,-10 L4.2,-8"/></g>')
    o.append('</g>')
    o.append(f'<text x="{x0+b/2:.1f}" y="{y0+35}" {FONT} font-style="italic" font-size="21" fill="{INK}" text-anchor="middle">cent pas de mousse</text>')
    return '\n'.join(o)


def cx_at(y):
    best = min(cut[:len(cut) // 3], key=lambda p: abs(p[1] - y))
    return best[0]


def top_text():
    west = ["Qui me lit ſeul", "Mon tréſor eſt", "Il dort ſous la", "du chemin qui", "Venez à deux"]
    east = ["me lit de travers.", "aux jumelles.", "dernière pierre", "marche ſur la mer.", "le jour de la grande maline."]
    o = [f'<g {FONT} font-style="italic" font-size="26" fill="{INK}" fill-opacity=".93">']
    for i in range(5):
        y = 96 + i * 30
        cx = cx_at(y - 8)
        o.append(f'<text x="{cx-17:.1f}" y="{y}" text-anchor="end">{west[i]}</text>')
        o.append(f'<text x="{cx+17:.1f}" y="{y}">{east[i]}</text>')
    o.append('</g>')
    return '\n'.join(o)


def cut_writing():
    txt = ("Avant la maline, quatre leçons. La première t'attend au bout du chemin que la mer reprend, "
           "dans la maiſon ſans lit ni feu, au toit de pierre. Cherche l'ancre qui n'a jamais mouillé.")
    # début : un peu sous le bord haut ; fin : avant la rose des vents
    s0 = next(ccl[i] for i, p in enumerate(cut) if p[1] >= 52)
    s1 = next(ccl[i] for i, p in enumerate(cut) if p[1] > 560 and math.hypot(p[0] - R[0], p[1] - R[1]) < 66)
    widths = [adv(ch) * 1.05 for ch in txt]
    fs = (s1 - s0) / sum(widths)
    print('écriture de la découpe : corps %.1f px, longueur %.0f px' % (fs, s1 - s0))
    o = [f'<g {FONT} font-style="italic" font-size="{fs:.2f}" fill="{INK}" text-anchor="middle">']
    s = s0
    for ch, w in zip(txt, widths):
        sc = s + w * fs / 2
        s += w * fs
        if ch == ' ':
            continue
        p, t = at(cut, ccl, sc)
        ang = math.degrees(math.atan2(t[1], t[0]))
        c = ch.replace("'", '&#8217;')
        o.append(f'<text transform="translate({p[0]:.1f} {p[1]:.1f}) rotate({ang:.1f})" y="{fs*0.25:.1f}">{c}</text>')
    o.append('</g>')
    return '\n'.join(o), fs


CUT_TXT, CUT_FS = cut_writing()


def label(x, y, t, anchor='middle', size=21, extra=''):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" {extra}>{t}</text>'


# ------------------------------------------------------------------ la carte (dessin commun)
def carte():
    o = []
    isl_d = path(isl, True)
    # --- lavis
    o.append('<rect x="40" y="225" width="1120" height="560" fill="url(#mer)"/>')
    o.append(f'<path d="{isl_d}" fill="none" stroke="#3f6f80" stroke-opacity=".30" stroke-width="34" filter="url(#flou8)"/>')
    for cx, cy, rx, ry, op in ((965, 415, 150, 62, .62), (890, 372, 60, 34, .45), (455, 548, 92, 50, .55),
                               (1070, 392, 46, 40, .4), (700, 478, 80, 18, .4), (170, 452, 40, 16, .3)):
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#f1e3b4" fill-opacity="{op}" filter="url(#flou8)"/>')
    # --- traits (plume)
    o.append('<g filter="url(#plume)">')
    o.append(f'<path d="{path(offset(5), True)}" fill="none" stroke="{INK}" stroke-opacity=".55" stroke-width=".9"/>')
    o.append(f'<path d="{path(offset(10), True)}" fill="none" stroke="{INK}" stroke-opacity=".38" stroke-width=".8" stroke-dasharray="9 5"/>')
    o.append(f'<path d="{path(offset(16), True)}" fill="none" stroke="{INK}" stroke-opacity=".22" stroke-width=".8" stroke-dasharray="4 9"/>')
    o.append(f'<path d="{isl_d}" fill="#cda65c" fill-opacity=".50"/>')
    o.append(f'<path d="{isl_d}" fill="url(#terre)"/>')
    o.append(f'<path d="{isl_d}" fill="none" stroke="{INK}" stroke-width="2.3" stroke-linejoin="round"/>')
    # falaises du dos (nord) : petits traits vers l'intérieur
    tk = []
    for i, p in enumerate(isl):
        n = inward(i)
        if n[1] > 0.55 and 215 < p[0] < 760 and i % 2 == 0:
            L = random.uniform(4, 7.5)
            tk.append(f'M{p[0]:.1f},{p[1]:.1f} l{n[0]*L+random.uniform(-1,1):.1f},{n[1]*L:.1f}')
    o.append(f'<path d="{" ".join(tk)}" fill="none" stroke="{INK}" stroke-width="1" stroke-opacity=".8"/>')
    # grève de la plage (flanc sud-est) : pointillé de sable
    dots = []
    for i, p in enumerate(isl):
        n = inward(i)
        if n[1] < -0.3 and 600 < p[0] < 742:
            for _ in range(5):
                d = random.uniform(2.5, 10)
                dots.append(f'<circle cx="{p[0]+n[0]*d+random.uniform(-4,4):.1f}" cy="{p[1]+n[1]*d:.1f}" r=".8"/>')
    o.append(f'<g fill="{INK}" fill-opacity=".7">{"".join(dots)}</g>')
    # la butte de la chapelle
    hb = []
    for a in range(200, 345, 12):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        hb.append(f'M{K[0]-10+40*ca:.1f},{K[1]+12-17*sa*-1:.1f} l{7*ca:.1f},{-5*sa*-1+3:.1f}')
    for a in range(20, 165, 13):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        hb.append(f'M{K[0]-10+42*ca:.1f},{K[1]+10+15*sa:.1f} l{7*ca:.1f},{6*sa:.1f}')
    o.append(f'<path d="{" ".join(hb)}" fill="none" stroke="{INK}" stroke-width="1" stroke-opacity=".75" stroke-linecap="round"/>')
    # touffes de lande
    tf = []
    for (x, y) in ((400, 312), (445, 300), (470, 318), (500, 300), (604, 316), (640, 334), (684, 348), (600, 362),
                   (648, 392), (500, 385), (455, 398), (530, 412), (372, 384), (412, 368), (620, 410), (700, 414),
                   (330, 322), (296, 384), (200, 392), (180, 372), (212, 420), (262, 432), (742, 372), (560, 330)):
        tf.append(f'M{x-4},{y} q1,-5 3,-6 M{x},{y} q0,-6 0,-8 M{x+4},{y} q-1,-5 -3,-6')
    o.append(f'<path d="{" ".join(tf)}" fill="none" stroke="{INK}" stroke-width=".9" stroke-opacity=".6" stroke-linecap="round"/>')
    # rochers du nez et écueils
    rk = []
    for (x, y) in ((112, 392), (104, 404), (118, 412), (98, 388), (150, 344), (866, 280), (876, 292), (300, 520),
                   (120, 430), (770, 325)):
        rk.append(f'M{x-3.5},{y+2} l2,-5 l3,-1 l2.5,4 z')
    o.append(f'<path d="{" ".join(rk)}" fill="{INK}" fill-opacity=".55" stroke="{INK}" stroke-width=".8"/>')
    # chapelle, croix, bourg, cale, Pierre Longue, moulin
    o.append(chapel(K))
    o.append(croix(X))
    for bx, by in ((415, 482), (440, 471), (466, 480), (492, 470), (520, 484)):
        o.append(house(bx, by))
    cxx, cyy = C
    o.append(f'<path d="M{cxx-17},{cyy-4} L{cxx-3},{cyy-4} L{cxx-4},{cyy+13} L{cxx-12},{cyy+13} Z" fill="#d9cfb4" stroke="{INK}" stroke-width="1.4" stroke-linejoin="round"/>'
             f'<path d="M{cxx-15.5},{cyy} L{cxx-3.5},{cyy} M{cxx-14},{cyy+4.5} L{cxx-3.6},{cyy+4.5} M{cxx-13},{cyy+9} L{cxx-3.8},{cyy+9}" stroke="{INK}" stroke-width=".9" fill="none"/>')
    o.append(f'<path d="M536,323 L538,301 L541.5,296 L545.5,302 L545,323 Z" fill="#d9cfb4" stroke="{INK}" stroke-width="1.7" stroke-linejoin="round"/>'
             f'<path d="M530,324 L551,324 M542,300 L542.5,318" fill="none" stroke="{INK}" stroke-width="1"/>')
    mx, my = 818, 401
    o.append(f'<path d="M{mx-6.5},{my} L{mx-4.5},{my-16} L{mx+4.5},{my-16} L{mx+6.5},{my} Z" fill="#eedfb6" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>'
             f'<path d="M{mx-5.5},{my-16} L{mx},{my-22} L{mx+5.5},{my-16} Z" fill="{INK}" fill-opacity=".7" stroke="{INK}" stroke-width="1.2"/>')
    sl = []
    for a in (32, 122, 212, 302):
        ca, sa = math.cos(math.radians(a)), math.sin(math.radians(a))
        px, py = -sa, ca
        hx, hy = mx, my - 17
        sl.append(f'M{hx:.1f},{hy:.1f} L{hx+15*ca:.1f},{hy+15*sa:.1f} M{hx+5*ca:.1f},{hy+5*sa:.1f} L{hx+5*ca+3.4*px:.1f},{hy+5*sa+3.4*py:.1f} '
                  f'L{hx+15*ca+3.4*px:.1f},{hy+15*sa+3.4*py:.1f} L{hx+15*ca:.1f},{hy+15*sa:.1f}')
    o.append(f'<path d="{" ".join(sl)}" fill="none" stroke="{INK}" stroke-width="1.1" stroke-linejoin="round"/>')
    # la Miette et le Corps de garde (toit de pierre plat)
    o.append(f'<ellipse cx="955" cy="428" rx="25" ry="10.5" fill="#cda65c" fill-opacity=".6" stroke="{INK}" stroke-width="1.6"/>')
    o.append(f'<path d="M934,428 q2,-3 5,-2 M968,432 q3,-1 5,-3" fill="none" stroke="{INK}" stroke-width=".8"/>')
    gx, gy = G
    o.append(f'<rect x="{gx-5.5}" y="{gy-3.5}" width="11" height="8.5" fill="#eedfb6" stroke="{INK}" stroke-width="1.4"/>'
             f'<path d="M{gx-7.5},{gy-4} L{gx+7.5},{gy-4}" stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>'
             f'<rect x="{gx-1.3}" y="{gy+0.5}" width="2.6" height="4.5" fill="{INK}"/>')
    # le Sillon et la Chaussée : en pointillé (la mer les reprend)
    o.append(f'<path d="M869,428 Q900,433 929,429" fill="none" stroke="{INK}" stroke-width="3.2" stroke-linecap="round" stroke-dasharray="0.1 7"/>')
    o.append(f'<path d="M981,430 Q1034,462 {M[0]-5:.1f},{M[1]+10:.1f}" fill="none" stroke="{INK}" stroke-width="3.2" stroke-linecap="round" stroke-dasharray="0.1 7"/>')
    # les Chanteuses : un semis de petits ronds
    ch = []
    random.seed(5)
    pts = []
    tries = 0
    while len(pts) < 40 and tries < 5000:
        tries += 1
        x = random.uniform(866, 920); y = random.uniform(354, 384)
        if ((x - 893) / 29) ** 2 + ((y - 369) / 16) ** 2 > 1:
            continue
        if all(math.hypot(x - a, y - b) > 5.6 for a, b in pts):
            pts.append((x, y))
    for x, y in pts:
        ch.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.uniform(1.9,2.7):.1f}"/>')
    o.append(f'<g fill="#b9c2c4" fill-opacity=".8" stroke="{INK}" stroke-width="1">{"".join(ch)}</g>')
    random.seed(23)
    # les Sœurs de pierre + lune
    o.append(f'<g id="soeurs">{tower(SA)}{tower(SB)}</g>')
    o.append(f'<circle cx="1113" cy="372" r="12" fill="#f4ead0" stroke="{INK}" stroke-width="1.5"/>'
             f'<path d="M1107,366 q3,-2 5,1 M1116,376 q2,2 4,0 M1109,377 q1.5,1.5 3,0" fill="none" stroke="{INK}" stroke-width=".8" stroke-opacity=".7"/>'
             f'<path d="M1120.5,362.5 A12,12 0 0 1 1113,384 A15,15 0 0 0 1120.5,362.5 Z" fill="{INK}" fill-opacity=".28"/>')
    # vagues
    wv = []
    for (x, y, s) in ((120, 472, 1), (176, 522, 1), (96, 566, 1), (226, 562, .9), (86, 318, 1), (416, 248, 1),
                      (664, 258, 1), (760, 282, .9), (990, 250, 1), (1064, 268, .9), (900, 262, 1), (560, 612, 1),
                      (640, 590, .9), (700, 548, .9), (866, 540, 1), (946, 566, 1), (1044, 528, 1), (1086, 604, .9),
                      (890, 628, 1), (604, 690, 1), (520, 652, .9), (452, 640, 1), (392, 702, .9), (850, 704, 1),
                      (1000, 640, 1), (70, 628, .9), (132, 700, 1), (1080, 470, .8), (300, 246, .9), (538, 588, .8),
                      (800, 480, .8), (190, 610, .8)):
        wv.append(wave(x, y, s))
    o.append(f'<g fill="none" stroke="{INK}" stroke-width="1" stroke-opacity=".62" stroke-linecap="round">{"".join(wv)}</g>')
    # navire, rose, échelle, flèche de la Grande Terre
    o.append(ship(748, 644))
    o.append(rose())
    o.append(scale_bar(1030 - BAR / 2, 700))
    o.append(f'<path d="M640,735 L640,751 M634,744 L640,752.5 L646,744" fill="none" stroke="{INK}" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/>')
    o.append('</g>')  # fin plume

    # --- le Môle : seul trait à l'encre rouge, et plein
    sx, sy = lerp(C, mole[10], .5)
    o.append(f'<ellipse cx="{sx+1:.1f}" cy="{sy+2:.1f}" rx="12" ry="15" fill="{RED}" fill-opacity=".22" filter="url(#flou3)"/>')
    o.append(f'<path d="{path(mole)}" fill="none" stroke="{RED}" stroke-width="5.2" stroke-linecap="round" stroke-linejoin="round" filter="url(#plume2)"/>')
    o.append(f'<circle cx="{Pm[0]}" cy="{Pm[1]}" r="5.6" fill="{RED}"/>')

    # --- noms
    o.append(f'<g {FONT} font-style="italic" fill="{INK}">')
    o.append(label(88, 286, 'Lodenn', 'start', 36))
    o.append(f'<path d="M90,296 q28,7 58,1 q30,-6 58,2" fill="none" stroke="{INK}" stroke-width="1.2"/>')
    o.append(label(262, 351, 'la Chapelle', 'start'))
    o.append(label(288, 461, 'la Croix'))
    o.append(label(470, 446, 'le Bourg'))
    o.append(label(308, 546, 'la Cale'))
    o.append(label(548, 349, 'Pierre Longue', 'end'))
    o.append(label(656, 447, 'la Plage'))
    o.append(label(797, 386, 'le Moulin', 'end'))
    o.append(label(872, 482, 'le Sillon'))
    o.append(label(962, 465, 'la Miette'))
    o.append(label(926, 338, 'les Chanteuses'))
    o.append(label(1064, 496, 'la Chaussée'))
    o.append('<g id="soeurs-nom">' + label(1081, 304, 'les Sœurs') + label(1081, 327, 'de pierre') + '</g>')
    o.append(label(640, 727, 'vers la Grande Terre', size=20))
    o.append('</g>')
    o.append(top_text())
    o.append(CUT_TXT)

    # --- les deux traits de crayon, fins comme des cheveux, arrêtés net à la découpe
    e1 = lerp(K, Pm, h1[0] - 0.004)
    e2 = lerp(M, Pm, h2[0] - 0.004)
    o.append(f'<g fill="none" stroke="#4d4a48" stroke-opacity=".78" stroke-width="1.15" stroke-linecap="round">'
             f'<path id="trait-ouest" d="M{K[0]:.2f},{K[1]:.2f} L{e1[0]:.2f},{e1[1]:.2f}"/>'
             f'<path id="trait-est" d="M{M[0]:.2f},{M[1]:.2f} L{e2[0]:.2f},{e2[1]:.2f}"/></g>')

    # --- les quatre ancres
    o.append(anchor(981, 399, 'ancre-1'))    # Corps de garde (leçon 1, épisode 3)
    o.append(anchor(516, 308, 'ancre-2'))    # Pierre Longue (leçon 2, épisode 4)
    o.append(anchor(203, 389, 'ancre-3'))    # chapelle (leçon 3, épisode 5)
    o.append(anchor(937, 367, 'ancre-4'))    # Chanteuses (leçon 4, épisode 6)
    return '\n'.join(o)


# ------------------------------------------------------------------ assemblage
DEFS_COMMON = f'''<radialGradient id="papier" cx="50%" cy="48%" r="72%">
<stop offset="0" stop-color="#f1e0b3"/><stop offset=".55" stop-color="#e8d19c"/><stop offset=".85" stop-color="#d9b97c"/><stop offset="1" stop-color="#c29a5c"/>
</radialGradient>
<radialGradient id="table" cx="50%" cy="45%" r="75%"><stop offset="0" stop-color="#3a2618"/><stop offset="1" stop-color="#170e08"/></radialGradient>
<linearGradient id="mer" x1="0" y1="225" x2="0" y2="785" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="#6d94a0" stop-opacity="0"/><stop offset=".09" stop-color="#6d94a0" stop-opacity=".24"/><stop offset="1" stop-color="#5f8896" stop-opacity=".30"/>
</linearGradient>
<radialGradient id="terre" cx="480" cy="390" r="380" gradientUnits="userSpaceOnUse">
<stop offset="0" stop-color="#e3c98a" stop-opacity=".35"/><stop offset="1" stop-color="#a97b3a" stop-opacity=".22"/>
</radialGradient>
<filter id="plume" x="-2%" y="-2%" width="104%" height="104%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="4" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="2.2" xChannelSelector="R" yChannelSelector="G"/></filter>
<filter id="plume2" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.09" numOctaves="2" seed="9" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="1.8" xChannelSelector="R" yChannelSelector="G"/></filter>
<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="3"/><feColorMatrix type="matrix" values="0 0 0 0 0.36  0 0 0 0 0.23  0 0 0 0 0.09  0 0 0 -1.5 0.82"/><feComposite in2="SourceGraphic" operator="in"/></filter>
<filter id="marbre" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.011" numOctaves="3" seed="21"/><feColorMatrix type="matrix" values="0 0 0 0 0.45  0 0 0 0 0.29  0 0 0 0 0.11  0 0 0 -2.2 1.0"/><feComposite in2="SourceGraphic" operator="in"/></filter>
<filter id="flou3" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3"/></filter>
<filter id="flou8" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="9"/></filter>
<filter id="flou14" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="14"/></filter>
<filter id="ombre" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="7"/></filter>
<filter id="lueur" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="3.2"/></filter>
<clipPath id="feuille"><path d="{path(PAPER, True)}"/></clipPath>
<clipPath id="moitie-ouest"><path d="{path(WEST, True)}"/></clipPath>
<clipPath id="moitie-est"><path d="{path(EAST, True)}"/></clipPath>'''

STAINS = [(210, 150, 60, 36, .16), (980, 610, 90, 50, .15), (1050, 150, 55, 40, .17), (140, 640, 70, 44, .13),
          (640, 380, 120, 70, .06), (420, 700, 50, 26, .12), (860, 200, 40, 24, .12), (700, 120, 30, 16, .10)]


def paper_layer():
    o = [f'<rect x="20" y="10" width="1160" height="780" fill="url(#papier)"/>']
    o.append('<rect x="20" y="10" width="1160" height="780" fill="#000" filter="url(#marbre)" opacity=".55"/>')
    for cx, cy, rx, ry, op in STAINS:
        o.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#7a5222" fill-opacity="{op}" filter="url(#flou8)"/>')
    o.append('<circle cx="1010" cy="232" r="27" fill="none" stroke="#7a5222" stroke-opacity=".16" stroke-width="3.5" filter="url(#flou3)"/>')
    o.append('<circle cx="150" cy="180" r="2.2" fill="#6a4318" fill-opacity=".35"/><circle cx="162" cy="188" r="1.3" fill="#6a4318" fill-opacity=".3"/>'
             '<circle cx="905" cy="690" r="1.8" fill="#6a4318" fill-opacity=".3"/><circle cx="726" cy="214" r="1.5" fill="#6a4318" fill-opacity=".3"/>')
    # plis
    o.append('<path d="M332,30 L329,770 M872,30 L875,770 M50,402 L1150,399" fill="none" stroke="#6b4a22" stroke-opacity=".13" stroke-width="2.2"/>')
    o.append('<path d="M334.5,30 L331.5,770 M874.5,30 L877.5,770 M50,404.5 L1150,401.5" fill="none" stroke="#fff6da" stroke-opacity=".22" stroke-width="1.4"/>')
    # bords assombris
    o.append(f'<path d="{path(PAPER, True)}" fill="none" stroke="#5e3b17" stroke-opacity=".5" stroke-width="46" filter="url(#flou14)"/>')
    return '\n'.join(o)


def piece(side, dx, dy, edge_op, line_op):
    clip = 'moitie-ouest' if side == 'O' else 'moitie-est'
    zd = path(zig)
    tr = f' transform="translate({dx},{dy})"' if (dx or dy) else ''
    return f'''<g id="{clip}-piece"{tr}>
<g filter="url(#ombre)" opacity=".6" transform="translate(4,6)"><g clip-path="url(#feuille)"><rect x="0" y="0" width="1200" height="800" fill="#000" clip-path="url(#{clip})"/></g></g>
<g clip-path="url(#feuille)"><g clip-path="url(#{clip})">
<use href="#fond-papier"/>
<use href="#carte"/>
<rect x="20" y="10" width="1160" height="780" fill="#000" filter="url(#grain)" opacity=".5"/>
<path d="{zd}" fill="none" stroke="#5e3b17" stroke-opacity="{edge_op}" stroke-width="13" filter="url(#flou3)"/>
<path d="{zd}" fill="none" stroke="#3a2410" stroke-opacity="{line_op}" stroke-width="1.1" stroke-linejoin="round"/>
<path d="{path(PAPER, True)}" fill="none" stroke="#4a2e12" stroke-opacity=".55" stroke-width="1.6"/>
</g></g>
</g>'''


def build(state):
    titles = {1: 'La carte du capitaine Trémeur — les deux moitiés séparées',
              2: 'La carte du capitaine Trémeur — les deux moitiés réunies',
              3: 'La carte du capitaine Trémeur — la carte comprise'}
    descs = {
        1: "État 1 (épisodes 1 et 2) : la moitié de l'ouest (les Bottes) et la moitié de l'est (les Tongs), chacune avec son bord en dents de loup.",
        2: "État 2 (fin de l'épisode 2 à l'épisode 6) : les deux moitiés bord à bord. Ajouter la classe « allumee » à #ancre-1 … #ancre-4 pour allumer une ancre par leçon trouvée.",
        3: "État 3 (épisodes 7 et 8) : les deux traits de crayon prolongés en doré jusqu'au bout du Môle, l'étoile allumée, les Sœurs de pierre éteintes.",
    }
    style = '''<style>
.ancre .halo{opacity:0}
.ancre.allumee .halo{opacity:.85}
.ancre.allumee .trait{stroke:#7a4c00;stroke-width:2}
.eteint{opacity:.26}
</style>'''
    c = carte()
    if state == 3:
        c = c.replace('<g class="ancre"', '<g class="ancre allumee"')
        c = c.replace('<g id="soeurs">', '<g id="soeurs" class="eteint">').replace('<g id="soeurs-nom">', '<g id="soeurs-nom" class="eteint">')
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" width="1200" height="800" role="img" aria-labelledby="t d">',
         f'<title id="t">{titles[state]}</title>', f'<desc id="d">{descs[state]}</desc>', style,
         '<defs>', DEFS_COMMON, f'<g id="fond-papier">{paper_layer()}</g>', f'<g id="carte">{c}</g>', '</defs>',
         '<rect id="fond-table" width="1200" height="800" fill="url(#table)"/>']
    if state == 1:
        o.append(piece('O', -30, -18, .30, .75))
        o.append(piece('E', 30, 18, .30, .75))
    else:
        o.append(piece('O', 0, 0, .13, .42))
        o.append(piece('E', 0, 0, .13, .42))
    if state == 3:
        star = []
        for k in range(10):
            r = 17 if k % 2 == 0 else 7
            a = math.radians(-90 + k * 36)
            star.append((Pm[0] + r * math.cos(a), Pm[1] + r * math.sin(a)))
        o.append(f'''<g id="carte-comprise">
<g fill="none" stroke="#f3c53a" stroke-linecap="round" filter="url(#lueur)" opacity=".8" stroke-width="7">
<path d="M{K[0]:.2f},{K[1]:.2f} L{Pm[0]},{Pm[1]}"/><path d="M{M[0]:.2f},{M[1]:.2f} L{Pm[0]},{Pm[1]}"/></g>
<g fill="none" stroke="#d99a12" stroke-linecap="round" stroke-width="2.6">
<path id="visee-clocher-croix" d="M{K[0]:.2f},{K[1]:.2f} L{Pm[0]},{Pm[1]}"/><path id="visee-soeurs-miette" d="M{M[0]:.2f},{M[1]:.2f} L{Pm[0]},{Pm[1]}"/></g>
<circle cx="{Pm[0]}" cy="{Pm[1]}" r="24" fill="#f6cf45" filter="url(#flou3)" opacity=".8"/>
<path id="etoile" d="{path(star, True)}" fill="#f8d24c" stroke="#8a5a08" stroke-width="1.4" stroke-linejoin="round"/>
<circle cx="{Pm[0]}" cy="{Pm[1]}" r="3.2" fill="{RED}"/>
</g>''')
    o.append('</svg>')
    return '\n'.join(o) + '\n'


for st in (1, 2, 3):
    fn = os.path.join(OUT, f'carte_{st}.svg')
    with open(fn, 'w', encoding='utf-8') as f:
        f.write(build(st))
    print(fn, os.path.getsize(fn))
