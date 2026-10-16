/* GWMS navigation — progressive enhancement.
   Without this script every link is visible in a stacked list (see .no-js rules).
   Pattern: disclosure buttons (aria-expanded + aria-controls), not ARIA menus.
   Opening is by click / tap / Enter / Space only (never hover), so behaviour is
   identical for mouse, keyboard and touch. */
(function () {
  "use strict";

  var header = document.querySelector(".site-header");
  var nav = document.getElementById("site-nav");
  var toggle = document.querySelector(".nav-toggle");
  if (!header || !nav) return;

  var triggers = Array.prototype.slice.call(nav.querySelectorAll("button[aria-controls]"));
  var desktop = window.matchMedia("(min-width: 70rem)");

  function panelOf(trigger) { return document.getElementById(trigger.getAttribute("aria-controls")); }

  function setOpen(trigger, open) {
    trigger.setAttribute("aria-expanded", open ? "true" : "false");
    panelOf(trigger).hidden = !open;
  }

  function closeAll(except) {
    triggers.forEach(function (t) { if (t !== except) setOpen(t, false); });
  }

  function setMenu(open) {
    if (!toggle) return;
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    header.classList.toggle("is-open", open);
    if (!open) closeAll();
  }

  // Start collapsed.
  triggers.forEach(function (t) { setOpen(t, false); });
  if (toggle) toggle.setAttribute("aria-expanded", "false");

  triggers.forEach(function (trigger) {
    trigger.addEventListener("click", function () {
      var open = trigger.getAttribute("aria-expanded") !== "true";
      // Desktop: one panel at a time. Mobile accordion: independent sections.
      if (desktop.matches) closeAll(trigger);
      setOpen(trigger, open);
    });

    // ArrowDown from a closed/open trigger moves into its panel.
    trigger.addEventListener("keydown", function (e) {
      if (e.key !== "ArrowDown") return;
      e.preventDefault();
      if (trigger.getAttribute("aria-expanded") !== "true") {
        if (desktop.matches) closeAll(trigger);
        setOpen(trigger, true);
      }
      var first = panelOf(trigger).querySelector("a");
      if (first) first.focus();
    });
  });

  if (toggle) {
    toggle.addEventListener("click", function () {
      setMenu(toggle.getAttribute("aria-expanded") !== "true");
    });
  }

  // Escape closes the innermost open thing and returns focus to its control.
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape") return;
    var openTrigger = triggers.filter(function (t) { return t.getAttribute("aria-expanded") === "true"; })[0];
    var focusInItem = openTrigger && openTrigger.parentElement.contains(document.activeElement);
    if (openTrigger && (desktop.matches || focusInItem)) {
      setOpen(openTrigger, false);
      openTrigger.focus();
    } else if (!desktop.matches && header.classList.contains("is-open")) {
      setMenu(false);
      toggle.focus();
    }
  });

  // Desktop: click outside, or keyboard focus leaving the navigation, closes panels.
  document.addEventListener("click", function (e) {
    if (desktop.matches && !header.contains(e.target)) closeAll();
  });
  // Desktop: when keyboard focus moves to anything outside the open item, close its panel.
  header.addEventListener("focusin", function (e) {
    if (!desktop.matches) return;
    triggers.forEach(function (t) {
      if (t.getAttribute("aria-expanded") === "true" && !t.parentElement.contains(e.target)) setOpen(t, false);
    });
  });
  document.addEventListener("focusin", function (e) {
    if (desktop.matches && !header.contains(e.target)) closeAll();
  });

  // Reset state when crossing the breakpoint.
  var onChange = function () { setMenu(false); closeAll(); };
  if (desktop.addEventListener) desktop.addEventListener("change", onChange);
  else desktop.addListener(onChange);
})();
