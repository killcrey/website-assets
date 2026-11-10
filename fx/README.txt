Effect sprite sheets for the 2D game (index.html: loadFx / spawnFx / stepFx).

Made with pixelfx (https://github.com/patch-gg/pixelfx, MIT). Its LICENSE and NOTICE are in this folder
(LICENSE-pixelfx.txt, NOTICE-pixelfx.md); keep them with the sheets.

Rendered from a clone with:
  node tools/render.mjs <id> --sheet --no-actor --bg dark --opts '{"palette":[...]}' [--fps N]
  burst-cyan / burst-green / burst-gold = pickups/collect-burst in the game's neon colours (8-colour ramps)
  spark = impacts/hit-spark          boom = explosions/plasma-explosion at 20 fps
manifest.json = the grid of each sheet: w, h, cols, frames, ms per frame, anchor (ax, ay) the effect is drawn around.
