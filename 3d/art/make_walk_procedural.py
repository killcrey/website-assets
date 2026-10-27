"""Build the player's 4-frame walk cycle straight from the standing sprites (no Gemini): the body stays exactly as drawn
and only the legs are re-posed, so the character can never change.

Run:  python 3d/art/make_walk_procedural.py          (writes sprites/player_<view>_w0..w3.webp and updates manifest.json)
      python 3d/art/make_walk_procedural.py --preview  (also writes a contact sheet to the temp folder)

Phases (same order the game plays them): 0 contact, 1 passing, 2 contact (other foot), 3 passing.
- back / front views: the camera sits a little above the character, so a leg that steps away from the camera looks
  shorter and sits higher, a trailing leg looks longer and sits lower. Each leg is cut into thigh, shin and boot and
  stretched in height by exactly that amount (plus a small heel lift), the arms swing by stretching the forearm.
- side view: each leg is cut into thigh, shin and boot and rotated at the hip, knee and ankle; a darker copy of the
  leg is the far leg. Everything is aligned so the lowest foot sits on the ground line.
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image, ImageEnhance

HERE = os.path.dirname(os.path.abspath(__file__))
SPR = os.path.join(HERE, 'sprites')
sys.path.insert(0, HERE)
import make_sprites as ms  # noqa: E402  (for save() and the manifest)

PHI = math.radians(25)  # how far above the character the camera looks, exaggerated a little so the stride reads on a phone
TOP = 40                # blank rows added above the standing figure (the body dips a little during a step)

# (hip angle forward in degrees, knee bend, foot pitch: + toes up / - toes down, extra heel lift in px for the back/front views)
CONTACT_FRONT = (26, 4, 10, 0)
CONTACT_BACK = (-20, 14, -45, 9)
PASS_PLANTED = (0, 0, 0, 0)
PASS_SWING = (12, 65, -25, 16)
PHASES = [  # (RIGHT leg, LEFT leg)
    (CONTACT_FRONT, CONTACT_BACK),
    (PASS_PLANTED, PASS_SWING),
    (CONTACT_BACK, CONTACT_FRONT),
    (PASS_SWING, PASS_PLANTED),
]


def load(name):
    return Image.open(os.path.join(SPR, name + '.webp')).convert('RGBA')


def alpha_rows(im, y0, y1):
    return np.asarray(im.getchannel('A'))[y0:y1]


# ---------------------------------------------------------------- back and front
def build_bf(view):
    im = load('player_' + view)
    W, H = im.size
    a = np.asarray(im.getchannel('A'))
    # where the legs split: the transparent column between them, found low on the legs
    row = a[int(H * 0.80)]
    on = np.where(row > 40)[0]
    gaps = np.where(np.diff(on) > 4)[0]
    cut = int((on[gaps[0]] + on[gaps[0] + 1]) / 2) if len(gaps) else W // 2
    crotch = next(y for y in range(int(H * 0.5), H) if a[y, cut] < 40)  # first row where the gap between the legs opens
    K, A = int(H * 0.775), int(H * 0.855)  # the knee cut sits just under the knee pads so they are never sliced
    left_img = im.crop((0, 0, cut, H))      # image-left half
    right_img = im.crop((cut, 0, W, H))     # image-right half
    side_of = {'back': {'R': 'right', 'L': 'left'}, 'front': {'R': 'left', 'L': 'right'}}[view]
    sgn = 1 if view == 'back' else -1       # back view: forward = away from the camera = higher on screen

    def fac(angle_deg):  # how tall a segment looks, compared with standing
        return max(0.35, math.cos(math.radians(angle_deg) + sgn * PHI) / math.cos(PHI))

    def leg_pieces(half, th, kb, pitch, lift):
        """thigh, shin and boot cut from one leg, each with the height it should have in this pose (the heel lift shortens the shin so the boot rises)"""
        pcs = [half.crop((0, crotch, half.width, K)), half.crop((0, K, half.width, A)), half.crop((0, A, half.width, H))]
        hs = [round(pcs[0].height * fac(th)), max(8, round(pcs[1].height * fac(th - kb)) - lift), round(pcs[2].height * (0.82 if lift else 1.0))]
        return pcs, hs

    frames = []
    for ph in PHASES:
        legs = {}
        for key, (th, kb, pitch, lift) in zip(('R', 'L'), ph):
            half = right_img if side_of[key] == 'right' else left_img
            pcs, hs = leg_pieces(half, th, kb, pitch, lift)
            legs[key] = (pcs, hs, sum(hs))
        ground = max(legs['R'][2], legs['L'][2])
        body_dy = (H - ground) - crotch  # the body drops as the legs shorten
        # arms: the forearm on the side of the forward foot swings back, the other forward
        fwd_leg = 'R' if ph[0][0] > ph[1][0] else 'L'
        canvas = Image.new('RGBA', (W, H + TOP), (0, 0, 0, 0))
        body = im.crop((0, 0, W, crotch))
        # arms swing by stretching the part of each sleeve below the elbow
        elbow = int(H * 0.45)
        arm_cols = {'left': (0, int(cut - W * 0.20)), 'right': (int(cut + W * 0.20), W)}
        body_img = Image.new('RGBA', body.size, (0, 0, 0, 0))
        body_img.paste(body, (0, 0))
        for sd, (c0, c1) in arm_cols.items():
            leg_of_side = 'R' if side_of['R'] == sd else 'L'
            # the arm opposite to the forward leg swings forward: forward = shorter and higher from behind, longer and lower from the front
            fwd = (leg_of_side != fwd_leg)
            if ph[0][0] == 0 or ph[1][0] == 0 and ph[0][0] == ph[1][0]:
                f = 1.0
            elif ph[0][0] == 0 or ph[1][0] == 0:
                f = 1.0
            else:
                f = (0.93 if fwd else 1.06) if view == 'back' else (1.06 if fwd else 0.93)
            seg = body.crop((c0, elbow, c1, crotch))
            if f != 1.0:
                seg2 = seg.resize((seg.width, max(1, round(seg.height * f))), Image.LANCZOS)
                body_img.paste((0, 0, 0, 0), (c0, elbow, c1, crotch))
                body_img.paste(seg2, (c0, elbow), seg2)
        canvas.alpha_composite(body_img, (0, TOP + body_dy))
        for key in ('R', 'L'):
            pcs, hs, _ = legs[key]
            x0 = cut if side_of[key] == 'right' else 0
            y = TOP + crotch + body_dy
            for img, h2 in zip(pcs, hs):
                canvas.alpha_composite(img.resize((img.width, h2), Image.LANCZOS), (x0, y))
                y += h2
        frames.append(canvas)
    return frames


# ---------------------------------------------------------------- side view
def rot_xy(vx, vy, deg):
    """rotate an image-space vector counter-clockwise on screen by deg"""
    r = math.radians(deg)
    return vx * math.cos(r) + vy * math.sin(r), -vx * math.sin(r) + vy * math.cos(r)


def build_side():
    im = load('player_side')
    W, H = im.size
    PAD = 120
    a = np.asarray(im.getchannel('A'))
    HIP, KNEE, ANK = int(H * 0.607), int(H * 0.733), int(H * 0.858)
    def cx(y):
        xs = np.where(a[y] > 60)[0]
        return float(xs.mean()) if len(xs) else W / 2
    hip = (cx(HIP + 6), float(HIP)); knee = (cx(KNEE), float(KNEE)); ank = (cx(ANK), float(ANK))
    OV = 8
    def layer(y0, y1):  # a piece on a full-size transparent layer, in original coordinates (shifted by PAD / TOP)
        L = Image.new('RGBA', (W + 2 * PAD, H + TOP), (0, 0, 0, 0))
        L.paste(im.crop((0, y0, W, y1)), (PAD, TOP + y0))
        return L
    thigh_l, shin_l, foot_l = layer(HIP - OV, KNEE + 2), layer(KNEE - OV, ANK + 2), layer(ANK - OV, H)
    P = lambda p: (p[0] + PAD, p[1] + TOP)

    def leg(th, kb, pitch, shade):
        k_new = (hip[0] + rot_xy(knee[0] - hip[0], knee[1] - hip[1], th)[0], hip[1] + rot_xy(knee[0] - hip[0], knee[1] - hip[1], th)[1])
        a_vec = rot_xy(ank[0] - knee[0], ank[1] - knee[1], th - kb)
        a_new = (k_new[0] + a_vec[0], k_new[1] + a_vec[1])
        t = thigh_l.rotate(th, center=P(hip), resample=Image.BICUBIC)
        s = shin_l.rotate(th - kb, center=P(knee), translate=(k_new[0] - knee[0], k_new[1] - knee[1]), resample=Image.BICUBIC)
        f = foot_l.rotate(pitch, center=P(ank), translate=(a_new[0] - ank[0], a_new[1] - ank[1]), resample=Image.BICUBIC)
        out = Image.new('RGBA', t.size, (0, 0, 0, 0))
        for piece in (f, s, t):
            out.alpha_composite(piece)
        if shade < 1:
            r, g, b, al = out.split()
            rgb = ImageEnhance.Brightness(Image.merge('RGB', (r, g, b))).enhance(shade)
            out = Image.merge('RGBA', (*rgb.split(), al))
        return out

    body = Image.new('RGBA', (W + 2 * PAD, H + TOP), (0, 0, 0, 0))
    body.paste(im.crop((0, 0, W, HIP + 4)), (PAD, TOP))
    frames = []
    for ph in PHASES:
        (rt, rk, rp, _), (lt, lk, lp, _) = ph
        comp = Image.new('RGBA', body.size, (0, 0, 0, 0))
        comp.alpha_composite(leg(lt, lk, lp, 0.78))   # far leg (left) is a little darker
        comp.alpha_composite(leg(rt, rk, rp, 1.0))    # near leg (right)
        comp.alpha_composite(body)
        bbox = comp.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
        dy = (H + TOP) - bbox[3]                      # drop the whole figure until the lowest foot is on the ground
        out = Image.new('RGBA', comp.size, (0, 0, 0, 0))
        out.alpha_composite(comp, (0, dy)) if dy >= 0 else out.alpha_composite(comp.crop((0, -dy, comp.width, comp.height)), (0, 0))
        frames.append(out)
    return frames


def main():
    mpath = os.path.join(SPR, 'manifest.json')
    manifest = json.load(open(mpath))
    made = {}
    for view in ('back', 'front', 'side'):
        frames = build_side() if view == 'side' else build_bf(view)
        made[view] = frames
        for i, fr in enumerate(frames):
            bb = fr.getchannel('A').point(lambda v: 255 if v > 20 else 0).getbbox()
            ms.save(fr, 'player_%s_w%d' % (view, i), manifest)
        print('ok', view, frames[0].size)
    json.dump(manifest, open(mpath, 'w'), indent=1)
    if '--preview' in sys.argv:
        rows = []
        for view, frames in made.items():
            H = 360
            row = [f.resize((int(f.width * H / f.height), H)) for f in frames]
            rows.append(row)
        Wt = max(sum(r.width for r in row) + 10 * (len(row) + 1) for row in rows)
        sheet = Image.new('RGBA', (Wt, 3 * 380), (200, 200, 205, 255))
        for ri, row in enumerate(rows):
            x = 10
            for r in row:
                sheet.alpha_composite(r, (x, ri * 380 + 10)); x += r.width + 10
        out = os.environ.get('PREVIEW', os.path.join(HERE, 'walk_preview.png'))
        sheet.convert('RGB').save(out); print('preview', out)


if __name__ == '__main__':
    sys.exit(main())
