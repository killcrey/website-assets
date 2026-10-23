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
