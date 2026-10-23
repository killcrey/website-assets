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
