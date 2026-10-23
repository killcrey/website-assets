# GEMINI.md

You are continuing development of "LAYERS: San Diego", the 3D game in `3d/index.html` of this repo (plus the older 2D game in `index.html`). Previous work was done by Claude; everything you need is written down.

1. Read `3d/HANDOFF.md` first (what the game is, how to run and test it, the code map, the user's rules, pitfalls, open items).
2. Then read the newest section of `3d/DESIGN.md` and the repo-wide `CLAUDE.md`.

Hard rules (from the user):
- **Do not `git push` unless the user's message says "Push".** Local commits are fine.
- Make targeted edits only; never rewrite whole files. No speculative refactors.
- Verify changes in a real browser (`python -m http.server 8935`, open `http://localhost:8935/3d/?debug&cb=<new number>`; drive the game through `window.__g`, see HANDOFF.md section 4). Say plainly what you did not verify. Nothing has been verified on a real phone.
- Short, plain replies. When the user asks "what do you think" or says "discuss", answer with an opinion and do not build yet.
- Never put a `//` comment in the middle of a one-line JavaScript statement; it comments out the rest of the line.
- Don't change how many random numbers the building loop consumes (the street layout is seeded; see "Layout parity" in HANDOFF.md).
