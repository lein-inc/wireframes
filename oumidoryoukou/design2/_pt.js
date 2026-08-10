/* ページ遷移演出：点線ガイドと同じ6×6マス目に赤いカードを敷き詰め、パラパラと消えて表示
   - 入場: 全画面を赤カード36枚が覆った状態から、短時間でランダムに消えていく
   - 退場: 内部リンククリックでカードがランダムに埋まっていき→遷移
   - prefers-reduced-motion では無効 */
(function () {
  if (matchMedia('(prefers-reduced-motion:reduce)').matches) return;

  var RED = '#ff0000', COLS = 6, ROWS = 6;
  var IN_DUR = 320, IN_SPREAD = 560;   /* 消えるアニメの長さ / ランダム遅延の幅 */
  var OUT_DUR = 240, OUT_SPREAD = 380;

  var style = document.createElement('style');
  style.textContent =
    '.pt-grid{position:fixed;inset:0;z-index:995;display:grid;' +
    'grid-template-columns:repeat(' + COLS + ',1fr);grid-template-rows:repeat(' + ROWS + ',1fr);pointer-events:none;}' +
    '.pt-grid i{display:block;background:' + RED + ';will-change:opacity;margin:-0.5px;}' +
    'html.pt-init body{visibility:hidden;}' +
    'html.pt-veil .burger,html.pt-veil .drawer{visibility:hidden!important;}';
  document.documentElement.appendChild(style);
  document.documentElement.classList.add('pt-init');
  document.documentElement.classList.add('pt-veil');

  function makeGrid(initialOpacity) {
    var g = document.createElement('div');
    g.className = 'pt-grid';
    var cells = [];
    for (var k = 0; k < COLS * ROWS; k++) {
      var i = document.createElement('i');
      i.style.opacity = initialOpacity;
      g.appendChild(i);
      cells.push(i);
    }
    document.body.appendChild(g);
    return { g: g, cells: cells };
  }

  /* ── 入場：赤カードがパラパラと消えていく ── */
  function reveal() {
    var o = makeGrid(1);
    document.documentElement.classList.remove('pt-init');
    requestAnimationFrame(function () { requestAnimationFrame(function () {
      o.cells.forEach(function (c) {
        var d = Math.random() * IN_SPREAD;
        c.style.transition = 'opacity ' + IN_DUR + 'ms ease ' + Math.round(d) + 'ms';
        c.style.opacity = '0';
      });
      setTimeout(function () {
        if (o.g.parentNode) o.g.parentNode.removeChild(o.g);
        document.documentElement.classList.remove('pt-veil');
      }, IN_DUR + IN_SPREAD + 120);
    }); });
  }

  /* ── 退場：赤カードがパラパラと埋まっていく → 遷移 ── */
  var leaving = false;
  document.addEventListener('click', function (e) {
    if (leaving || e.defaultPrevented || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button !== 0) return;
    var a = e.target.closest ? e.target.closest('a[href]') : null;
    if (!a || a.target === '_blank') return;
    var href = a.getAttribute('href');
    if (!href || /^(https?:|mailto:|tel:|#|javascript:)/.test(href)) return;
    if (href.indexOf('#') !== -1 && href.split('#')[0] === location.pathname.split('/').pop()) return;
    e.preventDefault();
    leaving = true;
    document.documentElement.classList.add('pt-veil');
    var o = makeGrid(0);
    requestAnimationFrame(function () { requestAnimationFrame(function () {
      o.cells.forEach(function (c) {
        var d = Math.random() * OUT_SPREAD;
        c.style.transition = 'opacity ' + OUT_DUR + 'ms ease ' + Math.round(d) + 'ms';
        c.style.opacity = '1';
      });
      setTimeout(function () { location.href = href; }, OUT_DUR + OUT_SPREAD + 80);
    }); });
  }, true);

  window.addEventListener('pageshow', function (e) {
    if (e.persisted) { leaving = false; reveal(); }
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', reveal);
  } else reveal();
})();
