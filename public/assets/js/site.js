// Mobiel menu openen en sluiten
(function () {
  var knop = document.querySelector('.menu-knop');
  var menu = document.getElementById('mobiel-menu');
  if (!knop || !menu) return;

  function zet(open) {
    menu.setAttribute('data-open', String(open));
    knop.setAttribute('aria-expanded', String(open));
    knop.setAttribute('aria-label', knop.getAttribute(open ? 'data-close-label' : 'data-open-label'));
    document.body.classList.toggle('menu-open', open);
  }

  knop.addEventListener('click', function () {
    zet(menu.getAttribute('data-open') !== 'true');
  });
  menu.addEventListener('click', function (e) {
    if (e.target.closest('a')) zet(false);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && menu.getAttribute('data-open') === 'true') { zet(false); knop.focus(); }
  });
  window.addEventListener('resize', function () {
    if (window.innerWidth > 1080 && menu.getAttribute('data-open') === 'true') zet(false);
  });
})();

// Taalkeuze in de header: sluit bij klik ernaast of Escape
(function () {
  var taal = document.querySelector('.taal');
  if (!taal) return;
  document.addEventListener('click', function (e) { if (taal.open && !taal.contains(e.target)) taal.open = false; });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && taal.open) { taal.open = false; taal.querySelector('summary').focus(); }
  });
})();

// Cookietoestemming en Google Analytics (laadt pas na "Akkoord")
(function () {
  var GA_ID = 'G-R9JLS0EYGG';
  var SLEUTEL = 'od-cookies';
  var banner = document.getElementById('cookiebanner');

  function lees() { try { return localStorage.getItem(SLEUTEL); } catch (e) { return null; } }
  function bewaar(v) { try { localStorage.setItem(SLEUTEL, v); } catch (e) {} }
  function toon(zichtbaar) { if (banner) banner.hidden = !zichtbaar; }

  function laadAnalytics() {
    if (window.__odGa) return;
    window.__odGa = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID);
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
  }

  function wisAnalyticsCookies() {
    document.cookie.split(';').forEach(function (c) {
      var naam = c.split('=')[0].trim();
      if (naam.indexOf('_ga') === 0) {
        document.cookie = naam + '=; Max-Age=0; path=/; domain=.opperdash.be';
        document.cookie = naam + '=; Max-Age=0; path=/';
      }
    });
  }

  var keuze = lees();
  if (keuze === 'ja') laadAnalytics();
  else if (keuze !== 'nee') toon(true);

  document.addEventListener('click', function (e) {
    var el = e.target.closest('[data-cookies]');
    if (!el) return;
    var actie = el.getAttribute('data-cookies');
    if (actie === 'open') { e.preventDefault(); toon(true); return; }
    bewaar(actie);
    toon(false);
    if (actie === 'ja') laadAnalytics(); else wisAnalyticsCookies();
  });
})();

// Veelgestelde vragen: ook bij dichtklappen een korte animatie
(function () {
  var stil = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.faq details').forEach(function (d) {
    var s = d.querySelector('summary');
    if (!s) return;
    s.addEventListener('click', function (e) {
      if (!d.open || stil) return;
      e.preventDefault();
      d.classList.add('sluit');
      setTimeout(function () { d.open = false; d.classList.remove('sluit'); }, 200);
    });
  });
})();

// Micro-animaties: onthullen bij scrollen en schaduw onder de header
(function () {
  var stil = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var header = document.querySelector('.header');
  if (header) {
    var bezig = false;
    var check = function () { header.classList.toggle('is-gescrold', window.scrollY > 8); bezig = false; };
    window.addEventListener('scroll', function () { if (!bezig) { bezig = true; requestAnimationFrame(check); } }, { passive: true });
    check();
  }

  if (stil || !('IntersectionObserver' in window)) return;
  // Alleen beelden en kaarten; tekst staat meteen vast, zodat lezen niet wacht op een animatie.
  var selectie = 'main .duo__beeld, main .case-kaart, main .beeld:not(.beeld--vast) img';
  var hoogte = window.innerHeight;
  var io = new IntersectionObserver(function (items) {
    items.forEach(function (it) {
      if (!it.isIntersecting) return;
      var el = it.target;
      el.classList.add('is-zichtbaar');
      io.unobserve(el);
      // Na de animatie de hulpklassen weghalen, zodat de gewone hover-effecten weer werken.
      setTimeout(function () { el.classList.remove('onthul', 'is-zichtbaar'); el.style.removeProperty('--vertraging'); }, 1200);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

  var vorige = null, teller = 0;
  document.querySelectorAll(selectie).forEach(function (el) {
    // Wat al in beeld staat bij het laden, blijft gewoon staan (geen flits, geen vertraging van de eerste weergave).
    if (el.getBoundingClientRect().top < hoogte) return;
    // Elementen naast elkaar in dezelfde rij krijgen een kleine trapsgewijze vertraging.
    teller = el.parentElement === vorige ? teller + 1 : 0;
    vorige = el.parentElement;
    el.style.setProperty('--vertraging', Math.min(teller, 4) * 0.08 + 's');
    el.classList.add('onthul');
    io.observe(el);
  });
})();

// "Terug"-knop op een case: ga terug naar de vorige pagina als die op deze site lag, anders naar het overzicht
(function () {
  document.addEventListener('click', function (e) {
    var a = e.target.closest('[data-terug]');
    if (!a || e.metaKey || e.ctrlKey || e.shiftKey) return;
    try {
      if (document.referrer && new URL(document.referrer).origin === location.origin && history.length > 1) {
        e.preventDefault();
        history.back();
      }
    } catch (err) {}
  });
})();
