/* v3.1-B：リボンを画面に入ったら描く／写真のゆっくりした視差／社員カードの左右送り */
(function () {
  // リボン：線の長さを測って、画面に入ったら端から描く
  var rbs = document.querySelectorAll('.rb');
  [].forEach.call(rbs, function (svg) {
    [].forEach.call(svg.querySelectorAll('path'), function (p) {
      try { p.style.setProperty('--len', Math.ceil(p.getTotalLength() * 1.2)); } catch (e) {}
    });
  });
  if ('IntersectionObserver' in window) {
    var o = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-drawn'); o.unobserve(e.target); } });
    }, { threshold: 0.15 });
    [].forEach.call(rbs, function (r) { o.observe(r); });
  } else {
    [].forEach.call(rbs, function (r) { r.classList.add('is-drawn'); });
  }

  // 写真の視差（data-par の割合だけ、画面の中の位置に応じて上下にずらす）
  var pars = [].slice.call(document.querySelectorAll('[data-par]'));
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  function par() {
    if (reduce) return;
    var vh = innerHeight;
    pars.forEach(function (el) {
      var r = el.parentNode.getBoundingClientRect();
      if (r.bottom < -200 || r.top > vh + 200) return;
      var k = parseFloat(el.getAttribute('data-par')) || 0;
      var c = (r.top + r.height / 2 - vh / 2);
      el.style.transform = 'translate3d(0,' + (-c * k).toFixed(1) + 'px,0) scale(1.12)';
    });
  }
  var t = false;
  addEventListener('scroll', function () { if (!t) { t = true; requestAnimationFrame(function () { t = false; par(); }); } }, { passive: true });
  addEventListener('resize', par); par();

  // 社員カードの左右送り
  var tr = document.getElementById('bTrack');
  [].forEach.call(document.querySelectorAll('.b-people__nav button'), function (b) {
    b.addEventListener('click', function () {
      if (!tr) return;
      var card = tr.querySelector('.b-pcard');
      tr.scrollBy({ left: (card ? card.offsetWidth + 32 : 340) * parseInt(b.getAttribute('data-dir'), 10), behavior: 'smooth' });
    });
  });
})();
