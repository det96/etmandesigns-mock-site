import "@fontsource-variable/outfit";
import "./style.css";

const header = document.querySelector(".site-header");
const toggle = document.querySelector(".nav-toggle");
const panel = document.querySelector(".nav-panel");
const progress = document.querySelector(".scroll-progress");
const form = document.querySelector("#quote-form");
const success = document.querySelector("#form-success");
const resetBtn = document.querySelector("#reset-form");

const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const sections = [...document.querySelectorAll("main section[id]")];

function markReveals() {
  const reveals = document.querySelectorAll(".reveal");
  if (reduceMotion || !("IntersectionObserver" in window)) {
    reveals.forEach((el) => el.classList.add("is-in"));
    return;
  }
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-in");
        observer.unobserve(entry.target);
      });
    },
    { threshold: 0.16, rootMargin: "0px 0px -8% 0px" },
  );
  reveals.forEach((el) => observer.observe(el));
}

function setCurrent(id) {
  document.querySelectorAll("[data-nav]").forEach((link) => {
    if (link.getAttribute("href") === `#${id}`) {
      link.setAttribute("aria-current", "true");
    } else {
      link.removeAttribute("aria-current");
    }
  });
}

function onScrollFrame() {
  const y = window.scrollY;
  header.classList.toggle("is-scrolled", y > 8);
  const max = document.documentElement.scrollHeight - window.innerHeight;
  const amount = max > 0 ? Math.min(1, Math.max(0, y / max)) : 0;
  progress.style.transform = `scaleX(${amount})`;

  const mark = y + 150;
  let current = "";
  for (const section of sections) {
    const top = section.getBoundingClientRect().top + y;
    if (top <= mark) current = section.id;
  }
  setCurrent(current);
}

let ticking = false;
function requestScroll() {
  if (ticking) return;
  ticking = true;
  requestAnimationFrame(() => {
    ticking = false;
    onScrollFrame();
  });
}

function menuIsOpen() {
  return toggle.getAttribute("aria-expanded") === "true";
}

function closeMenu(restoreFocus = false) {
  toggle.setAttribute("aria-expanded", "false");
  panel.classList.remove("is-open");
  panel.setAttribute("aria-hidden", "true");
  panel.setAttribute("inert", "");
  document.body.classList.remove("nav-open");
  header.classList.remove("is-menu-open");
  if (restoreFocus) toggle.focus();
}

function openMenu() {
  toggle.setAttribute("aria-expanded", "true");
  panel.removeAttribute("inert");
  panel.setAttribute("aria-hidden", "false");
  panel.classList.add("is-open");
  document.body.classList.add("nav-open");
  header.classList.add("is-menu-open");
  const first = panel.querySelector("a");
  first?.focus();
}

toggle.addEventListener("click", () => {
  if (menuIsOpen()) closeMenu(true);
  else openMenu();
});

panel.querySelectorAll('a[href^="#"]').forEach((link) => {
  link.addEventListener("click", () => closeMenu(false));
});

document.addEventListener("keydown", (event) => {
  if (!menuIsOpen()) return;
  if (event.key === "Escape") {
    closeMenu(true);
    return;
  }
  if (event.key !== "Tab") return;
  const items = [toggle, ...panel.querySelectorAll("a")];
  const first = items[0];
  const last = items[items.length - 1];
  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
});

const desktop = window.matchMedia("(min-width: 920px)");
desktop.addEventListener("change", (event) => {
  if (event.matches) closeMenu(false);
});

function cleanLine(value) {
  return String(value ?? "").replace(/[\r\n]+/g, " ").trim();
}

form.addEventListener("submit", (event) => {
  if (!form.checkValidity()) return;
  event.preventDefault();

  const name = cleanLine(form.elements.name.value);
  const business = cleanLine(form.elements.business.value);
  const email = cleanLine(form.elements.email.value);
  const phone = cleanLine(form.elements.phone.value);
  const need = cleanLine(form.elements.need.value);
  let message = String(form.elements.message.value ?? "").trim();
  if (message.length > 2000) {
    message = `${message.slice(0, 2000)}\n\n[Message truncated in this draft.]`;
  }

  const body = [
    `Name: ${name}`,
    `Business: ${business}`,
    `Email: ${email}`,
    `Phone: ${phone || "Not given"}`,
    `Need: ${need}`,
    "",
    message,
  ].join("\n");

  const href = `mailto:etmandesigns@gmail.com?subject=${encodeURIComponent(
    `Website quote for ${business}`,
  )}&body=${encodeURIComponent(body)}`;

  form.hidden = true;
  success.hidden = false;
  success.focus();

  const mail = document.createElement("a");
  mail.href = href;
  document.body.appendChild(mail);
  mail.click();
  mail.remove();
});

resetBtn.addEventListener("click", () => {
  success.hidden = true;
  form.hidden = false;
  form.elements.name.focus();
});

markReveals();
onScrollFrame();
window.addEventListener("scroll", requestScroll, { passive: true });
window.addEventListener("resize", requestScroll);
