(function () {
  var root = (typeof el !== 'undefined' && el && el.querySelector)
    ? (el.matches && el.matches('[data-hb-tech-scroll]') ? el : el.querySelector('[data-hb-tech-scroll]'))
    : document.querySelector('[data-hb-tech-scroll]');
  if (!root || root.dataset.hbReady === '1') return;

  var video = root.querySelector('[data-hb-video]');
  var steps = Array.prototype.slice.call(root.querySelectorAll('[data-hb-step]'));
  var buttons = Array.prototype.slice.call(root.querySelectorAll('[data-hb-go]'));
  var current = root.querySelector('[data-hb-current]');
  var progressBar = root.querySelector('[data-hb-progress]');
  var error = root.querySelector('[data-hb-video-error]');
  if (!video || steps.length !== 5 || buttons.length !== 5) return;
  root.dataset.hbReady = '1';

  // У этой HTML-секции и её компонента не должно быть overflow: hidden.
  if (typeof el !== 'undefined' && el && el.style) el.style.overflow = 'visible';
  var section = root.closest('.section');
  if (section) section.style.overflow = 'visible';

  var active = -1;
  var raf = 0;
  var wantedTime = Number(steps[0].dataset.time) || 0;
  video.pause();

  function seek() {
    if (video.readyState < 1 || !Number.isFinite(video.duration)) return;
    var limit = Math.max(0, video.duration - 0.05);
    var time = Math.max(0, Math.min(limit, wantedTime));
    if (Math.abs(video.currentTime - time) > 0.04) video.currentTime = time;
  }

  function showStep(index) {
    if (index === active) return;
    active = index;
    steps.forEach(function (step, i) { step.hidden = i !== index; });
    buttons.forEach(function (button, i) {
      if (i === index) button.setAttribute('aria-current', 'step');
      else button.removeAttribute('aria-current');
    });
    current.textContent = String(index + 1).padStart(2, '0');
    progressBar.style.width = ((index + 1) / steps.length * 100) + '%';
    wantedTime = Number(steps[index].dataset.time) || 0;
    seek();
  }

  function update() {
    raf = 0;
    var range = Math.max(1, root.offsetHeight - window.innerHeight);
    var position = -root.getBoundingClientRect().top / range;
    var index = Math.max(0, Math.min(steps.length - 1, Math.floor(position * steps.length)));
    showStep(index);
  }

  function requestUpdate() {
    if (!raf) raf = window.requestAnimationFrame(update);
  }

  buttons.forEach(function (button, index) {
    button.addEventListener('click', function () {
      var range = Math.max(1, root.offsetHeight - window.innerHeight);
      var top = root.getBoundingClientRect().top + window.scrollY;
      var position = (index + 0.35) / steps.length;
      var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top: top + position * range, behavior: reduced ? 'auto' : 'smooth' });
      showStep(index);
    });
  });

  video.addEventListener('loadedmetadata', seek);
  video.addEventListener('error', function () { error.hidden = false; });
  if (video.readyState >= 1) seek();
  window.addEventListener('scroll', requestUpdate, { passive: true });
  window.addEventListener('resize', requestUpdate, { passive: true });
  showStep(0);
  requestUpdate();
})();
