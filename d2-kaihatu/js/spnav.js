/* SP（900px以下）のグローバルナビ：電話番号の右にハンバーガー、開くと全画面のメニュー
   メニューの中身はヘッダーの .gnav と 採用情報（.header-cta）から組み立てる（ページごとのHTMLは触らない） */
(function () {
  function init() {
    var hr = document.querySelector('.site-header .header-right');
    var gnav = document.querySelector('.site-header .gnav');
    if (!hr || !gnav || document.querySelector('.sp-burger')) return;
    var btn = document.createElement('button');
    btn.type = 'button'; btn.className = 'sp-burger';
    btn.setAttribute('aria-label', 'メニューを開く'); btn.setAttribute('aria-expanded', 'false');
    btn.innerHTML = '<span></span><span></span><span></span>';
    var tel = hr.querySelector('.tel-box');
    if (tel && tel.nextSibling) hr.insertBefore(btn, tel.nextSibling); else hr.appendChild(btn);

    var dr = document.createElement('nav');
    dr.className = 'sp-drawer'; dr.setAttribute('aria-label', 'メニュー');
    var h = '<button type="button" class="sp-close" aria-label="メニューを閉じる"><span></span><span></span></button>'
      + '<a class="l" href="design31a-top.html">ホーム<i>→</i></a>';
    [].forEach.call(gnav.querySelectorAll('a'), function (a) {
      h += '<a class="l' + (a.classList.contains('cur') ? ' cur' : '') + '" href="' + a.getAttribute('href') + '">' + a.textContent + '<i>→</i></a>';
    });
    var cta = document.querySelector('.site-header .header-cta');
    if (cta) h += '<a class="rec" href="' + cta.getAttribute('href') + '">' + cta.textContent + ' →</a>';
    h += '<a class="tel" href="tel:0864231899"><small>お電話でのお問い合わせ</small>086-423-1899<small>平日 9:00〜17:00</small></a>';
    h += '<button type="button" class="sp-close2">閉じる ×</button>';
    dr.innerHTML = h;
    document.body.appendChild(dr);

    function set(open) {
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      btn.setAttribute('aria-label', open ? 'メニューを閉じる' : 'メニューを開く');
      dr.classList.toggle('is-open', open);
      document.documentElement.classList.toggle('sp-open', open);
    }
    btn.addEventListener('click', function () { set(btn.getAttribute('aria-expanded') !== 'true'); });
    dr.addEventListener('click', function (e) { if (e.target.closest('a, .sp-close, .sp-close2')) set(false); });
    addEventListener('keydown', function (e) { if (e.key === 'Escape') set(false); });
    addEventListener('resize', function () { if (innerWidth > 900) set(false); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
