# Replica guide: turning a real building into a game building

Goal: you give me real buildings, and we make stylised replicas that people from the neighbourhood recognise. Not photo textures: the same flat toy-city style as the key image, but with the right shape, colours, doors, windows, porch, roof and details.

## How a replica gets made (3 pieces)
1. **You** take photos and write a few notes per building (below).
2. **Gemy** turns the photo into a flat, straight-on facade texture in our style (prompt below). She never copies the photo pixel for pixel; she redraws it flat and simplified.
3. **Claude** builds the 3D shape (width, depth, height, roof type, porch, steps, awnings, signs) from your notes and the photo, drops her texture on it, and shows you a side-by-side with your photo so you can say "the door is wider", "the roof is flatter".

## What to photograph (4 photos per building is plenty)
1. **Front, straight-on**, from across the street, as square to the wall as you can, whole building in frame, no car or tree blocking if possible.
2. **Corner view (3/4)** showing the front and one side, so I can read depth and roof shape.
3. **Roof line / top**, from an angle if you can, or a satellite view.
4. **One close detail**: door, porch posts, a window style, security bars, a sign shape.
Tips: shoot in daylight, level the phone, avoid people and faces, avoid readable licence plates.

## Notes to write for each building (copy this form)
```
Building ID (block + name, e.g. A2-corner-house):
Type (house / one-story shop / apartment / church / other):
Floors:
Rough width and depth (steps, or "like 2 cars wide"):
Roof (flat with parapet / gable / hip / other):
Main wall colour(s) and trim colour(s):
Front door side (left / centre / right) and porch (yes/no, how big):
Special features (steps, security bars, awning, fence, mural, tree, sign shape):
What MUST be exact:
What can be simplified:
```

## Rules we keep
- **Real names and logos** on signs: leave the sign blank or fictional, unless the owner agrees. I add text in the game.
- **Murals** on real walls are the artists' work. We make original murals, or ask the artist.
- **People, faces, licence plates**: not in the photos.
- Very detailed buildings get **simplified** to read well on a phone. Tell me the 3 things that make each one recognisable and I will protect those.

## Prompt for Gemy: photo to flat facade (use one photo per message)
Attach the photo AND the key concept image (the approved style anchor).
```
Redraw the attached photo of a real building as a flat FACADE TEXTURE in the style of my approved key concept image. Keep the real building's proportions, window and door layout, wall colour, trim colour and any recognisable detail (porch, steps, security bars, awning shape, sign shape). Simplify everything else into chunky flat shapes. Straight-on orthographic view, no perspective, no baked shadows or lighting, no cars, no people, no trees in front of the wall, NO TEXT OR LETTERS (leave signs blank), no logos. At least 1024 px wide, PNG. Then make a second image of the plain side wall in the same style, and if the roof is pitched, a seamless top-down roof texture in the matching colour.
```
Name them `bl_replica_<building-id>_front.png`, `..._side.png`, `..._roof.png`.

## How many?
Start with the **5 to 8 buildings that matter most to you** on your drawn map, and the rest of each block uses our generic types. That keeps the street recognisable without needing every building.
