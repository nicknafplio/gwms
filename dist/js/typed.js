/* Hero headline: the last word types out letter by letter, stays in full for 3 seconds, is deleted
   letter by letter, and the next word follows (value > relationships > objectives > value ...).
   The words are listed in data-words on .typed. Screen readers get the static word "value" from the
   .sr-only copy; the animated text is aria-hidden. Without JavaScript the word "value" is simply shown. */
(function () {
  "use strict";
  var wrap = document.querySelector(".typed");
  if (!wrap) return;
  var out = wrap.querySelector(".typed__text");
  var words = (wrap.getAttribute("data-words") || "").split(",").filter(Boolean);
  if (!out || words.length < 2) return;

  var TYPE_MS = 95, DELETE_MS = 55, HOLD_MS = 3000, GAP_MS = 450;
  var w = 0, n = 0;

  wrap.classList.add("is-typing");
  out.textContent = "";

  function type() {
    n += 1;
    out.textContent = words[w].slice(0, n);
    if (n < words[w].length) { window.setTimeout(type, TYPE_MS); }
    else { wrap.classList.add("is-held"); window.setTimeout(erase, HOLD_MS); }
  }
  function erase() {
    wrap.classList.remove("is-held");
    n -= 1;
    out.textContent = words[w].slice(0, n);
    if (n > 0) { window.setTimeout(erase, DELETE_MS); }
    else { w = (w + 1) % words.length; window.setTimeout(type, GAP_MS); }
  }
  window.setTimeout(type, 600);
})();
