/* Entry notice: modal <dialog>, shown until ACCEPT is pressed, remembered for the browser session
   only (sessionStorage, no cookie). DECLINE is an ordinary link to https://google.com.
   Escape does not dismiss it (it is an acceptance gate, as on the previous site). */
(function () {
  "use strict";
  var dlg = document.getElementById("entry-notice");
  if (!dlg || typeof dlg.showModal !== "function") return;
  var KEY = "gwms-notice-accepted";
  try { if (window.sessionStorage.getItem(KEY) === "1") return; } catch (e) { /* storage blocked: show every time */ }

  dlg.addEventListener("cancel", function (e) { e.preventDefault(); });
  var accept = dlg.querySelector("[data-notice-accept]");
  accept.addEventListener("click", function () {
    try { window.sessionStorage.setItem(KEY, "1"); } catch (e) { /* ignore */ }
    dlg.close();
    document.documentElement.classList.remove("notice-open");
  });
  document.documentElement.classList.add("notice-open");
  dlg.showModal();
})();
