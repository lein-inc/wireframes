/* v3.1-A：スクロールに合わせて FV の3D（固定の iframe）へ「いまのセクション」を送る → カメラが各コンテンツの画角へ
   ・[data-shot] のセクションのうち、画面の中央にあるものと、その中の進み具合 p(0〜1) を postMessage
   ・コンテンツのパネル（.p31）は画面に入ったら .is-in で出てくる */
(function () {
  var fr = document.querySelector('.terrain-iframe');
  var secs = [].slice.call(document.querySelectorAll('[data-shot]'));
  if (!fr || !secs.length) return;
  var last = '';
  function send() {
    var mid = innerHeight * 0.5, cur = secs[0], p = 0;
    secs.forEach(function (s) {
      var r = s.getBoundingClientRect();
      if (r.top <= mid) { cur = s; p = Math.min(1, Math.max(0, (mid - r.top) / r.height)); }
    });
    var msg = { v31: { shot: cur.getAttribute('data-shot'), p: p } };
    try { fr.contentWindow.postMessage(msg, '*'); } catch (e) {}
    document.documentElement.setAttribute('data-cur', msg.v31.shot);
    last = msg.v31.shot;
  }
  var ticking = false;
  addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(function () { ticking = false; send(); }); } }, { passive: true });
  addEventListener('resize', send);
  fr.addEventListener('load', send);
  setInterval(send, 700);   // iframe の読み込み待ち・取りこぼし対策
  send();
})();
(function () {
  var els = document.querySelectorAll('.p31');
  if (!('IntersectionObserver' in window)) { [].forEach.call(els, function (e) { e.classList.add('is-in'); }); return; }
  var o = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); o.unobserve(e.target); } });
  }, { threshold: 0.08 });
  [].forEach.call(els, function (e) { o.observe(e); });
})();
