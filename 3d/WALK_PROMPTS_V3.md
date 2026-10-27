# Player walk cycle, round 3: one frame at a time, edited from the real sprite

V2 failed in two ways: Gemini **redrew the character** (it was asked to invent four new figures from two reference images), and the **planted leg stayed still** (it was never told how that leg has to turn between frames). This version fixes both:

1. **Edit, don't generate.** Each prompt says "edit this image, change only the legs", so the head, suit, backpack and colors stay exactly as they are.
2. **One figure per image, chained.** Frame 2 is edited from frame 1, frame 3 from frame 2, frame 4 from frame 3. The prompt for each step says exactly how every leg turns **from the previous frame**, so the planted leg has to rotate.
3. **No pose-guide upload** (a second picture is what made it redraw). The guides in `3d/art/pose_guides/` are now only for **you** to compare against.

## The rule that was missing: the planted leg keeps turning
One leg is "planted" for a whole step, and it never stays still. It turns at the hip:
**28 degrees forward (heel strike) -> straight down (passing) -> 22 degrees backward (heel lifts, toe pushes off)**.
Meanwhile the other leg lifts its heel, bends its knee, swings through and becomes the front leg. Angles below are measured at the hip, from straight down; forward = the direction he is walking.

| Frame | RIGHT leg | LEFT leg |
|---|---|---|
| 1 contact | 28 forward, heel down, toes up | 22 back, heel lifted, toe on ground |
| 2 passing | **0, straight down, planted** (it just turned back 28) | 14 forward, knee bent 70, foot lifted off the ground |
| 3 contact | **22 back**, heel lifted (it turned back another 22) | 28 forward, heel down, toes up |
| 4 passing | 14 forward, knee bent 70, foot lifted | **0, straight down, planted** (it just turned back 28) |

Arms swing opposite the legs, about 20 degrees, elbows bent a little.

## How to run it (same steps for each view)
1. Open a **new** Gemini chat per view. Upload ONE image: the current standing sprite (`3d/art/sprites/player_back.webp`, `player_side.webp` or `player_front.webp`; save as PNG first if Gemini refuses .webp).
2. Paste the **LOCK** paragraph for that view, then the **Frame 1** prompt. Generate, check, and regenerate until it passes the check below.
3. Upload that result as the new single image and paste the **LOCK** paragraph again + the **Frame 2** prompt. Same for frames 3 and 4.
4. If the character starts to drift (new colors, different backpack), go back to the original sprite and paste the LOCK + the full description of the frame you want (the "absolute" line), not the change line.
5. Save each frame as `3d/art/_originals/walk_<view>_1.png` ... `_4.png`. Tell me the view names and I will put them in one sheet and cut them.

## LOCK paragraph (paste at the start of EVERY prompt)
### Back view
```
EDIT the attached image. Do NOT redraw or restyle it. Keep these EXACTLY as they are: the head and hair, the neck ring,
the tan rectangular backpack with its blue panels and orange hose, the blue shoulder pads, the cream-and-orange suit,
the olive-green straps and boots, every color, the outline and shading style, the proportions, the body size, the
image size and the framing. Change ONLY the legs, boots and arm swing as described below. Plain flat light-gray
background, no shadow, no ground, no text.
```
### Side view
```
EDIT the attached image. Do NOT redraw or restyle it. Keep these EXACTLY as they are: the head and hair, the face and
neck ring, the tan backpack with its two round blue-gray fittings and orange hose, the orange shoulder, the cream suit
with olive straps and orange bands, every color, the outline and shading style, the proportions, the body size, the
image size and the framing, and he still faces RIGHT. Change ONLY the legs, boots and arm swing as described below.
Plain flat light-gray background, no shadow, no ground, no text.
```
### Front view
```
EDIT the attached image. Do NOT redraw or restyle it. Keep these EXACTLY as they are: the head, face and hair, the neck
ring, the chest panel with the eye emblem, the two orange hoses, the olive harness, the cream-and-orange suit, every
color, the outline and shading style, the proportions, the body size, the image size and the framing. Change ONLY the
legs, boots and arm swing as described below. Plain flat light-gray background, no shadow, no ground, no text.
```

## BACK view frames (camera behind him, slightly above; he walks away from the camera)
Because the camera is a little above, a foot that steps AWAY from the camera shows HIGHER in the picture and its thigh looks shorter; a trailing foot shows LOWER with the heel lifted and the boot sole facing the camera.

**Frame 1** (from the standing sprite)
```
Pose: mid-stride, contact. His RIGHT leg has swung forward (away from the camera) about 28 degrees from the hip: the
right boot sits clearly HIGHER in the picture than the left boot and the right thigh is foreshortened (shorter). His
LEFT leg is behind him, about 22 degrees back, with the heel lifted so the SOLE of the left boot faces the camera; the
left boot sits LOWER in the picture. The two boots are about one boot-length apart vertically. Left arm swings forward
(hand higher in the picture), right arm swings back (hand lower).
```
**Frame 2** (upload frame 1)
```
Change from the previous frame: the RIGHT leg, which was forward, has now turned BACK at the hip about 28 degrees until
it is straight down under his hip, planted flat on the ground. The LEFT leg has lifted its heel, bent the knee about 70
degrees and swung forward past the right leg: the left boot is clearly OFF the ground, at about the height of the right
ankle, bent knee visible. Body slightly lower. Arms hang near his sides, passing each other.
```
**Frame 3** (upload frame 2)
```
Change from the previous frame: the RIGHT leg keeps turning back another 22 degrees, so it is now trailing behind: its
heel is lifted, the sole of the right boot faces the camera and the right boot sits LOWER in the picture. The LEFT leg
has swung forward about 28 degrees and planted its heel: the left boot sits clearly HIGHER in the picture and its thigh
is foreshortened. Right arm swings forward, left arm back.
```
**Frame 4** (upload frame 3)
```
Change from the previous frame: the LEFT leg, which was forward, has turned BACK at the hip about 28 degrees until it is
straight down under his hip, planted flat. The RIGHT leg has lifted its heel, bent the knee about 70 degrees and
swung forward past the left leg: the right boot is clearly OFF the ground, at about the height of the left ankle.
Arms hang near his sides, passing each other.
```
(Absolute lines for step 4 of "How to run it": frame 2 = right leg straight down and planted, left knee bent 70 degrees with the foot lifted; frame 3 = right leg 22 back with heel lifted, left leg 28 forward; frame 4 = left leg straight down, right knee bent 70 with the foot lifted.)

## SIDE view frames (level camera, he faces RIGHT)
**Frame 1** (from the standing sprite)
```
Pose: mid-stride, contact. The RIGHT leg swings forward from the hip about 28 degrees from vertical, knee almost
straight, heel touching the ground, toes tipped up about 12 degrees. The LEFT leg swings backward from the hip about 22
degrees, knee slightly bent, heel lifted high, only the toe on the ground. The feet are about two-thirds of a
leg-length apart. The near (right) arm swings back about 20 degrees, the far (left) arm swings forward.
```
**Frame 2** (upload frame 1)
```
Change from the previous frame: the RIGHT leg, which was forward, has turned BACK at the hip about 28 degrees until it
is straight down under the hip, foot flat. The LEFT leg has lifted its heel, bent the knee about 70 degrees and
swung forward past the right leg: the left foot is OFF the ground at about the height of the right knee, the shin
pointing backward and down. Body slightly lower. Arms hang near his sides.
```
**Frame 3** (upload frame 2)
```
Change from the previous frame: the RIGHT leg keeps turning back another 22 degrees: heel lifted high, only the toe
on the ground, knee slightly bent. The LEFT leg has swung forward about 28 degrees from vertical, knee almost
straight, heel touching down, toes tipped up. Near (right) arm swings forward, far (left) arm back.
```
**Frame 4** (upload frame 3)
```
Change from the previous frame: the LEFT leg, which was forward, has turned BACK at the hip about 28 degrees until it
is straight down, foot flat. The RIGHT leg has lifted its heel, bent the knee about 70 degrees and swung forward: the
right foot is OFF the ground at about the height of the left knee. Arms hang near his sides.
```

## FRONT view frames (camera in front, slightly above; he walks toward the camera)
A foot stepping TOWARD the camera shows LOWER in the picture and a little bigger; a trailing foot shows HIGHER with the heel lifted.

**Frame 1** (from the standing sprite)
```
Pose: mid-stride, contact. His RIGHT leg has swung forward (toward the camera) about 28 degrees from the hip: the right
boot sits clearly LOWER in the picture and looks slightly bigger, heel down, toes tipped up, the right thigh
foreshortened. His LEFT leg is behind, about 22 degrees back, heel lifted: the left boot sits HIGHER in the picture.
The two boots are about one boot-length apart vertically. Left arm swings forward, right arm back.
```
**Frame 2** (upload frame 1)
```
Change from the previous frame: the RIGHT leg has turned BACK at the hip about 28 degrees to straight down under the
hip, planted flat. The LEFT leg has lifted its heel, bent the knee about 70 degrees and swung forward: the left boot is
clearly OFF the ground. Body slightly lower. Arms hang near his sides.
```
**Frame 3** (upload frame 2)
```
Change from the previous frame: the RIGHT leg keeps turning back another 22 degrees: heel lifted, right boot HIGHER in
the picture. The LEFT leg has swung forward about 28 degrees toward the camera: left boot LOWER in the picture and a
little bigger, heel down. Right arm swings forward, left arm back.
```
**Frame 4** (upload frame 3)
```
Change from the previous frame: the LEFT leg has turned BACK at the hip about 28 degrees to straight down, planted
flat. The RIGHT leg has lifted its heel, bent the knee about 70 degrees and swung forward: the right boot is clearly OFF
the ground. Arms hang near his sides.
```

## 20-second check after every frame (compare with `3d/art/pose_guides/walk_guide_*.png`)
1. Same character? Hair, backpack, suit colors and boots identical to the standing sprite.
2. Same size and same position in the picture as the previous frame.
3. Did the planted leg actually turn? Frame 1 -> 2: it goes from angled forward to straight down. Frame 2 -> 3: from straight down to angled back with the heel lifted.
4. Frame 2 and 4: one foot clearly off the ground with a bent knee.
5. Frames 1 and 3: the foot positions are swapped.

## Fix prompts (same chat, after a bad result)
- `You changed the character. Undo that: only the legs and arm swing may change. Restore the original head, hair, backpack, suit colors and boots exactly as in the first image.`
- `The planted leg did not move. In this frame the right leg must have turned back at the hip by 28 degrees compared with the previous frame. Redo only the legs.`
- `Same pose, but the image size and character position must match the previous frame exactly.`

## If Gemini still will not hold the character
Tell me. Plan B needs no Gemini at all: I cut your existing standing sprite into body and two legs and swing the legs from the hip in the game, so the look can never change. It works well for the back and front views; the side view needs a few small repaint fixes.
