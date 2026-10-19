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

  /* Generic slide down / up for any panel controlled by a nav button.
     Works on every `button[aria-controls]` in #site-nav, on desktop (absolute mega panel)
     and mobile (accordion) alike; no per-menu code. Duration: --slide-duration in CSS. */
  function slide(panel, open) {
    var token = (panel._slideToken = (panel._slideToken || 0) + 1);
    var sliding = panel.classList.contains("is-sliding");
    var from = sliding ? panel.getBoundingClientRect().height : (open ? 0 : panel.getBoundingClientRect().height);
    var borders = panel.offsetHeight - panel.clientHeight;
    function finish(fn) {
      var done = false;
      function end() { if (done || token !== panel._slideToken) return; done = true; panel.removeEventListener("transitionend", onEnd); fn(); }
      function onEnd(e) { if (e.target === panel && e.propertyName === "height") end(); }
      panel.addEventListener("transitionend", onEnd);
      window.setTimeout(end, 600);
    }
    if (open) {
      panel.hidden = false;
      panel.classList.add("is-open", "is-sliding");
      panel.style.height = from + "px";
      void panel.offsetHeight;                              // commit the starting height
      panel.style.height = panel.scrollHeight + borders + "px";
      finish(function () { panel.style.height = ""; panel.classList.remove("is-sliding"); });
    } else {
      panel.classList.add("is-sliding");
      panel.style.height = from + "px";
      void panel.offsetHeight;
      panel.style.height = "0px";
      finish(function () {
        panel.classList.remove("is-open", "is-sliding");
        panel.style.height = "";
        panel.hidden = true;
      });
    }
  }

  function setOpen(trigger, open, instant) {
    var panel = panelOf(trigger);
    var was = trigger.getAttribute("aria-expanded") === "true";
    trigger.setAttribute("aria-expanded", open ? "true" : "false");
    if (instant) {
      panel._slideToken = (panel._slideToken || 0) + 1;
      panel.classList.remove("is-sliding", "is-open"); panel.style.height = "";
      panel.hidden = !open; if (open) panel.classList.add("is-open");
      return;
    }
    if (open !== was) slide(panel, open);
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
  triggers.forEach(function (t) { setOpen(t, false, true); });
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
