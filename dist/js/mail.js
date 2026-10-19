/* E-mail addresses are never written into the page as an address. The markup carries them in pieces
   (data-user / data-domain) and shows "name [at] domain"; this script turns that into a link whose
   mailto: target is assembled only when the link is activated (click, tap or Enter), so a scraper that
   reads the HTML or the rendered link sees no address. Without JavaScript the same text is shown. */
(function () {
  "use strict";
  Array.prototype.forEach.call(document.querySelectorAll(".mail[data-user]"), function (el) {
    var user = el.getAttribute("data-user"), domain = el.getAttribute("data-domain");
    var link = document.createElement("a");
    link.href = "mailto:";
    link.className = "mail";
    link.textContent = el.textContent;
    link.addEventListener("click", function (e) {
      e.preventDefault();
      window.location.href = "mailto:" + user + String.fromCharCode(64) + domain;
    });
    el.parentNode.replaceChild(link, el);
  });
})();
