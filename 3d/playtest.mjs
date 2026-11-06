// Scripted movement playtests for the 3D prototype. Drives window.__g.update() directly
// at a fixed dt (so it works in a hidden tab, where requestAnimationFrame never fires),
// holds input through __g.stick, pins the camera yaw, and measures acceleration, stops,
// turns, wall slides, inside corners, thin-wall tunnelling, dt-independence and camera
// look-ahead. Run it before and after a movement change and compare.
//
//   python -m http.server 8935            (from the repo root, in another terminal)
//   node 3d/playtest.mjs --out before.json
//   ...change movement...
//   node 3d/playtest.mjs --out after.json --base before.json
//
// Needs playwright-core and an installed Microsoft Edge. PLAYWRIGHT_CORE can point at a
// playwright-core folder (default: the one in the bodega repo's scripts/audit).
import { createRequire } from 'node:module'
import { readFileSync, writeFileSync } from 'node:fs'

const require = createRequire(import.meta.url)
const PW = process.env.PLAYWRIGHT_CORE || 'C:/Users/16193/panchos-bodega/scripts/audit/node_modules/playwright-core'
const { chromium } = require(PW)

const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i > 0 ? process.argv[i + 1] : d }
const URL_ = arg('url', 'http://localhost:8935/3d/index.html?tier=0')
const OUT = arg('out', null)
const BASE = arg('base', null)

const browser = await chromium.launch({ channel: 'msedge', headless: true, args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] })
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } })
const errors = []
page.on('pageerror', (e) => errors.push(String(e)))
await page.goto(URL_ + (URL_.includes('?') ? '&' : '?') + 'cb=' + Date.now(), { waitUntil: 'domcontentloaded' })
await page.waitForFunction(() => window.__g && window.__g.walls, null, { timeout: 60000 })

const results = await page.evaluate(() => {
  const g = window.__g, R = 0.45, FIXED_YAW = 0
  g.start(); g.skipIntro()
  const calm = () => { g.hunt.setHeat(0); for (const e of g.hunt.enemies) e.dead = true; if (g.hunt.captured) throw new Error('player was captured mid-test') } // the Suits would otherwise catch the test character
  const p = g.player.position
  const dist = (x, z, w) => { const cx = Math.max(w.x0, Math.min(w.x1, x)), cz = Math.max(w.z0, Math.min(w.z1, z)); return Math.hypot(x - cx, z - cz) }
  const insideRect = (x, z, w) => x > w.x0 && x < w.x1 && z > w.z0 && z < w.z1
  // smallest gap between the player and any wall (negative = overlapping)
  const clearance = () => { let m = 1e9; for (const w of g.walls) { const d = insideRect(p.x, p.z, w) ? -1 : dist(p.x, p.z, w) - R; if (d < m) m = d } return m }
  const inWall = () => g.walls.some((w) => insideRect(p.x, p.z, w))

  function reset(x, z) {
    p.set(x, p.y, z); g.vel.set(0, 0, 0); g.stick.x = g.stick.y = 0; g.stick.id = null; g.yaw = FIXED_YAW
    for (const k in g.keys) g.keys[k] = false
    for (let i = 0; i < 90; i++) { g.yaw = FIXED_YAW; calm(); g.update(1 / 60) } // let the camera settle
    p.set(x, p.y, z); g.vel.set(0, 0, 0)
  }
  // dir is the world direction you push (x right, z toward the camera); walk=true holds Shift
  function push(dx, dz, walk) { const m = Math.hypot(dx, dz); g.stick.x = m ? dx / m : 0; g.stick.y = m ? -dz / m : 0; g.keys.ShiftLeft = !!walk }
  function step(dt, n, rec) {
    for (let i = 0; i < n; i++) {
      const x0 = p.x, z0 = p.z; g.yaw = FIXED_YAW; calm(); g.update(dt)
      if (rec) rec.push({ x: p.x, z: p.z, vx: g.vel.x, vz: g.vel.z, moved: Math.hypot(p.x - x0, p.z - z0), clr: clearance(), inside: inWall() })
    }
  }
  const spd = (s) => Math.hypot(s.vx, s.vz)
  const round = (v, d = 3) => Math.round(v * 10 ** d) / 10 ** d

  // a stretch of the main street with nothing in it, to measure on
  function clearStart() {
    for (let z = -20; z > -280; z -= 5) {
      const ok = !g.colliders.some((c) => Math.abs(c.x) < 2.6 && c.z < z + 4 && c.z > z - 45) && !g.walls.some((w) => w.x1 > -2.6 && w.x0 < 2.6 && w.z1 > z - 45 && w.z0 < z + 4)
      if (ok) return z
    }
    return null
  }
  const z0 = clearStart(), out = { clearStartZ: z0 }

  // 1. accelerating from rest, run and walk
  for (const [name, walk] of [['run', false], ['walk', true]]) {
    reset(0, z0); push(0, -1, walk); const rec = []; step(1 / 60, 180, rec)
    const fin = spd(rec[rec.length - 1]), t90 = rec.findIndex((s) => spd(s) >= 0.9 * fin) / 60, t50 = rec.findIndex((s) => spd(s) >= 0.5 * fin) / 60
    out['accel_' + name] = { topSpeed: round(fin, 2), t50: round(t50, 3), t90: round(t90, 3), distIn1s: round(z0 - rec[59].z, 2) }
  }
  // 2. stopping from a run
  reset(0, z0); push(0, -1); step(1 / 60, 150); const zRel = p.z; push(0, 0); { const rec = []; step(1 / 60, 120, rec)
    out.stop = { stopDist: round(zRel - p.z, 2), tTo0_5: round(rec.findIndex((s) => spd(s) < 0.5) / 60, 3), tTo5pc: round(rec.findIndex((s) => spd(s) < 0.05 * 10.44) / 60, 3) } }
  // 3. 90 degree turn at a run (forward, then straight right)
  reset(0, z0); push(0, -1); step(1 / 60, 90); const tx = p.x, tz = p.z; push(1, 0); { const rec = []; step(1 / 60, 120, rec)
    const head = (s) => Math.atan2(s.vz, s.vx) // heading; target is 0 (+x)
    const turned = rec.findIndex((s) => Math.abs(head(s)) < 10 * Math.PI / 180)
    out.turn90 = { tTo10deg: round(turned / 60, 3), minSpeedDuring: round(Math.min(...rec.slice(0, Math.max(turned, 1)).map(spd)), 2), sideStep: round(Math.abs(p.x - tx), 2) } }
  // 4. dt independence: same 3 s of input at different frame rates
  { const runs = {}
    for (const [label, dt] of [['60', 1 / 60], ['30', 1 / 30], ['20', 1 / 20], ['10', 0.1]]) { reset(0, z0); push(0, -1); step(dt, Math.round(3 / dt)); runs[label] = { dist: round(z0 - p.z, 2), speed: round(Math.hypot(g.vel.x, g.vel.z), 2) } }
    out.dtIndependence = runs; out.dtDrift = round(Math.max(...Object.values(runs).map((r) => Math.abs(r.dist - runs['60'].dist))), 2) }
  // 5. thin wall at run speed, swept over start phases and frame rates
  { const res = {}
    for (const [label, dt] of [['60', 1 / 60], ['30', 1 / 30], ['10', 0.1]]) {
      let tunnels = 0, trials = 0
      for (let ph = 0; ph < 20; ph++) {
        const wz = z0 - 14 - ph * 0.05, thin = { x0: -3, x1: 3, z0: wz, z1: wz + 0.08, cover: false }
        g.walls.push(thin); reset(0, z0); push(0, -1); step(dt, Math.round(2.2 / dt)); g.walls.pop(); trials++
        if (p.z < wz) tunnels++
      }
      res[label] = tunnels + '/' + trials
    }
    out.thinWallTunnelled = res }
  // 6. running diagonally into a building face and sliding along it
  { const face = g.walls.filter((w) => w.x0 > 5 && w.x0 < 9 && w.z1 - w.z0 > 6).sort((a, b) => b.z1 - b.z0 - (a.z1 - a.z0))[0]
    let zs = null; if (face) for (let z = face.z1 - 3; z > face.z0 + 12; z -= 1) { if (!g.colliders.some((c) => c.x > face.x0 - 6 && c.x < face.x0 + 0.5 && c.z < z + 1 && c.z > z - 14)) { zs = z; break } }
    if (face && zs !== null) { reset(face.x0 - 4, zs); push(1, -1); const rec = []; step(1 / 60, 150, rec)
      const hit = rec.findIndex((s) => s.clr < 0.02), after = rec.slice(hit + 15)
      let flips = 0; for (let i = 1; i < after.length; i++) if (after[i].vx * after[i - 1].vx < 0 && Math.abs(after[i].vx) > 0.05 && Math.abs(after[i - 1].vx) > 0.05) flips++
      out.wallSlide = { slideSpeed: round(after.reduce((a, s) => a + spd(s), 0) / after.length, 2), minClearance: round(Math.min(...rec.map((s) => s.clr)), 3), insideFrames: rec.filter((s) => s.inside).length, vxSignFlips: flips, maxAbsVxAfterContact: round(Math.max(...after.map((s) => Math.abs(s.vx))), 2) } } }
  // 7. inside corners: every place two walls make an L, approached on the diagonal at a run
  { const corners = [], eps = 0.02
    for (const a of g.walls) for (const b of g.walls) { if (a === b) continue
      for (const X of [a.x0, a.x1]) for (const Z of [b.z0, b.z1]) {
        if (!(Z >= a.z0 - eps && Z <= a.z1 + eps && X >= b.x0 - eps && X <= b.x1 + eps)) continue
        const sx = X === a.x0 ? -1 : 1, sz = Z === b.z0 ? -1 : 1
        if (X === a.x0 && X === a.x1) continue
        const free = (d) => !g.walls.some((w) => insideRect(X + sx * d, Z + sz * d, w)) && !g.colliders.some((c) => Math.hypot(X + sx * d - c.x, Z + sz * d - c.z) < c.r + 0.6)
        if (free(0.7) && free(2) && free(3.5) && Math.abs(X) < 30 && Z < 10 && Z > -295) corners.push({ X, Z, sx, sz })
      } }
    const seen = new Set(), uniq = corners.filter((c) => { const k = c.X.toFixed(2) + ',' + c.Z.toFixed(2) + ',' + c.sx + c.sz; if (seen.has(k)) return false; seen.add(k); return true })
    const sample = uniq.filter((_, i) => i % Math.max(1, Math.floor(uniq.length / 14)) === 0).slice(0, 14)
    let inside = 0, minClr = 1e9, jitterSum = 0, jitterMax = 0, stuckFar = 0
    for (const c of sample) { reset(c.X + c.sx * 3.2, c.Z + c.sz * 3.2); push(-c.sx, -c.sz); const rec = []; step(1 / 60, 150, rec)
      const tail = rec.slice(-60); let j = 0, jm = 0; for (const s of tail) { j += s.moved; jm = Math.max(jm, s.moved) }
      inside += rec.filter((s) => s.inside).length; minClr = Math.min(minClr, ...rec.map((s) => s.clr)); jitterSum += j / tail.length; jitterMax = Math.max(jitterMax, jm)
      if (Math.hypot(p.x - c.X, p.z - c.Z) > 1.2) stuckFar++ }
    out.insideCorners = { found: uniq.length, tested: sample.length, framesInsideWall: inside, minClearance: round(minClr, 3), restingJitterPerFrame: round(jitterSum / Math.max(1, sample.length), 5), restingJitterMax: round(jitterMax, 4), neverReachedCorner: stuckFar } }
  // 7b. a made-up inside corner in the clear lane (the street has very few real ones), run into on the diagonal at several frame rates
  { const res = {}
    for (const [label, dt] of [['60', 1 / 60], ['30', 1 / 30], ['10', 0.1]]) {
      const zc = z0 - 20, A = { x0: 1, x1: 5, z0: zc - 8, z1: zc + 8, cover: false }, B = { x0: -6, x1: 5, z0: zc - 12, z1: zc - 8, cover: false }
      g.walls.push(A, B); reset(-2.2, zc - 4.8); push(1, -1); const rec = []; step(dt, Math.round(2 / dt), rec); g.walls.pop(); g.walls.pop()
      const tail = rec.slice(-Math.round(0.6 / dt)); let j = 0; for (const s of tail) j += s.moved / dt
      res[label] = { minClearance: round(Math.min(...rec.map((s) => s.clr)), 3), insideFrames: rec.filter((s) => s.inside).length, restingSpeed: round(j / tail.length, 3), distToCorner: round(Math.hypot(p.x - 1, p.z - (zc - 8)), 2) } }
    out.syntheticCorner = res }
  // 8. camera: where the player sits on screen and how far ahead the view is centred
  { const proj = () => { const v = new g.camera.position.constructor(p.x, 1.6, p.z).project(g.camera); return v }
    const ahead = () => { const d = new g.camera.position.constructor(); g.camera.getWorldDirection(d); if (d.y > -1e-3) return NaN; const t = (1.6 - g.camera.position.y) / d.y; return { x: g.camera.position.x + d.x * t, z: g.camera.position.z + d.z * t } }
    reset(0, z0); step(1 / 60, 30); const idle = proj(), ia = ahead(), idleLA = p.z - ia.z
    push(0, -1); step(1 / 60, 120); const run = proj(), ra = ahead()
    out.camera = { idleNdcY: round(idle.y, 3), runNdcY: round(run.y, 3), runLookAheadM: round(p.z - ra.z, 2), idleLookAheadM: round(idleLA, 2), camToPlayerAtRun: round(Math.hypot(g.camera.position.x - p.x, g.camera.position.z - p.z), 2) } }
  reset(0, z0); g.stick.x = g.stick.y = 0
  return out
})

console.log(JSON.stringify(results, null, 2))
if (errors.length) console.log('PAGE ERRORS:', errors)
if (OUT) writeFileSync(OUT, JSON.stringify(results, null, 2))
if (BASE) {
  const base = JSON.parse(readFileSync(BASE, 'utf8'))
  const flat = (o, pre = '') => Object.entries(o).flatMap(([k, v]) => v && typeof v === 'object' ? flat(v, pre + k + '.') : [[pre + k, v]])
  const b = Object.fromEntries(flat(base))
  console.log('\nmetric'.padEnd(36) + 'before'.padEnd(12) + 'after')
  for (const [k, v] of flat(results)) console.log(k.padEnd(36) + String(b[k]).padEnd(12) + String(v) + (b[k] !== v ? '   <-' : ''))
}
await browser.close()
