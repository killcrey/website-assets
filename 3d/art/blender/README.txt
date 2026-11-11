Blender scripts behind the 3D models in 3d/art/models/ (kept here so they are not lost). The paths inside them point at this PC
(C:/Users/16193/game-research/...: a portable Blender 5.3 under blender/app/, and van-3d/ as the work folder); change them to run elsewhere.

make_vehicle.py <key> <heightM>   e.g. python make_vehicle.py truck 2.9
    Reads 3d/art/sprites/<key>_{front,side,back}.webp, measures them (one pixel scale k = heightM / front height), runs build_vehicle.py in
    headless Blender, prints the silhouette IoU gates and writes a review sheet. Needs Python with Pillow, numpy, scipy.
build_vehicle.py                  side silhouette extruded across the width, boolean-intersected with the front silhouette extruded along the length,
    bevelled, wheels added, the three painted views projected triplanar and baked to one 1024 atlas, exported as <key>.glb (WebP texture).
props.py                          bench, cone and hydrant built from primitives with vertex colours (blender.exe --background --python props.py -- <out>).

Method credit: the "measure, build to the measured silhouette, gate on silhouette IoU, then bake" workflow follows majidmanzarpour/blender-game-skills (MIT).
