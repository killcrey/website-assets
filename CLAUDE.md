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
Flat — no subfolders.
```
index.html          entire game: markup, styles, logic
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

## Known Quirks & Critical Context
- **Portal rarity is intentional** — do not "fix" the fact that portals can't spawn during a `'normal'`-anomaly state; this was explicitly confirmed by the user as by-design, not a bug.
- **`document.hidden` blocks `requestAnimationFrame`** — a backgrounded/headless test tab never advances `gameLoop`. Verify logic by calling game functions directly (`startGame()`, `checkCollisions()`, `entity.update()`, etc.), not by waiting on real frames.
- **Audio autoplay**: unlock is wired to multiple gesture types (`pointerdown`/`click`/`touchend`, each `{once:true}`) plus a persistent retry-on-every-touch fallback (`retryAudioIfStuck`) for in-app browsers (Instagram, etc.) that can silently ignore the first unlock gesture.
- **Boss/anomaly system**: three bosses exist — Octopus (`octo`, common), The Source (`source`, rare, triggers a Dissolve/Remember Home/I'm-Not-Ready choice + optional memory-flight bonus mode), Cobra (`cobra`, Toxic-anomaly capstone) and Super Ego (`superego`, Enemy-Zone capstone). Capstone bosses roll eligibility once when their anomaly starts (25% chance, score-gated, own cooldown) and spawn partway through if eligible.
- **Leaderboard hardening SQL is drafted but not applied** — score-range/username-format constraints were written for the user to run manually in the Supabase SQL editor; this repo/session has no service-role access to apply schema changes directly.
- No test suite exists and none is planned — verification is manual, via the Browser tools against the local static server and/or the live domain.

## AI Interaction Directives
- Never rewrite the whole file for a small change — use targeted edits scoped to the exact function/block.
- Do not explore beyond `index.html` and the asset files relevant to the requested change.
- No filler, no apologies, no restating the request before acting.
- No speculative refactors or abstractions outside the requested scope.
- Verify behavioral/UI changes live (local static server + Browser tools) before reporting done — there is no test suite to lean on instead.
- Always confirm before `git push` to `main` (see Deployment Protocol) — this repo has no standing push permission.
- Treat this file as authoritative; update it when something here goes stale rather than silently diverging from it.
