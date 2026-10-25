# HANDOFF: LAYERS: San Diego (the 3D game), 2026-10-23

Read this first, then `3d/DESIGN.md` (the running design log, newest decisions are in the section called "Phone controls, Tear timer, deliveries, baskets, ego blast v2 (2026-10-23)", which holds everything built in the last long session; some older sections lower in that file are early plans and are stale), then `CLAUDE.md` (the repo-wide rules).

## 1. What this is

A third-person 3D browser game, one file: `3d/index.html` (about 2,000 lines, Three.js loaded from a CDN, no build step, no npm). It is the sunlit, earth-tone, blue-sky counterpart to the dark space shooter in `index.html` (the 2D game, "LAYERS: Void Runner"). You play an astronaut on a long real-San-Diego street (Gaslamp Quarter at one end, Barrio Logan at the other), hunted by Agency Suits, thugs and a van. Collect baseball cards, copper wire and records, deliver them to the Kid and Pancho, find the crew (Juan Carlos, Christopher, Eduardo), fill your Low C to 100%, shoot the seal off the Tear, and run through the Tear before the VOID closes.

- Live: https://game.theinvisiblepanchos.com/3d/ (GitHub Pages, private repo `killcrey/website-assets`, branch `main`; a push to `main` IS the deploy).
- Local folder: `C:\Users\16193\Desktop\website-assets` (Windows; Git Bash and PowerShell both work).
- Audience: mostly phones in portrait, arriving from Instagram's in-app browser (so: tap-to-start for audio, no hover, small screens, WebGL only, no WebGPU). PC works too. The 2D game is portrait too, so portrait is the target.
- The band: The Invisible Panchos. The new album is **Memories of Home** (always call it an ALBUM, never an EP). Crew names in game: Juan Carlos (invisibility), Christopher (doubles Low C), Eduardo (clears heat). Pancho runs the bodega; the Kid takes baseball cards; Luz and Pancho's father are helpers.

## 2. Rules the user set (follow them)

- **Never `git push` unless the user's message says "Push"** (that single word is enough; "push when done" also counts for that turn's work). Committing locally is always fine. Commit messages end with a `Co-Authored-By:` line for whichever model wrote it.
- Make **targeted edits**, never rewrite whole files for a small change. No speculative refactors, no "while I'm here" cleanup.
- Keep replies short and plain: say what you did and what you verified, not a lecture. When the user asks "what do you think?" or "discuss", answer with an opinion and a recommendation and **do not build** until they say to. When they say "do your recs", build the recommendations.
- Verify every change in a real browser before saying it works (see section 4). Report honestly what you did NOT verify (anything on a real phone has never been verified by us).
- Standing facts: the user's Netlify/Supabase "bodega" shop is a separate project (`C:\Users\16193\panchos-bodega`); do not touch it from this repo.

## 3. How to run it

```bash
cd C:\Users\16193\Desktop\website-assets
python -m http.server 8935        # static server; this one has NO Range support, so seeking inside an MP3 resets to 0 locally (GitHub Pages is fine)
```
- Open `http://localhost:8935/3d/?debug` (the `?debug` flag shows fps/draw calls and the test hooks are always on). Add `&cb=NN` (any new number) every reload; browsers and the live domain serve stale JS on plain reloads.
- `?tips` replays every first-contact tip (otherwise they are remembered in localStorage key `layers3d_tips_v1`).
- Phone view in the browser pane: resize to 375x812 (the "mobile" preset), reload. Reset to desktop when done.
- Tools used so far: the Claude desktop app's built-in browser (`mcp__Claude_Browser__*`: navigate, javascript_tool, computer screenshot/zoom, resize_window, read_console_messages). Any Chromium with devtools works the same way.

## 4. How to test (important: this project has no test suite)

A hidden tab never runs `requestAnimationFrame`, and screenshots of the in-app pane can show a stale or oddly cropped frame. So tests drive the game directly through `window.__g`:

```js
const g = window.__g, H = g.hunt;
document.getElementById('start-btn').click();                      // start (the synthetic click is enough for game logic)
const run = (s) => { for (let i = 0; i < s * 60; i++) g.update(1 / 60); };   // advance s seconds of game time
const key = (t, code) => window.dispatchEvent(new KeyboardEvent(t, { code, key: code, bubbles: true }));
// quiet the world so a test only measures what you mean to:
H.van.stop = 999; H.van.z = -150; g.roamers.forEach(r => { r.wait = 999; }); H.enemies.forEach(e => { e.wait = 999; e.x = e.sx; e.z = e.sz; });
g.player.position.set(0, 0, -100); g.yaw = 0;
key('keydown', 'KeyW'); run(1); key('keyup', 'KeyW');              // walk
g.render();                                                         // then take a screenshot
```
- Touch input can be simulated with `new PointerEvent('pointerdown', { pointerId, pointerType: 'touch', clientX, clientY, bubbles: true })` dispatched on `window` (stick = left 56% of the screen, Low C/fire = right side below 35% height) or on the buttons (`#lowc-btn`, `#swap-btn`, `#ego-btn`).
- **Soak test** (always run after a big change): random WASD + Space for 4-6 minutes of game time via `g.update`, assert every position/yaw/camera value `isFinite`, call `H.restart()` whenever `H.captured` is true, and read the console for errors. See DESIGN.md for what each soak covered.
- Draw-call check: `g.setTier(0); g.renderer.info.reset(); g.render(); g.renderer.info.render.calls` (about 210/204/123 at z -20/-120/-230; keep it flat; phones are the constraint).
- Hooks on `window.__g`: `update render player camera scene renderer loot pickups billboards NPCS playerBill heat cloak cardsHeld wiresHeld egoCharges tearOpen tearT signs facades seal pressBuf vanWatchT music suitKills dbg ammo weapon swapWeapon skyK tipsSeen tipQueue humT dadOn luzCool fireEgo roamers lowC inTruck ego truck wanderers setTier tier yaw pitch camDist lowCActive start`, and `g.hunt` has `enemies van setHeat restart captured crew invis lowCMult lowC nav`. Several are getters/setters (for example `g.ammo = 12`, `g.lowC = 33`, `g.egoCharges = 1`, `g.wiresHeld = 3`, `g.cardsHeld = 3`). `g.dbg` exposes `sightOf visionRange firstHit invis cloak hidden`.
- Test-setup traps we hit: killing enemies (`e.dead = true`) in one page session means they are gone until reload (restart respawns Suits from `SUIT_DEFS` but not thugs); teleporting the player next to the bread truck while `stillFor` is already large makes you hide instantly; a test that stands near a Suit will get you captured, so park enemies at `sx, sz` first; heat toasts overwrite other toasts within one frame, so detect events from state (like `lureT`) not from toast text.

## 5. Code map of `3d/index.html` (line numbers drift; search the comment banners)

| Area | Where to look |
|---|---|
| CSS + HUD HTML | top of file; ids: `hud-loc hud-obj hud-status goals toast tip speech np void sealbar lowc lowc-btn swap-btn ego-btn stick stick-ghost audio-controls mute btn-skip back start null-screen fail` |
| Three.js load, renderer, quality tiers 0/1/2 (no bloom / half-res / full; adaptive step-down) | `// ---- load Three.js`, `// ---- renderer + quality tiers` |
| Sky canvas + fog + lights | near `paintSky`; `updateSky` recolors them while the Tear is open |
| World | `// ---- world: one long main street`: `STREET_START 12`, `STREET_END -300`, `GAPS [-88,-145,-202,-259]` (cross streets), alleys at x=+-20, `BL_Z -185` (Barrio Logan), collision map `walls` (AABBs, `cover:true` = low cover that blocks enemy sight but not bullets), `colliders` (circles), `firstHit` (segment vs AABB; used for camera, sight and line of fire), `addWall`, `box()` (everything is batched into ONE instanced mesh with merged ink edges) |
| Buildings, `STORE_SLOTS`/`FACADES` (storefront art), `BODEGA`/`OLD_BODEGA`, `buildingDetail()` (doors, trim, cornices, roof clutter), string lights | `// stucco buildings both sides` |
| Cover (cars, dumpsters, carts...), props, signs (`SIGN_LOG`) | `// ---- cover`, `// ---- art cover, street props` |
| Gaslamp arch (z -30), Barrio Logan arch, hills/skyline, `PORTAL` (Tear at z -284), `SEAL` object (z -281) | search `GASLAMP QUARTER arch`, `PORTAL`, `const SEAL` |
| Sprites: `Billboard` class (front/side/back art, tilt toward heading, tint/jitter), `makeStatic`/`buildHull` (stationary things are solid shapes built from their 3 views so they never turn), `STATIC_GROUPS` distance culling | `class Billboard`, `function buildHull` |
| NPCs: `addNpc`, wanderers (father, Luz), roamers (Pancho, Kid, crew via `goTo` on the nav graph), `CREW`, `makeBar` (name + power bar sprites), the bodega facade | `updateWanderers`, `updateRoamers`, `addCrew` |
| Items: `placePickup`, `collect()` (cards, wire, scratcher, record = ego charge, tape = analog static, baskets with a hidden `bugged` flag), `respawnPickups` | `// ---- collectibles` |
| Input: stick, lower-right fire/Low C zone, `lcDown/lcUp`, `pressBuf` (a short buffer so a quick tap still registers), wheel + R + 1/2 to switch weapon, F ego blast | `// ---- input` |
| Audio: WebAudio SFX (`tone`), synth bed (only a fallback), the album (`ALBUM`, `startMusic`, `nextTrack`, ducking in `updateMusic`), mute + skip icons | `// ---- audio`, `// ---- the album` |
| Low C | `updateLowC`, `repelBurst` |
| Hunt: `SPECS`, `makeEnemy`, `SUIT_DEFS` (8 posts, some pairs), `updateEnemy` (states PATROL/INVESTIGATE/CHASE/SEARCH, `lureT` when bugged), thug AI (hunts last seen spot, sweeps, only knows where you are if you're bugged), `updateVan` (beam; 4 s in it unloads thugs), `updateReinforce` (extra Suits at high heat), `capture`, `restartRun` | `// ---- the hunt`, `// ---- enemies`, `// ---- the van` |
| Bread truck (hide in it), deliveries, gun (`gunTarget`, `updateGun`, `killEnemy`, `sealHit`), ego blast, Tear + seal (`updateTear`, `sealUp`, `sealDown`, `breakSeal`), Luz/dad helpers, goals panel (`updateGoals`), tips (`TIPS`, `scanTips`), `updateHunt` (calls everything each frame) | `// ---- the bread truck` ... `function updateHunt` |
| Game loop `update(dt)`: input -> corridor camera -> movement + collisions + corner assist -> `updateHunt` -> camera -> HUD | `// ---- game loop` |
| Debug hooks | bottom: `window.__g = {...}` |

## 6. Current rules of the game (what is built and decided)

- **Controls (portrait phone)**: left thumb = floating stick (push well past the rim to run), faint ghost stick shows where. Right thumb = hold anywhere in the lower right for Low C, or **tap once per gun shot**. No latching, no auto-fire. A circle appears once you have ammo and swaps GUN/LOW C; another circle for the ego blast when you hold one. PC: WASD, Shift run, Space/left click = Low C (hold) or fire (tap), R / scroll wheel / 1-2 swap weapons, F ego blast, mouse look when the pointer is captured.
- **Camera**: always behind the way you head. It turns by itself only when you head along a corridor (main street/alley = z axis, cross street = x axis) and the view is not already looking that way: one fast turn (about 0.3 s), while the stick keeps its old meaning until you let go, flip it or push forward (this prevents lurching/spirals). Left/right only lean the view about 20 degrees. Standing still it settles square to the corridor. Pitch capped low (0.08-0.32). Distance steady (6.6 phone, 6.0 wide); only walls pull it in (three rays). FOV 80 on phones. Do not reintroduce turn-zoom or heading-chasing: both were tried and felt bad.
- **Low C**: hold. Burns 1.8 per second from a tank of 32.7 (x2 after Christopher). On press it shoves enemies within 16 m away for 1.6 s, then freezes anything within 8.5 m while held. Adds no heat, doesn't widen sight, dispels the Suits' "bad vibes" drain. Fills from: baseball cards to the Kid (7 = full), Pancho's father (stand still 4 s, costs heat), real gift baskets (+60%), Christopher (fills Low C, gun, laser and ego blast; see below).
- **Gun**: Pancho turns copper wire into AMMO (10 rounds per wire, 50 max; a laser gun pickup is 15 rounds in its own pool, 50 max, up to 6 lie around). Auto-aims at the nearest Suit/thug within 18 m with a clear line (cover doesn't stop bullets), else the seal. Never the van. Suit 2 hits, thug 5; a Suit killed respawns at its post after 20 s once you're 40 m away. 8 Suits patrol at the start, 5 more join at 60 s of play and 7 more at 140 s (20 in all; `def.after`, `runT`). **Caught**: you restart at the last checkpoint (z -90, -180, -260 passed, `cpZ`) with half your cards, copper, ammo, laser rounds and score, 30% Low C and 5 s invisible. **Reaching the Tear** shows a results card (time, kills, times caught, score) with a 6 s auto-elevate to the 2D game. A low horn plays when a thug first spots you. Sight cones are only drawn within 32 m on phones, 48 m on desktop. Each shot adds a little heat and is heard (Suits within 22 m investigate); each kill adds more heat than the last.
- **Heat** (0-3: CLEAR/WATCH/CULTIVATE/CONTAIN): rises while anything sees you. At CULTIVATE+ up to 4 extra Suits appear out of sight and a thug comes (3 at CONTAIN). Eduardo clears it; scratchers cut 1.5. **Hiding** (bread truck from the street side, or crouching by cover) works at any heat as long as no enemy has eyes on you and you aren't bugged.
- **Baskets**: all look the same; 40% are bugged (+1 heat, every Suit homes in on you for 15 s), rest give Low C. Luz's "hum" (20 s) shows enemies and which baskets are bugged.
- **Crew and helpers**: roam the whole map; walking up pays out again every 40 s (power bar with the name floats over them). Pancho walks between the bodega (now in Barrio Logan at z -267.6) and wherever a crew member is, 40 s each. The Kid walks between the bodega and the Gaslamp sign, 40 s each end. Everyone you walk up to stops and faces you.
- **Christopher** roams the whole map (alleys too) at 3.4 m/s, 2-5 s at each stop; finding him fills the gun, laser and ego blasts and charges Low C to at least half (every 40 s). **You start with 10 rounds** (`START_AMMO`). **Lock-on ring** (`updateReticle`) shows on whatever the gun will hit next with its health bar. **Phone HUD**: area line hidden, ammo shown on the FIRE/swap buttons, reminders only for what you carry, tips wait for toasts and speech, one short start card. **Green circle** (`BODEGA_SPOT`, in front of the bodega door): stand in it 5 s ("PANCHOS BODEGA IN: n") and the game pauses (`gamePaused`, the frame loop stops) under a full-screen iframe of bodega.theinvisiblepanchos.com with OPEN FULL SITE and BACK TO GAME buttons (Esc closes). Stripe Checkout can't run inside an iframe, so buying needs OPEN FULL SITE. **Red glow** on the bottom edge (enemy within 13 m behind you) and on the left or right edge (enemy within 13 m but off screen that side), `#behind-fx`, `#left-fx`, `#right-fx`. **Character rewards (crew, Luz, Pancho's dad, Kid, Pancho) only trigger within 1.7 m.**
- **The Tear** (once per full charge: `tearArmed` is cleared when it opens and only set again after Low C drops below full, so a full tank does not reopen it): closed until Low C is 100%; when it opens, 10 extra Suits start patrolling all over the map (`spawnTearMob`, gone when it closes; nothing is posted in front of the seal). Opens for max(25, distance/7.2 x 1.25 + 10) seconds ("VOID IS CLOSING!" red bar across the top, sky turns red). An **Agency seal** blocks it at z -281 (10 HP): bullet 2, Low C 1.2/s within 9 m, ego blast 6 (`SEAL_DMG`). It reforms each time the Tear reopens. Its health bar is on the wall under the words, plus an orange banner at the top. Entering the Tear currently just does `location.href = '../'` (see roadmap).
- **UI**: slim reminders on the right (`CARDS>KID n`, `WIRE>PANCHO n`, plus POWER>DAD, HEAT>EDUARDO, SEAL/TEAR when relevant), arrows over the Kid (red), Pancho (gold), his dad (blue) with names, quiet one-line dialogue, first-contact tips for 21 things, a how-to-play card on the start screen, top-right skip + mute icons, "now playing" line. No score is shown (loot points are still tracked, `loot.points`).
- **Music**: the 12 Memories of Home tracks in `3d/music/` (VBR about 145 kbps, 43 MB), shuffled and looping, started by the Start tap, ducked under Low C/gunfire/ego. Source masters: `P:\INVISIBLE PANCHOS MAIN\MEMORIES OF HOME\memories masters` (use the Oct-17 THE REIGN; ignore the `pre` folder). Encode command: `ffmpeg -nostdin -i "<src>.mp3" -vn -map_metadata 0 -id3v2_version 3 -codec:a libmp3lame -q:a 4 -ar 44100 3d/music/<slug>.mp3`, then add `['TITLE', 'slug']` to `ALBUM`.

## 7. Pitfalls we hit (save yourself the time)

- **Layout parity**: the building loop uses a seeded random stream (`rnd`) and anything that changes how many random numbers a building consumes reshuffles every later sign/window/color. The bodega move kept the old behavior with `OLD_BODEGA`, `wasBodega`, `hPar` and "roll the dice either way" lines. New decoration must use its own stream (`drnd`, `crnd`), never `rnd`.
- **Never put a `//` comment in the middle of a one-line JS statement** when patching text: it comments out the rest of the line (it silently disabled the kill effects once and broke the file once).
- When patching via Python in a shell heredoc, backslash escapes get re-interpreted (`\\u2019` may arrive as the real character). Match on text without escapes, or check the result with grep. The repo's own text uses real characters for some apostrophes and `\u25B8`-style escapes for others.
- Collisions are 2D (x,z): walls are AABBs, props are circles; the player radius is 0.45. "Corner assist" slides you around car fronts; do not remove it or players get stuck.
- Anything instanced/batched (boxes, windows, bulbs) is cheap; anything with its own material per object costs a draw call. The phone budget is the real limit.
- `scene.add` of transient effects (tracers, puffs) is cleaned in `updateFx`; always remove and dispose what you add per shot.
- The user can't see a hidden tab: if a test never changes, check `document.hidden`.
- Security/stability: nothing here talks to a server; the 2D game's Supabase leaderboard is separate (and was hardened against XSS: rows are built with `textContent`).

## 8. Open items and ideas (nothing here is built unless noted)

1. **2D <-> 3D handoff (the big one)**: the plan is a rare Tear portal in the 2D game's blue-sky cloud section (`memoryFlightActive` in `index.html`; recolor the portal sprite via an offscreen canvas with `source-atop`), a sessionStorage payload handing the run into `3d/`, and back. Being captured should throw the player back to the 2D game as STATUS: NULL, losing carried loot with a score penalty. Today the Tear just links to `../` and capture just resets the street (`restartRun`).
2. Enemies steal the Kid's cards (so you defend him); scratchers as bribes; a damaging Low C cone; a "life force" meter (the user floated it and we deferred it: Low C already drains, so ask what happens at zero before building).
3. **Art still missing**: mural wall, stadium corner (Gemini prompts 11/12 in `3d/ASSET_PROMPTS_2.md`), regenerated bench and traffic cones (the old ones came out smeared), optional Barrio Logan arch art (a code-built arch is in use), back-left/back-right/front-3/4 views of the astronaut so diagonal walks look right (the flat sprite is only tilted up to about 30 degrees today). Building detail "cheap pass" is done (doors/trim/roof clutter/string lights); the next level is Gemini storefront strips and wall textures for the two ends of the street, shutters and blade signs.
4. **Never verified on a real phone**: stick and Low C feel, camera in alleys, the seal, music autoplay in Instagram's browser, performance on older phones. Ask the user for feedback screenshots; they test on their own phone and send screenshots.
5. The 2D game's MP3s (14 files at the repo root, about 112 MB at 256 kbps) are untouched; re-encoding them to about 160 kbps would cut roughly 45 MB but adds git history weight (every committed version stays in `.git`, now about 120 MB). `PRE.mp3` is in the repo but not in the 2D playlist. The 3D "3D not available" fallback screen still links to the 2D game on purpose.
6. Tuning is first-guess everywhere (heat rates, spawn counts, Suit speed, tear timer); expect the user to ask for changes after playing. Their taste so far: fast, readable, less clutter on screen, precise movement, camera behind the character, everything on the street should feel alive.

## 9. A good first hour for the next model

1. Read this file, `3d/DESIGN.md`'s newest section, and `CLAUDE.md`. Start the server and load `?debug&tips`.
2. Run the soak test above to confirm a clean baseline (expect 0 errors, `bad` 0).
3. Ask the user what to build next; the most valuable open item is the 2D <-> 3D handoff (item 1). Discuss the plan before building, because it touches the 2D game's `index.html` as well.
- **Round-3 art (2026-10-24)**: Gaslamp Victorian/brick buildings (`gl_*`, 8 of them) and Barrio Logan pieces (`bl_row` Tierra Libre, `bl_farol` El Farol diner, `pillar_a/b` Chicano Park pillars) are flat facades dropped on building slots via `FRESH` / `FRESH_SLOTS` (a slot keeps every random roll of the plain building it replaces, so the rest of the street didn't change; only the 6 signs on those buildings are gone). `car_d` is the green lowrider (2 parked: first car past z -120 and past z -215). Cut with `python 3d/art/make_sprites.py car_d gl gl2 pillar bl_farol bl_row`. About 29 MB more decoded texture memory. **Waiting on a cleaner re-generation**: the Chicano Park pavilion (`chicanopark kiosk.jfif` has photo remnants in the backdrop); stadium (prompts 5, 6), Gaslamp arch (4) and Barrio Logan props (11) in `3d/ASSET_PROMPTS_3.md` are not generated yet.
