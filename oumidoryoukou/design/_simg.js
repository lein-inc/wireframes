/* スライス・リビール：写真をTOPの納入実績と同じく「6分割・下から上へ順にせり上がる」で出す
   - インライン background-image を持つ写真要素を自動でスライス化（ヒーロー phero__photo と帯 strip__bg は除外）
   - スクロールで画面に入ったら発火。ヒストリー（.hc-scene）はこのスクリプト自体を対象外にする */
(function(){
  if(document.querySelector('.hc-scene')) return;               // ヒストリーは除外
  var st=document.createElement('style');
  st.textContent =
   '.simg{overflow:hidden}'+
   '.simg__s{position:absolute;top:0;bottom:0;width:calc(100%/6 + 1px);overflow:hidden;transform:translateY(101%);transition:transform .78s cubic-bezier(.62,0,.24,1);z-index:1}'+
   '.simg__s::before{content:"";position:absolute;top:0;bottom:0;width:600%;background-image:var(--simg);background-size:cover;background-position:center}'+
   '.simg__s:nth-child(1){left:0}.simg__s:nth-child(1)::before{left:0}'+
   '.simg__s:nth-child(2){left:calc(100%*1/6)}.simg__s:nth-child(2)::before{left:-100%}'+
   '.simg__s:nth-child(3){left:calc(100%*2/6)}.simg__s:nth-child(3)::before{left:-200%}'+
   '.simg__s:nth-child(4){left:calc(100%*3/6)}.simg__s:nth-child(4)::before{left:-300%}'+
   '.simg__s:nth-child(5){left:calc(100%*4/6)}.simg__s:nth-child(5)::before{left:-400%}'+
   '.simg__s:nth-child(6){left:calc(100%*5/6)}.simg__s:nth-child(6)::before{left:-500%}'+
   '.simg.is-in .simg__s{transform:none;transition-delay:var(--sd)}'+
   '@media(prefers-reduced-motion:reduce){.simg__s{transform:none!important;transition:none}}';
  document.head.appendChild(st);

  function build(){
    var reduce = matchMedia('(prefers-reduced-motion:reduce)').matches;
    var io = reduce ? null : new IntersectionObserver(function(es){
      es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('is-in'); io.unobserve(e.target); } });
    },{threshold:.12, rootMargin:'0px 0px -8% 0px'});
    var sd=[0,.05,.1,.15,.2,.25];
    [].forEach.call(document.querySelectorAll('[style*="background-image"]'), function(el){
      if(el._simg) return;
      if(el.classList.contains('phero__photo') || el.classList.contains('strip__bg') || el.classList.contains('kstep__ph')) return; // ヒーロー背景・帯・工程サブ画像は除外
      var bg = el.style.backgroundImage;
      if(!bg || bg.indexOf('url') < 0) return;
      el._simg = 1;
      if(getComputedStyle(el).position === 'static') el.style.position='relative';
      el.classList.add('simg');
      el.style.setProperty('--simg', bg);
      el.style.backgroundImage = 'none';
      var html=''; for(var i=0;i<6;i++) html += '<div class="simg__s" style="--sd:'+sd[i]+'s"></div>';
      el.insertAdjacentHTML('afterbegin', html);
      if(io) io.observe(el); else el.classList.add('is-in');
    });
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded', build); else build();
})();
