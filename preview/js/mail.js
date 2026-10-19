/* Contact e-mail addresses are stored split in the page (data-user / data-domain) and joined here,
   as the previous site did. Without JavaScript the address is shown as "name [at] domain". */
(function () {
  "use strict";
  Array.prototype.forEach.call(document.querySelectorAll(".mail[data-user]"), function (el) {
    var address = el.getAttribute("data-user") + "@" + el.getAttribute("data-domain");
    var link = document.createElement("a");
    link.href = "mailto:" + address;
    link.textContent = el.getAttribute("data-label") || address;
    el.parentNode.replaceChild(link, el);
  });
})();
