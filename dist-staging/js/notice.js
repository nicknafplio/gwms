/* Entry notice: modal <dialog>, shown until ACCEPT is pressed. DECLINE is an ordinary link to
   https://google.com and sets nothing. Escape does not dismiss it (it is an acceptance gate).

   Remembering the acceptance depends on the visitor's cookie choice (see cookie-bar.js):
   - always: kept in sessionStorage (this browser tab/session only, not a cookie);
   - only if cookies were accepted: also stored in the cookie gwms_notice for 30 days. */
(function () {
  "use strict";
  var dlg = document.getElementById("entry-notice");
  if (!dlg || typeof dlg.showModal !== "function") return;
  var KEY = "gwms_notice", DAYS = 30;

  function hasCookie(name, value) { return document.cookie.split("; ").indexOf(name + "=" + value) !== -1; }
  function accepted() {
    if (hasCookie(KEY, "1")) return true;
    try { return window.sessionStorage.getItem(KEY) === "1"; } catch (e) { return false; }
  }
  function remember() {
    try { window.sessionStorage.setItem(KEY, "1"); } catch (e) { /* ignore */ }
    if (hasCookie("gwms_cookies", "accepted")) {
      document.cookie = KEY + "=1; max-age=" + DAYS * 86400 + "; path=/; SameSite=Lax" + (location.protocol === "https:" ? "; Secure" : "");
    }
  }
  if (accepted()) return;

  dlg.addEventListener("cancel", function (e) { e.preventDefault(); });
  dlg.querySelector("[data-notice-accept]").addEventListener("click", function () {
    remember();
    dlg.close();
    document.documentElement.classList.remove("notice-open");
    document.dispatchEvent(new CustomEvent("gwms:notice-closed"));
  });
  document.documentElement.classList.add("notice-open");
  dlg.showModal();
  dlg.scrollTop = 0;   // on small screens the autofocused button must not scroll the heading out of view
})();
