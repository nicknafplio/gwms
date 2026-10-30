/* Cookie bar. Accept / Decline / More info (the Cookie Information page).
   Nothing optional is set before the visitor chooses, and Google Analytics 4 (G-4F1S9L903X) is loaded
   only after Accept (and on later visits while the choice is "accepted"). Decline or a later change of
   mind stops it and removes the Google Analytics cookies. The choice is stored in the cookie gwms_cookies
   ("accepted" or "declined", 12 months); if cookies cannot be written (blocked, or opened from disk) it is
   kept in sessionStorage for the session instead.
   - Accept: loads Google Analytics and allows the gwms_notice cookie (the entry-notice acceptance is then kept for 30 days).
   - Decline: removes any gwms_notice cookie; the notice acceptance is then remembered for the tab session only.
   The bar appears once the entry notice is closed, and can be reopened from the Cookie Information page
   ([data-cookie-reopen]). */
(function () {
  "use strict";
  var bar = document.getElementById("cookie-bar");
  if (!bar) return;
  var CHOICE = "gwms_cookies", NOTICE = "gwms_notice", CHOICE_DAYS = 365, NOTICE_DAYS = 30;
  var secure = location.protocol === "https:" ? "; Secure" : "";
  var GA_ID = "G-4F1S9L903X";

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

  /* ---- Google Analytics 4: only with consent ---- */
  var gaLoaded = false;
  function loadAnalytics() {
    if (gaLoaded) return;
    gaLoaded = true;
    window["ga-disable-" + GA_ID] = false;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", GA_ID, { allow_google_signals: false, allow_ad_personalization_signals: false });
    var el = document.createElement("script");
    el.async = true;
    el.src = "https://www.googletagmanager.com/gtag/js?id=" + GA_ID;
    document.head.appendChild(el);
  }
  function stopAnalytics() {
    window["ga-disable-" + GA_ID] = true;
    var names = ["_ga", "_ga_" + GA_ID.replace("G-", ""), "_gid", "_gat"];
    var host = location.hostname, parts = host.split("."), domains = ["", host, "." + host];
    for (var i = 1; i < parts.length - 1; i++) domains.push("." + parts.slice(i).join("."));
    names.forEach(function (n) {
      domains.forEach(function (d) {
        document.cookie = n + "=; max-age=0; path=/" + (d ? "; domain=" + d : "") + "; SameSite=Lax" + secure;
      });
    });
  }

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
      loadAnalytics();
    } else {
      clearCookie(NOTICE);
      stopAnalytics();
    }
    hide();
    document.dispatchEvent(new CustomEvent("gwms:cookie-choice", { detail: value }));
  }

  bar.querySelector("[data-cookie-accept]").addEventListener("click", function () { decide("accepted"); });
  bar.querySelector("[data-cookie-decline]").addEventListener("click", function () { decide("declined"); });
  window.addEventListener("resize", resize);

  if (choice() === "accepted") loadAnalytics();

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
