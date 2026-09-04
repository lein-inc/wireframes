// ハンバーガーメニュー
jQuery('.drawer-icon').on('click', function() {

    //クリックした時にis－activeクラスを付与する
    jQuery('.drawer-icon').toggleClass('is-active');
    jQuery('.drawer-content').toggleClass('is-active');
    jQuery('.drawer-background').toggleClass('is-active');

    return false;
});

jQuery('.drawer-menu a').on('click',function() {
    jQuery('.drawer-icon').removeClass('is-active');
    jQuery('.drawer-content').removeClass('is-active');
    jQuery('.drawer-background').toggleClass('is-active');
});

