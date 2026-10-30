/* Header auto-hide: slides the sticky header up and out of view once the footer comes
   into view, and brings it back when scrolling up again. Generic: no menu-specific code.
   - Only after the page has been scrolled (a short page never hides its header at load).
   - Not while the mobile menu is open, and never while focus is inside the header.
   - Any open dropdown is closed first so it is not left open when the header returns. */
(function () {
  "use strict";
  var header = document.querySelector(".site-header");
  var footer = document.querySelector(".site-footer");
  if (!header || !footer || !("IntersectionObserver" in window)) return;

  var footerVisible = false;

  function apply() {
    var menuOpen = header.classList.contains("is-open");
    var hide = footerVisible && window.scrollY > 80 && !menuOpen;
    if (hide === header.classList.contains("is-hidden")) return;
    if (hide) {
      var open = header.querySelectorAll('button[aria-expanded="true"]');
      for (var i = 0; i < open.length; i++) open[i].click();
    }
    header.classList.toggle("is-hidden", hide);
  }

  new IntersectionObserver(function (entries) {
    footerVisible = entries[0].isIntersecting;
    apply();
  }, { threshold: 0 }).observe(footer);

  window.addEventListener("scroll", apply, { passive: true });
})();
