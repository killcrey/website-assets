# Gemy prompt pack: Barrio Logan art (copy one at a time)

How to use:
1. Open a NEW chat with Gemy. Attach these reference images first: `art-ref/facades_existing.png`, `art-ref/game_street_portrait.jpg`, `art-ref/game_courtyard_portrait.jpg`, `art-ref/game_characters_lineup.jpg`.
2. Paste **PROMPT 0** (the style header) as the first message. Wait for "ready".
3. Do **PROMPT 1** (key concept image) and approve the look BEFORE anything else.
4. Then paste the rest one at a time. Save each result with the file name shown, and send them to Claude.

File names: `bl_<thing>_<variant>.png`.

---

## PROMPT 0: style header (paste first, once)
```
You are the art partner for a mobile 3D game set in San Diego's Barrio Logan. It is a toy-city look (like the games Stealth Master and My Mini Mart): fixed high camera, chunky low-poly shapes, saturated flat colours, soft shadows, golden-hour warmth. Everything you make is either a FLAT 2D TEXTURE or a REFERENCE SHEET that a developer will wrap onto simple 3D boxes or use to build 3D shapes.
Rules for EVERY image unless I say otherwise: flat graphic style, crisp edges, no gradients on shapes, straight-on orthographic view (no perspective), no baked-in cast shadows, no people, NO TEXT OR LETTERS (the developer adds text later), no logos, no real brand names, not photorealistic, no outlines, at least 1024 px, PNG.
Stay in this warm saturated palette family: terracotta #b4543a, sand #f0c98b, teal #3f9aa3, pink #e48fa8, marigold #f2b134, navy #2c2a4a, cream #fff4dc, sky blue #8cc6e8. Match the simplicity of the reference images I attached.
Reply only "ready" and wait for my first request.
```

## PROMPT 1: key concept image (the look; approve this first)
```
Make ONE key concept image of a single street corner in Barrio Logan, San Diego, as a toy-city game scene. For this image only, you may use a high three-quarter camera angle (about 60 degrees looking down). Include: a taqueria and a panadería with striped awnings, a corner market, a short row of tall painted pillars under a highway bridge with abstract colourful murals (original art, not a copy of any real mural), a distant bridge silhouette, two palm trees, a street with a crosswalk, and one candy-paint lowrider parked at the curb. Golden-hour light, long soft shadows. Chunky simplified shapes, flat saturated colours from my palette, no text, no people. It should look like it belongs in the same game as my reference images.
```

## PROMPT 2: facade textures (do one per message; send 2 images each: SHOPFRONT and UPPER FLOORS)
Template, then the six types below it.
```
Make a flat building FACADE TEXTURE, straight-on, aspect 7:6, exactly 4 window columns by 3 floors, same construction as my reference sheet: the bottom floor is a SHOPFRONT with a striped awning and a big shop window, floors 2 and 3 are windows only. Then make a second matching image with all 3 floors as plain upper floors (no shopfront) for side walls. No text, no people, no signs with letters, no brand names. Building type: [TYPE]
```
Replace [TYPE] with, one message each:
```
TAQUERIA: terracotta and cream walls, a red-and-cream awning, a pass-through serving window, a painted sun motif above the door
```
```
PANADERÍA (bakery): pink and cream walls, a teal-and-cream awning, a glass display window with simple pastry shapes, a scalloped trim line
```
```
AUTO / TIRE SHOP: marigold and navy walls, a big roll-up garage door as the shopfront, a row of simple tire shapes along the bottom, flat practical windows above
```
```
CORNER MARKET (mercado): teal walls, a marigold-and-navy awning, fruit crates and a sidewalk produce stand drawn flat at the bottom, an upper-floor apartment above
```
```
STUCCO HOUSE with porch: sand stucco walls, a small covered porch with two pillars, a low fence line at the bottom, 2 floors only (leave floor 3 as a flat roof edge)
```
```
APARTMENT BLOCK: pale stucco in sand and cream, repeating balconies with thin iron railings on floors 2 and 3, a small recessed entrance on floor 1
```


## PROMPT 2B: the everyday low-rise buildings (MOST of the neighbourhood: homes and one-story shops, not downtown)
Attach `new_lowrise_types.png` (rough sketches) with these. Give each as TWO images: the front facade, and a plain side wall. Also make a matching ROOF texture for the two houses (pitched roof tiles, seamless, top-down).
```
Make a flat FACADE TEXTURE, straight-on, no text, no people, same flat toy-city style as my reference. Building type: ONE-STORY BUILDING. A normal single-storey commercial building with a flat roof and a parapet band on top, four large shop windows, one door, a plain worn wall in a warm colour from my palette. Aspect about 7:3. Make a second matching image of a plain side wall (one window).
```
```
Make a flat FACADE TEXTURE, straight-on, no text, no people. Building type: SMALL HOUSE WITH PORCH. A small single-storey house with a covered front porch (two posts and a porch beam), one window, one front door, stucco walls in a warm colour from my palette, and a low pitched-roof gable above. Aspect about 3:2. Make a second image of the plain side wall with one window, and a seamless top-down roof-tile texture.
```
```
Make a flat FACADE TEXTURE, straight-on, no text, no people. Building type: LARGER HOUSE. A larger two-storey family house with a pitched roof, four upstairs windows, two big ground-floor bay windows with a front door between them, a small balcony above the door, stucco walls in a warm colour from my palette. Aspect about 1:1. Make a second image of the plain side wall with two windows per floor, and a seamless top-down roof-tile texture.
```
Ask for 2 or 3 colour variants of each house so a street of homes does not look copied.

## PROMPT 3: original mural panels (flat, wall art; respectful, in the Chicano mural tradition, NOT copies of real murals)
```
Make an ORIGINAL mural panel, flat and straight-on, 2:1 wide, in the visual tradition of Chicano murals (bold colour blocks, strong outlines are allowed here, symbolic imagery). Theme: a lone astronaut floating between stacked parallel Earths ("layers"), warm sun behind, hands reaching up. Do not copy any existing mural. No text.
```
```
Make an ORIGINAL mural panel, flat, 2:1 wide, Chicano mural tradition. Theme: "memories of home": a warm neighbourhood kitchen window, an abuela's hands making tortillas, a family table, marigold flowers, a radio. Soft and warm. Do not copy any existing mural. No text.
```
```
Make an ORIGINAL mural panel, flat, 2:1 wide. Theme: a large geometric sun with stepped pyramid shapes and a flock of birds, rich oranges, teals and deep blue. Do not copy any existing mural. No text.
```
```
Make an ORIGINAL TALL pillar mural, flat, aspect 1:4 (very tall and narrow), for a painted highway pillar. Repeating geometric pattern in the lower third, a symbolic figure in the middle, sky and stars at the top. Do not copy any existing mural. No text.
```
Make 2 or 3 variations of the tall pillar (different colours), as the park needs several.

## PROMPT 4: sign plates and awnings (blank, I add text in-game)
```
Make a sheet of 12 BLANK sign shapes on a plain light-grey background, flat and straight-on, each clearly separated: 4 painted wooden signs, 4 backlit box signs, 4 neon-outline signs (outline only, no letters). Plus a second sheet of 8 striped awnings in different colour pairs from my palette. No text, no letters, no logos.
```

## PROMPT 5: ground textures (must tile seamlessly)
```
Make 4 seamless TILEABLE ground textures, each 1024x1024, top-down flat colour with very light texture: 1) worn asphalt with a few hairline cracks, 2) light concrete sidewalk with expansion joints, 3) dry grass and dirt patches, 4) painted crosswalk stripes on asphalt. Edges must tile with no visible seam. No text.
```

## PROMPT 6: vehicle reference sheets (orthographic: side, front, back, top)
```
Make a REFERENCE SHEET of a candy-paint LOWRIDER car in my toy-city style: orthographic side, front, back and top views on one sheet, plain background, the same car in each view. Very low stance, gold wire wheels, a pinstripe and a roof stripe, chunky simplified shapes. Colours: deep candy purple with gold. No text. After approval I will ask for 3 more colour variants.
```
```
Make the same kind of orthographic REFERENCE SHEET (side, front, back, top) for each of these, one image per vehicle: 1) a small pickup truck, 2) a taco truck with a serving window and awning, 3) a city bus, 4) a compact sedan. Chunky simplified toy-city style, flat colours from my palette, no text.
```

## PROMPT 7: street props
```
Make a REFERENCE SHEET of street props, each shown from the front and the side (orthographic), flat toy-city style, plain background, evenly spaced: an elote street cart with an umbrella, a taco stand with a striped canopy, a newspaper box, a trash can, a fire hydrant, a bus-stop bench, a mailbox, a planter with a small tree, a traffic cone, a bicycle rack. No text.
```

## PROMPT 8: neighbourhood NPC reference sheets (guidance for 3D figures I build; keep faces simple)
```
Make a CHARACTER REFERENCE SHEET: six neighbourhood characters, each shown front, side and back in an A-pose, flat colours, chunky toy-city proportions about 4.5 heads tall, plain background. Characters: 1) a street-food vendor with an apron and a straw hat, 2) a lowrider club owner with a pressed shirt and sunglasses, 3) an abuela with a shopping cart and a shawl, 4) a kid on a bike with a helmet, 5) a skater with a beanie and a board, 6) a taquero in a white cap and apron. Distinct silhouettes and one signature prop each. No text.
```

## PROMPT 9: UI icons (optional, later)
```
Make a flat icon set on a plain background: three glowing memory gems in cyan, gold and magenta; a HOME badge; an ammo crate; a battery meter with a lightning bolt; a red exclamation mark in a circle; an alien saucer. Chunky, clean shapes, no text.
```
