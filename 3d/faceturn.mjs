// Character-facing playtest: how the main character's body turns when you change direction (rotation.y of the player group), at a fixed 1/60 s step.
//   python -m http.server 8935 (repo root)      node 3d/faceturn.mjs [--out a.json] [--base b.json]
import { createRequire } from 'node:module'
import { readFileSync, writeFileSync } from 'node:fs'
const require = createRequire(import.meta.url)
const { chromium } = require(process.env.PLAYWRIGHT_CORE || 'C:/Users/16193/panchos-bodega/scripts/audit/node_modules/playwright-core')
const arg = (n, d) => { const i = process.argv.indexOf('--' + n); return i > 0 ? process.argv[i + 1] : d }
const URL_ = arg('url', 'http://localhost:8935/3d/index.html?tier=0'), OUT = arg('out', null), BASE = arg('base', null)
const browser = await chromium.launch({ channel: 'msedge', headless: true, args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] })
const page = await browser.newPage({ viewport: { width: 700, height: 420 } }); const errors = []
page.on('pageerror', (e) => errors.push(String(e)))
await page.goto(URL_ + '&cb=' + Date.now(), { waitUntil: 'domcontentloaded' })
await page.waitForFunction(() => window.__g && window.__g.walls, null, { timeout: 60000 })
const res = await page.evaluate(() => {
  const g = window.__g, p = g.player.position, DT = 1 / 60
  g.start(); g.skipIntro()
  const calm = () => { g.hunt.setHeat(0); for (const e of g.hunt.enemies) e.dead = true }
  const unwrap = (() => { let prev = null, acc = 0; return (a) => { if (prev === null) { prev = a; acc = a; return acc } let d = a - prev; while (d > Math.PI) d -= 2 * Math.PI; while (d < -Math.PI) d += 2 * Math.PI; prev = a; acc += d; return acc } })
  function scenario(z, warm, turn, secs) {
    p.set(0, 0, z); g.vel.set(0, 0, 0); g.stick.x = g.stick.y = 0; g.stick.id = null; g.yaw = 0
    for (let i = 0; i < 120; i++) { calm(); g.update(DT) }
    g.stick.x = warm[0]; g.stick.y = warm[1]; for (let i = 0; i < 70; i++) { calm(); g.update(DT) }
    const un = unwrap(), rec = [], a0 = un(g.player.rotation.y); g.stick.x = turn[0]; g.stick.y = turn[1]
    for (let i = 0; i < Math.round(secs / DT); i++) { calm(); g.update(DT); rec.push({ t: (i + 1) * DT, a: un(g.player.rotation.y) }) }
    const total = rec[rec.length - 1].a - a0, prog = (r) => (r.a - a0) / (total || 1)
    let wMax = 0, aMax = 0, pw = 0, over = 0
    for (let i = 1; i < rec.length; i++) { const w = (rec[i].a - rec[i - 1].a) / DT; wMax = Math.max(wMax, Math.abs(w)); aMax = Math.max(aMax, Math.abs(w - pw) / DT); pw = w; over = Math.max(over, Math.abs(rec[i].a - a0) - Math.abs(total)) }
    const t10 = rec.find((r) => prog(r) >= 0.1), t50 = rec.find((r) => prog(r) >= 0.5), t90 = rec.find((r) => prog(r) >= 0.9), r2 = (v, d = 3) => Math.round(v * 10 ** d) / 10 ** d
    return { turnDeg: r2(Math.abs(total) * 180 / Math.PI, 0), t10: t10 ? r2(t10.t) : null, t50: t50 ? r2(t50.t) : null, t90: t90 ? r2(t90.t) : null, peakDegPerS: r2(wMax * 180 / Math.PI, 0), peakAccelKDegPerS2: r2(aMax * 180 / Math.PI / 1000, 1), overshootDeg: r2(Math.max(0, over) * 180 / Math.PI, 1) }
  }
  const out = {}
  out.run_then_right = scenario(-105, [0, 1], [1, 0], 1.2)
  out.run_then_back = scenario(-105, [0, 1], [0, -1], 1.4)
  out.run_then_left = scenario(-105, [0, 1], [-1, 0], 1.2)
  // stop: how the body settles, plus whether dust puffs fire again after the first one (they should every push-off)
  return out
})
console.log(JSON.stringify(res, null, 2)); if (errors.length) console.log('PAGE ERRORS:', errors)
if (OUT) writeFileSync(OUT, JSON.stringify(res, null, 2))
if (BASE) { const b = JSON.parse(readFileSync(BASE, 'utf8')); const flat = (o, p = '') => Object.entries(o).flatMap(([k, v]) => v && typeof v === 'object' ? flat(v, p + k + '.') : [[p + k, v]]); const bb = Object.fromEntries(flat(b))
  console.log('\nmetric'.padEnd(40) + 'before'.padEnd(12) + 'after'); for (const [k, v] of flat(res)) console.log(k.padEnd(40) + String(bb[k]).padEnd(12) + String(v) + (bb[k] !== v ? '  <-' : '')) }
await browser.close()
