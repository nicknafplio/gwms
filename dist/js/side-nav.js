/* Section menu on small screens: the left-hand menu becomes a collapsed, sticky disclosure
   ("Explore this section"). The state lives in aria-expanded on the button and an .is-open class on
   the nav; CSS shows the full sidebar on desktop and hides the button there. Escape closes it and
   returns focus to the button. Without JavaScript the full list is shown. */
(function () {
  "use strict";
  var nav = document.querySelector(".side-nav");
  if (!nav) return;
  var btn = nav.querySelector(".side-nav__toggle");
  if (!btn) return;

  function set(open) {
    nav.classList.toggle("is-open", open);
    btn.setAttribute("aria-expanded", open ? "true" : "false");
  }
  btn.addEventListener("click", function () { set(btn.getAttribute("aria-expanded") !== "true"); });
  nav.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && btn.getAttribute("aria-expanded") === "true") { set(false); btn.focus(); }
  });
  document.addEventListener("click", function (e) {            // tapping outside closes it
    if (!nav.contains(e.target)) set(false);
  });
})();
