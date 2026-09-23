/* 藤岡エンジニアリング WF：スクロールフェード演出 */
(function () {
  'use strict';

  // フェード対象セレクタ（自動付与）
  var SELECTORS = [
    'section', 'article',
    '.card', '.st-card', '.page-card', '.num-item',
    '.hist-cell', '.contribution',
    '.cta-box', '.info-table',
    '.hero .catch', '.hero .sub', '.hero-visual',
    '.page-hero h1', '.page-hero .en',
    '.slide .label', '.slide .tagline', '.slide .body', '.slide .meta',
    '.img-ph.large', '.img-ph.wide',
    '.news-item'
  ];

  var GROUP_SELECTORS = [
    '.grid-2', '.grid-3', '.grid-4', '.numbers',
    '.st-grid', '.page-grid', '.news-list', '.hist-grid'
  ];

  // 1) 対象要素に .fade-target を付与
  var els = document.querySelectorAll(SELECTORS.join(','));
  els.forEach(function (el) { el.classList.add('fade-target'); });

  // 2) グリッド系はステガード（連番delay）
  GROUP_SELECTORS.forEach(function (sel) {
    document.querySelectorAll(sel).forEach(function (group) {
      var children = group.children;
      for (var i = 0; i < children.length; i++) {
        var c = children[i];
        c.classList.add('fade-target');
        var d = Math.min(6, i + 1);
        c.classList.add('d-' + d);
      }
    });
  });

  // 3) IntersectionObserverで可視化
  if (!('IntersectionObserver' in window)) {
    // フォールバック：全て表示
    document.querySelectorAll('.fade-target').forEach(function (el) {
      el.classList.add('is-visible');
    });
    return;
  }

  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        io.unobserve(entry.target);
      }
    });
  }, {
    threshold: 0.12,
    rootMargin: '0px 0px -8% 0px'
  });

  document.querySelectorAll('.fade-target').forEach(function (el) {
    io.observe(el);
  });

  // 4) 既にビューポート内にある要素（ファーストビュー）は即表示
  requestAnimationFrame(function () {
    document.querySelectorAll('.fade-target').forEach(function (el) {
      var r = el.getBoundingClientRect();
      if (r.top < window.innerHeight * 0.9) {
        el.classList.add('is-visible');
        io.unobserve(el);
      }
    });
  });
})();
