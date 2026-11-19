import json
paths=open('logo_paths.json').read()
html=r'''<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Shafi Consultancy Logo Motion</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="3D animated Shafi Consultancy emblem: particles assemble the disc, the three bands sweep into place, then it floats inside orbit rings.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
  /* Single deliberate dark stage, matching the showcase hero. Brand red #BE1E2D is the only colour. */
  :root { --ink: #0B0F19; --text: #F4F7FB; --muted: #9AA6BC; --line: rgba(255,255,255,.14); --red: #BE1E2D; color-scheme: dark; }
  html, body { height: 100%; margin: 0; }
  body { background: radial-gradient(90% 80% at 50% 45%, #141B2C 0%, var(--ink) 62%); background-color: var(--ink); color: var(--text); font-family: 'IBM Plex Sans', system-ui, sans-serif; overflow: hidden; }
  body.clear { background: transparent; }
  #stage { position: fixed; inset: 0; width: 100%; height: 100%; display: block; cursor: grab; touch-action: none; }
  #stage:active { cursor: grabbing; }
  .ui { position: fixed; left: 0; right: 0; bottom: 0; display: flex; justify-content: space-between; align-items: center; gap: 16px;
        padding: 0 max(20px, env(safe-area-inset-right, 0px)) calc(20px + env(safe-area-inset-bottom, 0px)) max(20px, env(safe-area-inset-left, 0px)); pointer-events: none; }
  .hint { font: 11.5px 'JetBrains Mono', monospace; letter-spacing: .14em; text-transform: uppercase; color: var(--muted); }
  .btn { pointer-events: auto; display: inline-flex; align-items: center; gap: 8px; min-height: 44px; padding: 0 18px; border-radius: 12px; border: 1px solid var(--line);
         background: rgba(255,255,255,.04); color: var(--text); font: 500 14px 'IBM Plex Sans', sans-serif; cursor: pointer; backdrop-filter: blur(8px);
         transition: border-color .25s, transform .3s cubic-bezier(.16,1,.3,1); }
  .btn:hover { border-color: rgba(190,30,45,.8); transform: translateY(-2px); }
  .btn:focus-visible { outline: 2px solid #fff; outline-offset: 3px; }
  .btn svg { width: 16px; height: 16px; }
  body.render .ui { display: none; }
  .nogl { position: fixed; inset: 0; display: grid; place-items: center; color: var(--muted); padding: 24px; text-align: center; }
</style>
</head>
<body>
<canvas id="stage" role="img" aria-label="Animated 3D Shafi Consultancy emblem: a red disc with three white bands, surrounded by orbit rings"></canvas>
<div class="ui">
  <span class="hint">Move or drag to tilt</span>
  <button class="btn" id="replay" type="button"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/></svg>Replay</button>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
(function () {
  'use strict';
  var LOGO = __PATHS__;
  var Q = new URLSearchParams(location.search);
  var RENDER = Q.has('render'), CLEAR = Q.get('bg') === 'none';
  var RM = !RENDER && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (RENDER) document.body.classList.add('render');
  if (CLEAR) document.body.classList.add('clear');
  if (typeof THREE === 'undefined') { document.body.insertAdjacentHTML('beforeend', '<p class="nogl">The animation needs WebGL, which is not available here.</p>'); return; }

  var RED = new THREE.Color(LOGO.color);
  function rng(s) { return function () { s |= 0; s = s + 0x6D2B79F5 | 0; var t = Math.imul(s ^ s >>> 15, 1 | s); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function seg(t, a, b) { return clamp((t - a) / (b - a), 0, 1); }
  var eOut = function (x) { return 1 - Math.pow(1 - x, 3); };
  var eIO = function (x) { return x < .5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; };
  var eBack = function (x) { var c1 = 1.4, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); };

  var canvas = document.getElementById('stage');
  var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true, preserveDrawingBuffer: RENDER });
  renderer.setPixelRatio(RENDER ? 1 : Math.min(window.devicePixelRatio || 1, 2));
  renderer.setClearColor(0x000000, 0);
  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(35, 1, .1, 100);
  camera.position.set(0, 0, 7.4);

  /* lights */
  scene.add(new THREE.AmbientLight(0xffffff, .5));
  var key = new THREE.DirectionalLight(0xffffff, .6); key.position.set(2.5, 3, 5); scene.add(key);
  var rim = new THREE.DirectionalLight(0xffe2e2, .35); rim.position.set(-4, -2, -3); scene.add(rim);
  var sheen = new THREE.PointLight(0xffffff, 0, 9); sheen.position.set(-4, 1.2, 2.4); scene.add(sheen);

  function sprite() {
    var c = document.createElement('canvas'); c.width = c.height = 64; var g = c.getContext('2d'), gr = g.createRadialGradient(32, 32, 0, 32, 32, 32);
    gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(.3, 'rgba(255,255,255,.7)'); gr.addColorStop(1, 'rgba(255,255,255,0)');
    g.fillStyle = gr; g.fillRect(0, 0, 64, 64); return new THREE.CanvasTexture(c);
  }
  var SPR = sprite();

  /* ---------- emblem geometry from traced paths ---------- */
  var root = new THREE.Group(); scene.add(root);
  var emblem = new THREE.Group(); root.add(emblem);
  var disc = new THREE.Shape(); disc.absarc(0, 0, 1, 0, Math.PI * 2, false);
  LOGO.bands.forEach(function (pts) { var h = new THREE.Path(); h.moveTo(pts[0][0], pts[0][1]); for (var i = 1; i < pts.length; i++) h.lineTo(pts[i][0], pts[i][1]); h.closePath(); disc.holes.push(h); });
  var dGeo = new THREE.ExtrudeGeometry(disc, { depth: .16, bevelEnabled: true, bevelThickness: .035, bevelSize: .022, bevelSegments: 4, curveSegments: 160 });
  dGeo.translate(0, 0, -.08);
  var dMat = new THREE.MeshPhysicalMaterial({ color: RED, metalness: .12, roughness: .34, clearcoat: .9, clearcoatRoughness: .2, transparent: true, opacity: 0 });
  var discMesh = new THREE.Mesh(dGeo, dMat); emblem.add(discMesh);

  var bands = LOGO.bands.map(function (pts, i) {
    var cx = 0, cy = 0; pts.forEach(function (p) { cx += p[0]; cy += p[1]; }); cx /= pts.length; cy /= pts.length;
    var s = new THREE.Shape(); s.moveTo(pts[0][0] - cx, pts[0][1] - cy); for (var k = 1; k < pts.length; k++) s.lineTo(pts[k][0] - cx, pts[k][1] - cy); s.closePath();
    var g = new THREE.ExtrudeGeometry(s, { depth: .12, bevelEnabled: true, bevelThickness: .022, bevelSize: .01, bevelSegments: 3 });
    g.translate(0, 0, -.04);
    var m = new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: .28, clearcoat: 1, clearcoatRoughness: .15, emissive: 0xffffff, emissiveIntensity: .25, transparent: true, opacity: 0 });
    var mesh = new THREE.Mesh(g, m), grp = new THREE.Group(); grp.add(mesh); grp.userData = { cx: cx, cy: cy, i: i };
    emblem.add(grp); return grp;
  });

  var glowMat = new THREE.SpriteMaterial({ map: SPR, color: RED, transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending });
  var glow = new THREE.Sprite(glowMat); glow.scale.set(4.6, 4.6, 1); glow.position.z = -.6; root.add(glow);

  /* ---------- assembling particles (sampled from the logo itself) ---------- */
  function inPoly(x, y, pts) { var c = false; for (var i = 0, j = pts.length - 1; i < pts.length; j = i++) { var xi = pts[i][0], yi = pts[i][1], xj = pts[j][0], yj = pts[j][1]; if (((yi > y) !== (yj > y)) && (x < (xj - xi) * (y - yi) / (yj - yi) + xi)) c = !c; } return c; }
  var R1 = rng(17), NP = window.innerWidth < 700 && !RENDER ? 1400 : 2400;
  var pStart = new Float32Array(NP * 3), pEnd = new Float32Array(NP * 3), pPos = new Float32Array(NP * 3), pCol = new Float32Array(NP * 3), pDel = new Float32Array(NP);
  var WHITE = new THREE.Color(0xffffff);
  for (var n = 0; n < NP; n++) {
    var x, y; do { x = R1() * 2 - 1; y = R1() * 2 - 1; } while (x * x + y * y > 1);
    var w = LOGO.bands.some(function (b) { return inPoly(x, y, b); }), c = w ? WHITE : RED;
    pEnd[n * 3] = x; pEnd[n * 3 + 1] = y; pEnd[n * 3 + 2] = .13;
    var th = R1() * Math.PI * 2, ph = Math.acos(2 * R1() - 1), rr = 4 + R1() * 4;
    pStart[n * 3] = Math.sin(ph) * Math.cos(th) * rr; pStart[n * 3 + 1] = Math.sin(ph) * Math.sin(th) * rr * .7; pStart[n * 3 + 2] = Math.cos(ph) * rr - 1;
    pCol[n * 3] = c.r; pCol[n * 3 + 1] = c.g; pCol[n * 3 + 2] = c.b;
    pDel[n] = .05 + R1() * .75 + (1 - Math.sqrt(x * x + y * y)) * .25;
  }
  var pGeo = new THREE.BufferGeometry(); pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3)); pGeo.setAttribute('color', new THREE.BufferAttribute(pCol, 3));
  var pMat = new THREE.PointsMaterial({ size: .075, map: SPR, vertexColors: true, transparent: true, depthWrite: false });
  var particles = new THREE.Points(pGeo, pMat); emblem.add(particles);

  /* ---------- orbit rings + particle shell ---------- */
  function ringLine(r, color, op) {
    var pts = []; for (var a = 0; a <= 256; a++) { var t = a / 256 * Math.PI * 2; pts.push(new THREE.Vector3(Math.cos(t) * r, Math.sin(t) * r, 0)); }
    var l = new THREE.Line(new THREE.BufferGeometry().setFromPoints(pts), new THREE.LineBasicMaterial({ color: color, transparent: true, opacity: op, depthWrite: false }));
    l.userData.op = op; return l;
  }
  var ringA = ringLine(1.62, 0xffffff, .45), ringB = ringLine(1.9, RED.getHex(), .8);
  var ringAG = new THREE.Group(), ringBG = new THREE.Group(); ringAG.add(ringA); ringBG.add(ringB);
  ringAG.rotation.set(1.18, .2, .35); ringBG.rotation.set(-1.02, -.25, -.6);
  root.add(ringAG, ringBG);
  function orb(color, s) { var o = new THREE.Sprite(new THREE.SpriteMaterial({ map: SPR, color: color, transparent: true, opacity: 0, depthWrite: false, blending: THREE.AdditiveBlending })); o.scale.set(s, s, 1); return o; }
  var orbA = orb(0xffffff, .2), orbB = orb(0xff4d5a, .24); ringA.add(orbA); ringB.add(orbB);

  var SH = 520, sPos = new Float32Array(SH * 3), sCol = new Float32Array(SH * 3), ga = Math.PI * (3 - Math.sqrt(5)), R2 = rng(5);
  for (var s = 0; s < SH; s++) {
    var yy = 1 - s / (SH - 1) * 2, rad = Math.sqrt(1 - yy * yy), t2 = ga * s, k = 2.45 + R2() * .25;
    sPos[s * 3] = Math.cos(t2) * rad * k; sPos[s * 3 + 1] = yy * k; sPos[s * 3 + 2] = Math.sin(t2) * rad * k;
    var cc = R2() < .55 ? RED : WHITE, b = .5 + R2() * .5; sCol[s * 3] = cc.r * b; sCol[s * 3 + 1] = cc.g * b; sCol[s * 3 + 2] = cc.b * b;
  }
  var sGeo = new THREE.BufferGeometry(); sGeo.setAttribute('position', new THREE.BufferAttribute(sPos, 3)); sGeo.setAttribute('color', new THREE.BufferAttribute(sCol, 3));
  var sMat = new THREE.PointsMaterial({ size: .05, map: SPR, vertexColors: true, transparent: true, opacity: 0, depthWrite: false });
  var shell = new THREE.Points(sGeo, sMat); root.add(shell);

  /* ---------- timeline ---------- */
  function setOpacity(mat, o) { var tr = o < .999; if (mat.transparent !== tr) { mat.transparent = tr; mat.needsUpdate = true; } mat.opacity = o; }
  var mouse = { x: 0, y: 0, tx: 0, ty: 0 }, drag = { on: false, x: 0, y: 0, rx: 0, ry: 0 };

  function update(t) {
    /* 1 · particles converge (0 → 2.1 s), then dissolve into the solid emblem */
    var conv = 0;
    for (var i = 0; i < NP; i++) {
      var p = eIO(seg(t, pDel[i], pDel[i] + 1.25)), sw = (1 - p) * 1.6, i3 = i * 3;
      var sx = pStart[i3], sy = pStart[i3 + 1], cs = Math.cos(sw), sn = Math.sin(sw);
      var rx = sx * cs - sy * sn, ry = sx * sn + sy * cs;
      pPos[i3] = rx + (pEnd[i3] - rx) * p; pPos[i3 + 1] = ry + (pEnd[i3 + 1] - ry) * p; pPos[i3 + 2] = pStart[i3 + 2] + (pEnd[i3 + 2] - pStart[i3 + 2]) * p;
      conv += p;
    }
    pGeo.attributes.position.needsUpdate = true;
    var solid = eOut(seg(t, 1.55, 2.45));
    pMat.opacity = 1 - eOut(seg(t, 1.9, 2.7)); particles.visible = pMat.opacity > .001;
    pMat.size = .075 + .02 * Math.sin(seg(t, 1.6, 2.4) * Math.PI);

    /* 2 · disc solidifies */
    setOpacity(dMat, solid);
    discMesh.scale.setScalar(.94 + .06 * solid);
    glowMat.opacity = .2 * solid * (1 + .12 * Math.sin(t * 1.8));

    /* 3 · bands sweep in, staggered */
    bands.forEach(function (g, i) {
      var a = seg(t, 2.0 + i * .24, 3.15 + i * .24), e = eBack(a), o = eOut(a), u = g.userData, dir = i % 2 ? -1 : 1;
      g.position.set(u.cx * (1 + (1 - o) * .5), u.cy * (1 + (1 - o) * .5), (1 - e) * 1.8);
      g.rotation.set((1 - e) * 1.25 * dir, (1 - e) * -.6 * dir, (1 - e) * .7);
      g.scale.setScalar(.7 + .3 * e);
      setOpacity(g.children[0].material, o);
    });

    /* 4 · rings draw on, shell appears, light sweep */
    var ra = eIO(seg(t, 2.9, 4.1)), rb = eIO(seg(t, 3.15, 4.4));
    ringA.geometry.setDrawRange(0, Math.floor(257 * ra)); ringB.geometry.setDrawRange(0, Math.floor(257 * rb));
    ringA.material.opacity = ringA.userData.op * Math.min(1, ra * 3); ringB.material.opacity = ringB.userData.op * Math.min(1, rb * 3);
    var oa = t * .9, ob = -t * .7 + 2;
    orbA.position.set(Math.cos(oa) * 1.62, Math.sin(oa) * 1.62, 0); orbB.position.set(Math.cos(ob) * 1.9, Math.sin(ob) * 1.9, 0);
    orbA.material.opacity = seg(t, 3.9, 4.4); orbB.material.opacity = seg(t, 4.1, 4.6);
    sMat.opacity = .55 * eOut(seg(t, 3.2, 4.4));
    shell.rotation.y = t * .06; shell.rotation.x = Math.sin(t * .2) * .1;
    ringAG.rotation.z = .35 + t * .05; ringBG.rotation.z = -.6 - t * .04;

    var sweep = seg(t, 3.7, 5.1);
    if (t < 5.1) { sheen.position.set(-4.2 + 8.4 * eIO(sweep), 1.4 - 1.2 * sweep, 2.2); sheen.intensity = 1.1 * Math.sin(sweep * Math.PI); }
    else { var q = (t - 5.1) * .35; sheen.position.set(Math.sin(q) * 3.6, 1 + Math.cos(q * .7) * .6, 2.4); sheen.intensity = .3; }

    /* 5 · idle float + pointer tilt */
    var intro = eOut(seg(t, 1.6, 2.9)), idle = seg(t, 4.2, 5.4);
    mouse.x += (mouse.tx - mouse.x) * .06; mouse.y += (mouse.ty - mouse.y) * .06;
    var tt = Math.max(0, t - 4.2);
    emblem.rotation.y = (1 - intro) * -.9 + idle * .3 * Math.sin(tt * .55) + mouse.x * .45 + drag.ry;
    emblem.rotation.x = idle * .07 * Math.sin(tt * .42) - mouse.y * .3 + drag.rx;
    root.position.y = idle * .06 * Math.sin(tt * .9);
    root.rotation.y = mouse.x * .12; root.rotation.x = -mouse.y * .08;
  }

  function resize() {
    var w = window.innerWidth, h = window.innerHeight; renderer.setSize(w, h, false);
    camera.aspect = w / h; camera.position.z = w / h < .8 ? 7.4 / (w / h) * .8 : 7.4; camera.updateProjectionMatrix();
  }
  resize(); window.addEventListener('resize', resize);

  var start = performance.now(), FINAL = 5.6;
  window.__renderAt = function (t) { update(t); renderer.render(scene, camera); return true; };
  if (RENDER) { update(0); renderer.render(scene, camera); window.__ready = true; return; }

  window.addEventListener('pointermove', function (e) {
    mouse.tx = (e.clientX / window.innerWidth) * 2 - 1; mouse.ty = -((e.clientY / window.innerHeight) * 2 - 1);
    if (drag.on) { drag.ry += (e.clientX - drag.x) * .006; drag.rx += (e.clientY - drag.y) * .004; drag.x = e.clientX; drag.y = e.clientY; drag.rx = clamp(drag.rx, -.8, .8); }
  }, { passive: true });
  canvas.addEventListener('pointerdown', function (e) { drag.on = true; drag.x = e.clientX; drag.y = e.clientY; });
  window.addEventListener('pointerup', function () { drag.on = false; });
  document.getElementById('replay').addEventListener('click', function () { start = performance.now(); drag.rx = drag.ry = 0; if (RM) frame(); });

  function frame() {
    var t = RM ? FINAL : (performance.now() - start) / 1000;
    if (!drag.on) { drag.rx *= .96; drag.ry *= .96; }
    update(t); renderer.render(scene, camera);
    if (!RM && !document.hidden) requestAnimationFrame(frame);
  }
  document.addEventListener('visibilitychange', function () { if (!document.hidden && !RM) requestAnimationFrame(frame); });
  frame();
})();
</script>
</body>
</html>
'''
open('shafi-consultancy-logo-animation.html','w').write(html.replace('__PATHS__',paths))
print('ok')
