// Offerte tekenen: vult de offertegegevens uit de link in, laat de klant tekenen en verstuurt naar Netlify Forms.
(function () {
  var f = document.getElementById('teken-formulier');
  if (!f) return;
  var T = JSON.parse(document.getElementById('teken-tekst').textContent);
  var q = new URLSearchParams(location.search);
  function param(n, max) { return (q.get(n) || '').trim().slice(0, max); }

  // Bedrag uit de link (4250, 4250.5 of 4.250,00) tonen in de notatie van de taal
  function bedragTekst(ruw) {
    var s = ruw.replace(/[€\s]/g, '');
    if (s.indexOf(',') > -1) s = s.replace(/\./g, '').replace(',', '.');
    var n = Number(s);
    if (!s || !isFinite(n)) return ruw;
    return new Intl.NumberFormat(T.locale, { style: 'currency', currency: 'EUR' }).format(n);
  }

  // Datum uit de link (2026-11-09) voluit in de taal van de pagina; andere tekst blijft zoals ze is
  function datumTekst(ruw) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(ruw)) return ruw;
    var d = new Date(ruw + 'T12:00:00');
    if (isNaN(d)) return ruw;
    return new Intl.DateTimeFormat(T.locale, { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' }).format(d);
  }

  var nr = param('nr', 40), klant = param('klant', 120), event = param('event', 160);
  var bedrag = param('bedrag', 40) ? bedragTekst(param('bedrag', 40)) : '';
  var personen = param('personen', 20);
  var details = {
    datum: datumTekst(param('datum', 40)),
    uur: param('uur', 40),
    locatie: param('locatie', 200),
    personen: /^\d+$/.test(personen) ? T.personen_tekst.replace('{n}', personen) : personen,
    formule: param('formule', 120)
  };
  var pdf = param('pdf', 600);
  if (!/^https:\/\//i.test(pdf)) pdf = '';

  // Alleen een link met klant en bedrag toont het formulier: nooit een blanco offerte laten tekenen
  if (!klant || !bedrag) {
    f.hidden = true;
    document.getElementById('teken-leeg').hidden = false;
    return;
  }
  f.elements.offertenummer.value = nr;
  f.elements.klant.value = klant;
  f.elements.bedrag.value = bedrag;
  f.elements.event.value = event;
  Object.keys(details).forEach(function (k) { f.elements[k].value = details[k]; });
  f.elements.pdf.value = pdf;
  f.elements.pagina.value = location.href;

  // Overzicht bovenaan: offerte en, als de link ze bevat, de gegevens van het event
  var lijst = document.getElementById('teken-overzicht');
  var waarden = { offerte: nr, klant: klant, bedrag: bedrag };
  Object.keys(details).forEach(function (k) { waarden[k] = details[k]; });
  Object.keys(waarden).forEach(function (k) {
    lijst.querySelector('[data-rij="' + k + '"]').hidden = !waarden[k];
    lijst.querySelector('[data-veld="' + k + '"]').textContent = waarden[k];
  });
  var heeftDetails = Object.keys(details).some(function (k) { return details[k]; });
  document.getElementById('teken-event').hidden = !event && !heeftDetails;
  document.getElementById('teken-event-label').hidden = !event;
  document.getElementById('teken-event-kop').textContent = event || T.ev_kop;
  lijst.querySelector('[data-rij="pdf"]').hidden = !pdf;
  if (pdf) lijst.querySelector('[data-veld="pdf"]').href = pdf;
  lijst.hidden = false;

  // Taalkeuze behoudt de offertegegevens
  document.querySelectorAll('.talen a').forEach(function (a) { a.href = a.getAttribute('href') + location.search; });

  // Handtekening met vinger of muis
  var c = document.getElementById('teken-canvas');
  var ctx = c.getContext('2d');
  var getekend = false, bezig = false, breedte = 0;
  function maat() {
    var r = c.getBoundingClientRect();
    if (Math.round(r.width) === breedte) return;
    breedte = Math.round(r.width);
    var d = window.devicePixelRatio || 1;
    c.width = r.width * d;
    c.height = r.height * d;
    ctx.setTransform(d, 0, 0, d, 0, 0);
    ctx.lineWidth = 2.4;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.strokeStyle = '#19194f';
    getekend = false;
  }
  function punt(e) { var r = c.getBoundingClientRect(); return { x: e.clientX - r.left, y: e.clientY - r.top }; }
  c.addEventListener('pointerdown', function (e) {
    e.preventDefault();
    c.setPointerCapture(e.pointerId);
    bezig = true;
    var p = punt(e);
    ctx.beginPath();
    ctx.moveTo(p.x, p.y);
    ctx.lineTo(p.x + 0.1, p.y + 0.1);
    ctx.stroke();
    getekend = true;
  });
  c.addEventListener('pointermove', function (e) {
    if (!bezig) return;
    var p = punt(e);
    ctx.lineTo(p.x, p.y);
    ctx.stroke();
  });
  ['pointerup', 'pointercancel'].forEach(function (n) { c.addEventListener(n, function () { bezig = false; }); });
  document.getElementById('teken-wis').addEventListener('click', function () { breedte = 0; maat(); });
  window.addEventListener('resize', maat);
  maat();

  // Kleine png (600 px breed) zodat de inzending licht blijft
  function handtekening() {
    if (!getekend) return '';
    var k = document.createElement('canvas');
    k.width = 600;
    k.height = Math.round(600 * c.height / c.width);
    k.getContext('2d').drawImage(c, 0, 0, k.width, k.height);
    return k.toDataURL('image/png');
  }

  var knop = f.querySelector('button[type="submit"]');
  var fout = document.getElementById('teken-fout');
  f.addEventListener('submit', function (e) {
    e.preventDefault();
    fout.hidden = true;
    knop.disabled = true;
    knop.textContent = T.bezig;
    f.elements.handtekening.value = handtekening();
    fetch('/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: new URLSearchParams(new FormData(f)).toString()
    }).then(function (r) {
      if (!r.ok) throw new Error(r.status);
      var tijd = new Intl.DateTimeFormat(T.locale, { dateStyle: 'long', timeStyle: 'short', timeZone: 'Europe/Brussels' }).format(new Date());
      document.getElementById('teken-klaar-tekst').textContent = T.klaar_p
        .replace('{nr}', f.elements.offertenummer.value).replace('{tijd}', tijd).replace('{email}', f.elements.email.value);
      f.hidden = true;
      var klaar = document.getElementById('teken-klaar');
      klaar.hidden = false;
      klaar.querySelector('h2').focus();
    }).catch(function () {
      fout.hidden = false;
      knop.disabled = false;
      knop.textContent = T.knop;
    });
  });
})();

// Interne hulppagina /offerte-link: bouwt de tekenlink voor een offerte
(function () {
  var f = document.getElementById('link-maker');
  if (!f) return;
  var paden = JSON.parse(f.getAttribute('data-paden'));
  var uit = document.getElementById('lm_uit'), open = document.getElementById('lm_open'), kopieer = document.getElementById('lm_kopieer');
  function bouw() {
    var q = new URLSearchParams();
    [['klant', 'lm_klant'], ['bedrag', 'lm_bedrag'], ['event', 'lm_event'], ['datum', 'lm_datum'], ['uur', 'lm_uur'],
     ['locatie', 'lm_locatie'], ['personen', 'lm_personen'], ['formule', 'lm_formule'], ['pdf', 'lm_pdf']].forEach(function (p) {
      var v = document.getElementById(p[1]).value.trim();
      if (v) q.set(p[0], v);
    });
    // Pas een link als alle verplichte velden ingevuld zijn, zodat de klant genoeg context ziet om te tekenen
    var klaar = Array.prototype.every.call(f.querySelectorAll('[required]'), function (el) { return el.value.trim(); });
    var link = 'https://www.opperdash.be' + paden[document.getElementById('lm_taal').value] + '?' + q;
    uit.value = klaar ? link : '';
    open.href = klaar ? location.origin + link.replace('https://www.opperdash.be', '') : '#';
    open.setAttribute('aria-disabled', String(!klaar));
    kopieer.disabled = !klaar;
    kopieer.textContent = 'Kopieer link';
  }
  open.addEventListener('click', function (e) { if (open.getAttribute('aria-disabled') === 'true') e.preventDefault(); });
  f.addEventListener('input', bouw);
  f.addEventListener('change', bouw);
  kopieer.addEventListener('click', function () {
    uit.select();
    try { navigator.clipboard.writeText(uit.value); } catch (e) { document.execCommand('copy'); }
    this.textContent = 'Gekopieerd';
  });
  bouw();
})();
