/* Home page for the three DK themes. Every fact comes from window.CCEL (Jinuk's _shared/content.js)
   through the helpers in window.S1 (Jinuk's assets/site.js); the page layout follows Kiheon's C draft. */
(function () {
  'use strict';
  var S = window.S1, D = S.D, esc = S.esc, rich = S.rich;
  function $(id) { return document.getElementById(id); }
  function put(id, html) { var el = $(id); if (el) el.innerHTML = html; }
  var OLD = 'http://ccel.snu.ac.kr/';   // the lab films stay on the current server

  var w = D.welcome || {}, lab = D.lab || {}, R = D.research || {};
  var covers = D.cover_publications || [];
  var front = covers.filter(function (c) { return c.kind !== 'back_page'; });

  // ---- hero ----
  put('tagline', esc(w.tagline || ''));
  put('stats', [
    [S.D.publications.length, 'publications since 2007'],
    [covers.length, 'journal covers'],
    [S.memberCount(), 'current members'],
    [S.areas.length, 'research areas']
  ].map(function (s) {
    return '<div><b data-count="' + s[0] + '">' + s[0] + '</b><span>' + esc(s[1]) + '</span></div>';
  }).join(''));

  // ---- approach ----
  put('approach-text', (R.intro || []).slice(0, 1).map(esc).join(''));

  // ---- research: numbered rows, the area image follows the pointer on hover ----
  put('rlist', S.areas.map(function (a, i) {
    return '<li><a href="research.html#area-' + esc(a.numeral) + '" data-img="' + esc(S.asset(a.image)) + '">' +
      '<span class="rn">' + String(i + 1).padStart(2, '0') + '</span>' +
      '<span class="rt">' + rich(a.title) + '</span>' +
      '<span class="rk">' + (a.keywords || []).map(esc).join(' · ') + '</span>' +
      '<img class="rthumb" src="' + esc(S.asset(a.image)) + '" alt="" loading="lazy">' +
      '<span class="rarrow" aria-hidden="true">→</span></a></li>';
  }).join(''));

  // ---- news: "<names>'s paper ... accepted to <journal>!" -> names bold, journal italic ----
  put('news', (w.news || []).map(function (n) {
    var t = esc(n.text || '').replace(/!$/, '');
    t = t.replace(/^(.+?)(&#39;s)/, '<b>$1</b>$2').replace(/(accepted to )(.+)$/, '$1<i>$2</i>');
    return '<li>' + (n.date ? '<time>' + esc(n.date) + '</time>' : '') + '<p>' + t + '</p></li>';
  }).join(''));
  put('join-ko', esc(w.opening_ko || ''));
  var mail = (D.contact && D.contact.email) || (D.professor && D.professor.email) || '';
  var jm = $('join-mail'); if (jm) { jm.href = 'mailto:' + mail; jm.textContent = mail; }

  // ---- selected publications: the professor's pins; the journal cover when the paper has one ----
  var cur = S.curated();
  put('selgrid', cur.pins.map(function (x) {
    var p = x.p, a = S.areaBy[x.area || p.area], cov = S.coverFor(p, ['front']);
    var href = S.pubHref(p) || '#';
    var fig = cov
      ? '<div class="simg is-cover"><img src="' + esc(S.asset(cov.image)) + '" alt="" loading="lazy"></div>'
      : '<div class="simg is-tile" aria-hidden="true"><span class="tn">' + esc(a ? a.numeral : '') + '</span><span class="tt">' + (a ? rich(a.title) : '') + '</span></div>';
    return '<article class="scard"><a href="' + esc(href) + '" rel="noopener">' + fig +
      (a ? '<p class="sarea">' + esc(a.numeral) + ' · ' + rich(a.title) + '</p>' : '') +
      '<h3>' + rich(p.title) + '</h3><p class="ssrc">' + esc(S.source(p)) + '</p></a></article>';
  }).join(''));

  // ---- covers: two rows running in opposite directions; each row is doubled so the loop is seamless ----
  function row(list) {
    var one = list.map(function (c) {
      var p = S.paperForCover(c);
      return '<a href="' + esc(S.https(c.url)) + '" rel="noopener" title="' + esc(p ? S.strip(p.title) : 'Journal cover') + '">' +
        '<img src="' + esc(S.asset(c.image)) + '" alt="' + esc(p ? 'Journal cover: ' + S.strip(p.title) : 'Journal cover') + '" loading="lazy"></a>';
    }).join('');
    return one + one.replace(/<a /g, '<a aria-hidden="true" tabindex="-1" ');
  }
  var half = Math.ceil(front.length / 2);
  put('cov1', row(front.slice(0, half)));
  put('cov2', row(front.slice(half)));
  put('cov-all', 'All ' + covers.length + ' covers');

  // ---- partners ----
  var sp = (R.sponsors || []).map(function (s) { return '<img src="' + esc(S.asset(s)) + '" alt="" loading="lazy">'; }).join('');
  put('spon', sp + sp.replace(/<img /g, '<img aria-hidden="true" '));

  // ---- about + lab films ----
  put('about-ko', esc(w.about_ko || ''));
  put('films', (w.videos || []).map(function (v) {
    return '<figure><video controls preload="none" playsinline poster="' + esc(S.asset(v.poster)) + '">' +
      '<source src="' + esc(OLD + v.src) + '" type="video/mp4"></video>' +
      '<figcaption>Lab film · ' + (v.lang === 'ko' ? '한국어' : 'English') + '</figcaption></figure>';
  }).join(''));
})();
