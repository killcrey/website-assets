# Gemini prompts, round 2: cover, props and storefronts for the long street

Same pipeline as before: generate, save into `3d\art\_originals\`, tell me the filenames, and I cut them out.
For **every** prompt below, upload a style reference with it (use `bread truck.jfif` for vehicles/props, `bodega.jfif` for storefronts) and add: "match the art style of the reference image exactly".

## Order to generate (in case the Gemini limit runs out)
**Priority 1 (needed to build the cover and hiding):** images 1-8
**Priority 2:** images 9-10
**Priority 3 (landmarks):** images 11-13

## Style block (paste at the start of every prompt)
```
Stylized low-poly 3D game art, clean flat-shaded shapes with soft color gradients, warm earth-tone
palette (terracotta, adobe, cream, sage green, dusty blue, mustard), daylight look, slightly worn and
lived-in. Not photorealistic. Neutral plain light-gray background, soft even lighting, no cast shadows.
No brand logos, no readable license plates.
```

## 3-view suffix (vehicles and big cover pieces)
```
Show three views side by side on the same plain background: front view, side view (facing left), and back view.
Same object, same scale in all three, whole object visible, nothing cropped, standing on a flat ground line.
```

---

## PRIORITY 1

### 1. Parked car A: classic lowrider sedan
```
A classic 1960s lowrider sedan, candy teal with gold trim, chrome wheels, sitting low to the ground, dusty
and a little sun-faded. Real-world length about 5 meters. [3-view suffix]
```

### 2. Parked car B: beat-up pickup truck
```
A beat-up old pickup truck, faded rust-red paint, a dented tailgate, a few cardboard boxes and a tarp in the
bed. Real-world length about 5 meters. [3-view suffix]
```

### 3. Parked car C: small hatchback with a surfboard rack
```
A small old hatchback car, mustard yellow, sun-bleached, with a roof rack carrying one surfboard,
San Diego beach-town vibe. Real-world length about 3.8 meters. [3-view suffix]
```

### 4. Dumpster (big cover piece)
```
A large dark-green metal dumpster with a hinged lid, scuffed and dented, a bit of faded graffiti, small
wheels at the bottom. Real-world length about 2 meters, height about 1.5 meters. [3-view suffix]
```

### 5. Street taco / vendor cart (big cover piece)
```
A street vendor food cart on two big wheels with a striped canvas umbrella, a steel counter, a propane tank
and a hand-painted sign. Sun-faded, charming, worn. Real-world length about 2.2 meters. [3-view suffix]
```

### 6. Small street props set (single view each)
```
A set of street props shown in one row on a plain background, each separate with space between, front view
only, all drawn at the same relative scale: two metal trash cans (one with the lid dented), a blue
generic mailbox, a red fire hydrant, a wooden park bench, a coin-operated newspaper box (no real
newspaper name), a stack of orange traffic cones.
```

### 7. Cover pieces set (single view each)
```
A set of low-poly cover pieces shown in one row on a plain background, each separate with space between,
front view only: a tall green hedge planter in a concrete box, a stack of wooden crates and pallets,
a concrete jersey barrier with faded stripes, a rolled-up chain-link fence section on a stand,
a row of three stacked tires.
```

### 8. Two more storefronts (one image, two facades)
The **record store and the taqueria will come from the user's own photos**, so they are not generated here (see "Photo to game art" at the bottom).
```
Two different small corner-store facades drawn side by side, straight-on front elevation, flat orthographic
view with no perspective, each facade fully visible with a gap between them, same height ground line.
Left to right: (1) a COFFEE SHOP with a hand-painted sign reading COFFEE, a striped awning, a chalkboard
menu on an easel, small round tables and a big window with a few espresso cups and a hanging plant;
(2) a PAN DULCE BAKERY (panaderia) with a hand-painted sign reading PANADERIA, a glass window full of
colorful pan dulce (conchas, cuernos, empanadas) on trays, a wooden door, and a striped awning.
Warm stucco and brick in earth tones, worn paint, hand-painted signs.
```

---

## PRIORITY 2

### 9. Bus shelter (big cover piece)
```
A city bus stop shelter with a glass side, a metal roof, a bench inside and a generic blank ad panel
(no real brands). Real-world length about 3.5 meters. [3-view suffix]
```

### 10. Alley and wall pieces (single view each)
```
A set of alley pieces in one row on a plain background, each separate, front view only: a brick wall
section with a drainpipe, a chain-link gate, a wooden fence section with peeling paint, a metal fire-escape
ladder hanging down a wall, a stack of old appliances (fridge and washing machine) by a wall.
```

---

## PRIORITY 3 (landmarks)

### 11. Mural wall under a bridge (original art)
```
A tall concrete bridge pillar wall covered in a colorful original Chicano-futurist mural: astronauts,
a tear in the sky, sun and moon, hummingbirds and geometric patterns. Flat straight-on front elevation,
plain gray background around it. Make the mural completely original (do not copy any existing mural).
```

### 12. Baseball stadium corner
```
The corner entrance of a small-city baseball stadium: a brick gate with brown-and-gold banners and ticket
windows, and a generic bronze baseball-player statue in a batting pose out front (no real person's
likeness, no team names or logos). Flat straight-on front elevation, plain gray background.
```

### 13. Street signs set (optional)
```
A set of street signs in one row on a plain background: a stop sign, a one-way sign, a no-parking sign,
a street-name sign reading FIFTH AVE, a pedestrian-crossing sign. Front view, flat, hand-worn.
```

---

## PHOTO TO GAME ART (for the record store, the taqueria, and any other real storefront photo)
Upload the photo first, then a style reference (the bodega image), and paste:
```
Use the first image (the photo) as the layout reference and the second image (the bodega storefront) as
the art style reference. Redraw the building in the same stylized low-poly 3D game art style as the second
image: clean flat-shaded shapes, soft color gradients, warm earth-tone palette, daylight look, slightly
worn. Not photorealistic. Straight-on front elevation, flat orthographic view with no perspective and no
angle, the whole facade centered on a plain light-gray background with a little margin around it, soft
even lighting, no cast shadows. Keep the same composition and the same sign names as the photo. Leave out
any political signs, brand logos and readable license plates.
```
Save each as its own file (for example `record_store.jfif`, `taqueria.jfif`) in `3d\art\_originals\`.
