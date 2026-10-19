/* Entry notice: modal <dialog>, shown until ACCEPT is pressed. Acceptance is remembered in a cookie
   (gwms_notice, 30 days, this site only), as described on the Cookie Information page: "a cookie is
   created that tells whether or not to display the popup". If cookies are unavailable (blocked, or the
   page is opened from disk) it falls back to sessionStorage for the browser session.
   DECLINE is an ordinary link to https://google.com and sets nothing.
   Escape does not dismiss it (it is an acceptance gate, as on the previous site). */
(function () {
  "use strict";
  var dlg = document.getElementById("entry-notice");
  if (!dlg || typeof dlg.showModal !== "function") return;
  var KEY = "gwms_notice", DAYS = 30;

  function accepted() {
    if (document.cookie.split("; ").indexOf(KEY + "=1") !== -1) return true;
    try { return window.sessionStorage.getItem(KEY) === "1"; } catch (e) { return false; }
  }
  function remember() {
    document.cookie = KEY + "=1; max-age=" + DAYS * 86400 + "; path=/; SameSite=Lax" + (location.protocol === "https:" ? "; Secure" : "");
    if (document.cookie.split("; ").indexOf(KEY + "=1") === -1) {
      try { window.sessionStorage.setItem(KEY, "1"); } catch (e) { /* shown again next page */ }
    }
  }
  if (accepted()) return;

  dlg.addEventListener("cancel", function (e) { e.preventDefault(); });
  dlg.querySelector("[data-notice-accept]").addEventListener("click", function () {
    remember();
    dlg.close();
    document.documentElement.classList.remove("notice-open");
  });
  document.documentElement.classList.add("notice-open");
  dlg.showModal();
})();
