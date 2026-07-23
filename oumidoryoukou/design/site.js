/* 近江度量衡 下層ページ共通：ヘッダー/フッター注入・メガメニュー・ドロワー・出現アニメ
   ページ側で window.OMI_ACTIVE に現在ページのキーを指定（products/service/delivery/company/history/recruit/contact 等） */
(function(){
  var A = window.OMI_ACTIVE || "";
  var HEADER = `
  <header class="nav" id="nav">
    <a class="nav__logo" href="index.html"><img src="logo_r.png" alt="近江度量衡株式会社"></a>
    <nav class="nav__menu">
      <div class="nitem" data-k="products">
        <a class="nlink" href="products.html">製品・技術</a>
        <div class="mega"><div class="mega__inner">
          <div class="mega__lead"><span class="men">Products</span><span class="mjp">製品・技術</span></div>
          <div class="mega__links">
            <a href="product-agri.html"><i class="arrow-i">→</i>農産物用計量システム</a>
            <a href="products-grain.html"><i class="arrow-i">→</i>穀類用計量システム</a>
            <a href="products-industry.html"><i class="arrow-i">→</i>工業用計量システム</a>
            <a href="products.html#others"><i class="arrow-i">→</i>その他・特殊用途</a>
          </div>
        </div></div>
      </div>
      <div class="nitem" data-k="service">
        <a class="nlink" href="service.html">サービス案内</a>
        <div class="mega"><div class="mega__inner">
          <div class="mega__lead"><span class="men">Service</span><span class="mjp">サービス案内</span></div>
          <div class="mega__links">
            <a href="service.html"><i class="arrow-i">→</i>企画・エンジニアリング</a>
            <a href="service.html"><i class="arrow-i">→</i>設計・制御・開発</a>
            <a href="service.html"><i class="arrow-i">→</i>製作・施工</a>
            <a href="service.html"><i class="arrow-i">→</i>メンテナンス・アフターサービス</a>
          </div>
        </div></div>
      </div>
      <div class="nitem" data-k="delivery"><a class="nlink" href="delivery.html">納入実績</a></div>
      <div class="nitem" data-k="company">
        <a class="nlink" href="company.html">会社案内</a>
        <div class="mega"><div class="mega__inner">
          <div class="mega__lead"><span class="men">Company</span><span class="mjp">会社案内</span></div>
          <div class="mega__links">
            <a href="company.html#concept"><i class="arrow-i">→</i>企業理念</a>
            <a href="company.html#message"><i class="arrow-i">→</i>代表挨拶</a>
            <a href="company.html#base"><i class="arrow-i">→</i>サービス拠点</a>
            <a href="company.html#quality"><i class="arrow-i">→</i>品質・認証</a>
            <a href="company.html#profile"><i class="arrow-i">→</i>会社概要</a>
          </div>
        </div></div>
      </div>
      <div class="nitem" data-k="history"><a class="nlink" href="history.html">126年ヒストリー</a></div>
      <div class="nitem" data-k="recruit">
        <a class="nlink" href="recruit.html">採用情報</a>
        <div class="mega"><div class="mega__inner">
          <div class="mega__lead"><span class="men">Recruit</span><span class="mjp">採用情報</span></div>
          <div class="mega__links">
            <a href="recruit.html#new"><i class="arrow-i">→</i>新卒採用</a>
            <a href="recruit.html#mid"><i class="arrow-i">→</i>キャリア採用</a>
            <a href="recruit.html#people"><i class="arrow-i">→</i>社員インタビュー</a>
            <a href="recruit.html#welfare"><i class="arrow-i">→</i>福利厚生・職場環境</a>
          </div>
        </div></div>
      </div>
    </nav>
    <button class="burger" aria-label="メニュー" aria-expanded="false"><span></span><span></span><span></span></button>
    <a class="nav__cta" href="contact.html">お問い合わせ</a>
  </header>
  <div class="drawer" id="drawer" aria-hidden="true">
    <nav>
      <div class="drawer__group">
        <button class="drawer__top">製品・技術</button>
        <div class="drawer__sub"><a href="product-agri.html">農産物用計量システム</a><a href="products-grain.html">穀類用計量システム</a><a href="products-industry.html">工業用計量システム</a><a href="products.html#others">その他・特殊用途</a></div>
      </div>
      <div class="drawer__group">
        <button class="drawer__top">サービス案内</button>
        <div class="drawer__sub"><a href="service.html">企画・エンジニアリング</a><a href="service.html">設計・制御・開発</a><a href="service.html">製作・施工</a><a href="service.html">メンテナンス・アフターサービス</a></div>
      </div>
      <a class="drawer__single" href="delivery.html">納入実績</a>
      <div class="drawer__group">
        <button class="drawer__top">会社案内</button>
        <div class="drawer__sub"><a href="company.html#concept">企業理念</a><a href="company.html#message">代表挨拶</a><a href="company.html#base">サービス拠点</a><a href="company.html#quality">品質・認証</a><a href="company.html#profile">会社概要</a></div>
      </div>
      <a class="drawer__single" href="history.html">126年ヒストリー</a>
      <a class="drawer__single" href="news.html">新着情報</a>
      <div class="drawer__group">
        <button class="drawer__top">採用情報</button>
        <div class="drawer__sub"><a href="recruit.html#new">新卒採用</a><a href="recruit.html#mid">キャリア採用</a><a href="recruit.html#people">社員インタビュー</a><a href="recruit.html#welfare">福利厚生・職場環境</a></div>
      </div>
      <a class="drawer__single" href="contact.html">お問い合わせ</a>
    </nav>
  </div>`;

  var FOOTER = `
  <section class="strip">
    <div class="strip__bg"></div>
    <div class="strip__marquee">
      <div class="strip__track"><span>We Measure the Future</span><span>We Measure the Future</span></div>
      <div class="strip__track" aria-hidden="true"><span>We Measure the Future</span><span>We Measure the Future</span></div>
    </div>
    <div class="strip__contact">
      <span class="en">( Contact )</span>
      <h3>お問い合わせ・ご相談</h3>
      <p>お気軽にご相談ください。<br>お見積もり依頼も可能です。</p>
      <a class="cbtn" href="contact.html">Contact Form <i class="arrow-i" style="color:inherit">→</i></a>
    </div>
  </section>
  <footer class="foot">
    <div class="foot__grid">
      <div class="foot__brand">
        <img src="logo_r.png" alt="近江度量衡株式会社">
        <p class="name">近江度量衡株式会社</p>
        <p>〒525-0054<br>滋賀県草津市東矢倉三丁目11番70号<br>TEL 077-562-7111 ／ FAX 077-562-7116<br><a href="https://maps.google.com/?q=滋賀県草津市東矢倉3丁目11番70号" target="_blank" rel="noopener">Google map</a></p>
      </div>
      <nav class="foot__nav">
        <div>
          <a href="index.html">トップページ</a>
          <a href="products.html">製品・技術</a>
          <a class="sub" href="product-agri.html">農産物用計量システム</a>
          <a class="sub" href="products-grain.html">穀類用計量システム</a>
          <a class="sub" href="products-industry.html">工業用計量システム</a>
          <a class="sub" href="products.html#others">その他・特殊用途</a>
          <a href="service.html">サービス案内</a>
          <a href="delivery.html">納入実績</a>
        </div>
        <div>
          <a href="company.html">会社案内</a>
          <a href="history.html">126年ヒストリー</a>
          <a href="news.html">新着情報</a>
          <a href="recruit.html">採用情報</a>
          <a href="contact.html">お問い合わせ</a>
          <a href="privacy.html">プライバシーポリシー</a>
        </div>
      </nav>
      <div class="foot__contact">
        <span class="en">( Contact )</span>
        <h3>お問い合わせ・ご相談</h3>
        <p>お気軽にご相談ください。<br>お見積もり依頼も可能です。</p>
        <a class="cbtn" href="contact.html">Contact Form <i class="arrow-i" style="color:inherit">→</i></a>
      </div>
    </div>
    <a class="foot__recruit" href="recruit.html">
      <span class="rtxt">
        <span class="en">Recruitment 2027</span>
        <h3>いきるの単位とは、なんだろう。</h3>
      </span>
      <span class="go">採用情報を見る <i class="arrow-i" style="color:inherit">→</i></span>
    </a>
    <div class="foot__bar"><span>OMISCALE CO.,LTD.</span><span>© 近江度量衡株式会社 ALL RIGHTS RESERVED.</span></div>
  </footer>`;

  var h = document.getElementById('site-header');
  var f = document.getElementById('site-footer');
  if (h) h.innerHTML = HEADER;
  if (f) f.innerHTML = FOOTER;

  // アクティブ表示
  if (A) { var act = document.querySelector('.nitem[data-k="'+A+'"]'); if (act) act.classList.add('is-active'); }

  // ハンバーガー／ドロワー
  var burger = document.querySelector('.burger');
  var drawer = document.getElementById('drawer');
  if (burger && drawer) {
    burger.addEventListener('click', function(){
      var open = drawer.classList.toggle('is-open');
      burger.classList.toggle('is-open', open);
      document.body.classList.toggle('menu-open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    drawer.querySelectorAll('.drawer__top').forEach(function(t){
      t.addEventListener('click', function(){ t.parentElement.classList.toggle('is-open'); });
    });
  }

  // ヘッダー：浮遊分離ナビ。暗色ヒーロー上はロゴ白→ヒーロー下端でロゴ赤（白ヒーローのページは常時赤）＋下スクロールで自動隠し
  var nav = document.getElementById('nav'); var last = 0;
  // 連続する暗色（ヒストリーは phero + hc-scene）の末尾までロゴ白を維持
  var darkHero = document.querySelector('.hc-scene') || document.querySelector('.phero');
  function heroBottom(){ return darkHero ? (darkHero.offsetTop + darkHero.offsetHeight - 90) : 0; }
  function navState(){
    if (!nav) return;
    var y = window.pageYOffset;
    nav.classList.toggle('is-logo-red', !darkHero || y > heroBottom());
  }
  window.addEventListener('scroll', function(){
    var y = window.pageYOffset;
    navState();
    if (nav) nav.classList.toggle('is-hidden', y > last && y > 240);
    last = y;
  }, {passive:true});
  window.addEventListener('resize', navState);
  navState();

  // 出現アニメ
  var io = new IntersectionObserver(function(es){
    es.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('is-in'); io.unobserve(e.target);} });
  }, {threshold:.16});
  document.querySelectorAll('.rv').forEach(function(el){ io.observe(el); });

  // サブナビのスクロールスパイ（任意）
  var subs = document.querySelectorAll('.subnav a[href^="#"]');
  if (subs.length){
    window.addEventListener('scroll', function(){
      var y = window.pageYOffset + 140; var cur = null;
      subs.forEach(function(a){ var t = document.querySelector(a.getAttribute('href')); if(t && t.offsetTop <= y) cur = a; });
      subs.forEach(function(a){ a.classList.toggle('is-active', a===cur); });
    }, {passive:true});
  }
})();
