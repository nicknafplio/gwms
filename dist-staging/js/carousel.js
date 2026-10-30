/* Fund-card carousel — progressive enhancement over a plain scrollable list.
   Buttons scroll by one card; no autoplay; list stays keyboard- and touch-scrollable. */
(function () {
  "use strict";
  var list = document.querySelector("[data-carousel]");
  if (!list) return;
  var prev = document.querySelector("[data-carousel-prev]");
  var next = document.querySelector("[data-carousel-next]");
  if (!prev || !next) return;

  function step() {
    var li = list.querySelector("li");
    var gap = parseFloat(getComputedStyle(list).columnGap) || 0;
    return li ? li.getBoundingClientRect().width + gap : list.clientWidth;
  }
  function update() {
    prev.disabled = list.scrollLeft <= 2;
    next.disabled = list.scrollLeft + list.clientWidth >= list.scrollWidth - 2;
  }
  prev.addEventListener("click", function () { list.scrollBy({ left: -step(), behavior: "smooth" }); });
  next.addEventListener("click", function () { list.scrollBy({ left: step(), behavior: "smooth" }); });
  list.addEventListener("scroll", update, { passive: true });
  window.addEventListener("resize", update);
  update();
})();
