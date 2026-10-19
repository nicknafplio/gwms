/* About photo crossfade: opacity of the warm image follows scroll position.
   Progress 0 when the photo's top edge is at 90% of the viewport height,
   1 when it reaches 30%. Passive listener + requestAnimationFrame; no libraries. */
(function () {
  "use strict";
  var el = document.querySelector("[data-photo-fade]");
  if (!el) return;
  var ticking = false;
  function update() {
    ticking = false;
    var vh = window.innerHeight || document.documentElement.clientHeight;
    var top = el.getBoundingClientRect().top;
    var start = vh * 0.9, end = vh * 0.3;
    var p = Math.min(1, Math.max(0, (start - top) / (start - end)));
    el.style.setProperty("--p", p.toFixed(3));
  }
  function onScroll() { if (!ticking) { ticking = true; window.requestAnimationFrame(update); } }
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  update();
})();
