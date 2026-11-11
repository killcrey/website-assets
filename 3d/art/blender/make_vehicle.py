# make_vehicle.py <key> <heightM> : sprite views (front/side/back) -> measured Blender model -> GLB + gate numbers.
#   python make_vehicle.py car_d 1.4
import sys, os, json, subprocess, statistics
from PIL import Image
import numpy as np
from scipy import ndimage
key, HM = sys.argv[1], float(sys.argv[2])
ROOT = 'C:/Users/16193/game-research/van-3d'; SRC = 'C:/Users/16193/Desktop/website-assets/3d/art/sprites/'
BL = [os.path.join('C:/Users/16193/game-research/blender/app', d, 'blender.exe') for d in os.listdir('C:/Users/16193/game-research/blender/app') if d.startswith('blender-')][0]
A = f'{ROOT}/{key}'; os.makedirs(f'{A}/ref', exist_ok=True); os.makedirs(f'{A}/review', exist_ok=True)
ims = {n: Image.open(f'{SRC}{key}_{n}.webp').convert('RGBA') for n in ('front', 'side', 'back')}
H = ims['front'].height; k = HM / H
info = {'k': k, 'H_px': H, 'HM': HM, 'key': key}
for n, im in ims.items():
    pad = Image.new('RGBA', (im.width, H), (0, 0, 0, 0)); pad.paste(im, (0, H - im.height)); pad.save(f'{A}/ref/{n}.png')
    a = np.array(pad); m = a[:, :, 3] > 128
    idx = ndimage.distance_transform_edt(~m, return_distances=False, return_indices=True)
    Image.fromarray(a[:, :, :3][idx[0], idx[1]]).save(f'{A}/ref/{n}_fill.png')
    info[n] = {'w': im.width, 'h': im.height, 'w_m': im.width * k}
a = np.array(Image.open(f'{A}/ref/side.png'))[:, :, 3] > 128
cols = []
for x in range(a.shape[1]):
    ys = np.where(a[:, x])[0]; cols.append(None if len(ys) == 0 else (float((H - 1 - ys.min()) * k), float((H - 1 - ys.max()) * k)))
info['side_env'] = cols
f = np.array(Image.open(f'{A}/ref/front.png'))[:, :, 3] > 128; rows = []
for y in range(f.shape[0]):
    xs = np.where(f[y, :])[0]; rows.append(None if len(xs) == 0 else (float(xs.min() * k), float((xs.max() + 1) * k)))
info['front_env'] = rows
# ground-contact runs -> wheel centres; wheel radius from the chord of the underside at several heights above the ground
bot = [c[1] if c else None for c in cols]
def runs_below(c):
    out = []; st = None
    for x, b in enumerate(bot):
        g = b is not None and b < c
        if g and st is None: st = x
        if not g and st is not None: out.append((st, x)); st = None
    if st is not None: out.append((st, len(bot)))
    return out
r0 = [r for r in runs_below(0.07) if r[1] - r[0] >= 4]
centres = [((a_ + b_) / 2) * k for a_, b_ in r0]
Rs = []
for c in (0.1, 0.15, 0.2):
    for a_, b_ in runs_below(c):
        w = (b_ - a_) * k
        if any(a_ <= (ra + rb) / 2 <= b_ for ra, rb in r0): Rs.append((w * w / 4 + c * c) / (2 * c))
tops = [c[0] for c in cols if c]; R = max(0.2, min(0.42, 0.185 * float(np.percentile(tops, 90))))   # wheel radius ~ 0.185 x body height (the van's measured 0.36 / 1.95)
info['wheel_centres_m'] = centres; info['wheel_R'] = R
json.dump(info, open(f'{A}/ref.json', 'w'))
print(f'[{key}] k={k:.5f} L={info["side"]["w_m"]:.2f} W={info["front"]["w_m"]:.2f} H={HM} wheels at {[round(c, 2) for c in centres]} R={R:.2f}')
r = subprocess.run([BL, '--background', '--python', f'{ROOT}/build_vehicle.py', '--', A], capture_output=True, text=True)
for ln in r.stdout.splitlines():
    if ln.startswith(('TRIS', 'GLB')) or 'Error' in ln or 'Traceback' in ln: print(ln)
if r.returncode: print(r.stderr[-800:])
def m(p): return np.array(Image.open(p).convert('RGBA'))[:, :, 3] > 128
for v in ('side', 'front', 'back'):
    ref, s = m(f'{A}/ref/{v}.png'), m(f'{A}/review/sil_{v}.png')
    print(f'  {v}: IoU {(ref & s).sum() / (ref | s).sum():.3f}')
# contact sheet
def bg(p): im = Image.open(p).convert('RGBA'); s = Image.new('RGBA', im.size, (200, 215, 225, 255)); s.alpha_composite(im); return s.convert('RGB')
r1 = [bg(f'{A}/ref/{n}.png') for n in ('side', 'front', 'back')]; r2 = [bg(f'{A}/review/tex_{n}.png') for n in ('side', 'front', 'back')]
r3 = [bg(f'{A}/review/{n}.png').resize((420, 315)) for n in ('tex_34f', 'tex_34b')]
W_ = sum(i.width for i in r1); Hh = r1[0].height
sh = Image.new('RGB', (max(W_, 840), Hh * 2 + 8 + 315 + 8), (255, 255, 255)); x = 0
for a_, b_ in zip(r1, r2): sh.paste(a_, (x, 0)); sh.paste(b_, (x, Hh + 8)); x += a_.width
sh.paste(r3[0], (0, Hh * 2 + 16)); sh.paste(r3[1], (420, Hh * 2 + 16)); sh.save(f'{A}/sheet.jpg', quality=85)
