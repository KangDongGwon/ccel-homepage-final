/* Scroll motion shared by every page of the three DK themes (from the 261026 mockups, extended to the inner pages):
   Lenis smooth scroll, progress bar, header that hides on the way down, reveal on entry, headline word rise,
   counters, hero parallax, scroll-scaled approach figure, research-row image that follows the pointer.
   Everything that moves keys off html.js, which the <head> skips under prefers-reduced-motion. */
(function () {
  'use strict';
  var H = document.documentElement, motion = H.classList.contains('js');
  function $(s) { return document.querySelector(s); }
  function $$(s) { return [].slice.call(document.querySelectorAll(s)); }
  document.querySelectorAll('a[href="#"]').forEach(function (a) { a.addEventListener('click', function (e) { e.preventDefault(); }); });

  var bar = $('.progress'), hdr = $('.site-hdr'), nav = document.getElementById('site-nav');
  var heroImg = $('.hero-media img'), ap = $('.approach img'), last = scrollY, tick = false;
  function upd() {
    tick = false;
    var y = scrollY, vh = innerHeight, max = H.scrollHeight - vh;
    if (bar) bar.style.transform = 'scaleX(' + (max > 0 ? y / max : 0) + ')';
    if (hdr) {
      hdr.classList.toggle('scrolled', y > 8);
      var open = nav && nav.classList.contains('is-open');
      if (motion && !open && y > 240 && y > last + 4) hdr.classList.add('hide');
      else if (y < last - 4 || y <= 240) hdr.classList.remove('hide');
    }
    last = y;
    if (!motion) return;
    if (heroImg && y < vh * 1.5) heroImg.style.setProperty('--py', (y * .12).toFixed(1) + 'px');
    if (ap) {
      var r = ap.getBoundingClientRect();
      ap.style.setProperty('--p', Math.max(0, Math.min(1, (vh - r.top) / (vh * .75))).toFixed(3));
    }
  }
  addEventListener('scroll', function () { if (!tick) { tick = true; requestAnimationFrame(upd); } }, { passive: true });
  addEventListener('resize', upd);
  upd();
  if (!motion) return;

  // headline word rise: the home hero and the inner page titles
  $$('.hero h1, .page-head h1').forEach(function (h1) {
    if (h1.children.length) return;
    h1.innerHTML = h1.textContent.trim().split(/\s+/).map(function (w, i) {
      return '<span class="w"><span style="--d:' + (.1 + i * .055).toFixed(2) + 's">' + w + '</span></span>';
    }).join(' ');
    h1.classList.add('rise');
  });

  // reveal: [selector, first delay, step]; siblings stagger, capped so long lists do not lag
  var GROUPS = [
    ['.hero .pill', .05], ['.hero .lead', .4], ['.hero .cta', .55], ['.stats > div', .7, .1],
    ['.home .sec-top', 0], ['.home .eyebrow', 0], ['.approach p', .1], ['.approach .more', .2],
    ['.rlist li', .02, .07], ['.newslist li', .02, .07], ['.joinbox', .1], ['.scard', .02, .08],
    ['.marquee', .1], ['.films figure', .05, .1], ['.about p', .1], ['.about h2', 0],
    ['.page-head .lede', .25], ['.page-head .subnav', .35], ['.toc', .3], ['.research-intro', 0], ['.fig', .1],
    ['.area', 0], ['.cite', 0, .05], ['.mrow', 0, .04], ['.ghead', 0], ['.vhead', 0], ['.profile', 0], ['.cv h2', 0],
    ['.cv-entry', 0, .03], ['.group-photo', 0], ['.contact-card', 0, .08], ['.filters', .1], ['.year > h2', 0], ['.pub', 0, .03],
    ['.cover-grid figure', 0, .04]
  ];
  GROUPS.forEach(function (g) {
    $$(g[0]).forEach(function (el) {
      var sibs = [].slice.call(el.parentElement.children).filter(function (c) { return c.matches(g[0]); });
      var i = sibs.indexOf(el) % 8;
      el.setAttribute('data-r', '');
      el.style.setProperty('--d', Math.min((g[1] || 0) + i * (g[2] || .08), .7).toFixed(2) + 's');
    });
  });
  if (heroImg) heroImg.setAttribute('data-ri', '');
  $$('[data-count]').forEach(function (b) { b.textContent = '0'; });
  function count(b) {
    var n = +b.getAttribute('data-count'), t0 = performance.now(), D = 1600;
    (function f(t) { var p = Math.min((t - t0) / D, 1); b.textContent = Math.round(n * (1 - Math.pow(1 - p, 3))); if (p < 1) requestAnimationFrame(f); })(t0);
  }
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) {
      if (!e.isIntersecting) return;
      io.unobserve(e.target);
      e.target.classList.add('in');
      e.target.querySelectorAll('[data-count]').forEach(count);
    });
  }, { threshold: .12, rootMargin: '0px 0px -5% 0px' });
  $$('[data-r], [data-ri], h1.rise').forEach(function (el) { io.observe(el); });

  // research rows: one floating image that follows the pointer (desktop pointers only)
  var peek = $('.rpeek'), list = $('.rlist');
  if (peek && list && matchMedia('(hover: hover) and (pointer: fine)').matches) {
    var img = peek.querySelector('img'), px = 0, py = 0, tx = 0, ty = 0, on = false;
    list.addEventListener('mouseover', function (e) {
      var a = e.target.closest('a[data-img]'); if (!a) return;
      if (img.getAttribute('src') !== a.getAttribute('data-img')) img.src = a.getAttribute('data-img');
      on = true; peek.classList.add('on');
    });
    list.addEventListener('mouseleave', function () { on = false; peek.classList.remove('on'); });
    addEventListener('mousemove', function (e) { tx = e.clientX; ty = e.clientY; }, { passive: true });
    (function follow() {
      px += (tx - px) * .16; py += (ty - py) * .16;
      peek.style.transform = 'translate(' + (px + 28).toFixed(1) + 'px,' + (py - 110).toFixed(1) + 'px)';
      requestAnimationFrame(follow);
    })();
  }

  // Lenis, then smooth in-page anchors
  var lenis = null;
  function startLenis() {
    if (!window.Lenis || lenis) return;
    lenis = window.__lenis = new Lenis({ lerp: .09 });
    (function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })(performance.now());
  }
  if (document.readyState === 'complete') startLenis(); else addEventListener('load', startLenis);
  $$('a[href^="#"]:not([href="#"])').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var t = document.getElementById(a.getAttribute('href').slice(1));
      if (!t || a.getAttribute('role') === 'tab') return;
      e.preventDefault(); if (hdr) hdr.classList.remove('hide');
      if (lenis) lenis.scrollTo(t, { offset: -90 }); else t.scrollIntoView({ behavior: 'smooth' });
    });
  });
})();
