/* 画像リビール：初期は真っ赤な不透過カバーに覆われ、表示時にスッと素早く右へ赤が抜ける
   - インライン background-image を持つ写真要素を自動で対象化
   - 除外: ヒーロー背景 phero__photo / 帯 strip__bg / kflow左大画像（独自フェード切替）
   - スクロールで画面に入ったら発火。ヒストリー（.hc-scene）はこのスクリプト自体を対象外にする */
(function(){
  if(document.querySelector('.hc-scene')) return;               // ヒストリーは除外
  var st=document.createElement('style');
  st.textContent =
   '.simg{overflow:hidden}'+
   '.simg::after{content:"";position:absolute;inset:0;background:#ff0000;transform:scaleX(1);transform-origin:right center;transition:transform .5s cubic-bezier(.72,0,.18,1);z-index:2;pointer-events:none}'+
   '.simg.is-in::after{transform:scaleX(0)}'+
   '@media(prefers-reduced-motion:reduce){.simg::after{display:none}}';
  document.head.appendChild(st);

  function build(){
    var reduce = matchMedia('(prefers-reduced-motion:reduce)').matches;
    var io = reduce ? null : new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('is-in'); io.unobserve(e.target); } });
    },{threshold:.12, rootMargin:'0px 0px -8% 0px'});
    [].forEach.call(document.querySelectorAll('[style*="background-image"]'), function(el){
      if(el._simg) return;
      if(el.classList.contains('phero__photo') || el.classList.contains('strip__bg') || el.classList.contains('kflow__img')) return;
      var bg = el.style.backgroundImage;
      if(!bg || bg.indexOf('url') < 0) return;
      el._simg = 1;
      if(getComputedStyle(el).position === 'static') el.style.position='relative';
      el.classList.add('simg');
      if(io) io.observe(el); else el.classList.add('is-in');
    });
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build); else build();
})();
