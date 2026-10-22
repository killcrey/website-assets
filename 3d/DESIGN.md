# LAYERS: San Diego — design notes (3D section)

Source material: *Memories of Home* script V1 and the Lore Book (Audience Edition). Status: proposal, not built.
The Lore Book's last page already describes this section: "The anomaly takes you back to Earth, unlocks a sample from Memories of Home, then sends you back into the void."

## Art direction (decided 2026-10-22)
Earth, not space. The 2D game is dark neon void; the 3D section is **daytime San Diego**: blue sky, sun, terracotta / adobe / cream / sage stucco, tan sidewalks, green palms, painted shop signs, ink-brown outlines. Neon is reserved for the one surreal thing: **the Tear** (a dark geometric rip with a cyan-white glow) — it should pop against the warm world. Agency vehicles and Suits are matte black/charcoal so they read instantly against the earth tones. The prototype is already re-themed this way. Character prompts for Nano Banana are in `CHARACTER_PROMPTS.md`.

## Flow
1. **2D game:** a rare **Tear** opens in the void (trigger TBD — suggested: after a boss). Fly in.
2. **3D, "Earth":** land on a San Diego street (home: 32.72° N, "DAYGO"). Goal: find and reach the **exit Tear** while the Agency hunts you.
3. **Escape:** exit Tear -> back to the 2D run, with bonuses, any unlocked Memories of Home sample, and a brief "P1. Out." sign-off.
4. **Captured:** thrown straight back into the 2D void as **STATUS: NULL** — carried 3D bonuses lost, plus a score penalty (size TBD), no unlock.

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

## Collectibles (carried until you exit; optionally bank at safe houses)
- **Tony Gwynn cards** — 8 of them (eight batting titles). Complete the set = big bonus.
- **Scratchers**, **copper wire**, **vinyl / reel-to-reel tape** (these carry the Memories of Home sample unlocks), **thermos** (Domingo's: stamina/heat relief).
- **Fruit basket** — looks like a gift pickup, actually bugged. Taking it spikes heat (lore trap).
- Collecting thins "the cover" -> the exit Tear becomes visible (lore: when the material runs low, the Tear shows through).

## Characters and what they do
| Character | Role in the level |
|---|---|
| **Pancho** (Frank Edison) | Bodega = main safe house and bank point. Sells hints ("foil hats are half off") for cards. |
| **Pancho's father (H-3)** | Appears near the bodega; a distraction or helper ("Right here, son"). |
| **Domingo** | Record store safe house, almost silent; gives the thermos, turns the tape off. |
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
