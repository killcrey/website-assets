# CLAUDE.md

## Project Overview
"LAYERS: Void Runner" — browser arcade game for The Invisible Panchos (band/brand), live at **game.theinvisiblepanchos.com**. Canvas-based dodge/shoot-em-up: pilot a ship through waves of enemies, anomalies, and bosses, chasing a global high-score leaderboard while background music streams from the band's catalog.

## Tech Stack & Architecture
- **Everything is one file**: `index.html` (~1650 lines) — HTML, inline `<style>` CSS, and inline `<script>` JS all in one document. No framework, no bundler, no build step, no `package.json`.
- **Rendering**: HTML5 Canvas 2D (`ctx`), 60fps `requestAnimationFrame` game loop.
- **Audio**: Web Audio API for two purposes — (1) fully synthesized SFX via oscillators/noise (`sfxTone`/`sfxNoise` helpers, no audio files), (2) an `AnalyserNode` on the streamed `<audio>` background track for bass-reactive visuals (screen tint, star size).
- **Backend**: Supabase JS client (`supabase-js@2`, loaded via CDN) — used *only* for the leaderboard. Table `void_runner_scores`, project `vihwbuiobowdreynxmgy.supabase.co`, publishable/anon key hardcoded in `index.html` (intentional — client-side leaderboard reads/writes, not a secret).
- **Styling**: Tailwind via CDN (`cdn.tailwindcss.com`, no config/build) + hand-written CSS in the `<style>` block for game-specific UI (HUD, overlays, glitch effects). Google Fonts: VT323 (pixel/HUD text), Rajdhani.
- **Assets**: PNG sprites and MP3 tracks sit at repo root, referenced by relative `./filename.ext` paths. Many filenames contain spaces/`&` and must stay URL-encoded in `src` attributes (e.g. `./WINS%20%26%20LOSSES.mp3`).

## Directory Structure
Flat — no subfolders, except `3d/` (see below).
```
index.html          entire game: markup, styles, logic
3d/index.html       LAYERS: San Diego — 3D prototype (Three.js, no build step). Separate from the 2D game; noindex
CNAME                GitHub Pages custom domain -> game.theinvisiblepanchos.com
*.png                sprites (ship, enemies, bosses, pickups) — root level
*.mp3                background tracks — root level
README.md            empty placeholder
```

## Core Commands
No npm, no build. Serve the directory with any static file server for local dev, e.g.:
```bash
python -m http.server 8935
```
Then open `http://localhost:8935`. No build command, no test command — none exist for this project.

## Coding Standards & Conventions
- **Naming**: camelCase for JS variables/functions/entity `type` strings (`'enemyship'`, `'source_logo'`); kebab-case for DOM element `id`s.
- **State management**: no framework state. Module-level `let`/`const` globals for all game state (score, entities, timers). Two tiers: **session-scoped** (plain JS vars, reset on page reload — e.g. unlocked-track list) vs **persistent** (`localStorage` — high score, one-time tutorial-tip flags).
- **Entity system**: single `Entity` class, branched entirely on a `type` string in `constructor`/`update`/`draw` (no subclasses). New enemy/pickup/boss types extend the existing if/else chains in those three methods, not new classes.
- **Sprite rendering**: sprites are pre-baked into glow-halo canvases once at load (`buildGlowCache()` / `GLOW` object) via `makeGlowSprite`/`drawGlow`, so per-frame draws never pay `ctx.shadowBlur` cost. Add new sprites to `ALL_SPRITES` (load-gating array) and `GLOW` (glow cache) together.
- **Spawn weighting**: data-driven via `SPAWN_TABLES` + `pickSpawnType()` — add new spawnable types as table rows, not new if/else chains.
- **Overlay text**: quotes, tutorial toasts, pancho-power banners, and level-up/anomaly text all share one serialized queue (`claimOverlaySlot`/`overlayBusyUntil`). A message whose wait would exceed `MAX_OVERLAY_QUEUE_WAIT` (2.5s) is dropped rather than shown late/stale. `forceClaimOverlay()` is the sole exception, reserved for the trench-portal countdown.
- **Layout fit**: overlay screens (start/game-over/choice) are fit to the viewport at runtime via `fitOverlay()`, which measures real `offsetHeight` and applies CSS `zoom` — **not** static CSS breakpoints, which have repeatedly failed to match real device/OS font/DPI scaling in this project.
- **Data fetching**: `supabase.from('void_runner_scores').select(...)`/`.insert(...)` directly from the client (anon key + RLS), for leaderboard reads/writes only.

## Deployment Protocol
- **GitHub Pages**, private repo `killcrey/website-assets`, `main` branch, custom domain via committed `CNAME` file. No Actions workflow — a push to `main` is the deploy.
- **Standing rule**: confirm with the user before `git push` on this repo (no standing auto-push permission granted here, unlike other Panchos projects).
- Verify live changes with a cache-busted query param (`?cb=...`) — both the local dev server and the live domain have repeatedly served stale JS on plain reloads/force-reloads during this project's testing.

## Known Quirks & Critical Context (INDEX ONLY)
Full write-ups live in `docs/NOTES-ARCHIVE.md` (not auto-loaded). Before changing an area below, `grep -n -i "<keyword>" docs/NOTES-ARCHIVE.md` and read the matching entry. Add NEW incident/change notes to the archive, not to this file.

- Portal rarity is intentional
- `document.hidden` blocks `requestAnimationFrame`
- Audio autoplay
- Boss/anomaly system
- Leaderboard hardening SQL is drafted but not applied
- No test suite exists and none is planned — verification is manual, via the Browser tools against the local static server and/or the live domain.
- `3d/` prototype (2026-10-22)
- 3D movement playtests + movement model (2026-11-05)
- The Source -> sky level -> 3D, no choices (2026-11-05)
- Back from the 3D game: saved run + reward (2026-11-05)
- Blue circle under the Tear (2026-11-05)
- Vendored agent skills (2026-11-06)
- First audit fixes built (2026-11-06, from `AUDITS.md`)
- Camera closer + wall zoom cause found (2026-11-06)
- Pull-in softened (2026-11-06)
- 2D launch screen for sideways phones + small a11y fixes (2026-11-06, audit A1/A2/A3/A5)
- 3D sprites load by distance (2026-11-06, audit B2)
- 2D logic runs on a fixed 60 steps/s clock (2026-11-06, audit B6)
- pixelfx effect sheets in the 2D game (2026-11-10)
- 3D vehicle hulls: black fringes at grazing angles fixed (2026-11-10)
- Blender-made 3D props: bench, cones, hydrant (2026-11-10, branch `blender-props`)
- 3D vehicles as real models built from their own sprites: van, bread truck, pickup, hatchback, sedan (2026-11-10)
- 3D camera corner swing: smooth start, shorter wait (2026-11-10, reported: jerky and slow on turns)

- **3D camera follows you sideways too (2026-11-10)**: pushing left/right on the main street (or forward/back in a cross street) used to leave the camera facing along the corridor (measured: yaw stayed 0 while walking across the street); only the corridor's own axis turned it. `update()` now sets `wantYaw` for either axis (stick direction snapped to the nearest of four ways), so the view swings to sit behind you whichever way you head; a sideways swing needs the push held 0.22 s (`alongAxis` false) versus 0.1 s for along-corridor turns, so a quick dodge doesn't spin the view. To avoid the zoom/jerk this used to cause when a building is behind you, the swing first looks for a clear angle: it tries the wanted yaw, then 20/40/60 degrees either side (nearest the current view first) with `camClipT`, takes the first clear one (else the least blocked) and eases the offset in as `yawBias` (6/s), instead of letting `camLimit` pull the lens in. Idle recentering now snaps to the nearest of the four ways (`Math.round(yaw / (PI/2))`), so a view that turned to follow you stays there when you stop. Measured headless (vs the pushed build): walk right/left across the street -> yaw -90/+90, camera distance range unchanged (3.2-5.1 m), 0-3 distance pops, max jump 0.5 m (was 0.37); forward control unchanged. Known trade-off: strafing left/right repeatedly (zig-zag) swings the view every sideways stretch (4 yaw reversals in 5 s of the test) — raise the 0.22 s threshold if that feels too busy. **Not verified by hand / on a phone.**

## AI Interaction Directives
- Before changing movement, camera, input, UI layout or performance, consult the matching skill in `.claude/skills/` (physics-tuning, camera-systems, game-feel, input-systems, game-ui-ux, performance-optimization); this repo's own rules in this file win on any conflict.
- Never rewrite the whole file for a small change — use targeted edits scoped to the exact function/block.
- Do not explore beyond `index.html` and the asset files relevant to the requested change.
- No filler, no apologies, no restating the request before acting.
- No speculative refactors or abstractions outside the requested scope.
- Verify behavioral/UI changes live (local static server + Browser tools) before reporting done — there is no test suite to lean on instead.
- Always confirm before `git push` to `main` (see Deployment Protocol) — this repo has no standing push permission.
- Treat this file as authoritative; update it when something here goes stale rather than silently diverging from it.
- Keep this file short: it loads every session. Put change logs and incident details in `docs/NOTES-ARCHIVE.md`.
