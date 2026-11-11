# Fresh street props for the 3D game: park bench, traffic cone, fire hydrant.
#   blender.exe --background --python props.py -- <out_dir>
# Each prop is built at real size (metres), front toward -Y, then rendered (front / side / 3-4) with a transparent background and exported as a vertex-colour GLB.
import bpy, bmesh, math, sys, os, random

out = sys.argv[sys.argv.index('--') + 1] if '--' in sys.argv else '.'
os.makedirs(out, exist_ok=True)
random.seed(7)

def new_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    return bpy.context.scene

_mats = {}
def mat(name, rgb, rough=0.65, metal=0.0, emit=0.0):
    key = (name, rgb)
    if key in _mats: return _mats[key]
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*rgb, 1); b.inputs['Roughness'].default_value = rough; b.inputs['Metallic'].default_value = metal
    if emit: b.inputs['Emission Color'].default_value = (*rgb, 1); b.inputs['Emission Strength'].default_value = emit
    _mats[key] = m; return m

def finish(o, m):
    o.data.materials.append(m)
    for p in o.data.polygons: p.use_smooth = False
    return o

def box(loc, size, m, rot=(0, 0, 0), bevel=0.0):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.active_object; o.scale = (size[0] / 2, size[1] / 2, size[2] / 2); bpy.ops.object.transform_apply(scale=True)
    if bevel:
        bm = bmesh.new(); bm.from_mesh(o.data); bmesh.ops.bevel(bm, geom=bm.edges[:], offset=bevel, segments=1, affect='EDGES'); bm.to_mesh(o.data); bm.free()
    return finish(o, m)

def cyl(loc, r, depth, m, verts=12, rot=(0, 0, 0), r2=None):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r2, depth=depth, location=loc, rotation=rot)
    return finish(bpy.context.active_object, m)

def sphere(loc, r, m, scale=(1, 1, 1), seg=12):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, radius=r, location=loc)
    o = bpy.context.active_object; o.scale = scale; bpy.ops.object.transform_apply(scale=True); return finish(o, m)

# ------------------------------------------------------------------ props
def bench():
    wood = [mat(f'wood{i}', c, 0.8) for i, c in enumerate([(0.36, 0.2, 0.1), (0.31, 0.17, 0.085), (0.4, 0.23, 0.11), (0.34, 0.19, 0.095)])]
    iron = mat('iron', (0.05, 0.065, 0.06), 0.55, 0.5)
    L = 1.6
    # seat: 4 slats, back rest: 3 slats (slight tilt back)
    for i in range(4): box((0, -0.17 + i * 0.115, 0.45), (L, 0.1, 0.045), wood[i % 4])
    for i in range(3): box((0, 0.27 + i * 0.015, 0.62 + i * 0.145), (L, 0.045, 0.125), wood[(i + 1) % 4], rot=(math.radians(-10), 0, 0))
    for sx in (-1, 1):
        x = sx * (L / 2 - 0.07)
        box((x, 0.0, 0.5 - 0.22), (0.045, 0.5, 0.04), iron)            # ground rail
        box((x, -0.2, 0.22), (0.04, 0.05, 0.44), iron)                  # front leg
        box((x, 0.24, 0.36), (0.04, 0.05, 0.7), iron)                   # rear leg to back
        box((x, 0.31, 0.95), (0.04, 0.05, 0.34), iron, rot=(math.radians(-10), 0, 0))  # back post
        box((x, 0.0, 0.5), (0.05, 0.52, 0.04), iron)                    # arm / seat rail
        box((x, -0.2, 0.48), (0.05, 0.05, 0.05), iron)                  # joins the front leg to the arm
    return 1.1

def cone():
    orange = mat('cone_orange', (0.95, 0.30, 0.04), 0.5); white = mat('cone_white', (0.92, 0.92, 0.9), 0.4); base = mat('cone_base', (0.07, 0.07, 0.07), 0.8)
    box((0, 0, 0.02), (0.46, 0.46, 0.04), base, bevel=0.02)
    H = 0.7; r0, r1 = 0.17, 0.035
    cyl((0, 0, 0.04 + H / 2), r0, H, orange, 10, r2=r1)
    def band(z0, z1):  # reflective collar following the cone's taper
        ra = r0 + (r1 - r0) * (z0 / H) + 0.004; rb = r0 + (r1 - r0) * (z1 / H) + 0.004
        cyl((0, 0, 0.04 + (z0 + z1) / 2), ra, z1 - z0, white, 10, r2=rb)
    band(0.30, 0.42); band(0.5, 0.58)
    return 0.8

def hydrant():
    red = mat('hyd_red', (0.62, 0.07, 0.05), 0.5, 0.1); dark = mat('hyd_dark', (0.18, 0.17, 0.17), 0.6, 0.6); cap = mat('hyd_cap', (0.72, 0.62, 0.12), 0.45, 0.3)
    cyl((0, 0, 0.05), 0.2, 0.1, red, 10)                    # flange
    cyl((0, 0, 0.36), 0.13, 0.52, red, 10)                  # barrel
    cyl((0, 0, 0.64), 0.155, 0.06, red, 10)                 # collar
    sphere((0, 0, 0.7), 0.13, red, (1, 1, 0.8), seg=8)             # dome
    cyl((0, 0, 0.82), 0.04, 0.07, cap, 8)                   # top nut
    for sx in (-1, 1):
        cyl((sx * 0.2, 0, 0.45), 0.065, 0.16, red, 10, rot=(0, math.pi / 2, 0))          # side nozzles
        cyl((sx * 0.29, 0, 0.45), 0.075, 0.035, cap, 10, rot=(0, math.pi / 2, 0))        # nozzle caps
    cyl((0, -0.2, 0.42), 0.095, 0.17, red, 12, rot=(math.pi / 2, 0, 0))                  # pumper nozzle
    cyl((0, -0.3, 0.42), 0.105, 0.04, dark, 12, rot=(math.pi / 2, 0, 0))
    return 0.95

PROPS = {'bench': bench, 'cone': cone, 'hydrant': hydrant}

def render_views(name, height):
    scene = bpy.context.scene
    sun = bpy.data.objects.new('sun', bpy.data.lights.new('sun', 'SUN')); scene.collection.objects.link(sun)
    sun.data.energy = 3.4; sun.data.color = (1, 0.95, 0.85); sun.rotation_euler = (math.radians(52), math.radians(8), math.radians(-38))
    fill = bpy.data.objects.new('fill', bpy.data.lights.new('fill', 'SUN')); scene.collection.objects.link(fill)
    fill.data.energy = 0.9; fill.data.color = (0.8, 0.88, 1); fill.rotation_euler = (math.radians(60), 0, math.radians(150))
    world = bpy.data.worlds.new('w'); scene.world = world; world.use_nodes = True
    bg = world.node_tree.nodes['Background']; bg.inputs['Color'].default_value = (0.65, 0.78, 0.95, 1); bg.inputs['Strength'].default_value = 1.0
    scene.render.engine = 'CYCLES'; scene.cycles.device = 'CPU'; scene.cycles.samples = 48; scene.cycles.use_denoising = False
    scene.render.film_transparent = True; scene.render.image_settings.file_format = 'PNG'; scene.render.image_settings.color_mode = 'RGBA'; scene.view_settings.view_transform = 'Standard'
    d = 8
    views = {'front': ((0, -d, height / 2), (math.pi / 2, 0, 0)), 'side': ((d, 0, height / 2), (math.pi / 2, 0, math.pi / 2)), '34': ((d * 0.655, -d * 0.655, height / 2 + d * 0.375), (math.radians(68), 0, math.radians(45)))}
    for v, (loc, rot) in views.items():
        cam = bpy.data.objects.new('cam' + v, bpy.data.cameras.new('cam' + v)); scene.collection.objects.link(cam)
        cam.data.type = 'ORTHO'; cam.data.ortho_scale = max(height * 1.25, 1.1) if name != 'bench' else 2.0
        cam.location = loc; cam.rotation_euler = rot; scene.camera = cam
        scene.render.resolution_x = scene.render.resolution_y = 480
        scene.render.filepath = os.path.join(out, f'{name}_{v}.png'); bpy.ops.render.render(write_still=True)

def export_glb(name):
    # vertex colours with a little weathering: grime and dust toward the ground, a touch of desaturation, and a random brightness per face (so flat colours stop reading as plastic)
    objs = [o for o in bpy.context.scene.objects if o.type == 'MESH']
    rnd = random.Random(11)
    for o in objs:
        m = o.data.materials[0].node_tree.nodes['Principled BSDF']; base = m.inputs['Base Color'].default_value
        emissive = m.inputs['Emission Strength'].default_value > 0
        me = o.data; a = me.color_attributes.new('Col', 'FLOAT_COLOR', 'CORNER'); cols = []
        for poly in me.polygons:
            jit = 1.0 + rnd.uniform(-0.07, 0.07)
            for li in poly.loop_indices:
                z = (o.matrix_world @ me.vertices[me.loops[li].vertex_index].co).z
                g = max(0.0, 1.0 - z / 0.28) * 0.38                      # ground grime
                lum = 0.299 * base[0] + 0.587 * base[1] + 0.114 * base[2]
                c = [base[k] + (lum - base[k]) * 0.12 for k in range(3)]   # slight desaturation
                dirt = (0.17, 0.14, 0.11)
                c = [min(1.0, (c[k] * (1 - g) + dirt[k] * g) * jit) for k in range(3)]
                cols += [c[0], c[1], c[2], 1.0]
        a.data.foreach_set('color', cols)
    bpy.ops.object.select_all(action='DESELECT')
    for o in objs: o.select_set(True)
    bpy.context.view_layer.objects.active = objs[0]; bpy.ops.object.join(); j = bpy.context.active_object; j.name = name; j.data.materials.clear()
    bm = bmesh.new(); bm.from_mesh(j.data); bmesh.ops.triangulate(bm, faces=bm.faces[:]); bm.to_mesh(j.data); bm.free()
    for p in j.data.polygons: p.use_smooth = False
    tris = len(j.data.polygons)
    bpy.ops.object.select_all(action='DESELECT'); j.select_set(True)
    bpy.ops.export_scene.gltf(filepath=os.path.join(out, f'{name}.glb'), export_format='GLB', use_selection=True, export_materials='NONE', export_vertex_color='ACTIVE')
    print('PROP', name, 'triangles', tris, 'glb_bytes', os.path.getsize(os.path.join(out, f'{name}.glb')))

for name, build in PROPS.items():
    new_scene(); _mats.clear()
    h = build()
    render_views(name, h)
    export_glb(name)
