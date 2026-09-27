/* ニュース一覧: 行ホバーでアイキャッチをマウス位置に浮かせて表示（design2 共通）
   - 画像は各行の data-img。未指定の行はダミー写真を順番に割り当て（本番はWPのアイキャッチ）
   - マウス追従は lerp でゆるく遅らせる／タッチ端末では無効 */
(function(){
  if (!window.matchMedia('(hover:hover) and (pointer:fine)').matches) return;
  var items = document.querySelectorAll('.news-item, .top-news-item');
  if (!items.length) return;
  var DUMMY = ['img/eng3_city.jpg','img/eng2_mountain.jpg','img/eng1_sky.jpg','img/eng4_construction.jpg','img/terrain-a.jpg','img/sky.jpg','img/terrain-b.jpg'];
  var box = document.createElement('div');
  box.className = 'news-float';
  box.setAttribute('aria-hidden','true');
  box.innerHTML = '<img alt=""><img alt="">';
  document.body.appendChild(box);
  var imgs = box.querySelectorAll('img'), cur = 0;
  var tx = 0, ty = 0, x = 0, y = 0, raf = null, active = false;
  function loop(){
    x += (tx - x) * 0.18; y += (ty - y) * 0.18;
    box.style.transform = 'translate3d(' + x + 'px,' + y + 'px,0)';
    if (active || Math.abs(tx - x) > .5 || Math.abs(ty - y) > .5) raf = requestAnimationFrame(loop); else raf = null;
  }
  function kick(){ if (!raf) raf = requestAnimationFrame(loop); }
  items.forEach(function(el, i){
    var src = el.getAttribute('data-img') || DUMMY[i % DUMMY.length];
    new Image().src = src;
    el.addEventListener('mouseenter', function(e){
      var next = imgs[1 - cur];
      if (imgs[cur].getAttribute('src') !== src){
        next.src = src; next.classList.add('on'); imgs[cur].classList.remove('on'); cur = 1 - cur;
      }
      if (!active){ x = tx = e.clientX; y = ty = e.clientY; }
      active = true; box.classList.add('is-show'); kick();
    });
    el.addEventListener('mousemove', function(e){ tx = e.clientX; ty = e.clientY; kick(); });
    el.addEventListener('mouseleave', function(){ active = false; box.classList.remove('is-show'); });
  });
  window.addEventListener('scroll', function(){ if (active){ active = false; box.classList.remove('is-show'); } }, {passive:true});
})();
