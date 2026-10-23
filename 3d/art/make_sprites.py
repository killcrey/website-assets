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
    'christopher': ('christopher.jfif', 3, {0: 'front', 1: 'side', 2: 'back'}, 480),
    'juancarlos': ('Juan Carlos.jfif', 3, {0: 'front', 1: 'side', 2: 'back'}, 480),
    'eduardo': ('eduardo.jfif', 3, {0: 'front', 1: 'side', 2: 'back'}, 480),
    'car_a': ('Parked car A.jfif', 3, {0: 'front', 1: 'side', 2: 'back'}, 380, 0.33),
    'car_b': ('Parked car B.jfif', 3, {0: 'front', 1: 'side', 2: 'back'}, 380),
    'car_c': ('Parked car C.jfif', 3, {0: 'front', 1: 'side', 2: 'back'}, 380),
    'dumpster': ('Dumpster.jfif', 3, {0: 'front', 1: 'side', 2: 'back'}, 340, 0.25),
    'cart': ('Street taco vendor cart.jfif', 3, {0: 'front', 1: 'side', 2: 'back'}, 420),
    'bus': ('Bus shelter.jfif', 3, {0: 'front', 1: 'side', 2: 'back'}, 300, 0.54),
    'suit': ('the suits.jfif', 6, {0: 'front', 2: 'side', 4: 'back'}, 480),
    'van': ('black van.jfif', 3, {0: 'front', 1: 'side', 2: 'back'}, 380),
    'truck': ('bread truck.jfif', 3, {0: 'front', 1: 'side', 2: 'back'}, 380),
}
ITEMS = ('The collectibles set.jfif', ['card', 'scratcher', 'wire', 'vinyl', 'tape', 'basket'], 256)
# single flat pieces: name: (source file, output width px)
FLATS = {'bodega': ('bodega.jfif', 1024), 'recordstore': ('record store.jfif', 1024), 'taqueria': ('tacoshop.jfif', 1200)}
# several different items on one sheet, each saved on its own: (file, names left to right, 'h' or 'w', size px, name prefix, name suffix)
SETS = [
    ('Small street props set.jfif', ['cans', 'mailbox', 'hydrant', 'bench', 'newsbox', 'cones'], 'h', 300, 'prop_', '_front'),
    ('Cover pieces set.jfif', ['hedge', 'crates', 'barrier', 'fence', 'tires'], 'h', 300, 'cov_', '_front'),
    ('Alley and wall.jfif', ['wall', 'gate', 'fence', 'ladder', 'appliances'], 'h', 340, 'alley_', '_front'),
    ('Street signs set.jfif', ['stop', 'oneway', 'noparking', 'fifth', 'ped'], 'h', 340, 'sign_', '_front'),
    ('Two more storefronts.jfif', ['coffee', 'panaderia'], 'w', 900, 'facade_', ''),
]
WORK_W = 1376  # process at half size, it is plenty for 480px sprites


def load(path, crop_top=0.0):
    im = Image.open(path).convert('RGB')
    h = round(im.height * WORK_W / im.width)
    im = im.resize((WORK_W, h), Image.LANCZOS)
    if crop_top:
        im = im.crop((0, int(h * crop_top), WORK_W, h))
    return im


def cutout(im, strip_lines=True):
    """Returns an RGBA image with the plain studio background removed and clean edges."""
    a = np.asarray(im).astype(np.float32)
    border = np.concatenate([a[0], a[-1], a[:, 0], a[:, -1]])
    bg = np.median(border, axis=0)
    dist = np.sqrt(((a - bg) ** 2).sum(axis=2))
    bg_like = dist < 30
    lab, n = ndi.label(bg_like)
    edge_labels = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg_mask = np.isin(lab, list(edge_labels))
    # enclosed bits that are clearly just background (e.g. between an arm and the body); only look at the big ones
    sizes = np.bincount(lab.ravel(), minlength=n + 1)
    cand = [i for i in range(1, n + 1) if i not in edge_labels and sizes[i] > 150]
    if cand:
        means = np.atleast_1d(ndi.mean(dist, lab, cand))
        for i, mval in zip(cand, means):
            if mval < 14:
                bg_mask |= lab == i
    fg = ~bg_mask
    if strip_lines:  # a long unbroken horizontal run is a ground line, not part of a vehicle or character
        W = fg.shape[1]
        for y in range(fg.shape[0]):
            row = fg[y]
            if row.sum() < 0.5 * W:
                continue
            d = np.diff(np.concatenate([[0], row.astype(np.int8), [0]]))
            if (np.where(d == -1)[0] - np.where(d == 1)[0]).max() > 0.5 * W:
                fg[y] = False
    fg = ndi.binary_opening(fg, iterations=1)
    fg = ndi.binary_opening(fg, structure=np.ones((6, 1), bool))  # drops thin horizontal ground lines that join separate views
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
    for gap in (60, 40, 28, 20, 14, 10, 7, 5, 3, 2, 1):
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


ONLY = set(sys.argv[1:])  # optional: only re-cut these keys, e.g.  python make_sprites.py alley sign bodega


def want(*names):
    return not ONLY or any(n in ONLY for n in names)


def main():
    mpath = os.path.join(OUT, 'manifest.json')
    manifest = json.load(open(mpath)) if os.path.exists(mpath) else {}
    for key, spec in SHEETS.items():
        if not want(key):
            continue
        fname, expected, keep, target_h = spec[:4]
        crop_top = spec[4] if len(spec) > 4 else 0.0
        path = os.path.join(SRC, fname)
        if not os.path.exists(path):
            print('skip (no file yet):', key)
            continue
        rgba, fg = cutout(load(path, crop_top))
        runs = split_views(fg, expected)
        pieces = {keep[i]: trim(rgba, *runs[i]) for i in keep}
        scale = target_h / pieces['front'].height
        for view, img in pieces.items():
            size = (max(1, round(img.width * scale)), max(1, round(img.height * scale)))
            save(img.resize(size, Image.LANCZOS), '%s_%s' % (key, view), manifest)
        print('ok', key, [(v, manifest['%s_%s' % (key, v)]['w'], manifest['%s_%s' % (key, v)]['h']) for v in pieces])
    fname, names, target_h = ITEMS
    path = os.path.join(SRC, fname)
    if os.path.exists(path) and want('items'):
        rgba, fg = cutout(load(path))
        runs = split_views(fg, len(names))
        for name, run in zip(names, runs):
            img = trim(rgba, *run)
            s = target_h / max(img.width, img.height)
            save(img.resize((max(1, round(img.width * s)), max(1, round(img.height * s))), Image.LANCZOS), 'item_' + name, manifest)
        print('ok items', names)
    for fname, names, mode, size, prefix, suffix in SETS:
        if not want(prefix.strip('_'), fname):
            continue
        path = os.path.join(SRC, fname)
        if not os.path.exists(path):
            print('skip (no file yet):', fname)
            continue
        rgba, fg = cutout(load(path))
        runs = split_views(fg, len(names))
        for name, run in zip(names, runs):
            img = trim(rgba, *run)
            sc = size / (img.height if mode == 'h' else img.width)
            save(img.resize((max(1, round(img.width * sc)), max(1, round(img.height * sc))), Image.LANCZOS), prefix + name + suffix, manifest)
        print('ok set', fname, names)
    for name, (fname, out_w) in FLATS.items():
        if not want(name):
            continue
        path = os.path.join(SRC, fname)
        if not os.path.exists(path):
            continue
        rgba, fg = cutout(load(path), strip_lines=False)
        bbox = rgba.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
        img = rgba.crop(bbox)
        save(img.resize((out_w, max(1, round(img.height * out_w / img.width))), Image.LANCZOS), name, manifest)
        print('ok', name, manifest[name])
    with open(os.path.join(OUT, 'manifest.json'), 'w') as f:
        json.dump(manifest, f, indent=1)
    print('total KB', round(sum(m['kb'] for m in manifest.values())))


if __name__ == '__main__':
    sys.exit(main())
