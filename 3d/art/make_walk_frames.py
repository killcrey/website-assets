"""Cut a 4-figure walk-cycle sheet into 4 equal-canvas transparent frames: <key>_<view>_w0 .. _w3 in 3d/art/sprites/.

Run:  python 3d/art/make_walk_frames.py            (all sheets below)
Phases left to right: contact (left foot), passing, contact (right foot), passing.
All 4 frames of a view share one canvas and one scale, and the body (not the feet) is centred in it,
so the sprite never slides sideways while the legs swing. The tallest figure is scaled to HEIGHT px,
the same size as the standing sprites. Reuses the cut-out code from make_sprites.py.
"""
import json
import os
import sys

import numpy as np
from PIL import Image

import make_sprites as ms

HEIGHT = 480
WALKS = {
    'player': {'back': 'PLAYER_WALK__BACK.jfif', 'side': 'PLAYER_WALK__SIDE.jfif', 'front': 'PLAYER_WALK__FRONT.jfif'},
}


def body_centre(img):
    """x of the body's weight centre: the upper 60% of the figure (head, torso, pack), ignoring swinging legs."""
    a = np.asarray(img.getchannel('A')).astype(np.float32)
    top = a[: int(a.shape[0] * 0.6)]
    xs = np.arange(a.shape[1])
    return float((top.sum(axis=0) * xs).sum() / max(1.0, top.sum()))


def cut(path):
    rgba, fg = ms.cutout(ms.load(path))
    runs = ms.split_views(fg, 4)
    figs = [ms.trim(rgba, *r) for r in runs]
    scale = HEIGHT / max(f.height for f in figs)
    figs = [f.resize((max(1, round(f.width * scale)), max(1, round(f.height * scale))), Image.LANCZOS) for f in figs]
    cx = [body_centre(f) for f in figs]
    left = max(c for c in cx)
    right = max(f.width - c for f, c in zip(figs, cx))
    W, H = int(round(left + right)) + 2, max(f.height for f in figs)
    frames = []
    for f, c in zip(figs, cx):
        canvas = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        canvas.paste(f, (int(round(left - c)) + 1, H - f.height), f)  # feet on the bottom edge
        frames.append(canvas)
    return frames


def main():
    mpath = os.path.join(ms.OUT, 'manifest.json')
    manifest = json.load(open(mpath))
    for key, views in WALKS.items():
        for view, fname in views.items():
            path = os.path.join(ms.SRC, fname)
            if not os.path.exists(path):
                print('skip (no file):', fname)
                continue
            frames = cut(path)
            for i, img in enumerate(frames):
                ms.save(img, '%s_%s_w%d' % (key, view, i), manifest)
            print('ok', key, view, [(f.width, f.height) for f in frames][:1], 'x4')
    json.dump(manifest, open(mpath, 'w'), indent=1)


if __name__ == '__main__':
    sys.exit(main())
