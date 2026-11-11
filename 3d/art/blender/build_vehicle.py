# VH_Van from the three Gemini sprite views, following the blender-image-to-3d method: measure, build to the measured silhouette, gate on a world-registered silhouette IoU, then project + bake the painted colour.
#   blender.exe --background --python build_van.py -- <asset_dir>
# Frame: 1 unit = 1 m, Z up, front of the van is -Y, origin at the ground under the van's centre. Reference pixel scale k = 2.3 m / 380 px (all three views share it, as in the game's hull builder).
import bpy, bmesh, json, math, os, sys
import numpy as np
from mathutils import Vector

A = sys.argv[sys.argv.index('--') + 1]
J = json.load(open(os.path.join(A, 'ref.json'))); KEY = J['key']; WR = J['wheel_R']; SILL = 0.85 * WR
k, HM, Hpx = J['k'], J['HM'], J['H_px']
L = J['side']['w'] * k; W = J['front']['w'] * k; WB = J['back']['w'] * k
side_env = J['side_env']; front_env = J['front_env']
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene

# ---------- measured profiles (all in metres) ----------
def erode(arr, r):  # running minimum: drops thin spikes (the antenna, the mirrors) from an envelope
    out = []
    for i in range(len(arr)):
        w = [v for v in arr[max(0, i - r):i + r + 1] if v is not None]
        out.append(min(w) if w and arr[i] is not None else None)
    return out

top = erode([c[0] if c else None for c in side_env], 9)            # roof line along the van, antenna removed
side_pts = [(i * k - L / 2, t) for i, t in enumerate(top) if t is not None][::6]   # every 6 px: about half the triangles of every 3 px, same silhouette to ~2 cm
side_poly = side_pts + [(y, SILL) for y, _ in reversed(side_pts)]   # underside kept above the wheels (the wheels are separate parts)

half = []
for r in range(Hpx):
    z = (Hpx - 1 - r) * k; e = front_env[r]
    half.append(None if e is None or z < SILL else (e[1] - e[0]) / 2)
half = erode(half, 26)                                              # mirrors are ~0.25 m tall: a +-0.16 m window removes them
zs = [(Hpx - 1 - r) * k for r in range(Hpx)]
roof = max(t for t in top if t is not None)
hmax = max(h for h in half if h is not None)
ok = [(z, h) for z, h in zip(zs, half) if h is not None and h > 0.25 * hmax and z < roof + 0.02]
ok = sorted(ok)[::8]
front_poly = [(-h, z) for z, h in ok] + [(h, z) for z, h in reversed(ok)]  # (x, z), left side up, right side down
front_poly = [(-h, z) for z, h in ok] + [(h, z) for z, h in reversed(ok)]

def prism(poly2d, axis_vals, kind):
    bm = bmesh.new()
    if kind == 'side':   # polygon in (y, z), extruded across x
        f = bm.faces.new([bm.verts.new((axis_vals[0], y, z)) for y, z in poly2d]); span = (axis_vals[1] - axis_vals[0], 0, 0)
    else:                # polygon in (x, z), extruded along y
        f = bm.faces.new([bm.verts.new((x, axis_vals[0], z)) for x, z in poly2d]); span = (0, axis_vals[1] - axis_vals[0], 0)
    r = bmesh.ops.extrude_face_region(bm, geom=[f])
    bmesh.ops.translate(bm, vec=span, verts=[v for v in r['geom'] if isinstance(v, bmesh.types.BMVert)])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    me = bpy.data.meshes.new('p'); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new('p', me); scene.collection.objects.link(o); return o

P1 = prism(side_poly, (-1.2, 1.2), 'side'); P2 = prism(front_poly, (-L / 2 - 0.3, L / 2 + 0.3), 'front')
m = P1.modifiers.new('cut', 'BOOLEAN'); m.operation = 'INTERSECT'; m.solver = 'EXACT'; m.object = P2
bpy.context.view_layer.objects.active = P1; bpy.ops.object.modifier_apply(modifier='cut'); bpy.data.objects.remove(P2)
body = P1; body.name = KEY + '_Body'
bv = body.modifiers.new('bev', 'BEVEL'); bv.width = 0.05; bv.segments = 1; bv.limit_method = 'ANGLE'; bv.angle_limit = math.radians(35)
bpy.ops.object.modifier_apply(modifier='bev')

def cyl(name, loc, r, depth, rot, verts=14):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot); o = bpy.context.active_object; o.name = name; return o
def box(name, loc, size, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot); o = bpy.context.active_object; o.name = name; o.scale = (size[0] / 2, size[1] / 2, size[2] / 2); bpy.ops.object.transform_apply(scale=True); return o

parts = [body]
wy = [c - L / 2 for c in J['wheel_centres_m']]                      # wheel centres from the side view's ground-contact runs
for sx in (-1, 1):
    for y in wy: parts.append(cyl(f'{KEY}_Wheel_{sx}_{y:.1f}', (sx * (W / 2 - 0.13), y, WR), WR, 0.26, (0, math.pi / 2, 0)))

bpy.ops.object.select_all(action='DESELECT')
for o in parts: o.select_set(True)
bpy.context.view_layer.objects.active = body; bpy.ops.object.join()
van = bpy.context.active_object; van.name = KEY
for p in van.data.polygons: p.use_smooth = False
bm = bmesh.new(); bm.from_mesh(van.data); bmesh.ops.triangulate(bm, faces=bm.faces[:]); bm.to_mesh(van.data); bm.free()
tris = len(van.data.polygons); print('TRIS', tris, 'L %.2f W %.2f' % (L, W))

# ---------- render helpers ----------
def setup_render(engine='BLENDER_WORKBENCH'):
    scene.render.engine = engine; scene.render.film_transparent = True
    scene.render.image_settings.file_format = 'PNG'; scene.render.image_settings.color_mode = 'RGBA'
    scene.display.shading.light = 'FLAT'; scene.display.shading.color_type = 'MATERIAL'
    scene.view_settings.view_transform = 'Standard'
def shoot(name, loc, rot, ortho, res):
    cam = bpy.data.objects.new('c' + name, bpy.data.cameras.new('c' + name)); scene.collection.objects.link(cam)
    cam.data.type = 'ORTHO'; cam.data.ortho_scale = ortho; cam.location = loc; cam.rotation_euler = rot; scene.camera = cam
    scene.render.resolution_x, scene.render.resolution_y = res; scene.render.filepath = os.path.join(A, 'review', name + '.png'); bpy.ops.render.render(write_still=True)
os.makedirs(os.path.join(A, 'review'), exist_ok=True)
vm = bpy.data.materials.new('clay'); vm.diffuse_color = (0.5, 0.5, 0.5, 1); van.data.materials.append(vm)
setup_render(); scene.display.shading.color_type = 'MATERIAL'
d = 12; zc = HM / 2
shoot('sil_side', (d, 0, zc), (math.pi / 2, 0, math.pi / 2), J['side']['w'] * k, (J['side']['w'], Hpx))
shoot('sil_front', (0, -d, zc), (math.pi / 2, 0, 0), max(HM, J['front']['w'] * k), (J['front']['w'], Hpx))
shoot('sil_back', (0, d, zc), (math.pi / 2, 0, math.pi), max(HM, J['back']['w'] * k), (J['back']['w'], Hpx))

# ---------- triplanar projection of the three painted views, baked to one atlas ----------
van.data.materials.clear()
bpy.context.view_layer.objects.active = van; van.select_set(True)
bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='SELECT'); bpy.ops.uv.smart_project(angle_limit=math.radians(66), island_margin=0.015); bpy.ops.object.mode_set(mode='OBJECT')
mt = bpy.data.materials.new(KEY + '_Paint'); mt.use_nodes = True; nt = mt.node_tree; nt.nodes.clear()
N = lambda t, **kw: nt.nodes.new(t)
def link(a, ao, b, bi): nt.links.new(a.outputs[ao], b.inputs[bi])
tc = N('ShaderNodeTexCoord'); geo = N('ShaderNodeNewGeometry')
sp = N('ShaderNodeSeparateXYZ'); link(tc, 'Object', sp, 0)
def imgnode(path):
    n = N('ShaderNodeTexImage'); n.image = bpy.data.images.load(path); n.extension = 'EXTEND'; n.interpolation = 'Linear'; return n
def planar(a_out, b_out, su, sv, ou, ov):  # (a, b) object axes -> uv = (a*su+ou, b*sv+ov)
    cb = N('ShaderNodeCombineXYZ'); link(sp, a_out, cb, 0); link(sp, b_out, cb, 1)
    mp = N('ShaderNodeMapping'); mp.vector_type = 'POINT'; mp.inputs['Location'].default_value = (ou, ov, 0); mp.inputs['Scale'].default_value = (su, sv, 1); link(cb, 0, mp, 0); return mp
tf = imgnode(os.path.join(A, 'ref', 'front_fill.png')); ts = imgnode(os.path.join(A, 'ref', 'side_fill.png')); tb = imgnode(os.path.join(A, 'ref', 'back_fill.png'))
link(planar('X', 'Z', 1 / W, 1 / HM, 0.5, 0), 0, tf, 0)
link(planar('Y', 'Z', 1 / L, 1 / HM, 0.5, 0), 0, ts, 0)
link(planar('X', 'Z', -1 / WB, 1 / HM, 0.5, 0), 0, tb, 0)
sn = N('ShaderNodeSeparateXYZ'); link(geo, 'Normal', sn, 0)
def mathn(op, a=None, b=None, ain=None, bin_=None, clamp=False):
    n = N('ShaderNodeMath'); n.operation = op; n.use_clamp = clamp
    if a is not None: link(*a, n, 0)
    if b is not None: link(*b, n, 1)
    if ain is not None: n.inputs[0].default_value = ain
    if bin_ is not None: n.inputs[1].default_value = bin_
    return n
ax = mathn('ABSOLUTE', (sn, 'X')); az = mathn('ABSOLUTE', (sn, 'Z')); wside = mathn('MAXIMUM', (ax, 0), (az, 0))
negy = mathn('MULTIPLY', (sn, 'Y'), bin_=-1.0); wfront = mathn('MAXIMUM', (negy, 0), bin_=0.0); wback = mathn('MAXIMUM', (sn, 'Y'), bin_=0.0)
pw = lambda w: mathn('POWER', (w, 0), bin_=6.0)
ws, wf, wb = pw(wside), pw(wfront), pw(wback)
tot = mathn('ADD', (ws, 0), (wf, 0)); tot2 = mathn('ADD', (tot, 0), (wb, 0)); tot3 = mathn('ADD', (tot2, 0), bin_=0.0001)
def scaled(tex, w):
    s = mathn('DIVIDE', (w, 0), (tot3, 0)); v = N('ShaderNodeVectorMath'); v.operation = 'SCALE'; link(tex, 'Color', v, 0); link(s, 0, v, 3); return v
a1 = scaled(tf, wf); a2 = scaled(ts, ws); a3 = scaled(tb, wb)
s1 = N('ShaderNodeVectorMath'); s1.operation = 'ADD'; link(a1, 0, s1, 0); link(a2, 0, s1, 1)
s2 = N('ShaderNodeVectorMath'); s2.operation = 'ADD'; link(s1, 0, s2, 0); link(a3, 0, s2, 1)
em = N('ShaderNodeEmission'); link(s2, 0, em, 'Color'); out = N('ShaderNodeOutputMaterial'); link(em, 0, out, 0)
van.data.materials.append(mt)
img = bpy.data.images.new(KEY + '_albedo', 1024, 1024); bt = nt.nodes.new('ShaderNodeTexImage'); bt.image = img; nt.nodes.active = bt
scene.render.engine = 'CYCLES'; scene.cycles.device = 'CPU'; scene.cycles.samples = 4
scene.render.bake.margin = 12
bpy.ops.object.bake(type='EMIT')
img.filepath_raw = os.path.join(A, KEY + '_albedo.png'); img.file_format = 'PNG'; img.save()
# delivery material: the baked atlas
for n in list(nt.nodes): nt.nodes.remove(n)
b = nt.nodes.new('ShaderNodeBsdfPrincipled'); b.inputs['Roughness'].default_value = 0.85; tx = nt.nodes.new('ShaderNodeTexImage'); tx.image = img
nt.links.new(tx.outputs['Color'], b.inputs['Base Color']); o2 = nt.nodes.new('ShaderNodeOutputMaterial'); nt.links.new(b.outputs[0], o2.inputs[0])
scene.render.engine = 'BLENDER_WORKBENCH'; scene.display.shading.light = 'FLAT'; scene.display.shading.color_type = 'TEXTURE'
shoot('tex_side', (d, 0, zc), (math.pi / 2, 0, math.pi / 2), J['side']['w'] * k, (J['side']['w'], Hpx))
shoot('tex_front', (0, -d, zc), (math.pi / 2, 0, 0), max(HM, J['front']['w'] * k), (J['front']['w'], Hpx))
shoot('tex_back', (0, d, zc), (math.pi / 2, 0, math.pi), max(HM, J['back']['w'] * k), (J['back']['w'], Hpx))
for nm, loc, rot in (('tex_34f', (7.5, -8.5, 5.5), (math.radians(64), 0, math.radians(41))), ('tex_34b', (7.5, 8.5, 5.5), (math.radians(64), 0, math.radians(139))), ('tex_graze', (1.6, -10, 1.3), (math.radians(88), 0, math.radians(9)))):
    shoot(nm, loc, rot, 5.2, (800, 600))
bpy.ops.object.select_all(action='DESELECT'); van.select_set(True)
bpy.ops.export_scene.gltf(filepath=os.path.join(A, KEY + '.glb'), export_format='GLB', use_selection=True, export_image_format='WEBP', export_cameras=False, export_lights=False)
print('GLB', os.path.getsize(os.path.join(A, KEY + '.glb')))
