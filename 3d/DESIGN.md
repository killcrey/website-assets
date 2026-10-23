# LAYERS: San Diego — design notes (3D section)

Source material: *Memories of Home* script V1 and the Lore Book (Audience Edition). Status: proposal, not built.
The Lore Book's last page already describes this section: "The anomaly takes you back to Earth, unlocks a sample from Memories of Home, then sends you back into the void."

## Art direction (decided 2026-10-22)
Earth, not space. The 2D game is dark neon void; the 3D section is **daytime San Diego**: blue sky, sun, terracotta / adobe / cream / sage stucco, tan sidewalks, green palms, painted shop signs, ink-brown outlines. Neon is reserved for the one surreal thing: **the Tear** (a dark geometric rip with a cyan-white glow) — it should pop against the warm world. Agency vehicles and Suits are matte black/charcoal so they read instantly against the earth tones. The prototype is already re-themed this way. Character prompts for Nano Banana are in `CHARACTER_PROMPTS.md`.

## Decisions (2026-10-22)
- **Trigger:** a **rare portal in the blue-sky cloud section** of the 2D game (the hazard-free `memoryFlightActive` stretch that currently spawns only clouds). It reuses the existing portal entity (`portal.png`, drawn in `Entity.draw`) with a different color and glow so it can't be confused with the purple Pancho Portal. Tint it with an offscreen canvas and `source-atop` (works everywhere; `ctx.filter` isn't reliable on iOS). Handoff stays behind a test flag until the 3D side is ready.
- **No music unlocks in 3D** — the 2D game already does that. Vinyl and tape therefore pay out as points and utility, not tracks.
- **Thermos removed.** **Domingo removed** as a character (the record store can still exist as a safe-house location, with no keeper).

## Collectibles (built in the prototype, carried until you escape; lost if caught)
| Item | Count | What it does |
|---|---|---|
| **Tony Gwynn card** | 8 | +300 each; full set (eight batting titles) +5,000. Later: each card thins "the cover" so the exit Tear shows through. |
| **Scratcher** | 6 | Scratch-off roll: 100 (70%) / 250 (20%) / 500 (8%) / 2,000 jackpot (2%). Lore: they bought scratchers before every launch. |
| **Copper wire** | 3 | +50 and a longer Low C hold (stored as a boost for when the ability exists). Placed on the sidewalk edges. |
| **Vinyl** | 3 | +1,000 — the big prize, in out-of-the-way spots (later: near van routes). |
| **Reel-to-reel tape** | 2 | +200 and an 8-second **analog cloak** (stacks to 12s): the Agency can't see you (heat won't rise from sight). |
| **Fruit basket** | 2 | **Trap.** Looks like a gift, has a tiny blinking red bug light. Taking it raises heat one level for ~12s. No points. |

Tuning numbers live at the top of the collectibles block in `3d/index.html`.

## Art pipeline (built 2026-10-22)
- Gemini turnaround sheets go in `3d/art/_originals/` (git-ignored, full size). `python 3d/art/make_sprites.py` cuts each sheet into transparent front/side/back WebP sprites in `3d/art/sprites/` (~0.5 MB total, committed) plus `manifest.json`.
- The game draws them as **camera-facing billboards** (`Billboard` in `3d/index.html`): the right view is chosen from where the camera is, mirrored for the side view. Cheap on phones, matches the 2D art exactly, and can be swapped for rigged 3D models later without changing the level.
- To add a character: drop the sheet in `_originals/`, add a line to `SHEETS` in `make_sprites.py`, run it, then `addNpc(...)` in `index.html`. If a sprite fails to load, that figure just doesn't appear.
- **Done:** every character, both vehicles, all six collectibles and the bodega facade now use the Gemini art: Player, Pancho, Pancho's father, the Kid, Luz, the Suits (x2), the thugs (x2), Christopher, Juan Carlos, Eduardo, the black van, the bread truck. The bodega is a flat facade piece (`bodega.webp`) on its building; the shape-built storefront in the code is only a fallback if that image fails to load.
- **Sizes (meters, in `addNpc` / `Billboard`):** Kid 1.3 (smallest) < Luz 1.66 < Pancho's father 1.68 < Juan Carlos 1.72 < Pancho 1.75 < Eduardo 1.76 < Player 1.8 < Christopher 1.82 < Suits 1.85 < thugs 2.15 (tallest, and bulkier in the art).
- Christopher, Juan Carlos and Eduardo stand near the Tear for now (no role in the hunt yet).
- Approaching an NPC shows a line from the script. NPCs and Agency figures turn to face the player; none of them can catch you yet.

## Controls and camera (built 2026-10-22)
- **PC:** W A S D (or arrows) move, **mouse aims** (click the game once to capture the mouse, Esc frees it), **hold Left Click or Space = Low C**, Shift runs, E / Enter enters the Tear. Pressing any key on the title screen starts the game.
- **Phone:** floating left thumb stick (with a dead zone and a smooth ramp) moves, dragging on the right side looks (left/right turns, up/down tilts), and a round **LOW C** button on the right is held to use the power.
- **Camera:** it orbits behind the player, **zooms in when you turn toward the walls**, never leaves the street corridor (it slides along the wall and never sits inside the character), eases back behind you about 1.3 seconds after you let go of the look control, and the mouse tilts it up and down. Tested across 135 angle/position combinations: it never passed x = 7.5.
- **Low C** is the trigger: a 30-second meter (each copper wire adds 10), cyan ripples and a screen pulse while held, a 65 Hz tone (phones can't play 32.7 Hz), and it can overstrain ("waking hurts": locked out until the meter recovers to 30%, slower movement). It doesn't stall anything yet because the Agency doesn't chase you yet; the hook is `lowCActive` in `3d/index.html`.

## Long street: built (2026-10-22), step 1 of the hunt plan
- **Layout:** one ~310 m main street (Gaslamp start) with **4 cross streets** (z = -88, -145, -202, -259) that open into **two parallel alleys** (x = +-20), so you can loop around a block. All of it is a collision map of boxes (`walls` in `3d/index.html`); the player slides along buildings and cover, the camera is pulled in by a ray against the map (it stops in front of buildings and cover), and inside a cross street the camera swings to follow your heading.
- **Cover (placeholder boxes until the Gemini art arrives):** parked cars along the curbs, dumpsters, hedges, crates, concrete barriers, vendor carts with canopies. Stand still beside cover ~1 s and you're **HIDDEN** (shown in the HUD, the sprite fades). `hasLineOfSight()` already exists for the enemies to use.
- **Compass arrow** points to the Tear with the distance. HUD area label switches to **BARRIO LOGAN** past z = -185.
- **Pickups** re-spread for the long street: 14 cards (11 street + 3 in alleys), 8 scratchers, 4 glowing copper wire, 2 vinyl (rare, in alleys), 3 tapes, 4 fruit-basket traps. (Card set bonus is still at 8 cards.)
- **Performance:** the whole scene is ~58 draw calls and ~7.5k triangles (all boxes are one instanced mesh; lamps and palms are instanced).
- **Tested:** 37,800 random-walk samples across the map: 0 escapes from the walkable area; it reached the alleys and cross streets; never stuck on the way down the street.

## Round-2 art in the level (2026-10-22)
- **In:** 3 parked cars (lowrider, pickup, surf hatchback; front/side/back), dumpster, vendor cart, bus shelters, hedge, crates, concrete barrier, tires, rolled fence, old fridge + washer, sidewalk props (trash cans, mailbox, newspaper box, hydrant), 5 street signs, and storefront facades: **coffee** and **panaderia** (Gaslamp end), **taqueria** (middle), **BEAT BOX RECORDS** (Barrio Logan, right side near z = -232). All are billboards cut by `3d/art/make_sprites.py`; the placeholder boxes remain only as a fallback if an image fails to load.
- **Held back / still needed:** the **park bench** and **traffic cones** came out of Gemini with a smeared white band through the middle, so they are cut but not placed; regenerate them (and the mural wall and the stadium corner, images 11 and 12, which have not arrived).
- **Cutter notes:** `python 3d/art/make_sprites.py` re-cuts everything (~3 min); `python 3d/art/make_sprites.py alley sign` re-cuts only the named sheets. It removes thin ground lines under vehicles, can ignore a faint "ghost" row above a sheet (`crop_top`), and now splits items with a 1-2 px gap.
- **Performance:** ~45-200 draw calls depending on where you stand (props beyond 100 m are hidden, static shadows are one instanced mesh, clouds/skyline/hills/planters are instanced).

## Barrio Logan (decided 2026-10-22)
**Built:** a code-made **BARRIO LOGAN arch** over the main street at z = -186 (orange curved band with gold letters on both sides, two white towers with teal panels, a stepped crest), modeled on the real arch (the user's photo). The area label switches to BARRIO LOGAN past z = -185. A Gemini art version of the arch is an optional prompt (#14 in `ASSET_PROMPTS_2.md`).
The **far end of the street is Barrio Logan** and **the record store is there** (the user will provide a reference picture; it becomes a storefront like the bodega, plus the vinyl spots, the mural wall / bridge pillars and the Tear nearby). The Gaslamp end stays the start. Real-life note: Barrio Logan sits under the Coronado Bridge, which is already the bridge span in the skyline.

## Crew boons, empty start, low-rise Barrio Logan (2026-10-22)
- **You start with 0 Low C** and it no longer refills by itself. Until the Kid's stash is built, each baseball card gives +3 Low C and each copper wire +5 (placeholder for the Kid). Capacity = 32.7 x (2 with Christopher) x (1 + 15% per wire).
- **Find the crew** (hidden in the alleys, each with a tall glow marker over the rooftops; HUD shows CREW n/3): **Juan Carlos** (right alley, z = -133): 20 s of **invisibility** with a big countdown; he says "You're one of us now." Nobody can see, drain or grab you; heat can't rise. **Christopher** (left alley, z = -186): **doubles your Low C** (capacity x2; if you're empty you get at least 10). "It's not mine. It's ours." **Eduardo** (right alley, Barrio Logan, z = -246): **heat to zero**, thugs leave, chasing Suits go searching. "Hold the line."
- **Barrio Logan buildings** (past z = -185) are mostly **one story** (about 78%), a few **two-story** (14%) and **three-story** (8%) apartment buildings, with low back buildings; the record store is a taller landmark. The BARRIO LOGAN arch is taller than anything around it.

## Solid statics, narrower sight, Low C freeze, cloak glow, basket variants (2026-10-22)
- **Stationary things are solid shapes that never turn.** Parked cars, dumpsters, carts, shelters and the bread truck are built once from their front/side/back art (`buildHull`: the front view gives width at each height, the side view gives length, the shape that fits both is the body; the three views are wrapped on its faces). Single-view props stay one fixed panel. Only characters, enemies, the van and pickups still face the camera.
- **Enemy sight is short and narrow so you can slip around it:** Suit 8.5 m deep, about 7 m wide at full range (cone 0.42); thug 11 m (0.5); van beam 16 m (0.28). Heat >= WATCH only adds 12%, running 25%, Low C blasting 30%. Hidden still cuts it to 35%.
- **The Low C stops enemies in their tracks.** While it's on, any Suit/thug within 8.5 m (van within 12 m) freezes: no movement, no sight, suspicion drains, sprite tinted cyan and jittering. They resume when you let go.
- **Analog cloak** lasts 30 s per tape (stacks to 60 s, countdown in the HUD). While cloaked you're 50% see-through, tinted cyan, with a pulsing cyan glow (36% opacity and the same glow while invisible).
- **Fruit baskets come in two kinds** (2 of each): bugged ones (blinking red LED, +1 heat, "IT WAS BUGGED!") and gifts (LED painted out, green glow, **+20% move speed for 60 s**, HUD line "SPEED +20% Ns").

## Items diversified, the Kid, more Suits, moving cast, bread truck (2026-10-22)
- **Baseball cards do nothing by themselves.** You carry them (HUD: "CARDS FOR THE KID: n", with an arrow and distance to him) and hand them to **the Kid**; **7 cards = a full Low C** (he only takes as many as you need). Copper wire no longer adds Low C either (it still grows the tank and speeds the Suits).
- **Scratchers** now just lower heat by 1.5 (and calm chasing Suits if that drops you under CULTIVATE). No points. Only 3 on the street.
- **Records** (2 in the alleys): **EGO BLAST EQUIPPED** for 18 s: red screen edge, HUD countdown, every enemy and the van at 30% speed.
- **7 Suits**, spread down the street: solos at z -48, -168, -270 and **pairs** at about -102 and -218. The second of a pair follows the first on patrol; when one notices you the other is alerted.
- **The cast walks around**: Pancho, his father, Luz and the Kid have routes (the Kid runs bodega <-> record store, with long stops at each); they stop to talk when you get close. The crew walk from their alleys out to the sidewalk of the nearest cross street now and then, so Juan Carlos can actually be seen from the main street.
- **Crew boons repeat**: every meeting pays out again (40 s cooldown; the tall beam shows only when they're ready). Juan Carlos = 20 s invisible, Christopher = doubles your current Low C (capacity stays x2), Eduardo = heat to zero.
- **Bread truck**: parked parallel at the right curb like the cars (lettering readable from the street), faint warm glow. It **drives or backs to a new curb spot every 30-70 s** (never with you inside; the colliders move with it). **Stand still next to it for about a second to hide inside**: enemies can't see, drain or grab you; move to climb out.

## Phone controls, Tear timer, deliveries, baskets, ego blast v2 (2026-10-23)
- **Two-thumb phone controls** (the old scheme made the right thumb choose between looking and LOW C): left thumb = floating stick (push to the rim = run); right thumb = big LOW C button (hold, or a quick tap **latches** it on and another tap turns it off, so the thumb is free) and an **EGO BLAST** button above it when you have one. Free-look only works as a drag in the upper right; the camera recentres after 0.5 s on touch, so you never have to look. Pointer capture on the buttons; a second touch on the left half can no longer become a look drag.
- **Camera**: pitch capped lower (0.08-0.32, was 0.1-0.46), phone camera distance 6.6 (was 7.4), and the building check now casts three rays (centre and +-0.7 m at the lens) and stays 0.75 m off the wall, so corners don't slice the picture. **Corner assist**: walking straight into a car or cart front slides you around the nearer open side instead of stopping dead (the "forced in a direction / can't go down the block" report: every x across the street near the bodega now gets through in a head-on test).
- **Deliveries**: cards -> the Kid (7 = full), **copper wire -> Pancho (3 = full)**; both respawn somewhere else on the street after you hand them in. A standing goals panel (right side) shows each target, how many you hold, and an arrow + distance; it adds HEAT HIGH -> FIND EDUARDO at CULTIVATE+ and the Tear countdown. Wire no longer grows the tank (it still makes the Suits faster).
- **Who roams**: Pancho goes between the bodega and wherever a crew member is, 40 s at each; the Kid goes bodega <-> Barrio Logan, 40 s at each end; Juan Carlos, Christopher and Eduardo roam the whole lane map. Father and Luz still walk short routes.
- **The Tear** is closed until your Low C hits 100%, then opens for max(25, distance/7.2 x 1.25 + 10) s (about 60 s from the start of the street). It stays open even if you spend your Low C; when it closes it can reopen (8 s later) once you're full again.
- **Baskets** all look the same (the bug LED is painted out); 40% are bugged: +1 heat and every Suit homes in on you for 15 s ("TRACKED"). The rest give +60% Low C. The speed reward is gone.
- **Analog tape** = ANALOG STATIC for 30 s: enemies glitch, can't hold a stare, and see only about 1.6 m. No more see-through player (Juan Carlos's invisibility stays).
- **Ego blast** (records, up to 2 stored): a button / F key; for 12 s every enemy and the van **freezes and sees nothing** (red tint, red screen edge). **Low C opening pulse** knocks enemies within 12 m back for a second (2.5 s cooldown), then the freeze-while-held works as before.
- **Luz = the hum**: meet her (40 s cooldown, same as the crew) for 20 s of seeing every Suit, thug and the van through walls (cyan diamonds), and every basket glows **red if bugged, green if real** (each basket's bug is now decided once per run instead of at pickup).
- **Pancho's dad = power up**: stand still within about 3 m and he charges your Low C from empty to full in 4 s, but your heat rises 0.4 a second the whole time (about +1.6 for a full charge) and it can't cool while you do it, so time it for when nobody's near. Moving off stops it. A "POWER UP" reminder shows in the goals panel when you're under 60%.
- **The camera follows your heading**: push back toward it (S / stick down) and the view swings around behind you (about 1 s for a half turn). The stick keeps its old meaning until you let go or flip it, so there's no lurch mid-turn (S then W without releasing keeps going the same way). Idle recentering now settles onto whichever way the street runs that you're already facing, instead of snapping back to the old direction.
- **Camera is quicker and follows sideways turns too**: pushing back or sideways (more than about 55 degrees off straight ahead) swings the view round behind the new heading, about 0.25 s for most of the turn (it was about 0.7 s and back-only). Cross-street recentering is faster too.
- **Camera stays behind the heading (revised)**: it now follows any turn of more than about 15 degrees, not just sideways and back, and it follows where you're *trying* to go (the stick), so a wall in a tight spot doesn't leave it on a side view; it still pulls in tight against walls. Standing still, it settles in behind whichever way the character faces instead of onto the street axis. Forward-again unlocks the stick once the view has caught up (W+D then letting go of D keeps the same heading).
- **Phone controls v3 (portrait stays the target: it matches the 2D game and Instagram)**: the whole lower-right of the screen is the LOW C thumb (hold, or tap to latch), so there's no circle to miss; the visible button is only a hint and sits about 15% up from the bottom edge (clear of the OS swipe zone); EGO BLAST is up and to the left of it. A faint dashed ghost stick shows where the left thumb goes and vanishes once you touch (the real stick still appears under the thumb). **No look-drag on touch any more** (the camera follows your heading); mouse drag-look is unchanged. Phone vertical field of view 80 degrees (was 74) for a wider side view.
- **Turning no longer zooms**: the old zoom-in whenever the view was sideways made turns feel jumpy. Camera distance is now steady (6.6 phone / 6.0 wide); only a wall in the way pulls it in.
- **Reminders slimmed down**: the right-side panel is now single boxless lines (CARDS▸KID 2 ↑64m, WIRE▸PANCHO 0 ←42m; POWER▸DAD under 40% Low C, HEAT▸EDUARDO at CULTIVATE+, TEAR 49s when open), dimmed when you hold nothing. The compass is gone (the Tear line replaces it). Luz has no line: the power bar over her head shows when she's ready.
- **Tutorial**: (1) the start screen has a one-screen how-to-play card (move / hold LOW C, 7 cards -> Kid, 3 wires -> Pancho, 100% opens the Tear, find Eduardo for heat) using the item and character sprites. (2) **First-contact tips**: the first time you come within a few meters of each item, character or enemy (21 of them: the six items, Kid, Pancho, his dad, Luz, the three crew, Suit, thug, van, truck, plus heat, Low C and the Tear), one short titled line appears for about 5 s, one at a time, queued. They're remembered in the browser (localStorage `layers3d_tips_v1`) so they never repeat; add `?tips` to the address to see them all again. While heat is CULTIVATE or higher only the enemy, heat and Tear tips are shown. The copy lives in the `TIPS` table in `3d/index.html`.
- **Links**: the Void Runner button and start-screen link now point to theinvisiblepanchos.com (new tab); the 2D game is reached through the Tear. The "3D not available" fallback screen still links to the 2D game.
- **Controls reset for precision (2026-10-23)**: the camera no longer swings on its own while you walk (that, plus an idle-recenter bug that kept turning the view while you held a diagonal, is what made left and right feel loose). The stick is always relative to the camera. Two camera behaviours remain: (1) **hold the stick back toward the camera for 0.2 s** and the view spins round behind you (the stick keeps meaning the way you were going until you let go or push forward); (2) **a small lean**: pushing left or right tilts the camera up to about 20 degrees that way so you can see round corners, without changing which way the stick points. Idle recentering (behind the way the character faces) only happens when you're standing still.
- **Stick**: radius 62 px (was 50), dead zone 0.08 (was 0.12); **run only when you drag well past the rim** (1.35 times the radius, so it can't trigger by accident); the left-stick zone is the left 56% of the screen and the LOW C zone the right 44%, so a left thumb near the middle can't fire LOW C.
- **8 Suits** (was 7): added a roamer with a long beat (z -40 to -270).
- **Corridor camera, true facing, diagonal tilt (2026-10-23)**: (1) the camera turns on its own at one moment only: when you head along the street, an alley (z) or a cross street (x) and the view isn't already looking that way (entering a corridor, or turning round to go back); it snaps there fast (about 0.3 s) and the stick keeps its old meaning until you let go, flip it or push forward. Strafing across the street never turns it; left/right only lean it. Standing still, the view settles square to the corridor (never off a wall-slide). (2) He faces the way he really moves (sliding along a wall he faces along it); if a corner-assist side-step would swing him more than 80 degrees off what the stick says, he keeps facing the stick. (3) The flat front/back sprites tilt up to ~30 degrees toward their heading so a diagonal walk reads as diagonal (`TILT_B`/`TILT_F`, applies to every character). The next step if that isn't enough: new back-left/back-right art for the astronaut.
- **The gun (2026-10-23)**: **Pancho now gives AMMO, not Low C**: each copper wire = 8 rounds, 24 max (3 wires), he only takes what fits. Once you have ammo a **new circle appears on the right** that swaps the main thumb between **GUN** and **LOW C** (the big button/zone becomes FIRE, orange); PC: **R** swaps, Space/left click fires. Auto-aim: nearest **Suit or thug** within 18 m in clear line of fire (low cover doesn't stop a bullet; the **van is never a target**); 3.5 shots/s; no target = no shot and no ammo spent. **Suit = 2 hits, thug = 5.** Each shot adds a little heat and is heard (Suits within 22 m go to investigate); out of ammo drops you back to Low C. A kill is worth +500 (Suit) / +800 (thug) carried points. **A killed Suit returns at its post after 45 s**, and only when you're more than 40 m away. Low C works exactly as before (the cards -> Kid and dad/basket Low C routes are untouched).
- **VOID IS CLOSING!**: while the Tear is open a red bar runs across the very top of the screen with the countdown (it blinks under 10 s, and the HUD shifts down to make room), the **sky turns from blue to a bruised red**, and the fog and street light go red with it; it fades back when the Tear closes.
- **Quieter dialogue**: the speech box is now a slim, translucent one-liner near the bottom (name inline), not a boxed panel in the middle of the screen. **The PC start screen fits with no scrolling** (checked at 1024x768 and 1366x600): a two-column how-to-play card and tighter spacing on wide screens; on a short window it scrolls from the top instead of clipping the title.
- **More copper, hotter kills, a real hiding rule, a heavier gun (2026-10-23)**: 16 copper wires on the map (was 4: street, sidewalks and all four alleys), and the Suits' speed-up now follows the copper you're **carrying** (capped at 6), not every wire ever picked up. **Each kill adds more heat than the last** (0.25, 0.35, 0.45 ... capped at +1.0 per kill, plus a little per shot); the count fades by one every 50 s you lie low and resets on a restart. **You can only hide (bread truck, or crouching behind cover) when no enemy has eyes on you and you haven't been bugged**; try it while watched and you get "THEY CAN SEE YOU / YOU'RE BUGGED: YOU CAN'T HIDE". **Gun feel**: a fat hot bolt instead of a hairline, a muzzle flash, hit sparks, a red flash and a one-step knockback on every hit, screen shake (bigger on a kill), a bigger blast on a kill, and a much louder layered shot sound.
- **Music: the Memories of Home album plays in the 3D game (2026-10-23)**: only the new album plays here (the 2D game keeps its own playlist at the repo root). Files live in `3d/music/` as 12 web MP3s (VBR about 145 kbps, 43 MB total), re-encoded with ffmpeg (`libmp3lame -q:a 4`) from the masters in `P:\INVISIBLE PANCHOS MAIN\MEMORIES OF HOME\memories masters` (the 256 kbps originals are about 74 MB for the same 12; the older drafts in that folder's `pre` subfolder and the older Sep-16 THE REIGN were not used). Playback: the album plays shuffled (and loops) from the tap on TAP TO START (phones need that tap), advances on its own, and a small "now playing" line shows for 6 s at each track. It's quieter than the effects and ducks further under the Low C, the gun and the ego blast. The SND button mutes and pauses it; leaving the tab pauses it; a blocked autoplay retries on the next tap. The built-in synth bed only plays if the files can't. **To add a track**: encode it into `3d/music/` and add a `['TITLE', 'file-stem']` row to `ALBUM` in `3d/index.html`.
- **Rework round (2026-10-23, late)**: **Music player** now matches the 2D game: small skip and speaker icons in the top-right (SND text button gone). **Names** sit over every power bar (Juan Carlos, Christopher, Eduardo, Luz), the width of the bar. **You choose every shot**: no latching, no auto-fire. The gun aims for you but fires one round per tap or click; **Low C is on only while you hold it** and now **burns 1.8 per second** (about 18 s from a full tank), adds **no heat**, doesn't widen what enemies can see, and **dispels the bad vibes** (a Suit next to you can't drain it while it's on). **Scroll wheel** (or R, or 1/2) cycles the weapons you have. **The seal**: when the Tear opens an Agency seal (red, wall to wall) blocks it at z -281; it takes **10 hits** from the gun (about 10 of your 24 rounds, shot noise included), then you can walk in; it reforms every time the Tear reopens. **The van** unloads thugs if you stay in its beam for 4 s (a warning shows at 1.5 s). **Heat only brings more**: at CULTIVATE+ up to 4 extra Suits spawn out of sight (they leave when it cools) and 1 thug (3 at CONTAIN); **thugs no longer know where you are**: they go to the last place something saw you, then sweep nearby, unless you're bugged (then they come straight for you). Hiding works at any heat as long as nobody has eyes on you and you aren't bugged. **Everyone you walk up to** (the crew, Luz, Pancho, the Kid, his dad) stops and turns to face you within about 4.5 m.
- **Low C pulse sends them the other way**: on switching it on, every enemy within 16 m runs directly away for 1.6 s at 11 m/s (about 17 m; Suits then search), with a cyan shockwave ring so you can see it; holding it still freezes anything that comes back within 8.5 m. 2.5 s between pulses.
- **Power bars** float over each crew member and Luz: they fill over the 40 s recharge and turn green when they can give their reward again. **Always-on markers**: red arrow over the Kid, gold over Pancho, blue over his dad, visible from anywhere on the street (they grow with distance).
- **The van** is a solid shape like the parked cars, so it no longer swivels as you pass it. The bread truck only hides you from the street side.

## The hunt: built (2026-10-22), step 2 of the plan
- **Heat** (0-3, shown as a bar and a name in the HUD): rises while any Suit or the van can see you (faster when they're close, when you run, or when you use the Low C in sight), cools off 2 s after you break line of sight (3x faster when hidden). Levels: CLEAR / WATCH / CULTIVATE / CONTAIN. Baskets add one level. Constants and speeds are at the top of the `// ---- the hunt` block in `3d/index.html`.
- **Suits (3 on patrol, each with a zone):** patrol -> notice you -> INVESTIGATE (at WATCH) or CHASE (at CULTIVATE+) -> SEARCH -> back to patrol. Sight is a cone plus line of sight (buildings and cover block it; hidden = 35% range; running +35%; analog cloak = almost blind). Ground cones show what each one can see (white = calm, orange = suspicious, red = chasing). `?` and `!` marks float over their heads. Speed rises 12% per copper wire carried. They path around the map using a small lane graph (main street, cross streets, alleys) with sidestep when blocked, and give up only after ~32 s on a cold trail.
- **The van** drives the main street with a headlight cone, turns around at the ends, and at CONTAIN stops and unloads 2 thugs (max 3, 16 s apart).
- **Thugs:** fast, always hunting; each hit takes 8 Low C and shoves you; they leave after heat stays under CULTIVATE for 8 s.
- **Damage/capture:** a Suit that has noticed you (or is within ~3 m) drains Low C as "bad vibes" (pink screen edge). At 0 Low C, a Suit's touch or a thug's hit captures you: **STATUS: NULL** screen, loot lost, street reset (this stands in for "thrown back into the void"). Low C now holds 32.7 and only trickles back (0.35/s) until the Kid exists.
- **Stationary things never turn.** Parked cars, dumpsters, carts, bus shelters and the bread truck are boxes of fixed panels (front/back/both flanks, each with its own art); props, signs and hedges are one fixed panel. Only characters, enemies and the van turn toward you.
- **Tested:** Suits notice and chase, walls block sight and heat cools, capture needs an empty Low C, restart resets everything, chases reach players in both alleys, and a 4-minute random-walk soak had no crashes or bad numbers. **Not built yet:** the Low C cone's damage to enemies, the Kid's stash/refill, scratcher bribes, records, and the handoff to the 2D game.

## Hunt rules v2 (decided with the user 2026-10-22; tuning numbers are first guesses to playtest; NOT built yet)
**Low C is your weapon and your health.** Capacity **32.7** units ("seconds" at the lore's slow rate). Blasting burns it ~3x faster, so a full bar is about 11 seconds of blast. It does not come back by itself (only a trickle); the Kid refills it.
- **Zero charge:** if an enemy touches you at 0 -> caught (STATUS: NULL). At 0 with no enemy touching you, you are only weak and slow ("waking hurts"). A Suit's aura alone never ends the run.
- **Blast:** a **directional cone** (~60-70 deg, ~9 m) drawn as the cyan **ripple arcs** you liked, moving outward where you aim (mouse on PC; character facing + auto-aim on phone). It damages enemies' **stability**: they glitch (static, jitter, cyan sparks), slow down, then are stunned when stability hits 0. Cover blocks the cone.

| Enemy | Behavior | Damage to you | Blast |
|---|---|---|---|
| **Suit** | Always on patrol. Speed rises with copper wire carried (+12% per wire). | **Bad vibes:** aura drain ~1.5/s within ~5 m | stability ~2 -> stunned after ~5 s of blast |
| **Thug** | Only appears at high heat (unloaded by vans). Faster than a Suit. | **Big chunks:** ~8 per hit, 1.2 s apart, with knockback | resists: slowed in the cone, stunned only after ~8 s of blast |
| **Van** | Drives a patrol loop with a headlight cone; at CONTAIN it unloads 2 thugs (max 3 at once). | none directly | stalled while in the blast |

**Heat:** CLEAR -> WATCH (Suits alerted) -> CULTIVATE (Suits chase) -> CONTAIN (vans unload thugs). Goes up when seen, running in sight, blasting in sight, grabbing loot in sight. Goes down out of sight, faster when hidden behind cover, and by 1 level when you pay off enemies with a scratcher. Heat also creeps up if you stay in one place too long.
**Cover/hiding:** cars, dumpsters, carts, hedges, walls block sight and the cone. Stand still behind cover ~1 s to be "hidden". Running is noisy (bigger detection radius); a gentle thumb push is a quiet sneak.

**Items**
- **Baseball cards:** more of them, spread out; some sit where a patrol guards them and can only be grabbed once it moves on (no booby-trapped cards). Give them to **the Kid**. He holds a **stash**; you refill Low C by standing near him (it draws from his stash). **Enemies can steal his cards** (1 card per ~2 s while a Suit is on him); stun the thief and the card drops. You defend him. Keeping cards for the full-set bonus vs. giving them to him is the tension.
- **Scratchers:** no points. Use one to **pay off** nearby enemies (they ignore you ~30 s) and drop heat one level. Unused ones convert to +150 each at the Tear.
- **Records (rare):** hold at most 1; press a button for the **red blast**: all enemies in slow motion (x0.3) for ~15-20 s, with a red wash and red rings. **Regeneration:** only one record exists on the map at a time; ~75 s (+-15) after one is picked up, a new one appears at a random one of ~8 record spots (stoops, windows, alley mouths, the record store), never the same spot twice in a row, with a faint red glow and a "scratch" sound when it appears. Cap 4 per run.
- **Copper wire:** now **glows** (a brighter beacon). Each wire: Low C capacity +15%, but Suits move +12% faster.

## Level layout (DECIDED: long street)
The user chose the long street over a full grid. The Kid is not fixed: he **moves occasionally** between the bodega, the record store and random spots down the street (only when no enemy is near; the walk takes ~20 s and is when he's most exposed; his stash goes with him; show an arrow to him when Low C is low). Wire trade-off (+15% capacity, Suits +12% faster) confirmed fair.

Original recommendation, kept for reference ("spine + ribs"):
One long main street (~2x today's length) with 4 cross streets / alleys (the ribs) every ~50-60 m, parked cars and props along the curbs, and alley loops that let you circle enemies. Cheaper than a full 3x3 grid, but gives real hiding spots and flanking. It needs the same new tech either way: a collision map (building boxes), camera collision against it, line-of-sight checks, and patrol paths. It can grow into a full grid later.

**More Gemini art needed:** parked cars (3 views each), street props (dumpster, trash cans, mailbox, hydrant, bench, bus shelter), vendor cart / crates / hedge planter / barriers, 4 more storefronts (record store, taqueria, barber, laundromat), a mural-wall landmark (original art, not a copy of real murals) and a baseball-stadium corner with a generic baseball statue (no real player's likeness).

## Flow
1. **2D game:** the rare Tear-portal drifts through the blue-sky section. Fly in.
2. **3D, "Earth":** land on a San Diego street (home: 32.72° N, "DAYGO"). Goal: find and reach the **exit Tear** while the Agency hunts you.
3. **Escape:** exit Tear -> back to the 2D run, with the loot you carried as bonus points, and a brief "P1. Out." sign-off.
4. **Captured:** thrown straight back into the 2D void as **STATUS: NULL** — carried 3D bonuses lost, plus a score penalty (size TBD).

Handoff is a small saved object passed between the two pages (score, dimension, power-ups, song). A missing/broken handoff just starts a normal 2D run.

## The hunt = the Agency's three files
Heat meter with three levels, named exactly like the lore:
- **WATCH** — black vans idle and patrol ("protection detail"). Stay out of headlight cones.
- **CULTIVATE** — the Suits come on foot: friendly, polite, try to "check on you" (the welfare check). Get close and they grab you.
- **CONTAIN** — thugs and chasing vans. Fast, loud, lethal to a run.
Heat rises when you're seen, run in the open, use digital things, or grab loot in view. It falls when you break line of sight or hide in analog zones.

## Player abilities
- **Hold the Low C (32.7 Hz):** hold a button to stall everything digital nearby — van headlights stutter, dashboards die, locks pop (Ch. 8 convoy scene). It has a short meter (lore: ~30 seconds alone, ~90 with two minds). Using it has a cost: "waking hurts" — screen strain, slow recovery.
  - Phones can't actually reproduce 32.7 Hz (the Lore Book says so), so use visuals (ripples, shaking water/glass), haptics where available, and a higher harmonic for the sound.
- **Analog beats digital:** copper-mesh spots (the bodega back room, the record store) hide you completely. Phones/cameras/digital signs raise heat.
- **Sprint/hide:** alleys, dumpsters, ducking behind palms. Mobile: auto-hide when you stop in cover.

## Possible later use of collectibles
- Gwynn cards could thin "the cover" so the exit Tear only shows through once you've collected enough (lore: when the material runs low, the Tear shows through). Cards could also be spent with Pancho for hints ("foil hats are half off").
- Optionally bank loot at safe houses (bodega / record store) so a capture doesn't cost everything.

## Characters and what they do
| Character | Role in the level |
|---|---|
| **Pancho** (Frank Edison) | Bodega = main safe house and bank point. Sells hints ("foil hats are half off") for cards. |
| **Pancho's father (H-3)** | Appears near the bodega; a distraction or helper ("Right here, son"). |
| **Luz** ("light") | Guide: a light that shows the way to safe houses / the Tear. |
| **Juan Carlos** | Voice on an analog speaker/radio: hints, and the second mind that doubles Low C time. |
| **The Kid** | Runs around with a stack of cards; chase/pickup side-challenge ("I watch greatness, kid"). |
| **The Suits / Agency thugs / The Voice** | The hunters; The Voice announces heat changes over speakers ("Not authorized"). |
| **Eduardo** | Only heard: "P1. Out." when you escape. |

## Map ideas (real San Diego, our layer)
Gaslamp street (the current prototype) -> Barrio Logan / Chicano Park under the Coronado Bridge -> Petco Park and the Tony Gwynn statue -> Panchos Bodega and the record store as the two safe houses. The exit Tear sits near the bridge.

## Technical constraints (mobile first)
- Vans = boxes with emissive headlights; patrols on waypoints; sight = cone test, not raycasts. Suits = capsules like the player.
- Keep draw calls low; instance the collectibles and windows. Quality tiers and fallback stay as in the prototype.
- No fail state in the first minute (tutorial grace) so first-timers aren't wiped immediately.

## Build order
1. More street + a patrolling van with a headlight cone and a heat meter (prove the hunt works on a phone).
2. Low C ability and one collectible type; capture -> `NULL` return screen (local stub).
3. Bodega safe house + Pancho; Gwynn cards.
4. Handoff to/from the 2D game behind a test flag; then add the Tear to the live 2D game.

## Open questions
- Tear trigger in 2D (after a boss?).
- Capture penalty size (lose carried loot only vs. also a % of score vs. a life).
- Carry-until-exit vs. bank at safe houses (suggest: both).
- Player identity: a new astronaut ("You", flagged CULTIVATE) vs. Christopher.
