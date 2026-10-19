/* Runs in <head> before first paint: marks the document as script-capable so
   the CSS can switch from the no-JavaScript fallback to the enhanced navigation. */
document.documentElement.className = document.documentElement.className.replace("no-js", "js");
