#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-only
"""AISLING FX-1's card: AISLING's gold 8-bit harp (tools/make_card.py's shapes, cell for cell), moved up and left, with
FX in the same gold below its soundbox. 30 cells x8 = 240 x 240 PNG, The Firmware Hub's best size.

  tools/make_card_fx.py docs/card-fx1.png [--ground green|night]      (needs Pillow: the .venv)

green is AISLING's own ground; night (indigo) sets FX-1 apart from it on a page of cards."""
import argparse, math
from PIL import Image

# make_card.py's palette and shapes, as they are there (it draws as it loads, so they are copied, not imported)
N, Z = 24, 8
OUTL, GOLD, DARK, LIGHT, STR = (64, 38, 6), (232, 176, 52), (176, 118, 26), (255, 226, 120), (250, 214, 130)
BOX = [(5.6, 19.6), (8.6, 21.4), (20.6, 5.4), (18.0, 3.4)]
PILLAR = [(6.5, 20.0), (1.4, 12.0), (4.6, 3.2)]
NECK = [(4.6, 3.0), (9.0, 0.6), (12.0, 8.4), (18.6, 4.2)]


def bez(p, t):
    if len(p) == 3:
        a, b, c = p
        return tuple((1 - t) ** 2 * a[i] + 2 * (1 - t) * t * b[i] + t * t * c[i] for i in (0, 1))
    a, b, c, d = p
    return tuple((1 - t) ** 3 * a[i] + 3 * (1 - t) ** 2 * t * b[i] + 3 * (1 - t) * t * t * c[i] + t ** 3 * d[i]
                 for i in (0, 1))


def near_curve(p, x, y, w):
    return min(math.hypot(x - q[0], y - q[1]) for q in (bez(p, i / 200) for i in range(201))) <= w


def in_poly(poly, x, y):
    inside = False
    for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]):
        if (y0 > y) != (y1 > y) and x < x0 + (y - y0) * (x1 - x0) / (y1 - y0):
            inside = not inside
    return inside


def grid():
    """The harp on make_card.py's 24 cells: box, frame, string or None in each."""
    g = [[None] * N for _ in range(N)]
    for gy in range(N):
        for gx in range(N):
            x, y = gx + 0.5, gy + 0.5
            if in_poly(BOX, x, y):
                g[gy][gx] = "box"
            elif near_curve(PILLAR, x, y, 1.05) or near_curve(NECK, x, y, 1.0):
                g[gy][gx] = "frame"
            elif 3.2 <= x <= 5.8 and 1.0 <= y <= 3.0:
                g[gy][gx] = "frame"
            elif 4.0 <= x <= 9.8 and 20.4 <= y <= 22.4:
                g[gy][gx] = "frame"
    for gx in range(7, 18, 2):
        col = [g[gy][gx] for gy in range(N)]
        top = next((gy for gy in range(N) if col[gy] == "frame"), None)
        bot = next((gy for gy in range(N) if col[gy] == "box"), None)
        if top is None or bot is None:
            continue
        while top + 1 < N and g[top + 1][gx] == "frame":
            top += 1
        for gy in range(top + 1, bot):
            if g[gy][gx] is None:
                g[gy][gx] = "string"
    return g


C = 30                                           # the canvas, in cells (make_card's harp is N = 24 of them)
GROUNDS = {"green": ((22, 120, 72), (14, 84, 50)), "night": ((40, 34, 92), (24, 20, 60))}
HARP_AT = (2, 1)                                 # the harp's top-left cell on the canvas
FX_AT = (15, 21)                                 # the letters' top-left cell
F = ["#####", "##...", "####.", "##...", "##...", "##..."]          # F in a two-cell stroke, six high,
X = ["##...##", ".##.##.", "..###..", "..###..", ".##.##.", "##...##"]   # X on two-cell diagonals


def main():
    a = argparse.ArgumentParser()
    a.add_argument("out")
    a.add_argument("--ground", default="green", choices=list(GROUNDS))
    o = a.parse_args()
    bg, shadow = GROUNDS[o.ground]
    cell = [[None] * C for _ in range(C)]
    h = grid()
    for gy in range(N):
        for gx in range(N):
            if h[gy][gx]:
                cell[gy + HARP_AT[1]][gx + HARP_AT[0]] = h[gy][gx]
    for rows, x0 in ((F, FX_AT[0]), (X, FX_AT[0] + 6)):
        for r, row in enumerate(rows):
            for c, ch in enumerate(row):
                if ch == "#":
                    cell[FX_AT[1] + r][x0 + c] = "frame"
    solid = lambda x, y: 0 <= x < C and 0 <= y < C and cell[y][x] in ("box", "frame")
    lit = lambda x, y: 0 <= x < C and 0 <= y < C and cell[y][x] is not None
    img = Image.new("RGB", (C, C), bg)
    px = img.load()
    for y in range(C):                           # the drop shadow, down and right, as the card's
        for x in range(C):
            if cell[y][x] is None and lit(x - 1, y - 1):
                px[x, y] = shadow
    for y in range(C):
        for x in range(C):
            k = cell[y][x]
            if k == "string":
                px[x, y] = STR
            elif k in ("box", "frame"):
                edge = not all(solid(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                if edge and (not solid(x - 1, y) or not solid(x, y - 1)):
                    px[x, y] = LIGHT             # lit from the top left
                elif edge:
                    px[x, y] = DARK
                else:
                    px[x, y] = GOLD if k == "frame" else DARK if (x + y) % 2 else GOLD
            elif px[x, y] == bg and any(solid(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                px[x, y] = OUTL
    img.resize((C * Z, C * Z), Image.NEAREST).save(o.out, optimize=True)
    print(o.out, f"{C * Z} x {C * Z}")


if __name__ == "__main__":
    main()
