(function () {
  "use strict";

  document.documentElement.classList.add("js");

  var logoFiles = {
    a: "logo-concepts/a-state-line/logo-header.svg",
    b: "logo-concepts/b-schematic/logo-header.svg",
    c: "logo-concepts/c-monogram/logo-header.svg",
    d: "logo-concepts/d-field-badge/logo-header.svg"
  };
  var logoChoice = "";
  try {
    logoChoice = new URLSearchParams(window.location.search).get("logo") || "";
  } catch (err) {
    logoChoice = "";
  }
  if (logoFiles[logoChoice]) {
    var logoImg = document.querySelector(".logo img");
    if (logoImg) {
      logoImg.src = logoFiles[logoChoice];
      logoImg.removeAttribute("width");
      logoImg.removeAttribute("height");
    }
  }

  var header = document.querySelector(".site-header");
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");
  var form = document.querySelector("#bid-form");
  var success = document.querySelector("#form-success");
  var sections = Array.prototype.slice.call(document.querySelectorAll("main section[id]"));
  var desktop = window.matchMedia("(min-width: 980px)");

  var glideToken = 0;
  var glideFrame = 0;

  function syncHeader() {
    if (!header) return;
    var rect = header.getBoundingClientRect();
    var height = Math.ceil(rect.height);
    document.documentElement.style.setProperty("--header-h", height + "px");
    document.documentElement.style.setProperty("--header-bottom", Math.ceil(rect.bottom) + "px");
    var hero = document.querySelector(".hero");
    var pastHero = hero ? hero.getBoundingClientRect().bottom < height : window.scrollY > 8;
    header.classList.toggle("is-scrolled", pastHero);
  }

  function headerClearance() {
    return Math.ceil(header.getBoundingClientRect().height) + 12;
  }

  function scrollInstant(y) {
    var root = document.scrollingElement || document.documentElement;
    root.scrollTop = y;
  }

  function destination(el) {
    var root = document.scrollingElement || document.documentElement;
    if (!el || el.id === "top") return 0;
    var top = el.getBoundingClientRect().top + root.scrollTop - headerClearance();
    var max = Math.max(0, root.scrollHeight - root.clientHeight);
    return Math.max(0, Math.min(top, max));
  }

  function cancelGlide() {
    glideToken += 1;
    if (glideFrame) {
      cancelAnimationFrame(glideFrame);
      glideFrame = 0;
    }
  }

  // Anchor glides always run, including when Windows reports reduced motion.
  // Chrome drops CSS smooth-scroll in that mode, so the offset is driven here.
  function glideTo(el) {
    var token = ++glideToken;
    if (glideFrame) cancelAnimationFrame(glideFrame);
    var root = document.scrollingElement || document.documentElement;
    var start = root.scrollTop;
    var end = destination(el);
    var distance = Math.abs(end - start);
    var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var duration = reduced
      ? Math.min(480, Math.max(320, distance * 0.22))
      : Math.min(900, Math.max(520, distance * 0.4));

    function ease(t) {
      return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
    }

    if (distance < 2) {
      scrollInstant(end);
      return;
    }

    var t0 = performance.now();
    function step(now) {
      if (token !== glideToken) return;
      var t = Math.min(1, (now - t0) / duration);
      scrollInstant(start + (end - start) * ease(t));
      if (t < 1) {
        glideFrame = requestAnimationFrame(step);
        return;
      }
      scrollInstant(end);
      glideFrame = 0;
      if (el && el.id !== "top" && typeof el.focus === "function") {
        el.focus({ preventScroll: true });
      }
    }
    glideFrame = requestAnimationFrame(step);
  }

  function setHash(id) {
    var next = "#" + id;
    if (location.hash === next) return;
    try {
      history.pushState(null, "", next);
    } catch (err) {
      var root = document.scrollingElement || document.documentElement;
      var y = root.scrollTop;
      location.hash = id;
      root.scrollTop = y;
    }
  }

  function menuIsOpen() {
    return toggle.getAttribute("aria-expanded") === "true";
  }

  function syncNavA11y() {
    var mobileClosed = !desktop.matches && !menuIsOpen();
    if (mobileClosed) {
      nav.setAttribute("aria-hidden", "true");
      nav.setAttribute("inert", "");
    } else {
      nav.removeAttribute("aria-hidden");
      nav.removeAttribute("inert");
    }
  }

  function closeMenu(restoreFocus) {
    var wasOpen = menuIsOpen();
    var y = parseInt(document.body.dataset.scrollY || "0", 10);
    toggle.setAttribute("aria-expanded", "false");
    nav.classList.remove("is-open");
    document.body.classList.remove("nav-open");
    document.body.style.top = "";
    syncNavA11y();
    if (wasOpen) scrollInstant(y);
    if (restoreFocus) toggle.focus();
  }

  function openMenu() {
    document.body.dataset.scrollY = String(window.scrollY || 0);
    document.body.style.top = "-" + (window.scrollY || 0) + "px";
    document.body.classList.add("nav-open");
    nav.classList.add("is-open");
    toggle.setAttribute("aria-expanded", "true");
    syncNavA11y();
    var first = nav.querySelector("a");
    if (first) first.focus();
  }

  toggle.addEventListener("click", function () {
    if (menuIsOpen()) closeMenu(true);
    else openMenu();
  });

  document.addEventListener("click", function (event) {
    if (event.defaultPrevented || event.button !== 0) return;
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    var link = event.target.closest("a[href^='#']");
    if (!link) return;
    var id = link.getAttribute("href").slice(1);
    if (!id) return;
    var target = document.getElementById(id);
    if (!target) return;
    event.preventDefault();
    var fromMenu = menuIsOpen() && nav.contains(link);
    if (fromMenu) closeMenu(false);
    setHash(id);
    glideTo(target);
  });

  window.addEventListener("popstate", function () {
    var id = location.hash.replace(/^#/, "");
    var target = document.getElementById(id) || document.getElementById("top");
    if (target) glideTo(target);
  });

  window.addEventListener("wheel", cancelGlide, { passive: true });
  window.addEventListener("touchmove", cancelGlide, { passive: true });
  window.addEventListener("keydown", function (event) {
    var keys = { ArrowUp: 1, ArrowDown: 1, PageUp: 1, PageDown: 1, Home: 1, End: 1, " ": 1 };
    if (keys[event.key]) cancelGlide();
    if (!menuIsOpen()) return;
    if (event.key === "Escape") {
      closeMenu(true);
      return;
    }
    if (event.key !== "Tab") return;
    var items = [toggle].concat(Array.prototype.slice.call(nav.querySelectorAll("a, button")));
    var first = items[0];
    var last = items[items.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  desktop.addEventListener("change", function (event) {
    if (event.matches) closeMenu(false);
    syncNavA11y();
  });

  function setCurrent() {
    var y = window.scrollY || 0;
    var mark = y + headerClearance() + 8;
    var current = "";
    sections.forEach(function (section) {
      var top = section.getBoundingClientRect().top + y;
      if (top <= mark) current = section.id;
    });
    document.querySelectorAll("[data-nav]").forEach(function (link) {
      if (link.getAttribute("href") === "#" + current) link.setAttribute("aria-current", "true");
      else link.removeAttribute("aria-current");
    });
  }

  var ticking = false;
  function requestScroll() {
    if (ticking) return;
    ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      syncHeader();
      setCurrent();
    });
  }

  function clean(value) {
    return String(value || "").replace(/[\r\n]+/g, " ").trim();
  }

  function addLine(dl, label, value) {
    var row = document.createElement("div");
    var dt = document.createElement("dt");
    var dd = document.createElement("dd");
    dt.textContent = label;
    dd.textContent = value || "—";
    row.appendChild(dt);
    row.appendChild(dd);
    dl.appendChild(row);
  }

  if (form && success) {
    form.addEventListener("submit", function (event) {
      if (!form.checkValidity()) return;
      event.preventDefault();
      success.replaceChildren();

      var title = document.createElement("h3");
      title.textContent = "Kept on this page";
      var note = document.createElement("p");
      note.className = "demo-flag";
      note.textContent = "Demonstration only. This request was not sent and was not saved.";
      var dl = document.createElement("dl");
      addLine(dl, "Name", clean(form.elements.name.value));
      addLine(dl, "Company", clean(form.elements.company.value));
      addLine(dl, "Phone", clean(form.elements.phone.value));
      addLine(dl, "Email", clean(form.elements.email.value));
      addLine(dl, "Request", clean(form.elements.request.value));
      addLine(dl, "Project", clean(form.elements.site.value) || "Not given");
      var notes = document.createElement("p");
      notes.className = "echo-notes";
      notes.textContent = String(form.elements.message.value || "").trim();

      var again = document.createElement("button");
      again.type = "button";
      again.className = "button button-outline";
      again.textContent = "Edit the note";
      again.addEventListener("click", function () {
        success.hidden = true;
        success.replaceChildren();
        form.hidden = false;
        form.elements.name.focus();
      });

      success.appendChild(title);
      success.appendChild(note);
      success.appendChild(dl);
      success.appendChild(notes);
      success.appendChild(again);
      form.hidden = true;
      success.hidden = false;
      success.focus();
    });
  }

  function markReveals() {
    var nodes = Array.prototype.slice.call(document.querySelectorAll(".reveal"));
    if (!nodes.length) return;
    function arm(el) {
      el.classList.add("is-in");
    }
    nodes.forEach(function (el) {
      var rect = el.getBoundingClientRect();
      if (rect.top < window.innerHeight * 0.94 && rect.bottom > 0) arm(el);
    });
    if (!("IntersectionObserver" in window)) {
      nodes.forEach(arm);
      return;
    }
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          arm(entry.target);
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -6% 0px" }
    );
    nodes.forEach(function (el) {
      if (!el.classList.contains("is-in")) observer.observe(el);
    });
  }

  syncHeader();
  syncNavA11y();
  setCurrent();
  markReveals();

  if (location.hash) {
    var openEl = document.getElementById(location.hash.replace(/^#/, ""));
    if (openEl) scrollInstant(destination(openEl));
  }

  window.addEventListener("scroll", requestScroll, { passive: true });
  window.addEventListener("resize", requestScroll);
  window.addEventListener("load", function () {
    syncHeader();
    if (!location.hash) return;
    var el = document.getElementById(location.hash.replace(/^#/, ""));
    if (el) scrollInstant(destination(el));
  });
})();
