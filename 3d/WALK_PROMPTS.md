# Player walk-cycle prompts for Gemini (Nano Banana), 2026-10-27

Goal: replace the player's three still views with a real walk cycle. Do the **BACK view first** (the camera sits behind you, so it is what players see 90% of the time), then SIDE, then FRONT.

## How to use
1. Upload the matching current sprite as the reference image: `3d/art/sprites/player_back.webp` (then `player_side.webp`, `player_front.webp`). If Gemini will not take .webp, open it and save a PNG first.
2. Paste the prompt below for that view. Generate several, keep the one where all 4 figures are clearly the SAME character at the SAME size.
3. If one frame is off, ask: "Redo only figure 3, keep everything else identical."
4. Save the sheets in `3d/art/_originals/` as `player_walk_back.png`, `player_walk_side.png`, `player_walk_front.png`. I will cut them into frames (same pipeline as the current sprites).

## Shared rules (already inside the prompts)
- 4 figures in one row, left to right = the 4 phases of a walk: contact (left foot forward), passing, contact (right foot forward), passing.
- Same character, same costume, same proportions, same camera, same scale in every figure.
- Feet of all four figures sit on one invisible horizontal line. Equal gaps; no figure overlaps or touches another.
- Plain flat light-gray background, no shadows, no ground, no motion lines, nothing cropped.

## BACK view (do this first)
```
Same character as the reference image: the young astronaut in the worn cream-and-orange flight suit with
the tan backpack, blue shoulder pads and olive boots. Keep the exact same style: stylized low-poly 3D game
character, clean flat-shaded shapes with soft color gradients, warm earth tones, daylight look, not photorealistic.

Make a WALK CYCLE SHEET seen from BEHIND (back view, camera directly behind him): four full-body figures in one
row, left to right, the four phases of a natural walking step:
1) contact pose: left foot stepping forward, right heel lifting, right arm swinging forward, left arm back, shoulders slightly twisted
2) passing pose: legs together under the body, body at its lowest point, arms hanging beside the body
3) contact pose: right foot stepping forward, left heel lifting, left arm swinging forward, right arm back
4) passing pose: the same as 2, but body at its highest point, slight lift on the back foot

Keep the figures the same height and scale, feet on one shared horizontal line, equal spacing, nothing
overlapping, nothing cropped. Subtle weight shift and a little head bob, a relaxed confident walk, not a march.
Plain flat light-gray background, flat even lighting, no cast shadows, no ground, no motion lines, no text.
```

## SIDE view (facing right, as in the reference)
```
Same character as the reference image (young astronaut, cream-and-orange flight suit, tan backpack, olive boots),
same stylized low-poly game-character style and earth-tone palette as the reference.

Make a WALK CYCLE SHEET in SIDE VIEW, character facing RIGHT, exactly like the reference's facing: four full-body
figures in one row, left to right, the four phases of a natural walk:
1) contact: front (right-side) foot reaching forward heel-first, back foot behind on its toes, near arm swinging back, far arm forward
2) passing: back leg swinging through next to the standing leg, knee bent, body at its lowest
3) contact: the opposite foot forward, arms swapped
4) passing: the other leg swinging through, body at its highest

Same height and scale in every figure, feet on one shared horizontal line, equal spacing, no overlap, nothing cropped.
Plain flat light-gray background, flat even lighting, no cast shadows, no ground, no motion lines, no text.
```

## FRONT view
```
Same character as the reference image (young astronaut, cream-and-orange flight suit, tan backpack, olive boots),
same stylized low-poly game-character style and earth-tone palette.

Make a WALK CYCLE SHEET seen from the FRONT (character walking toward the camera): four full-body figures in one
row, left to right: 1) left foot stepping toward camera, right arm forward; 2) passing, legs together, body lowest;
3) right foot stepping toward camera, left arm forward; 4) passing, body highest.
Same height and scale in every figure, feet on one shared horizontal line, equal spacing, no overlap, nothing cropped.
Plain flat light-gray background, flat even lighting, no cast shadows, no ground, no motion lines, no text.
```

## Optional action poses (later, after the walk looks good)
- **Low C cast**: arms thrust out in front, braced stance, back view and front view.
- **Run**: same 4-phase layout but a forward lean, longer stride, arms bent at 90 degrees, both feet briefly off the ground in phases 2 and 4.
- **Hurt / caught**: one frame each, flinching back, then arms raised.

## Tips
- Gemini drifts the costume across frames. If the colors or backpack change, say: "The backpack is a tan rectangular pack with two blue panels and an orange hose; do not change it."
- If the figures come out different sizes, ask for "all four figures exactly the same height as the first figure".
- Ask for 4096 px wide output if available; the frames get shrunk to about 300 px tall for the game.
