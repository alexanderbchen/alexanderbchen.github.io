(function () {
  // KaTeX (same delimiters as the original site; no SRI so the CDN loads cleanly)
  if (window.renderMathInElement) {
    renderMathInElement(document.body, {
      delimiters: [
        { left: "\\[", right: "\\]", display: true },
        { left: "\\(", right: "\\)", display: false }
      ],
      throwOnError: false
    });
  }

  // Band reveal (numbered aside + underline + content fade), same as original.
  // threshold must stay 0: a section taller than the viewport can never reach a
  // percentage threshold (a 20,000px band in a 900px window peaks at ~4%), which
  // would leave its content stuck at opacity:0 forever.
  var bands = document.querySelectorAll(".band");
  if ("IntersectionObserver" in window) {
    var reveal = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting || e.intersectionRatio > 0) {
          e.target.classList.add("in"); reveal.unobserve(e.target);
        }
      });
    }, { rootMargin: "0px 0px -12% 0px", threshold: 0 });
    bands.forEach(function (b) { reveal.observe(b); });

    // Safety net: anything still unrevealed shortly after load gets shown.
    // Guards against a band already spanning the viewport on first paint, and
    // against late image layout shifting things around.
    window.setTimeout(function () {
      bands.forEach(function (b) {
        var r = b.getBoundingClientRect();
        if (!b.classList.contains("in") && r.top < window.innerHeight && r.bottom > 0) {
          b.classList.add("in"); reveal.unobserve(b);
        }
      });
    }, 700);
  } else {
    bands.forEach(function (b) { b.classList.add("in"); });
  }
})();
