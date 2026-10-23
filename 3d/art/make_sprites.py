"""Cut character / vehicle / item sheets (3d/art/_originals/*.jfif) into transparent WebP sprites (3d/art/sprites/).

Run from anywhere:  python 3d/art/make_sprites.py
Re-run whenever a new sheet is added to SHEETS below (e.g. when Christopher / Juan Carlos / Eduardo arrive).
Needs: pillow, numpy, scipy.
"""
import json
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, '_originals')
OUT = os.path.join(HERE, 'sprites')
os.makedirs(OUT, exist_ok=True)

VIEWS3 = ['front', 'side', 'back']
# name: (source file, expected figures, names for the figures we keep {index: name}, front-view height in px)
SHEETS = {
    'player': ('the player.jfif', 3, {0: 'front', 1: 'side', 2: 'back'}, 480),
    'pancho': ('pancho.jfif', 3, {0: 'front', 1: 'side', 2: 'back'}, 480),
    'father': ('Pancho’s father.jfif', 3, {0: 'front', 1: 'side', 2: 'back'}, 480),
    'luz': ('Luz.jfif', 3, {0: 'front', 1: 'side', 2: 'back'}, 480),
    'thug': ('The thugs.jfif', 3, {0: 'front', 1: 'side', 2: 'back'}, 480),
    'kid': ('the kid.jfif', 3, {0: 'front', 1: 'side', 2: 'back'}, 480),
    'suit': ('the suits.jfif', 6, {0: 'front', 2: 'side', 4: 'back'}, 480),
    'van': ('black van.jfif', 3, {0: 'front', 1: 'side', 2: 'back'}, 380),
    'truck': ('bread truck.jfif', 3, {0: 'front', 1: 'side', 2: 'back'}, 380),
}
ITEMS = ('The collectibles set.jfif', ['card', 'scratcher', 'wire', 'vinyl', 'tape', 'basket'], 256)
WORK_W = 1376  # process at half size, it is plenty for 480px sprites


def load(path):
    im = Image.open(path).convert('RGB')
    h = round(im.height * WORK_W / im.width)
    return im.resize((WORK_W, h), Image.LANCZOS)


def cutout(im):
    """Returns an RGBA image with the plain studio background removed and clean edges."""
    a = np.asarray(im).astype(np.float32)
    border = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    bg = np.median(border, axis=0)
    dist = np.sqrt(((a - bg) ** 2).sum(axis=2))
    bg_like = dist < 30
    lab, n = ndi.label(bg_like)
    edge_labels = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg_mask = np.isin(lab, list(edge_labels))
    # enclosed bits that are clearly just background (e.g. between an arm and the body)
    for i in range(1, n + 1):
        if i in edge_labels:
            continue
        m = lab == i
        if m.sum() > 150 and dist[m].mean() < 14:
            bg_mask |= m
    fg = ~bg_mask
    fg = ndi.binary_opening(fg, iterations=1)
    lab2, n2 = ndi.label(fg)
    if n2:
        sizes = ndi.sum(fg, lab2, range(1, n2 + 1))
        keep = [i + 1 for i, s in enumerate(sizes) if s > 250]
        fg = np.isin(lab2, keep)
    fg = ndi.binary_fill_holes(fg)
    core = ndi.binary_erosion(fg, iterations=2)
    # take colour from the nearest solid interior pixel so the grey backdrop never bleeds into the edge
    _, idx = ndi.distance_transform_edt(~core, return_indices=True)
    rgb = a[idx[0], idx[1]]
    alpha = ndi.gaussian_filter(ndi.binary_erosion(fg, iterations=1).astype(np.float32), 0.9)
    alpha = np.clip((alpha - 0.2) / 0.6, 0, 1)
    out = np.dstack([rgb, alpha * 255]).astype(np.uint8)
    return Image.fromarray(out, 'RGBA'), fg


def split_views(fg, expected):
    cols = fg.any(axis=0)
    for gap in (60, 40, 28, 20, 14, 10, 7, 5, 3):
        runs, start, empty = [], None, 0
        for x, on in enumerate(cols):
            if on:
                if start is None:
                    start = x
                empty = 0
                end = x
            elif start is not None:
                empty += 1
                if empty >= gap:
                    runs.append((start, end))
                    start = None
        if start is not None:
            runs.append((start, end))
        runs = [r for r in runs if r[1] - r[0] > 30]
        if len(runs) == expected:
            return runs
    raise SystemExit('could not split into %d views (best found %d)' % (expected, len(runs)))


def trim(rgba, x0, x1):
    box = rgba.crop((x0, 0, x1 + 1, rgba.height))
    bbox = box.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
    pad = 3
    l, t, r, b = bbox
    return box.crop((max(0, l - pad), max(0, t - pad), min(box.width, r + pad), min(box.height, b + pad)))


def save(img, name, manifest):
    path = os.path.join(OUT, name + '.webp')
    img.save(path, 'WEBP', quality=82, method=6)
    manifest[name] = {'w': img.width, 'h': img.height, 'kb': round(os.path.getsize(path) / 1024, 1)}


def main():
    manifest = {}
    for key, (fname, expected, keep, target_h) in SHEETS.items():
        path = os.path.join(SRC, fname)
        if not os.path.exists(path):
            print('skip (no file yet):', key)
            continue
        rgba, fg = cutout(load(path))
        runs = split_views(fg, expected)
        pieces = {keep[i]: trim(rgba, *runs[i]) for i in keep}
        scale = target_h / pieces['front'].height
        for view, img in pieces.items():
            size = (max(1, round(img.width * scale)), max(1, round(img.height * scale)))
            save(img.resize(size, Image.LANCZOS), '%s_%s' % (key, view), manifest)
        print('ok', key, [(v, manifest['%s_%s' % (key, v)]['w'], manifest['%s_%s' % (key, v)]['h']) for v in pieces])
    fname, names, target_h = ITEMS
    path = os.path.join(SRC, fname)
    if os.path.exists(path):
        rgba, fg = cutout(load(path))
        runs = split_views(fg, len(names))
        for name, run in zip(names, runs):
            img = trim(rgba, *run)
            s = target_h / max(img.width, img.height)
            save(img.resize((max(1, round(img.width * s)), max(1, round(img.height * s))), Image.LANCZOS), 'item_' + name, manifest)
        print('ok items', names)
    with open(os.path.join(OUT, 'manifest.json'), 'w') as f:
        json.dump(manifest, f, indent=1)
    print('total KB', round(sum(m['kb'] for m in manifest.values())))


if __name__ == '__main__':
    sys.exit(main())
