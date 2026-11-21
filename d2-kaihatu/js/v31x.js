/* v3.1 B／C／D 共通の動き
   [data-rv]    画面に入ったら .is-in（同じ親の中では少しずつ遅らせる）
   [data-count] 画面に入ったら 0 から数える
   [data-step]  画面の中央に来た工程を .is-on（工程の行が順に濃くなる）
   [data-par]   写真のゆっくりした視差
   #sFloat      C の社員カード：左右送り */
(function () {
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var rv = [].slice.call(document.querySelectorAll('[data-rv]'));
  rv.forEach(function (el) {
    var sib = [].filter.call(el.parentNode.children, function (c) { return c.hasAttribute('data-rv'); });
    el.style.setProperty('--d', Math.min(6, sib.indexOf(el)) * 0.09 + 's');
  });
  function count(el) {
    var to = parseInt(el.getAttribute('data-count'), 10), t0 = null, dur = 1400;
    if (reduce) { el.textContent = to; return; }
    function f(t) { if (!t0) t0 = t; var k = Math.min(1, (t - t0) / dur); el.textContent = Math.round(to * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(f); }
    requestAnimationFrame(f);
  }
  if ('IntersectionObserver' in window) {
    var o = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        e.target.classList.add('is-in');
        [].forEach.call(e.target.querySelectorAll('[data-count]'), count);
        if (e.target.hasAttribute('data-count')) count(e.target);
        o.unobserve(e.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
    rv.forEach(function (el) { o.observe(el); });
  } else rv.forEach(function (el) { el.classList.add('is-in'); });

  var steps = [].slice.call(document.querySelectorAll('[data-step]'));
  var pars = [].slice.call(document.querySelectorAll('[data-par]'));
  function onScroll() {
    var vh = innerHeight;
    steps.forEach(function (s) {
      var r = s.getBoundingClientRect();
      s.classList.toggle('is-on', r.top < vh * 0.62 && r.bottom > vh * 0.3);
    });
    if (reduce) return;
    pars.forEach(function (el) {
      var r = el.parentNode.getBoundingClientRect();
      if (r.bottom < -200 || r.top > vh + 200) return;
      var k = parseFloat(el.getAttribute('data-par')) || 0;
      el.style.transform = 'translate3d(0,' + (-(r.top + r.height / 2 - vh / 2) * k).toFixed(1) + 'px,0) scale(1.12)';
    });
  }
  var tk = false;
  addEventListener('scroll', function () { if (!tk) { tk = true; requestAnimationFrame(function () { tk = false; onScroll(); }); } }, { passive: true });
  addEventListener('resize', onScroll); onScroll();

  /* C イントロ：網点で描く地形モデル（ゆっくり回転・マウスで傾き・中心から広がるスキャンの輪） */
  var cv = document.getElementById('sTerrain');
  if (cv && cv.getContext) (function () {
    var ctx = cv.getContext('2d'), W = 0, H = 0, dpr = 1, N = 54, run = false, t0 = performance.now();
    var mx = 0, my = 0, tx = 0, ty = 0;
    var oN = document.getElementById('sgN'), oE = document.getElementById('sgE'), oH = document.getElementById('sgH'), oA = document.getElementById('sgA');
    function hgt(u, v, t) {
      var h = 0.62 * Math.exp(-((u - .18) * (u - .18) + (v + .12) * (v + .12)) * 5.5)
            + 0.38 * Math.exp(-((u + .38) * (u + .38) + (v - .3) * (v - .3)) * 7)
            + 0.22 * Math.exp(-((u - .1) * (u - .1) + (v - .55) * (v - .55)) * 9);
      return h + 0.05 * Math.sin(u * 7 + t * .7) * Math.cos(v * 6 - t * .5);
    }
    function size() {
      var r = cv.getBoundingClientRect(); dpr = Math.min(2, devicePixelRatio || 1);
      W = r.width; H = r.height; N = W < 500 ? 38 : 56; cv.width = W * dpr; cv.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    function frame(now) {
      var t = (now - t0) / 1000;
      tx += (mx - tx) * .05; ty += (my - ty) * .05;
      var a = t * .12 + tx * .5, ca = Math.cos(a), sa = Math.sin(a), tilt = .42 + ty * .12;
      var R = Math.min(W * .5, H * .62), cx = W / 2, cy = H * .62, scan = (t * .32) % 1.4, pts = [], hmax = 0;
      for (var i = 0; i < N; i++) for (var j = 0; j < N; j++) {
        var u = i / (N - 1) * 2 - 1, v = j / (N - 1) * 2 - 1, d = Math.sqrt(u * u + v * v);
        if (d > 1) continue;
        var h = hgt(u, v, t), e = .002, gx = (hgt(u + e, v, t) - h) / e, gy = (hgt(u, v + e, t) - h) / e;
        var lit = Math.max(0, Math.min(1, .55 - gx * .35 + gy * .25 + h * .6));
        var x = u * ca - v * sa, y = u * sa + v * ca;
        if (h > hmax) hmax = h;
        pts.push([y, cx + x * R, cy + y * R * tilt - h * R * .8, lit, 1 - Math.pow(d, 6), Math.abs(d - scan) < .035]);
      }
      pts.sort(function (p, q) { return p[0] - q[0]; });
      ctx.clearRect(0, 0, W, H);
      for (var k = 0; k < pts.length; k++) {
        var p = pts[k], depth = .45 + (p[0] + 1) * .3, rr = (.5 + p[3] * 2.1) * (.7 + depth * .45) * p[4];
        if (rr < .25) continue;
        ctx.fillStyle = p[5] ? '#FFD54F' : 'rgba(255,255,255,' + (depth * (.35 + p[3] * .65)).toFixed(3) + ')';
        ctx.beginPath(); ctx.arc(p[1], p[2], p[5] ? rr + .9 : rr, 0, 6.283); ctx.fill();
      }
      /* 測量の注記：中心の十字と基準の楕円 */
      ctx.strokeStyle = 'rgba(255,255,255,.22)'; ctx.lineWidth = 1; ctx.setLineDash([3, 5]);
      ctx.beginPath(); ctx.ellipse(cx, cy, R, R * tilt, 0, 0, 6.283); ctx.stroke(); ctx.setLineDash([]);
      ctx.beginPath(); ctx.moveTo(cx - 10, cy); ctx.lineTo(cx + 10, cy); ctx.moveTo(cx, cy - 10); ctx.lineTo(cx, cy + 10); ctx.stroke();
      if (oH) oH.textContent = (hmax * 186).toFixed(1);
      if (oA) oA.textContent = ('00' + Math.round(((a * 57.2958) % 360 + 360) % 360)).slice(-3);
      if (oN && (now | 0) % 6 === 0) { oN.textContent = ('0' + (12 + Math.round(tx * 9 + Math.sin(t) * 2))).slice(-2); oE.textContent = ('0' + (48 + Math.round(ty * 9 + Math.cos(t) * 2))).slice(-2); }
      if (run && !reduce) requestAnimationFrame(frame);
    }
    size(); addEventListener('resize', function () { size(); if (!run) frame(performance.now()); });
    cv.parentNode.addEventListener('pointermove', function (e) {
      var r = cv.getBoundingClientRect(); mx = (e.clientX - r.left) / r.width * 2 - 1; my = (e.clientY - r.top) / r.height * 2 - 1;
    });
    cv.parentNode.addEventListener('pointerleave', function () { mx = my = 0; });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) {
      var was = run; run = es[0].isIntersecting; if (run && !was) requestAnimationFrame(frame);
    }).observe(cv);
    frame(performance.now());
  })();

  var fl = document.getElementById('sFloat');
  [].forEach.call(document.querySelectorAll('.s-float__nav button'), function (b) {
    b.addEventListener('click', function () {
      if (!fl) return;
      var c = fl.querySelector('.s-iv');
      fl.scrollBy({ left: (c ? c.offsetWidth + 40 : 400) * parseInt(b.getAttribute('data-dir'), 10), behavior: 'smooth' });
    });
  });
})();
