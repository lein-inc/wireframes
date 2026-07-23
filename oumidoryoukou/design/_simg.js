/* 画像リビール：初期は真っ赤な不透過カバーに覆われ、画像全体が画面に入ってからスッと右へ赤が抜ける
   - インライン background-image を持つ写真要素を自動で対象化（カバー付与は即時）
   - 発火はローディング/ページ遷移演出の完了後に開始（演出中に抜けてしまうのを防止）
   - 除外: ヒーロー背景 phero__photo / 帯 strip__bg / kflow左大画像（独自フェード切替） */
(function(){
  if(document.querySelector('.hc-scene')) return;               // ヒストリーは除外
  var st=document.createElement('style');
  st.textContent =
   '.simg{overflow:hidden}'+
   '.simg::after{content:"";position:absolute;inset:0;background:#ff0000;transform:scaleX(1);transform-origin:right center;transition:transform .5s cubic-bezier(.72,0,.18,1);z-index:2;pointer-events:none}'+
   '.simg.is-in::after{transform:scaleX(0)}'+
   '@media(prefers-reduced-motion:reduce){.simg::after{display:none}}';
  document.head.appendChild(st);

  var els = [];
  function build(){
    [].forEach.call(document.querySelectorAll('[style*="background-image"]'), function(el){
      if(el._simg) return;
      if(el.classList.contains('phero__photo') || el.classList.contains('strip__bg') || el.classList.contains('kflow__img')) return;
      var bg = el.style.backgroundImage;
      if(!bg || bg.indexOf('url') < 0) return;
      el._simg = 1;
      if(getComputedStyle(el).position === 'static') el.style.position='relative';
      el.classList.add('simg');          // 赤カバーは即時ON
      els.push(el);
    });
  }
  function arm(){
    var reduce = matchMedia('(prefers-reduced-motion:reduce)').matches;
    if(reduce){ els.forEach(function(el){ el.classList.add('is-in'); }); return; }
    function cb(es, io){ es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('is-in'); io.unobserve(e.target); } }); }
    var ioFull = new IntersectionObserver(cb, {threshold:.98});   // 画像全体が見えてから
    var ioBig  = new IntersectionObserver(cb, {threshold:.35});   // 画面より大きい画像の救済
    els.forEach(function(el){
      (el.offsetHeight > window.innerHeight * .85 ? ioBig : ioFull).observe(el);
    });
  }
  function start(){
    build();
    /* ローディング（TOP）/ページ遷移の演出が終わってから観測開始 */
    var delay = document.getElementById('loader') ? 4600
              : (document.documentElement.classList.contains('pt-init') || document.querySelector('.pt-grid')) ? 1200
              : 250;
    setTimeout(arm, delay);
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start); else start();
})();
