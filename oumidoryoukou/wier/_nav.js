/* wire v2：ハンバーガー格納メニュー（〜1100px）。メガメニューはCSSホバー */
(function(){
  var burger = document.querySelector('.wburger');
  var drawer = document.getElementById('wdrawer');
  if(!burger || !drawer) return;
  function set(open){
    drawer.classList.toggle('is-open', open);
    burger.classList.toggle('is-open', open);
    document.body.classList.toggle('menu-open', open);
    burger.setAttribute('aria-expanded', open?'true':'false');
    drawer.setAttribute('aria-hidden', open?'false':'true');
  }
  burger.addEventListener('click', function(){ set(!drawer.classList.contains('is-open')); });
  drawer.querySelectorAll('.wdrawer__top').forEach(function(btn){
    btn.addEventListener('click', function(){ btn.parentNode.classList.toggle('is-open'); });
  });
  drawer.querySelectorAll('a').forEach(function(el){ el.addEventListener('click', function(){ set(false); }); });
})();

/* 左レール：お知らせティッカー（5秒切替） */
(function(){var it=document.querySelectorAll('.wrail__item');if(it.length<2)return;var i=0;
setInterval(function(){it[i].classList.remove('is-on');i=(i+1)%it.length;it[i].classList.add('is-on');},5000);})();
