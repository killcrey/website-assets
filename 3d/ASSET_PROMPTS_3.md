# Gemini prompts, round 3: San Diego landmarks and a new lowrider

Built from the reference photos added on 2026-10-24 (all in `3d\art\_originals\`). Same pipeline as before: generate, save into `3d\art\_originals\`, tell me the filenames, and I cut them out and place them.

**How to run every prompt below**
1. Upload the **photo first**, then the **style reference second** (`bodega.jfif` for buildings and landmarks, `Parked car A.jfif` for the lowrider).
2. Paste the prompt. Each one already contains the style block.
3. If Gemini adds people, cars, wires or extra buildings, say: "Remove everything except the building."
4. Save the result under the filename given.

**Size budget:** I shrink every image to about 768 px wide. All 11 prompts together cost roughly 26 MB of phone memory (we have room, see the earlier audit).

## Decisions I made (change any you disagree with)
- **No real business names or brand marks.** The photos show real shops (El Carrito, Aztlan Libre, Basile) and a real stadium wordmark. Every prompt swaps them for invented names, the same way the taqueria became "TACO SHOP". If you want the real Petco Park wordmark, tell Gemini to "keep the red PETCO PARK lettering" in prompts 5 and 6.
- **Chicano Park murals are redrawn as original art.** The photos show real artists' murals, so the prompts keep the pillar shapes, the colors and the pavilion architecture but ask for new Chicano-futurist murals.
- **The lowrider is a new car, not a replacement.** It becomes `car_d` next to the existing teal sedan.

## Order (in case the Gemini limit runs out)
Priority 1: **1** (lowrider), **9**, **10** (Barrio Logan), **7**, **8** (Chicano Park)
Priority 2: **2**, **3** (Gaslamp), **5**, **6** (stadium)
Priority 3: **4** (arch), **11** (props)

## Style block (already inside each prompt)
```
Stylized low-poly 3D game art, clean flat-shaded shapes with soft color gradients, warm earth-tone palette,
bright daylight look, slightly worn and lived-in. Not photorealistic. Plain light-gray background, soft even
lighting, no cast shadows. No brand logos, no readable license plates, no people.
```

---

## PRIORITY 1

### 1. Lowrider convertible (new car) — photo: `lowrider 1.webp`, style ref: `Parked car A.jfif`
Save as `parked_car_D.jfif`
```
Use the first image (the photo) as the design reference and the second image (the teal lowrider sedan) as the
art style reference. Draw the same kind of car as the photo: a late-1960s American full-size convertible
lowrider with the top down, candy-green paint with flowing gold and orange pinstripe and filigree patterns
along the side and on the hood, a chrome grille and bumpers, gold chrome wire-spoke wheels with white-wall
tires, a teal interior, and a very low stance. Remove every badge and brand mark. Stylized low-poly 3D game
art, clean flat-shaded shapes with soft color gradients, bright daylight look, slightly worn. Not
photorealistic. Real-world length about 5.4 meters.
Show three views side by side on the same plain light-gray background: front view, side view (facing left),
and back view. Same car, same scale in all three, whole car visible, nothing cropped, standing on a flat
ground line. No people, no street, no other cars, no readable license plates.
```

### 9. Barrio Logan diner — photo: `barrio logan 2.png`, style ref: `bodega.jfif`
Save as `bl_diner.jfif`
```
Use the first image (the photo) as the layout reference and the second image (the bodega storefront) as the
art style reference. Redraw the building as a single low diner-style restaurant: olive-green walls with cream
trim, a long row of tall windows under a red-and-maroon striped metal awning, a small maroon entrance awning
with a glass door, a pitched shingle roof peeking up in the middle, a rooftop vent, and a big hand-lettered
sign board on a post above the roof reading EL FAROL / COCINA MEXICANA (invented name, not the name in the
photo). Keep the picnic tables with yellow wooden tops along the front, the red umbrella on the left, and
the painted wall panel on the left reading BREAKFAST & LUNCH. Leave out the street number plaques, the
power lines, the cars and the people. Stylized low-poly 3D game art, clean flat-shaded shapes with soft color
gradients, bright daylight look, slightly worn. Not photorealistic. Straight-on front elevation, flat
orthographic view with no perspective and no angle, the whole building centered on a plain light-gray
background with a margin around it, soft even lighting, no cast shadows.
```

### 10. Barrio Logan storefront row — photo: `barrio logan building ex 1.webp`, style ref: `bodega.jfif`
Save as `bl_row.jfif`
```
Use the first image (the photo) as the layout reference and the second image (the bodega storefront) as the
art style reference. Redraw the buildings as two different low storefronts side by side, straight-on front
elevation, with a small gap between them, same ground line. Left: a weathered cream stucco building with
patches of peeling paint and old bullet-hole-style pockmarks, a heavy rusted-steel awning band across the top
with large cut-out metal letters (keep the letters abstract, not readable), a tall brown-framed window with
lace curtains on the left, a pair of rusted double doors with small glass panes in the middle, and a second
brown-framed window on the right. Right: a narrow turquoise storefront with a bold hand-painted cactus mural
on the walls, a white-lettered sign reading TIERRA LIBRE (invented name), a small window with a poster
and a dark doorway. Add a few worn details: a red spray-paint tag on the stucco, and a couple of tire planters
with green succulents at the base. Leave out the street, the power poles and wires, the trees, the cars and
the people. Stylized low-poly 3D game art, clean flat-shaded shapes with soft color gradients, bright
daylight look, worn. Not photorealistic. Flat orthographic view with no perspective, both facades fully
visible and centered on a plain light-gray background, soft even lighting, no cast shadows.
```

### 7. Chicano Park bridge pillars (original murals) — photo: `ChicanoPark with kiosk in middle.jpg`, style ref: `bodega.jfif`
Save as `chicano_pillars.jfif`
```
Use the first image (the photo) as the layout reference and the second image (the bodega storefront) as the
art style reference. Draw two different concrete freeway-bridge support pillars shown side by side, straight-on
front elevation, each with the wide angled concrete capital (the flared top) and a slice of the underside of
the freeway deck above it, standing on a flat ground line. Each pillar is covered in its own ORIGINAL
Chicano-futurist mural: the left pillar shows a tall woman astronaut in a woven serape-style cape holding a
glowing lantern, a desert and a rip in the sky behind her; the right pillar shows a giant hummingbird and a
sun-and-moon pair with geometric Aztec-inspired borders in purple, orange, teal and gold. Make both murals
completely original (do not copy any existing mural or any real artist's work). Leave out the park, the trees,
the people, the cars, the kiosk and the sky. Stylized low-poly 3D game art, clean flat-shaded shapes with soft
color gradients, bright daylight look, slightly worn. Not photorealistic. Flat orthographic view with no
perspective, plain light-gray background with a margin, soft even lighting, no cast shadows.
```

### 8. Chicano Park pavilion (kiosco) — photo: `Chicano_Park_Kiosk.jpg`, style ref: `bodega.jfif`
Save as `chicano_kiosk.jfif`
```
Use the first image (the photo) as the layout reference and the second image (the bodega storefront) as the
art style reference. Redraw the open-air park pavilion: a flat orange-and-gold roof slab held up on four
tall slanted white legs, each leg and the beam above painted with bold geometric diamond and zigzag patterns
in red, green and teal on white (keep it a clean ORIGINAL pattern, not a copy of the photo's exact pattern),
a painted ceiling visible underneath, and a wide stepped base with green steps on the left, a dark stone
slab in the middle and red steps on the right. Straight-on front elevation, flat orthographic view with no
perspective, the whole pavilion centered on a plain light-gray background with a margin, soft even lighting,
no cast shadows. Leave out the park, the trees, the freeway, the cars and the people. Stylized low-poly 3D
game art, clean flat-shaded shapes with soft color gradients, bright daylight look, slightly worn. Not
photorealistic.
```

---

## PRIORITY 2

### 2. Gaslamp Victorian row — photo: `gas lamp example 2.jpg` (top photo and bottom-left photo), style ref: `bodega.jfif`
Save as `gaslamp_victorian.jfif`
```
Use the first image (the photo collage, the top and bottom-left pictures) as the layout reference and the
second image (the bodega storefront) as the art style reference. Draw three different tall historic downtown
buildings side by side, straight-on front elevation with a small gap between them, same ground line. Left to
right: (1) a narrow ornate Victorian tower with a green copper-roofed turret and spire, cream and red trim
and many small arched windows; (2) a red-brick Victorian building with tall white-framed arched windows,
white decorative trim, black iron fire-escape balconies and a green awning over a ground-floor restaurant;
(3) a cream and white ornate building with rows of arched windows and a ground-floor cafe with a maroon
awning. Warm brick and stucco in earth tones, slightly worn. Leave out the street, cars, traffic lights,
trees, people and any readable signs or brand names. Stylized low-poly 3D game art, clean flat-shaded shapes
with soft color gradients, bright daylight look. Not photorealistic. Flat orthographic view with no
perspective, all three fully visible on a plain light-gray background, soft even lighting, no cast shadows.
```

### 3. Gaslamp brick row with string lights — photos: `gaslamp example 1.webp` and `gas lamp example 2.jpg` (bottom-right picture), style ref: `bodega.jfif`
Save as `gaslamp_brick.jfif`
```
Use the first two images (the photos) as the layout reference and the last image (the bodega storefront) as
the art style reference. Draw two different brick buildings side by side, straight-on front elevation, small
gap between them, same ground line. Left: a three-story dark red-brick corner building with cream trim,
tall rectangular windows with warm yellow light inside, small iron balconies on the second floor, and a
ground-floor steakhouse with a glowing neon-style sign reading SEAFOOD & GRILL (invented), warm string
lights and a few round patio heaters out front. Right: a four-story red-brick building with cream bands and
rows of windows each topped with an orange canvas awning, and a ground-floor coffee shop with a dark
awning. Leave out the street, cars, palm trees, the arch sign, people and any real brand names. Stylized
low-poly 3D game art, clean flat-shaded shapes with soft color gradients, bright late-afternoon daylight,
slightly worn. Not photorealistic. Flat orthographic view with no perspective, both fully visible on a plain
light-gray background, soft even lighting, no cast shadows.
```

### 5. Baseball stadium exterior (replaces the old stadium-corner idea) — photo: `petco park1.jpg`, style ref: `bodega.jfif`
Save as `stadium_exterior.jfif`
```
Use the first image (the photo) as the layout reference and the second image (the bodega storefront) as the
art style reference. Redraw the baseball stadium exterior: a huge curved white steel-truss lattice facade
with diagonal bracing and open concourse levels, a tall sandstone-colored tower with a metal lattice crown on
the left, a sandstone office block on the right with greenery on its roof edge, a rooftop light tower, and a
row of palm trees along the base. Across the top of the truss put a big red lowercase sign reading ballpark
(a generic sign, no team name and no real stadium name). Leave out the people, cars, street and the
surrounding skyscrapers. Stylized low-poly 3D game art, clean flat-shaded shapes with soft color gradients,
bright blue-sky daylight look. Not photorealistic. Straight-on front elevation, flat orthographic view with
no perspective, the whole stadium centered on a plain light-gray background with a margin, soft even
lighting, no cast shadows. Wide landscape format.
```

### 6. Stadium gate plaza — photos: `petco park 2.webp` and `petco park 3.webp`, style ref: `bodega.jfif`
Save as `stadium_gate.jfif`
```
Use the first two images (the photos) as the layout reference and the last image (the bodega storefront) as
the art style reference. Draw the stadium's street-level entrance plaza: a long tan sandstone wall with a
gap holding a row of silver metal security gates and turnstile frames, tall iron-bar fences on both sides
with red, white and blue bunting, several tall slender palm trees in front, a few small round trees with
purple flowers, and the white steel truss of the stadium rising behind with a red lowercase sign reading
ballpark (generic, no team or real stadium name). On the wall put plain blank banner panels in brown and
gold (no logos, no readable text). Leave out the people, the cars, the street and the skyline. Stylized
low-poly 3D game art, clean flat-shaded shapes with soft color gradients, bright blue-sky daylight look.
Not photorealistic. Straight-on front elevation, flat orthographic view with no perspective, centered on a
plain light-gray background with a margin, soft even lighting, no cast shadows. Wide landscape format.
```

---

## PRIORITY 3

### 4. Gaslamp arch (optional art version of the street-start sign) — photos: `gaslamp example 1.webp` and `gas lamp example 2.jpg` (bottom-right picture), style ref: `bodega.jfif`
Save as `gaslamp_arch.jfif`
```
Use the first two images (the photos of the Gaslamp Quarter arch sign) as the layout reference and the last
image (the bodega storefront) as the art style reference. Redraw ONLY the arch sign: a wide shallow arch
spanning a street, with an ornate cream-and-gold filigree crest in the middle holding an oval medallion that
reads Gaslamp Quarter in gold script, a teal-green curved band across the whole arch reading HISTORIC HEART OF
SAN DIEGO in gold capital letters with a round seal in the middle, and a decorative scroll at each end where
the arch meets a short pillar. Straight-on front elevation, flat orthographic view with no perspective, the
whole arch centered on a plain light-gray background with a margin. Leave out the buildings, street, cars,
trees, wires, lamp posts and people. Stylized low-poly 3D game art, clean flat-shaded shapes with soft color
gradients, bright daylight look, slightly worn. Not photorealistic. Soft even lighting, no cast shadows.
```

### 11. Barrio Logan sidewalk props (single view each) — photo: `barrio logan building ex 1.webp`
Save as `bl_props.jfif`
```
A set of street props shown in one row on a plain light-gray background, each separate with space between,
front view only, all at the same relative scale: a big carved stone-head planter (a large stylized ancient
colossal-head sculpture used as a flower pot, with a worn teal-and-clay painted face) sitting on a wooden
pallet; a stack of two black tires planted with green succulents; a single black tire planter with a
cluster of succulents; a rusted metal bollard; a worn wooden sidewalk bench. Stylized low-poly 3D game art,
clean flat-shaded shapes with soft color gradients, bright daylight look, slightly worn. Not photorealistic.
No people, no brand logos.
```

---

## After you generate them
Send me the filenames. For each I will: add it to `make_sprites.py`, cut it out, shrink it to about 768 px wide, place it in the street (Gaslamp end for 2, 3, 4, 5, 6; Barrio Logan end for 7, 8, 9, 10, 11; the lowrider as a parked car), and re-run the checks. Where each goes, my proposal:
- **Stadium (5, 6):** a big backdrop at the start of the street on the right, so it reads as the Gaslamp edge of the ballpark.
- **Chicano Park (7, 8):** between the last cross street and the Tear, so the final run goes under the pillars.
- **Lowrider:** parked at the Barrio Logan end, near the diner.
