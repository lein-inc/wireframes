/* 下層ページ共通：初回読み込みの段階演出（amu.co.jp 参考）
   ① ページ大見出し（＋パンくず・英字ラベル）  … 左→右にマスクが抜ける
   ② ヘッダーメニュー                          … 上から下へすっとフェードイン
   ③ 見出し下の罫線                            … 左→右に伸びる
   ④ コピー／サブコピー                        … 左→右にマスクが抜ける
   ⑤ ページコンテンツ                          … 左→右にマスクが抜ける

   ⚠️このファイルは <head> で同期読み込みすること。
     スタイルの流し込みと html.intro の付与を body が組まれる前に済ませないと、
     素の状態が一瞬見えてから隠れる＝かえって目立つ。
   ⚠️終わったら intro / intro-run を外して clip-path を completely 消す。
     inset(0 0 0 0) を残したままだと、その要素が position:fixed / sticky の
     包含ブロックになり、中の追従要素が効かなくなる。
   ⚠️罫線は border-bottom なので左→右に伸ばせない。intro の間だけ border を透明にして
     背景グラデーションの線に差し替え、background-size を 0%→100% で伸ばしている。 */
(function () {
  if (matchMedia('(prefers-reduced-motion:reduce)').matches) return;

  var root = document.documentElement;

  /* ── 時間設計（ms）。順番を変えるならここだけ ── */
  var T = {
    head: 150,    /* ① 大見出し */
    nav: 550,     /* ② メニュー */
    rule: 850,    /* ③ 罫線 */
    copy: 1100,   /* ④ コピー */
    body: 1450,   /* ⑤ 本文 */
    end: 2700     /* 後片付け */
  };

  var HEAD = '.pcrumb,.phero-en2,.phero-jp2';
  var COPY = '.phero__catch,.phero__lead';
  var BODY = '.pmain > *:not(.phero),.strip,.foot';

  function mask(sel, on) {
    return 'html.' + (on ? 'intro-run' : 'intro') + ' ' +
      sel.split(',').join(',html.' + (on ? 'intro-run' : 'intro') + ' ');
  }
  function clipHide(sel) {
    return mask(sel, false) + '{-webkit-clip-path:inset(0 100% 0 0);clip-path:inset(0 100% 0 0)}';
  }
  function clipShow(sel, dur, delay) {
    return mask(sel, true) + '{-webkit-clip-path:inset(0 0 0 0);clip-path:inset(0 0 0 0);' +
      'transition:clip-path ' + dur + 'ms cubic-bezier(.2,.7,.2,1) ' + delay + 'ms,' +
      '-webkit-clip-path ' + dur + 'ms cubic-bezier(.2,.7,.2,1) ' + delay + 'ms}';
  }

  var css =
    /* ① 大見出し */
    clipHide(HEAD) + clipShow(HEAD, 850, T.head) +
    /* ② メニュー＋左上ロゴ：上から下へ（同じタイミング・同じ動き）
       ⚠️ロゴ(.site-logo)はヘッダーの外に置かれた別要素なので、.nav だけ指定しても付いてこない。 */
    'html.intro .nav,html.intro .site-logo{opacity:0;transform:translateY(-18px)}' +
    'html.intro-run .nav,html.intro-run .site-logo{opacity:1;transform:none;' +
      'transition:opacity 600ms ease ' + T.nav + 'ms,transform 600ms cubic-bezier(.2,.7,.2,1) ' + T.nav + 'ms}' +
    /* ③ 罫線 */
    'html.intro .phero__bar{border-bottom-color:transparent;' +
      'background-image:linear-gradient(var(--ink),var(--ink));background-repeat:no-repeat;' +
      'background-position:left bottom;background-size:0% 1px}' +
    'html.intro .phero__bar::before,html.intro .phero__bar::after{opacity:0}' +
    'html.intro-run .phero__bar{background-size:100% 1px;' +
      'transition:background-size 700ms cubic-bezier(.2,.7,.2,1) ' + T.rule + 'ms}' +
    'html.intro-run .phero__bar::before,html.intro-run .phero__bar::after{opacity:1;' +
      'transition:opacity 300ms ease ' + (T.rule + 550) + 'ms}' +
    /* ④ コピー */
    clipHide(COPY) + clipShow(COPY, 850, T.copy) +
    /* ⑤ 本文 */
    clipHide(BODY) + clipShow(BODY, 900, T.body);

  var st = document.createElement('style');
  st.id = 'intro-css';
  st.textContent = css;
  (document.head || root).appendChild(st);
  root.classList.add('intro');

  function run() {
    requestAnimationFrame(function () {
      requestAnimationFrame(function () {
        root.classList.add('intro-run');
        setTimeout(function () {
          root.classList.remove('intro', 'intro-run');
          if (st.parentNode) st.parentNode.removeChild(st);
        }, T.end);
      });
    });
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
})();
