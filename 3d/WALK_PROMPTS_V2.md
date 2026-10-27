# Player walk cycle, round 2: prompts that force the legs to swing

Use this instead of `WALK_PROMPTS.md`. Same four-figure sheet idea, but each prompt now comes with a **pose guide image** and exact leg angles.

## What went wrong in the first sheets (so we do not repeat it)
Checked against `PLAYER_WALK__BACK / SIDE / FRONT`:
- **Back and front:** the legs stay as two straight columns with the feet side by side. From directly behind (or in front) a real stride only shows up if the camera is a little **above** the character: the foot stepping away from you sits **higher** on the screen, the trailing foot sits **lower** with the heel lifted, and the stepping thigh looks **shorter** (it points away from the camera). With a flat, level camera the stride is invisible, and Gemini drew the legs standing still with a bit of side-splay. The arms swung sideways instead of forward and back.
- **Side:** the stride is tiny. The thighs barely rotate at the hip, the knees stay almost straight, the "passing" frames have no clearly bent knee and no foot lifted off the ground, and the arms barely swing. It reads as a shuffle.
- The prompt only said "left foot stepping forward". That describes nothing Gemini can measure. This version gives angles and a drawn guide.

## Files you upload with each prompt
| View | Upload 1 (the character) | Upload 2 (the pose guide) |
|---|---|---|
| Back | `3d/art/sprites/player_back.webp` (save as PNG first if Gemini refuses .webp) | `3d/art/pose_guides/walk_guide_back.png` |
| Side | `3d/art/sprites/player_side.webp` | `3d/art/pose_guides/walk_guide_side.png` |
| Front | `3d/art/sprites/player_front.webp` | `3d/art/pose_guides/walk_guide_front.png` |

The guide shows the four phases as stick figures. **Red = right limbs, blue = left limbs.** It is a pose reference only.

## Do the BACK view first, then SIDE, then FRONT

### BACK view (camera behind and about 25 degrees above)
```
You have two reference images. Image 1 is the CHARACTER (young astronaut: cream-and-orange flight suit, tan
rectangular backpack with blue panels and an orange hose, blue shoulder pads, olive boots). Image 2 is a POSE GUIDE
of stick figures: copy ONLY the leg and arm positions from it, never its drawing style.

Draw a 4-frame WALK CYCLE SHEET of the character from BEHIND, with the camera directly behind him and about 25 degrees
ABOVE, looking slightly down at his back. Four full-body figures in one row, left to right, matching the four stick
figures of image 2 exactly. The character is walking AWAY from the camera.

Leg rules (this is the whole point, do not skip it):
Frame 1, CONTACT: his RIGHT foot has stepped forward (away from the camera), so the right boot sits HIGHER on the
screen than the left boot and its thigh looks SHORTER (foreshortened). His LEFT leg is trailing behind: the left
heel is lifted off the ground so the SOLE of the left boot is visible to the camera, and the left boot sits LOWER on
the screen. The two feet must be at clearly different heights in the picture, about one boot-length apart.
Frame 2, PASSING: right leg straight and planted, left knee bent about 70 degrees, left foot lifted off the ground
and swinging forward past the right leg, so the left boot is clearly OFF the floor and higher than the right boot's
sole. Body at its lowest.
Frame 3, CONTACT: the mirror of frame 1: LEFT foot forward and higher on the screen, RIGHT foot trailing with the heel
up and the sole visible.
Frame 4, PASSING: the mirror of frame 2: left leg planted, right knee bent about 70 degrees, right foot lifted.
Arms swing FORWARD AND BACK (not sideways) and always opposite to the legs: when the right foot is forward, the left
hand is forward (it looks higher and slightly smaller) and the right hand is back (lower and slightly bigger).
Shoulders twist a few degrees with the step; the head stays level.

Frames 1 and 3 must look clearly different from each other, and frames 1 and 2 must look clearly different. If any
two frames look the same, you have not done it right.
Keep the exact costume, colors, proportions and low-poly game-character style of image 1 in every frame, all four
figures the same size, the planted foot of each figure on one shared horizontal line, equal spacing, nothing overlapping,
nothing cropped. Plain flat light-gray background, flat even lighting, no cast shadows, no ground, no motion lines, no text.
```

### SIDE view (facing right)
```
You have two reference images. Image 1 is the CHARACTER (young astronaut, cream-and-orange flight suit, tan backpack,
olive boots), facing RIGHT. Image 2 is a POSE GUIDE of stick figures: copy ONLY the leg and arm angles from it, never
its drawing style.

Draw a 4-frame WALK CYCLE SHEET in pure SIDE VIEW (level camera), the character facing RIGHT, four full-body figures in
one row, left to right, matching the four stick figures of image 2 exactly.

Leg rules (do not skip):
Frame 1, CONTACT: a long natural stride. The front (right) leg swings forward from the HIP about 28 degrees from
vertical with the knee almost straight and the heel touching down, toes pointing up about 12 degrees. The back (left)
leg swings backward from the hip about 22 degrees, knee slightly bent, the heel lifted high and only the toe still on the
ground. The feet are about 70 percent of a leg-length apart, front heel to back toe.
Frame 2, PASSING: the right leg is straight and planted flat under the hip. The left leg has swung through with the knee
bent about 70 degrees, the left foot lifted OFF the ground to about the height of the right knee, the shin pointing
backward and down. Body at its lowest.
Frame 3, CONTACT: the mirror of frame 1 with the other leg forward.
Frame 4, PASSING: the mirror of frame 2 with the other leg swinging through.
The legs must rotate at the HIP, whole thigh and shin together, not just at the boot. Arms swing opposite to the legs by
about 20 degrees each way, with the elbow bent about 20 degrees, so the near arm is back when the near foot is forward.

Frames 1 and 2 must look clearly different. A stiff shuffle with straight, near-vertical legs is WRONG.
Keep the exact costume, colors, proportions and low-poly game-character style of image 1 in every frame, all four
figures the same size, the planted foot of each figure on one shared horizontal line, equal spacing, nothing overlapping,
nothing cropped. Plain flat light-gray background, flat even lighting, no cast shadows, no ground, no motion lines, no text.
```

### FRONT view (camera in front and about 25 degrees above)
```
You have two reference images. Image 1 is the CHARACTER (young astronaut, cream-and-orange flight suit, tan backpack,
olive boots) seen from the front. Image 2 is a POSE GUIDE of stick figures: copy ONLY the leg and arm positions from it,
never its drawing style.

Draw a 4-frame WALK CYCLE SHEET of the character from the FRONT, camera directly in front and about 25 degrees ABOVE,
looking slightly down at him, as he walks TOWARD the camera. Four full-body figures in one row, left to right,
matching the four stick figures of image 2 exactly.

Leg rules (do not skip):
Frame 1, CONTACT: his RIGHT foot has stepped toward the camera, so the right boot sits LOWER on the screen and looks a
little bigger than the left boot, with the right thigh foreshortened (pointing at the camera) and the heel on the ground,
toes tipped up. His LEFT leg trails behind: the left heel is lifted, the left boot sits HIGHER on the screen. The two
feet must be at clearly different heights in the picture, about one boot-length apart.
Frame 2, PASSING: right leg straight and planted, left knee bent about 70 degrees, left foot lifted off the ground and
swinging forward, clearly off the floor. Body at its lowest.
Frame 3, CONTACT: the mirror of frame 1 (left foot toward the camera, lower and bigger).
Frame 4, PASSING: the mirror of frame 2.
Arms swing forward and back (not sideways), opposite to the legs: the hand on the side of the forward foot is back, the
other hand is forward and looks lower and bigger.

Frames 1 and 3 must look clearly different from each other and from frame 2.
Keep the exact costume, colors, proportions and low-poly game-character style of image 1 in every frame, all four
figures the same size, the planted foot of each figure on one shared horizontal line, equal spacing, nothing overlapping,
nothing cropped. Plain flat light-gray background, flat even lighting, no cast shadows, no ground, no motion lines, no text.
```

## 20-second check before you send me the sheet
Do these on the generated sheet. If one fails, use the fix prompts below instead of re-rolling blindly.
1. **Squint test:** cover the heads. Can you tell in every frame which foot is forward? In frames 1 and 3 the feet must be at clearly different heights (back and front view) or clearly apart (side view).
2. **Frames 1 and 3 are mirror images of each other**, not the same pose.
3. **Frame 2 and frame 4 each show one foot lifted off the ground** with a bent knee.
4. **Side view:** the thighs tilt at the hip. If both legs are close to vertical, it fails.
5. **Arms swing front and back**, not out to the sides.
6. Same costume and size in all four.

## Fix prompts (paste as a follow-up in the same Gemini chat)
- Back or front, legs standing still: `The legs are standing instead of walking. Redo the sheet exactly like the pose guide: in frames 1 and 3 one foot must be clearly higher on the screen than the other (the foot stepping away from the camera is higher in the back view; the foot stepping toward the camera is lower in the front view), with the trailing heel lifted. In frames 2 and 4 one foot is lifted off the floor with a bent knee. Keep everything else identical.`
- Side, stiff legs: `The stride is too short and the legs are stiff. Swing each leg from the hip: 28 degrees forward and 22 degrees back in frames 1 and 3, and in frames 2 and 4 bend the swinging knee to about 70 degrees with the foot lifted off the ground to knee height. Keep everything else identical.`
- One figure is wrong: `Redo only figure 3. Keep figures 1, 2 and 4 exactly as they are.`
- Costume drifted: `The backpack is a tan rectangular pack with two blue panels and an orange hose. The suit is cream with orange sleeves and olive straps. Do not change them.`

## Tips
- Ask for the widest image Gemini can give (4096 px if offered); frames are shrunk to about 300 px tall in the game.
- If Gemini ignores the guide image, add one line at the start: `The second image is a stick-figure pose guide. Your four figures must have the same leg positions as the four stick figures, in the same order.`
- Save the sheets in `3d/art/_originals/` as `PLAYER_WALK__BACK.jfif`, `PLAYER_WALK__SIDE.jfif`, `PLAYER_WALK__FRONT.jfif` (or tell me the names) and I will re-cut them into frames.
