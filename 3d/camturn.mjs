// Camera-turn playtest: how long the camera takes to come round at a corner, and how smoothly. Drives window.__g.update() at a fixed dt (works in a hidden tab),
// does NOT pin the yaw (playtest.mjs does), holds input through __g.stick and records the camera yaw every frame.
//   python -m http.server 8935     (repo root)       node 3d/camturn.mjs [--out a.json] [--base b.json]
import { createRequire } from 'node:module'
import { readFileSync, writeFileSync } from 'node:fs'
const require = createRequire(import.meta.url)
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'C:/Users/16193/panchos-bodega/scripts/audit/node_modules/playwright-core')
const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i > 0 ? process.argv[i + 1] : d }
const URL_ = arg('url', 'http://localhost:8935/3d/index.html?tier=0'), OUT = arg('out', null), BASE = arg('base', null)
const browser = await chromium.launch({ channel: 'msedge', headless: true, args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] })
const page = await browser.newPage({ viewport: { width: 900, height: 500 } }); const errors = []
page.on('pageerror', (e) => errors.push(String(e)))
await page.goto(URL_ + '&cb=' + Date.now(), { waitUntil: 'domcontentloaded' })
await page.waitForFunction(() => window.__g && window.__g.walls, null, { timeout: 60000 })
const res = await page.evaluate(() => {
  const g = window.__g, p = g.player.position, DT = 1 / 60
  g.start(); g.skipIntro()
  const calm = () => { g.hunt.setHeat(0); for (const e of g.hunt.enemies) e.dead = true }
  const unwrap = (() => { let prev = null, acc = 0; return (a) => { if (prev === null) { prev = a; acc = a; return acc } let d = a - prev; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI; prev = a; acc += d; return acc } })
  function scenario(name, x, z, yaw0, warm, inputs, secs) {
    p.set(x, 0, z); g.vel.set(0, 0, 0); g.stick.x = g.stick.y = 0; g.stick.id = null; g.yaw = yaw0
    for (const k in g.keys) g.keys[k] = false
    for (let i = 0; i < 120; i++) { calm(); g.update(DT) }                       // settle the camera, let lookIdle pass its 0.25 s gate
    g.stick.x = warm[0]; g.stick.y = warm[1]
    for (let i = 0; i < 70; i++) { calm(); g.update(DT) }                         // run up to speed
    const un = unwrap(), rec = [], y0 = un(g.yaw); let t = 0
    g.stick.x = inputs[0]; g.stick.y = inputs[1]                                  // the turn
    for (let i = 0; i < Math.round(secs / DT); i++) {
      calm(); g.update(DT); t += DT
      const cam = g.camera.position; rec.push({ t, yaw: un(g.yaw), cx: cam.x, cz: cam.z, px: p.x, pz: p.z })
    }
    const total = rec[rec.length - 1].yaw - y0, sgn = Math.sign(total) || 1
    const prog = (r) => (r.yaw - y0) / (total || 1)
    const first = rec.find((r) => Math.abs(r.yaw - y0) > 0.035), t10 = rec.find((r) => prog(r) >= 0.1), t90 = rec.find((r) => prog(r) >= 0.9)
    let wMax = 0, aMax = 0, camV = 0, prevW = 0, camVmax = 0, camAmax = 0, pvc = 0
    for (let i = 1; i < rec.length; i++) {
      const w = (rec[i].yaw - rec[i - 1].yaw) / DT; wMax = Math.max(wMax, Math.abs(w)); aMax = Math.max(aMax, Math.abs(w - prevW) / DT); prevW = w
      const v = Math.hypot(rec[i].cx - rec[i - 1].cx, rec[i].cz - rec[i - 1].cz) / DT; camVmax = Math.max(camVmax, v); camAmax = Math.max(camAmax, Math.abs(v - pvc) / DT); pvc = v
    }
    const r2 = (v, d = 3) => Math.round(v * 10 ** d) / 10 ** d
    return { turnDeg: r2(Math.abs(total) * 180 / Math.PI, 1), startDelayS: first ? r2(first.t) : null, t10: t10 ? r2(t10.t) : null, t90: t90 ? r2(t90.t) : null,
      peakDegPerS: r2(wMax * 180 / Math.PI, 0), peakAccelKiloDegPerS2: r2(aMax * 180 / Math.PI / 1000, 1), camSpeedPeak: r2(camVmax, 1), camAccelPeak: r2(camAmax, 0) }
  }
  const out = {}
  const gz = -88                                                                  // a cross street
  out.rightIntoCrossStreet = scenario('r', 0, gz + 10, 0, [0, 1], [1, 0], 2.0)    // running forward, then hard right
  out.leftIntoCrossStreet = scenario('l', 0, gz + 10, 0, [0, 1], [-1, 0], 2.0)
  out.uTurn = scenario('u', 0, -105, 0, [0, 1], [0, -1], 2.0)                     // running forward, then back the way you came
  out.diagonalRight = scenario('d', 0, -105, 0, [0, 1], [0.7, 0.7], 2.0)          // a gentle bend
  return out
})
console.log(JSON.stringify(res, null, 2)); if (errors.length) console.log('PAGE ERRORS:', errors)
if (OUT) writeFileSync(OUT, JSON.stringify(res, null, 2))
if (BASE) { const b = JSON.parse(readFileSync(BASE, 'utf8')); const flat = (o, p = '') => Object.entries(o).flatMap(([k, v]) => v && typeof v === 'object' ? flat(v, p + k + '.') : [[p + k, v]]); const bb = Object.fromEntries(flat(b))
  console.log('\nmetric'.padEnd(46) + 'before'.padEnd(12) + 'after'); for (const [k, v] of flat(res)) console.log(k.padEnd(46) + String(bb[k]).padEnd(12) + String(v) + (bb[k] !== v ? '  <-' : '')) }
await browser.close()
