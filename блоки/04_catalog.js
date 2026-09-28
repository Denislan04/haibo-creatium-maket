/* Каталог уже находится в HTML. Этот JS только переключает готовые карточки. */
(function () {
  var root = el.querySelector('.hb-catalog');
  if (!root) return;
  var cards = Array.prototype.slice.call(root.querySelectorAll('.hb-product'));
  var buttons = Array.prototype.slice.call(root.querySelectorAll('.hb-tabs [data-filter]'));
  var status = root.querySelector('.hb-catalog__status');
  if (!cards.length || !status) return;

  function parts(value) {
    return String(value || '').split('|').map(function (part) { return part.trim(); });
  }

  function matches(card, filter) {
    if (filter === 'all') return true;
    if (filter === 'motor' || filter === 'accessory') return card.dataset.type === filter;
    if (card.dataset.type === 'motor') return card.dataset.voltage === filter;
    var series = { '12': 'P001', '24': 'P002', '36': 'P003' }[filter];
    var compatible = parts(card.dataset.compatibleVoltage);
    var families = parts(card.dataset.compatibility);
    return compatible.indexOf(filter) !== -1 || families.indexOf(series) !== -1 || families.indexOf('Universal') !== -1;
  }

  function render(filter) {
    var count = 0;
    cards.forEach(function (card) {
      card.hidden = !matches(card, filter);
      if (!card.hidden) count++;
    });
    buttons.forEach(function (button) {
      var active = button.dataset.filter === filter;
      button.classList.toggle('is-active', active);
      button.setAttribute('aria-pressed', active ? 'true' : 'false');
    });
    status.textContent = 'Показано ' + count + ' из ' + cards.length + ' товаров';
  }

  buttons.forEach(function (button) {
    button.addEventListener('click', function () { render(button.dataset.filter); });
  });
  render('all');
})();
