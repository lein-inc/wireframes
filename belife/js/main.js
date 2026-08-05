/* BELIEF inc. LP - interactions */
(function () {
  'use strict';

  /* ===== SP Drawer ===== */
  var drawer = document.getElementById('spDrawer');
  var openBtn = document.getElementById('menuOpen');
  var closeBtn = document.getElementById('menuClose');

  function openDrawer() { drawer.classList.add('is-open'); document.body.style.overflow = 'hidden'; }
  function closeDrawer() { drawer.classList.remove('is-open'); document.body.style.overflow = ''; }

  if (openBtn) openBtn.addEventListener('click', openDrawer);
  if (closeBtn) closeBtn.addEventListener('click', closeDrawer);
  if (drawer) {
    drawer.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', closeDrawer);
    });
  }

  /* ===== FAQ accordion ===== */
  document.querySelectorAll('.faq__q').forEach(function (q) {
    q.addEventListener('click', function () {
      var item = q.closest('.faq__item');
      var isOpen = item.classList.toggle('is-open');
      q.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  });
})();
