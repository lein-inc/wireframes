/* 網点の図（C案 Fig.01 Ground Model の表現を部品化）  2026-11-19
   <figure class="hfig" data-model="terrain" data-fig="Fig. 01 — Ground Model" data-mode="Halftone / Point Cloud"
           data-metric="H.max|m|186" data-n="34°35′" data-e="133°45′"></figure>
   中身（canvas・注記）はこのスクリプトが作る。画面に入っている間だけ動かす。prefers-reduced-motion なら止め絵
   model: terrain / strata / river / eco / air / ripple / disaster / route / scan / drone / structure / gnss */
(function () {
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var ACC = '#FFD54F';
  function g(u, v, x, y, k) { return Math.exp(-((u - x) * (u - x) + (v - y) * (v - y)) * k); }
  function hills(u, v, t) {
    return 0.62 * g(u, v, .18, -.12, 5.5) + 0.38 * g(u, v, -.38, .3, 7) + 0.22 * g(u, v, .1, .55, 9)
      + 0.05 * Math.sin(u * 7 + t * .7) * Math.cos(v * 6 - t * .5);
  }
  /* 各モデル：h=高さ, hl=黄色にする点, hide=描かない点, ov=上に重ねる注記, metric=右上の数値, spin=回転の速さ */
  var M = {
    terrain: { h: hills, hl: function (u, v, t, d) { return Math.abs(d - (t * .32) % 1.4) < .035; } },
    eco: { h: function (u, v, t) { return .5 * hills(u, v, t * .3); },
      hl: function (u, v, t, d, i, j) { var k = (i * 7 + j * 13) % 97; return k < 3 && ((t * .8 + k) % 3) < 2.2; } },
    air: { h: function (u, v, t) { return .1 * Math.sin(u * 5 + t * 1.1) * Math.cos(v * 4 - t * .8) + .06 * Math.sin((u + v) * 9 - t * 1.6); },
      hl: function (u, v, t) { return Math.abs(u - ((t * .35) % 2.4 - 1.2)) < .025; } },
    ripple: { h: function (u, v, t, d) { return .16 * Math.sin(d * 16 - t * 3) * Math.exp(-d * 2.2); },
      hl: function (u, v, t, d) { return d < .06; } },
    river: { spin: .05, h: function (u, v, t) { var c = .35 * Math.sin(u * 2.2 + .6); return .32 - .55 * g(0, v, 0, c, 7) + .04 * Math.sin(u * 9 + v * 4); },
      hl: function (u, v, t) { return Math.abs(u - ((t * .3) % 2.4 - 1.2)) < .03; } },
    disaster: { h: function (u, v, t) {
        var base = hills(u, v, 0), s = g(u, v, .28, -.02, 14), ph = (Math.sin(t * .9) + 1) / 2;
        return base - s * .38 * ph; },
      hl: function (u, v, t) { return g(u, v, .28, -.02, 14) > .35 && Math.sin(t * .9) > -.2; } },
    route: { spin: .04, h: function (u, v, t) { return .25 * hills(u, v, 0) - .1; },
      hl: function (u, v, t, d) {
        var c = .45 * Math.sin(u * 2.4) - .1 * Math.cos(u * 6); /* 海岸線ぞいに歩く線 */
        return Math.abs(v - c) < .05 && (u + 1) / 2 < ((t * .12) % 1.15); } },
    scan: { h: hills, hide: function (u, v, t) { return (u + 1) / 2 > ((t * .22) % 1.3); },
      hl: function (u, v, t) { return Math.abs((u + 1) / 2 - ((t * .22) % 1.3)) < .02; } },
    drone: { spin: .03, h: function (u, v, t) { return .45 * hills(u, v, 0); },
      hl: function (u, v, t) { /* 往復の飛行ライン */
        var lane = Math.round((v + 1) * 3.5) / 3.5 - 1, p = (t * .18) % 1, row = Math.floor(p * 8), x = (p * 8 % 1) * 2 - 1;
        if (row % 2) x = -x; return Math.abs(v - lane) < .03 && Math.round((lane + 1) * 3.5) === row && Math.abs(u - x) < .08; } },
    structure: { spin: .08, h: function (u, v, t) { /* 橋：アーチの桁と橋脚 */
        var deck = Math.abs(v) < .16 ? .42 + .12 * Math.cos(u * 1.6) : 0, pier = (Math.abs(Math.abs(u) - .5) < .06 && Math.abs(v) < .16) ? .42 : 0;
        return Math.max(deck, pier) - .05 * g(u, v, 0, 0, 1); },
      hl: function (u, v, t) { return Math.abs(u - ((t * .4) % 2.4 - 1.2)) < .03 && Math.abs(v) < .16; } },
    gnss: { h: function (u, v, t) { return .3 * hills(u, v, 0); }, hl: function (u, v, t, d) { return Math.abs(d - (t * .25) % 1.2) < .03 && d < .5; },
      ov: function (c, P, t, W, H) {
        var base = P(0, 0, .3 * hills(0, 0, 0)), sats = [[-.8, -.6], [.7, -.8], [.2, -1.05], [-.3, -.95]];
        sats.forEach(function (s, i) {
          var x = W / 2 + s[0] * W * .34, y = H * .44 + s[1] * H * .13 + Math.sin(t * .6 + i) * 4;
          c.strokeStyle = 'rgba(255,255,255,.28)'; c.setLineDash([2, 5]); c.beginPath(); c.moveTo(x, y); c.lineTo(base[0], base[1]); c.stroke(); c.setLineDash([]);
          c.fillStyle = '#fff'; c.fillRect(x - 3, y - 3, 6, 6);
        });
        c.fillStyle = ACC; c.beginPath(); c.arc(base[0], base[1], 3.5, 0, 6.283); c.fill();
      } }
  };

  function strata(fig, c, W, H, t) { /* 地質の断面：層ごとに網点の大きさ・間隔を変え、ボーリングが上から降りていく */
    var cols = W < 420 ? 30 : 46, x0 = W * .06, x1 = W * .8, sx = (x1 - x0) / cols, top = H * .24, bot = H * .82;
    var rows = Math.floor((bot - top) / sx), bx = Math.round(cols * .58);
    var depth = reduce ? rows : Math.floor(((t * .16) % 1.3) * rows);
    var NAME = ['表土', '粘性土', '砂礫', '岩盤'], bnd = function (L, u) { return [0, .2 + .03 * Math.sin(u * 4), .48 + .05 * Math.cos(u * 3 + 1), .76 + .02 * Math.sin(u * 6)][L]; };
    for (var i = 0; i <= cols; i++) {
      var u = i / cols, surf = top + Math.sin(u * 5 + 1) * sx * 1.2;
      for (var j = 0; j <= rows; j++) {
        var y = surf + j * sx; if (y > bot) break;
        var f = j / rows, L = f < bnd(1, u) ? 0 : f < bnd(2, u) ? 1 : f < bnd(3, u) ? 2 : 3;
        if (L === 0 && (i + j) % 2) continue;            /* 表土：まばら */
        if (L === 2 && (i * 3 + j * 5) % 7 === 0) continue; /* 砂礫：粒がばらつく */
        var r = [1.1, 1.5, 2.2 + ((i * 7 + j * 3) % 5) * .25, 2.7][L] * (sx / 15);
        var bore = i === bx && j <= depth;
        c.fillStyle = bore ? ACC : 'rgba(255,255,255,' + [.4, .55, .7, .85][L] + ')';
        c.beginPath(); c.arc(x0 + i * sx, y, bore ? r + 1.2 : r, 0, 6.283); c.fill();
      }
    }
    /* 層の境目（破線）と名前・N値の目盛り */
    c.font = (W < 420 ? 10 : 11) + 'px "Noto Sans JP",sans-serif'; c.textBaseline = 'middle';
    for (var L = 1; L < 4; L++) {
      c.strokeStyle = 'rgba(255,255,255,.28)'; c.setLineDash([3, 5]); c.beginPath();
      for (var k = 0; k <= 40; k++) { var uu = k / 40, yy = top + Math.sin(uu * 5 + 1) * sx * 1.2 + bnd(L, uu) * rows * sx; k ? c.lineTo(x0 + uu * (x1 - x0), yy) : c.moveTo(x0, yy); }
      c.stroke(); c.setLineDash([]);
    }
    for (L = 0; L < 4; L++) {
      var ym = top + Math.sin(6) * sx * 1.2 + ((bnd(L, 1) + (L < 3 ? bnd(L + 1, 1) : 1)) / 2) * rows * sx;
      c.fillStyle = 'rgba(255,255,255,.75)'; c.fillText(NAME[L], x1 + 18, ym);
      c.fillStyle = '#8C9AA8'; c.fillText('N=' + [3, 8, 27, 50][L], x1 + 18 + (W < 420 ? 40 : 50), ym);
    }
    var o = fig._m; if (o) o.textContent = (depth / rows * 20).toFixed(1);
  }

  function setup(fig) {
    var model = fig.getAttribute('data-model') || 'terrain', m = M[model] || M.terrain;
    var met = (fig.getAttribute('data-metric') || 'H.max|m|186').split('|');
    fig.innerHTML = '<canvas></canvas><i class="hfig__c tl"></i><i class="hfig__c tr"></i><i class="hfig__c bl"></i><i class="hfig__c br"></i>'
      + '<span class="hfig__fig">' + (fig.getAttribute('data-fig') || 'Fig. 01 — Ground Model') + '</span>'
      + '<span class="hfig__mode">' + (fig.getAttribute('data-mode') || 'Halftone / Point Cloud') + '</span>'
      + '<span class="hfig__h">' + met[0] + ' <b>0.0</b> ' + (met[1] || '') + '</span>'
      + '<span class="hfig__xy">N ' + (fig.getAttribute('data-n') || '34°35′') + '<b>10</b>″<br>E ' + (fig.getAttribute('data-e') || '133°45′') + '<b>47</b>″</span>'
      + '<span class="hfig__scale"><i></i>0　　50　　100 m</span>'
      + '<span class="hfig__az">AZ <b>000</b>°</span>';
    fig.setAttribute('aria-hidden', 'true');
    var cv = fig.querySelector('canvas'), c = cv.getContext('2d'), bs = fig.querySelectorAll('b');
    fig._m = bs[0];
    var W = 0, H = 0, N = 50, run = false, t0 = performance.now() - Math.random() * 4000, mx = 0, my = 0, tx = 0, ty = 0;
    function size() {
      var r = fig.getBoundingClientRect(), dpr = Math.min(2, devicePixelRatio || 1);
      W = r.width; H = r.height; N = W < 420 ? 34 : W < 700 ? 46 : 56;
      fig.classList.toggle('is-s', W < 460); fig.classList.toggle('is-2d', model === 'strata');
      cv.width = W * dpr; cv.height = H * dpr; c.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    function frame(now) {
      var t = reduce ? 6 : (now - t0) / 1000;
      c.clearRect(0, 0, W, H);
      if (model === 'strata') { strata(fig, c, W, H, t); }
      else {
        tx += (mx - tx) * .05; ty += (my - ty) * .05;
        var a = t * (m.spin == null ? .12 : m.spin) + tx * .5 + .5, ca = Math.cos(a), sa = Math.sin(a), tilt = .42 + ty * .12;
        var R = Math.min(W * .46, H * .62), cx = W / 2, cy = H * .6, pts = [], hmax = 0;
        var P = function (u, v, h) { var x = u * ca - v * sa, y = u * sa + v * ca; return [cx + x * R, cy + y * R * tilt - h * R * .8, y]; };
        for (var i = 0; i < N; i++) for (var j = 0; j < N; j++) {
          var u = i / (N - 1) * 2 - 1, v = j / (N - 1) * 2 - 1, d = Math.sqrt(u * u + v * v);
          if (d > 1) continue;
          if (m.hide && m.hide(u, v, t)) continue;
          var h = m.h(u, v, t, d), e = .002, gx = (m.h(u + e, v, t, d) - h) / e, gy = (m.h(u, v + e, t, d) - h) / e;
          var lit = Math.max(0, Math.min(1, .55 - gx * .35 + gy * .25 + h * .6)), p = P(u, v, h);
          if (h > hmax) hmax = h;
          pts.push([p[2], p[0], p[1], lit, 1 - Math.pow(d, 6), m.hl ? m.hl(u, v, t, d, i, j) : false]);
        }
        pts.sort(function (p, q) { return p[0] - q[0]; });
        var sc = W < 420 ? .8 : 1;
        for (var k = 0; k < pts.length; k++) {
          var q = pts[k], depth = .45 + (q[0] + 1) * .3, rr = (.5 + q[3] * 2.1) * (.7 + depth * .45) * q[4] * sc;
          if (rr < .25) continue;
          c.fillStyle = q[5] ? ACC : 'rgba(255,255,255,' + (depth * (.35 + q[3] * .65)).toFixed(3) + ')';
          c.beginPath(); c.arc(q[1], q[2], q[5] ? rr + .9 : rr, 0, 6.283); c.fill();
        }
        c.strokeStyle = 'rgba(255,255,255,.22)'; c.lineWidth = 1; c.setLineDash([3, 5]);
        c.beginPath(); c.ellipse(cx, cy, R, R * tilt, 0, 0, 6.283); c.stroke(); c.setLineDash([]);
        c.beginPath(); c.moveTo(cx - 10, cy); c.lineTo(cx + 10, cy); c.moveTo(cx, cy - 10); c.lineTo(cx, cy + 10); c.stroke();
        if (m.ov) m.ov(c, P, t, W, H);
        bs[0].textContent = (hmax * (parseFloat(met[2]) || 186)).toFixed(1);
        bs[3].textContent = ('00' + Math.round(((a * 57.2958) % 360 + 360) % 360)).slice(-3);
      }
      if ((now | 0) % 7 === 0) { bs[1].textContent = ('0' + (10 + Math.round(Math.sin(t) * 2))).slice(-2); bs[2].textContent = ('0' + (47 + Math.round(Math.cos(t) * 2))).slice(-2); }
      if (run && !reduce) requestAnimationFrame(frame);
    }
    size();
    addEventListener('resize', function () { size(); if (!run) frame(performance.now()); });
    fig.addEventListener('pointermove', function (e) { var r = fig.getBoundingClientRect(); mx = (e.clientX - r.left) / r.width * 2 - 1; my = (e.clientY - r.top) / r.height * 2 - 1; });
    fig.addEventListener('pointerleave', function () { mx = my = 0; });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) {
      var was = run; run = es[0].isIntersecting; if (run && !was) requestAnimationFrame(frame);
    }).observe(fig);
    frame(performance.now());
  }
  function init() { [].forEach.call(document.querySelectorAll('figure.hfig'), setup); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
