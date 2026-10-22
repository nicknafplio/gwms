/* Cookie bar. Accept / Decline / More info (the Cookie Information page).
   Nothing optional is set before the visitor chooses. The choice is stored in the cookie gwms_cookies
   ("accepted" or "declined", 12 months); if cookies cannot be written (blocked, or opened from disk) it is
   kept in sessionStorage for the session instead.
   - Accept: allows the gwms_notice cookie (the entry-notice acceptance is then kept for 30 days).
   - Decline: removes any gwms_notice cookie; the notice acceptance is then remembered for the tab session only.
   The bar appears once the entry notice is closed, and can be reopened from the Cookie Information page
   ([data-cookie-reopen]). No analytics or advertising cookies exist on this site. */
(function () {
  "use strict";
  var bar = document.getElementById("cookie-bar");
  if (!bar) return;
  var CHOICE = "gwms_cookies", NOTICE = "gwms_notice", CHOICE_DAYS = 365, NOTICE_DAYS = 30;
  var secure = location.protocol === "https:" ? "; Secure" : "";

  function getCookie(name) {
    var m = document.cookie.split("; ").filter(function (c) { return c.indexOf(name + "=") === 0; })[0];
    return m ? m.slice(name.length + 1) : "";
  }
  function setCookie(name, value, days) {
    document.cookie = name + "=" + value + "; max-age=" + days * 86400 + "; path=/; SameSite=Lax" + secure;
  }
  function clearCookie(name) { document.cookie = name + "=; max-age=0; path=/; SameSite=Lax" + secure; }
  function session(key, value) {
    try { if (value === undefined) return window.sessionStorage.getItem(key); window.sessionStorage.setItem(key, value); } catch (e) { /* ignore */ }
    return null;
  }
  function choice() { return getCookie(CHOICE) || session(CHOICE) || ""; }

  function resize() {
    document.documentElement.style.setProperty("--cookie-bar-h", bar.hidden ? "0px" : bar.offsetHeight + "px");
  }
  function show() { bar.hidden = false; document.documentElement.classList.add("cookie-bar-open"); resize(); }
  function hide() { bar.hidden = true; document.documentElement.classList.remove("cookie-bar-open"); resize(); }

  function decide(value) {
    setCookie(CHOICE, value, CHOICE_DAYS);
    if (!getCookie(CHOICE)) session(CHOICE, value);          // cookies unavailable: remember for this session
    if (value === "accepted") {
      if (session(NOTICE) === "1") setCookie(NOTICE, "1", NOTICE_DAYS);
    } else {
      clearCookie(NOTICE);
    }
    hide();
    document.dispatchEvent(new CustomEvent("gwms:cookie-choice", { detail: value }));
  }

  bar.querySelector("[data-cookie-accept]").addEventListener("click", function () { decide("accepted"); });
  bar.querySelector("[data-cookie-decline]").addEventListener("click", function () { decide("declined"); });
  window.addEventListener("resize", resize);

  function maybeShow() {
    if (!choice() && !document.documentElement.classList.contains("notice-open")) show();
  }
  document.addEventListener("gwms:notice-closed", maybeShow);
  maybeShow();

  // "Review your cookie choice" (Cookie Information page)
  var reopen = document.querySelectorAll("[data-cookie-reopen]");
  Array.prototype.forEach.call(reopen, function (b) {
    b.hidden = false;
    b.addEventListener("click", function () { show(); bar.querySelector("button").focus(); });
  });
})();
