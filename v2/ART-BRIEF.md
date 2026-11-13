# Art brief for Gemy (v2)

The game is a fixed angled-camera 3D toy-city (think Stealth Master / My Mini Mart): simple chunky shapes, saturated flat colours, soft shadows. It is NOT pixel art and NOT photo billboards. Art goes in as **flat textures and reference sheets**; Claude builds the 3D from them.

## 1. Facade textures (highest value, easiest to drop in)
Tileable front-of-building textures, flat/graphic style, no perspective, no people, no text, 512 px wide, ground-floor shopfront in the bottom 1/4, windows above. One per style, each with a "shopfront" version and a plain "side wall" version:
`brick`, `stucco`, `teal`, `pink`, `mural`, `sand`.
Prompt idea: "flat 2D facade texture for a stylised toy city building, front view, [style] San Diego [neighbourhood], graphic shapes, crisp edges, saturated colours, no perspective, no shadows, no text, seamless tile".

## 2. Landmarks (real San Diego, simplified to 3 to 5 big shapes each)
For each: a front reference + a side reference, flat colours, no photo detail. Claude turns them into low-poly models. Pick the ones that matter for the story:
- A Gaslamp Quarter street sign / lamp / iron balcony facade
- A corner bodega / mercado (awning, neon sign, produce stand)
- A Barrio Logan mural wall (full-wall flat art, colourful)
- A Chicano Park pillar (the painted highway pillars)
- A trolley stop / MTS trolley (side + front)
- Petco Park corner / a palm-lined boulevard piece
Give each real name, so the in-game block names and the Memories of Home tracks can map to real places.

## 3. Characters (reference sheets only; the 3D figures are built in code)
Front / side / back, A-pose, flat colours, big readable silhouette, chunky proportions (about 4.5 heads tall):
- Hero astronaut (cream suit, orange shoulders, olive boots, blue knee pads, backpack with two tanks)
- Patrol guard (navy uniform, cap, torch) and 2 more NPC types (street vendor, skater)
- Optional: one boss / rival

## 4. UI / logo
Flat icon set: memory gem (3 tiers: cyan, gold, magenta), HOME badge, car-hit icon, spotted "!" icon; plus a title-card logo.

## Rules
Flat shading, no gradients on shapes, no outlines unless asked, high contrast silhouettes, consistent palette across everything, names for every real place used.
