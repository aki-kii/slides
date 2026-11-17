// サイトの外枠の動き: 狭い画面の目次（ヘッダーのボタンで開く）と、目次の今のページまでのスクロール。
(function () {
  var menu = document.querySelector('[data-menu-toggle]');
  var side = document.getElementById('side');
  function showCurrent() {
    if (!side) return;
    var cur = side.querySelector('[aria-current="page"]');
    if (!cur) return;
    side.scrollTop = Math.max(0, cur.offsetTop - side.clientHeight / 3);
  }
  showCurrent();
  if (menu && side) {
    menu.addEventListener('click', function () {
      var open = side.classList.toggle('is-open');
      menu.setAttribute('aria-expanded', String(open));
      var text = open ? '目次を閉じる' : '目次を開く';
      menu.setAttribute('aria-label', text);
      menu.setAttribute('title', text);
      menu.querySelector('[data-menu-icon="open"]').hidden = open;
      menu.querySelector('[data-menu-icon="close"]').hidden = !open;
      document.body.style.overflow = open ? 'hidden' : '';
      if (open) showCurrent();
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && side.classList.contains('is-open')) { menu.click(); menu.focus(); }
    });
  }
})();
