/*
  In-page links scroll with a JS animation on purpose.
  Chrome can report prefers-reduced-motion (including on file:// previews)
  and will ignore CSS scroll-behavior and scrollIntoView({behavior:"smooth"}).
  Decorative motion still turns off. This scroll animation does not.
*/
(function () {
  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".menu-toggle");
  var nav = document.getElementById("site-nav");
  var scrollToken = 0;

  function headerOffset() {
    if (!header) return 0;
    return Math.ceil(header.getBoundingClientRect().height) + 10;
  }

  function setMenu(open) {
    if (!toggle || !nav) return;
    nav.classList.toggle("is-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    document.body.classList.toggle("menu-open", open);
    if (open) {
      var first = nav.querySelector("a");
      if (first) first.focus();
    }
  }

  function smoothScrollTo(targetY) {
    var token = ++scrollToken;
    var startY = window.pageYOffset || document.documentElement.scrollTop || 0;
    var distance = targetY - startY;
    if (Math.abs(distance) < 2) {
      window.scrollTo(0, targetY);
      return;
    }
    var duration = Math.min(900, Math.max(480, Math.abs(distance) * 0.45));
    var start = null;

    function ease(t) {
      return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }

    function frame(now) {
      if (token !== scrollToken) return;
      if (start === null) start = now;
      var t = Math.min(1, (now - start) / duration);
      window.scrollTo(0, startY + distance * ease(t));
      if (t < 1) window.requestAnimationFrame(frame);
    }

    window.requestAnimationFrame(frame);
  }

  function scrollToId(id) {
    var y = 0;
    var target = null;
    if (id && id !== "top") {
      target = document.getElementById(id);
      if (!target) return false;
      y = target.getBoundingClientRect().top + (window.pageYOffset || 0) - headerOffset();
      if (y < 0) y = 0;
    }
    setMenu(false);
    smoothScrollTo(y);
    if (target) {
      target.setAttribute("tabindex", "-1");
      if (target.focus) target.focus({ preventScroll: true });
    }
    try {
      history.pushState(null, "", "#" + (id || "top"));
    } catch (err) {
      /* file:// can reject history changes; the animated scroll still runs. */
    }
    return true;
  }

  document.addEventListener("click", function (event) {
    var node = event.target;
    var link = null;
    while (node && node !== document) {
      if (node.tagName === "A") {
        link = node;
        break;
      }
      node = node.parentNode;
    }
    if (!link) return;
    var href = link.getAttribute("href");
    if (!href || href.charAt(0) !== "#") return;
    if (link.getAttribute("target")) return;
    var id = href.slice(1);
    if (!id) return;
    if (id !== "top" && !document.getElementById(id)) return;
    event.preventDefault();
    scrollToId(id);
  });

  if (toggle) {
    toggle.addEventListener("click", function () {
      setMenu(toggle.getAttribute("aria-expanded") !== "true");
    });
  }

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && nav && nav.classList.contains("is-open")) {
      setMenu(false);
      if (toggle) toggle.focus();
    }
  });

  var form = document.getElementById("request-form");
  var result = document.getElementById("form-demo-result");
  if (form) {
    form.addEventListener("submit", function (event) {
      event.preventDefault();
      if (typeof form.checkValidity === "function" && !form.checkValidity()) {
        if (form.reportValidity) form.reportValidity();
        return;
      }
      if (result) result.hidden = false;
    });
  }

  var reduce = false;
  try {
    reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  } catch (err) {
    reduce = false;
  }

  if (!reduce && "IntersectionObserver" in window) {
    var nodes = document.querySelectorAll(".reveal");
    if (nodes.length) {
      var observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            entry.target.classList.add("is-in");
            observer.unobserve(entry.target);
          });
        },
        { threshold: 0.14, rootMargin: "0px 0px -6% 0px" }
      );
      Array.prototype.forEach.call(nodes, function (node) {
        observer.observe(node);
      });
      window.setTimeout(function () {
        Array.prototype.forEach.call(nodes, function (node) {
          node.classList.add("is-in");
        });
      }, 4000);
    }
  } else {
    Array.prototype.forEach.call(document.querySelectorAll(".reveal"), function (node) {
      node.classList.add("is-in");
    });
  }
})();
