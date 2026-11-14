# Opperdash-website: bron van alle pagina's in NL, EN en FR.
# Pas teksten hier aan en voer daarna uit:  python -I bouw.py
# Het script schrijft de HTML-pagina's en de sitemap naar public/. Netlify publiceert public/.
# Stijl: public/assets/css/style.css. Redirects: public/_redirects.
import os, json, sys, shutil, base64
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")
# Conceptpreview: python -I bouw.py --concept bouwt ook niet-gepubliceerde cases, maar in een aparte map
# (.tmp/website-concept), zodat er nooit een concept in public/ belandt.
CONCEPT = "--concept" in sys.argv
if CONCEPT:
    BRON = OUT
    OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".tmp", "website-concept")
    shutil.rmtree(OUT, ignore_errors=True)
    shutil.copytree(BRON, OUT, ignore=shutil.ignore_patterns("*.html", "sitemap.xml"))
SITE = "https://www.opperdash.be"
DATUM = "2026-10-20"
TALEN = ["nl", "en", "fr"]

# Paginasleutel -> pad per taal ("" = startpagina van die taal)
PAD = {
    "home":      {"nl": "",                            "en": "en/",                 "fr": "fr/"},
    "catering":  {"nl": "catering",                    "en": "en/catering",         "fr": "fr/traiteur"},
    "foodtruck": {"nl": "foodtruck",                   "en": "en/food-truck",       "fr": "fr/food-truck"},
    "aanpak":    {"nl": "onze-aanpak",                 "en": "en/how-we-work",      "fr": "fr/notre-approche"},
    "verhaal":   {"nl": "ons-verhaal",                 "en": "en/our-story",        "fr": "fr/notre-histoire"},
    "contact":   {"nl": "contact",                     "en": "en/contact",          "fr": "fr/contact"},
    "off_cat":   {"nl": "offerte-aanvragen-catering",  "en": "en/quote-catering",   "fr": "fr/devis-traiteur"},
    "off_truck": {"nl": "offerte-aanvragen-foodtruck", "en": "en/quote-food-truck", "fr": "fr/devis-food-truck"},
    "bedankt":   {"nl": "bedankt",                     "en": "en/thank-you",        "fr": "fr/merci"},
    "404":       {"nl": "404",                         "en": "en/404",              "fr": "fr/404"},
    "cases":     {"nl": "cases/",                      "en": "en/cases/",           "fr": "fr/references/"},
    "faq":       {"nl": "veelgestelde-vragen",         "en": "en/faq",              "fr": "fr/questions-frequentes"},
    "tekenen":   {"nl": "offerte-tekenen",             "en": "en/sign-quote",       "fr": "fr/signer-devis"},
    "offerte_link": {"nl": "offerte-link",             "en": "offerte-link",        "fr": "offerte-link"},  # interne hulppagina, alleen NL
}
HTML_LANG = {"nl": "nl-BE", "en": "en", "fr": "fr-BE"}
OG_LOCALE = {"nl": "nl_BE", "en": "en_GB", "fr": "fr_BE"}


def url(page, L):
    return "/" + PAD[page][L]


def bestand(page, L):
    p = PAD[page][L]
    if p == "":
        return "index.html"
    if p.endswith("/"):
        return p + "index.html"
    return p + ".html"


C = {  # gedeelde teksten
 "nl": {"slot": "Plan je event met Opperdash", "skip": "Naar de inhoud", "menu_open": "Menu openen", "menu_dicht": "Menu sluiten", "hoofdmenu": "Hoofdmenu", "mobiel": "Mobiel menu",
        "logo": "Opperdash, naar de startpagina", "door": "door", "taal": "Taal kiezen",
        "nav": [("verhaal", "Mijn verhaal"), ("foodtruck", "Foodtruck"), ("catering", "Catering"), ("aanpak", "Mijn aanpak")],
        "band": "• Whole foods • Verse kruiden • Levendig",
        "f_tag": "Culinaire catering en foodtruck voor bedrijven en events, vanuit Leuven.", "f_aanbod": "Aanbod", "f_links": [("catering", "Bedrijfscatering &amp; buffet"), ("foodtruck", "Foodtruck huren"), ("cases", "Cases"), ("faq", "Veelgestelde vragen")], "f_volg": "Volg Opperdash", "f_contact": "Contact",
        "f_off": "Offerte catering", "knop_off": "Gratis offerte", "f_truck": "Foodtruck aanvragen", "op": "Opperdash op",
        "home": "Home", "boek_cat": "Boek de catering", "boek_truck": "Boek de foodtruck", "verstuur": "Verstuur", "niet_invullen": "Niet invullen:",
        "ck_tekst": "Ik gebruik analytische cookies (Google Analytics) om te zien hoe bezoekers deze site gebruiken. Zo kan ik ze verbeteren. Ga je akkoord?",
        "ck_ja": "Akkoord", "ck_nee": "Liever niet", "ck_label": "Cookievoorkeuren", "ck_link": "Cookie-instellingen",
        "tb_cases": "Cases", "tb_faq": "Meest gestelde vragen", "tb_label": "Extra menu"},
 "en": {"slot": "Plan your event with Opperdash", "skip": "Skip to content", "menu_open": "Open menu", "menu_dicht": "Close menu", "hoofdmenu": "Main menu", "mobiel": "Mobile menu",
        "logo": "Opperdash, go to the home page", "door": "by", "taal": "Choose language",
        "nav": [("verhaal", "My story"), ("foodtruck", "Food truck"), ("catering", "Catering"), ("aanpak", "How I work")],
        "band": "• Whole foods • Fresh herbs • Vibrant",
        "f_tag": "Culinary catering and food truck for companies and events, from Leuven.", "f_aanbod": "What I offer", "f_links": [("catering", "Corporate catering &amp; buffets"), ("foodtruck", "Food truck hire"), ("cases", "Cases"), ("faq", "FAQ")], "f_volg": "Follow Opperdash", "f_contact": "Contact",
        "f_off": "Catering quote", "knop_off": "Free quote", "f_truck": "Book the food truck", "op": "Opperdash on",
        "home": "Home", "boek_cat": "Book the catering", "boek_truck": "Book the food truck", "verstuur": "Send", "niet_invullen": "Do not fill in:",
        "ck_tekst": "I use analytics cookies (Google Analytics) to see how visitors use this site, so I can improve it. Do you agree?",
        "ck_ja": "Accept", "ck_nee": "No thanks", "ck_label": "Cookie preferences", "ck_link": "Cookie settings",
        "tb_cases": "Cases", "tb_faq": "Frequently asked questions", "tb_label": "Extra menu"},
 "fr": {"slot": "Organisez votre événement avec Opperdash", "skip": "Aller au contenu", "menu_open": "Ouvrir le menu", "menu_dicht": "Fermer le menu", "hoofdmenu": "Menu principal", "mobiel": "Menu mobile",
        "logo": "Opperdash, retour à l’accueil", "door": "par", "taal": "Choisir la langue",
        "nav": [("verhaal", "Mon histoire"), ("foodtruck", "Food truck"), ("catering", "Traiteur"), ("aanpak", "Mon approche")],
        "band": "• Produits bruts • Herbes fraîches • Plein de vie",
        "f_tag": "Traiteur culinaire et food truck pour entreprises et événements, depuis Louvain.", "f_aanbod": "L’offre", "f_links": [("catering", "Traiteur d’entreprise &amp; buffet"), ("foodtruck", "Location de food truck"), ("cases", "Références"), ("faq", "Questions fréquentes")], "f_volg": "Suivre Opperdash", "f_contact": "Contact",
        "f_off": "Devis traiteur", "knop_off": "Devis gratuit", "f_truck": "Réserver le food truck", "op": "Opperdash sur",
        "home": "Accueil", "boek_cat": "Réserver le traiteur", "boek_truck": "Réserver le food truck", "verstuur": "Envoyer", "niet_invullen": "Ne pas remplir :",
        "ck_tekst": "J’utilise des cookies analytiques (Google Analytics) pour comprendre comment les visiteurs utilisent ce site et l’améliorer. Êtes-vous d’accord ?",
        "ck_ja": "Accepter", "ck_nee": "Non merci", "ck_label": "Préférences cookies", "ck_link": "Paramètres des cookies",
        "tb_cases": "Références", "tb_faq": "Questions fréquentes", "tb_label": "Menu secondaire"},
}

SOCIAL = [("instagram", "https://instagram.com/opperdash", "Instagram"),
          ("tiktok", "https://tiktok.com/@opperdash.be", "TikTok"),
          ("facebook", "https://www.facebook.com/profile.php?id=61572850222575", "Facebook"),
          ("linkedin", "https://www.linkedin.com/in/elias-nys-a01702294/", "LinkedIn")]

ORG_ID = SITE + "/#organisatie"
ORG_DESC = {
    "nl": "Voedzame culinaire gerechten met mediterrane invloeden. Catering, buffet en foodtruck voor bedrijven en events.",
    "en": "Nourishing culinary dishes with Mediterranean influences. Catering, buffets and a food truck for companies and events.",
    "fr": "Des plats culinaires et nourrissants aux influences méditerranéennes. Traiteur, buffet et food truck pour entreprises et événements.",
}


def org(L):
    return {"@type": "FoodEstablishment", "@id": ORG_ID, "name": "Opperdash", "url": SITE + "/",
            "logo": SITE + "/assets/img/og-opperdash.jpg", "image": SITE + "/assets/img/catering-sfeer.webp",
            "description": ORG_DESC[L], "email": "elias@opperdash.be", "telephone": "+32470326332",
            "address": {"@type": "PostalAddress", "addressLocality": "Leuven", "addressCountry": "BE"},
            "servesCuisine": ["Mediterranean"], "founder": {"@type": "Person", "name": "Elias Nys"},
            "knowsLanguage": ["nl", "en", "fr"], "sameAs": [u for _, u, _ in SOCIAL],
            "areaServed": [{"@type": "City", "name": "Leuven"}, {"@type": "City", "name": "Brussel"}, {"@type": "City", "name": "Mechelen"},
                           {"@type": "AdministrativeArea", "name": "Vlaams-Brabant"}, {"@type": "Country", "name": "België"}]}


def band(L):
    return '<div class="band" aria-hidden="true"><div class="band__spoor">' + "".join(
        f"<span>{C[L]['band']} </span>" for _ in range(6)) + "</div></div>"


def slotband(L):
    """Afsluitende balk boven de footer: titel links, offerte en contact rechts (zoals Sweetgreen)."""
    c = C[L]
    return f'''<section class="slotband">
  <div class="container slotband__binnen">
    <h2>{c["slot"]}</h2>
    <div class="knoppen"><a class="knop knop--groen" href="{url("off_cat", L)}">{c["knop_off"]}</a><a class="knop" href="{url("contact", L)}">Contact</a></div>
  </div>
</section>'''


def talen(page, L, klasse):
    links = "".join(
        f'<a href="{url(page, T)}" hreflang="{HTML_LANG[T]}" lang="{HTML_LANG[T]}"{" aria-current=\"true\"" if T == L else ""}>{T.upper()}</a>'
        for T in TALEN)
    return f'<nav class="{klasse}" aria-label="{C[L]["taal"]}">{links}</nav>'


def taalkeuze(page, L):
    """Compacte taalkeuze in de header: huidige taal, klik voor de andere twee."""
    andere = "".join(f'<a href="{url(page, T)}" hreflang="{HTML_LANG[T]}" lang="{HTML_LANG[T]}">{T.upper()}</a>' for T in TALEN if T != L)
    return f'<details class="taal"><summary aria-label="{C[L]["taal"]}: {L.upper()}">{L.upper()}</summary><nav class="taal__lijst" aria-label="{C[L]["taal"]}">{andere}</nav></details>'


def header(page, L):
    c = C[L]
    huidig = lambda p: ' aria-current="page"' if p == page else ""
    links = "".join(f'<a href="{url(p, L)}"{huidig(p)}>{lab}</a>' for p, lab in c["nav"])
    extra = f'<a href="{url("faq", L)}"{huidig("faq")}>{c["tb_faq"]}</a><a href="{url("contact", L)}"{huidig("contact")}>Contact</a>'
    return f'''<a class="skip" href="#inhoud">{c["skip"]}</a>
<header class="header">
  <div class="header__binnen">
    <nav class="nav" aria-label="{c["hoofdmenu"]}">{links}</nav>
    <a class="logo" href="{url("home", L)}" aria-label="{c["logo"]}"><img src="/assets/img/logo-zwart.svg" alt="Opperdash" width="195" height="40"></a>
    <div class="header__rechts">{taalkeuze(page, L)}<a class="knop knop--groen knop--klein" href="{url("off_cat", L)}"{huidig("off_cat")}>{c["knop_off"]}</a><span class="header__streep" aria-hidden="true"></span><a class="header__contact" href="{url("contact", L)}"{huidig("contact")}>Contact</a></div>
    <button class="menu-knop" aria-label="{c["menu_open"]}" data-open-label="{c["menu_open"]}" data-close-label="{c["menu_dicht"]}" aria-expanded="false" aria-controls="mobiel-menu">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path class="l1" d="M4 7h16"/><path class="l2" d="M4 12h16"/><path class="l3" d="M4 17h16"/></svg>
    </button>
  </div>
  <div class="mobiel-menu" id="mobiel-menu" data-open="false">
    <nav class="mobiel-menu__links" aria-label="{c["mobiel"]}">{links}</nav>
    <nav class="mobiel-menu__extra" aria-label="{c["tb_label"]}">{extra}</nav>
    <div class="mobiel-menu__onder">
      <a class="knop knop--accent" href="{url("off_cat", L)}">{c["knop_off"]}</a>
      {talen(page, L, "talen talen--mobiel")}
    </div>
  </div>
</header>'''


def footer(L):
    c = C[L]
    soc = "<br>".join(f'<a href="{u}" target="_blank" rel="noopener">{n}</a>' for _, u, n in SOCIAL)
    return f'''<footer class="footer">
  <div class="container">
    <div class="footer__raster">
      <p class="footer__tag">{c["f_tag"]}</p>
      <div>
        <h2>{c["f_aanbod"]}</h2>
        <p>{"<br>".join(f'<a href="{url(p, L)}">{lab}</a>' for p, lab in c["f_links"])}</p>
      </div>
      <div>
        <h2>{c["f_volg"]}</h2>
        <p>{soc}</p>
      </div>
      <div>
        <h2>{c["f_contact"]}</h2>
        <p><a href="mailto:elias@opperdash.be">elias@opperdash.be</a><br><a href="tel:+32470326332">+32 470 32 63 32</a><br><a href="{url("off_cat", L)}">{c["f_off"]}</a><br><a href="{url("off_truck", L)}">{c["f_truck"]}</a></p>
      </div>
    </div>
    <a class="footer__woordmerk" href="{url("home", L)}" aria-label="{c["logo"]}"><img src="/assets/img/logo-linnen.svg" alt="Opperdash" width="753" height="154" loading="lazy"></a>
    <div class="footer__onder">
      <span>© Opperdash 2026</span>
      <span>Design &amp; Build by <a href="https://www.wolfverelst.com/" target="_blank" rel="noopener">Wolf Ver Elst</a></span>
      <a class="footer__cookies" href="#" data-cookies="open">{c["ck_link"]}</a>
    </div>
  </div>
</footer>
<div class="cookiebanner" id="cookiebanner" role="dialog" aria-label="{c["ck_label"]}" hidden>
  <p>{c["ck_tekst"]}</p>
  <div class="cookiebanner__knoppen">
    <button type="button" class="knop knop--vol knop--klein" data-cookies="ja">{c["ck_ja"]}</button>
    <button type="button" class="knop knop--klein" data-cookies="nee">{c["ck_nee"]}</button>
  </div>
</div>
<script src="/assets/js/site.js?v={versie("assets/js/site.js")}" defer></script>'''


def breadcrumbs(page, L, naam):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": C[L]["home"], "item": SITE + url("home", L)},
        {"@type": "ListItem", "position": 2, "name": naam, "item": SITE + url(page, L)}]}


# Een antwoord is een tekst, of een lijst van alinea's (tekst) en opsommingen (lijst van (label, tekst)).
def faq_delen(a):
    return [a] if isinstance(a, str) else a


def faq_tekst(a):
    return " ".join(d if isinstance(d, str) else " ".join(f"{l} {t}" for l, t in d) for d in faq_delen(a))


def faq_antwoord(a):
    return "".join(f"<p>{d}</p>" if isinstance(d, str) else
                   "<ul>" + "".join(f"<li><strong>{l}</strong> {t}</li>" for l, t in d) + "</ul>" for d in faq_delen(a))


def faq_schema(vragen):
    return {"@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": v, "acceptedAnswer": {"@type": "Answer", "text": faq_tekst(a)}} for v, a in vragen]}


def faq_html(vragen):
    return '<div class="faq">' + "".join(f'<details><summary>{v}</summary><div class="faq__antwoord">{faq_antwoord(a)}</div></details>' for v, a in vragen) + "</div>"


IMG_DIR = os.path.join(OUT, "assets", "img")


def versie(pad):
    """Korte hash van een bestand, zodat browsers na een wijziging meteen de nieuwe versie laden."""
    import hashlib
    with open(os.path.join(OUT, pad), "rb") as f:
        return hashlib.md5(f.read()).hexdigest()[:8]


def srcset(naam, w):
    """Geeft srcset-tekst terug als er een lichtere gsm-versie (-m.webp, 960 px) bestaat."""
    m = naam.replace(".webp", "-m.webp")
    if os.path.exists(os.path.join(IMG_DIR, m)):
        return f"/assets/img/{m} 960w, /assets/img/{naam} {w}w"
    return ""


def img(naam, alt, w, h, lazy=True, sizes="100vw"):
    extra = ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high"'
    ss = srcset(naam, w)
    ss = f' srcset="{ss}" sizes="{sizes}"' if ss else ""
    return f'<img src="/assets/img/{naam}"{ss} alt="{alt}" width="{w}" height="{h}"{extra}>'


def met_punt(html):
    """Zet een punt achter elke grote titel (h1, h2) die nog niet op . ? ! of : eindigt (Elias, 12/11/2026)."""
    import re as _re
    def zet(m):
        attrs, binnen = m.group(2), m.group(3)
        if any(k in attrs for k in ("visueel-verborgen", "case-kaart__titel", "teken__eventnaam")):
            return m.group(0)
        tekst = _re.sub(r"<[^>]+>", "", binnen).strip()
        if not tekst or "{" in tekst or tekst[-1] in ".?!:…":
            return m.group(0)
        return f"<h{m.group(1)}{attrs}>{binnen.rstrip()}.</h{m.group(1)}>"
    return _re.sub(r"<h([12])([^>]*)>(.*?)</h\1>", zet, html, flags=_re.S)


def pagina(page, L, titel, beschrijving, inhoud, index=True, schema=None, ogbeeld="og-opperdash.jpg", hero=None, ogalt="Opperdash: culinaire catering en foodtruck"):
    canon = SITE + url(page, L)
    robots = '<meta name="robots" content="index, follow, max-image-preview:large">' if index else '<meta name="robots" content="noindex">'
    alt_links = ""
    if index:
        alt_links = "".join(f'\n<link rel="alternate" hreflang="{HTML_LANG[T]}" href="{SITE}{url(page, T)}">' for T in TALEN)
        alt_links += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{url(page, "nl")}">'
    og_alt = "".join(f'\n<meta property="og:locale:alternate" content="{OG_LOCALE[T]}">' for T in TALEN if T != L)
    preload = ""
    if hero:
        ss = srcset(hero, 1920)
        extra = f' imagesrcset="{ss}" imagesizes="100vw"' if ss else ""
        preload = f'\n<link rel="preload" as="image" href="/assets/img/{hero}"{extra} fetchpriority="high">'
        # Wazige mini-versie (-p.webp, 32 px) als achtergrond, zodat de hero niet donker staat terwijl de foto laadt.
        p = os.path.join(IMG_DIR, hero.replace(".webp", "-p.webp"))
        if os.path.exists(p):
            with open(p, "rb") as f:
                data = base64.b64encode(f.read()).decode()
            preload += f'\n<style>.hero{{background-image:url(data:image/webp;base64,{data});background-size:cover;background-position:center}}</style>'
    ld = ""
    if schema:
        ld = '\n<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": schema}, ensure_ascii=False) + "</script>"
    inhoud = met_punt(inhoud)
    html = f'''<!doctype html>
<html lang="{HTML_LANG[L]}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{titel}</title>
<meta name="description" content="{beschrijving}">
{robots}
<link rel="canonical" href="{canon}">{alt_links}
<meta property="og:type" content="website">
<meta property="og:locale" content="{OG_LOCALE[L]}">{og_alt}
<meta property="og:site_name" content="Opperdash">
<meta property="og:title" content="{titel}">
<meta property="og:description" content="{beschrijving}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{SITE}/assets/img/{ogbeeld}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{ogalt}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{titel}">
<meta name="twitter:description" content="{beschrijving}">
<meta name="twitter:image" content="{SITE}/assets/img/{ogbeeld}">
<meta name="twitter:image:alt" content="{ogalt}">
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/assets/img/icon-192.png" type="image/png" sizes="192x192">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="preload" href="/assets/fonts/teko-var.woff2" as="font" type="font/woff2" crossorigin>{preload}
<link rel="stylesheet" href="/assets/css/style.css?v={versie("assets/css/style.css")}">{ld}
</head>
<body>
{header(page, L)}
<main id="inhoud">
{inhoud.strip()}
</main>
{footer(L)}
</body>
</html>
'''
    pad = os.path.join(OUT, bestand(page, L))
    os.makedirs(os.path.dirname(pad), exist_ok=True)
    with open(pad, "w", encoding="utf-8", newline="\n") as f:
        f.write(html)


# ============================================================ HOME
HOME = {
 "nl": dict(titel="Bedrijfscatering en foodtruck vanuit Leuven | Opperdash",
    desc="Culinaire catering, buffet en foodtruck voor personeelsfeesten, teamevents en bedrijfslunches. Voedzame gerechten met mediterrane invloeden, vanuit Leuven.",
    h1="Opperdash: culinaire bedrijfscatering, buffet en foodtruck voor events, vanuit Leuven",
    alt_hero="Chef Elias Nys en een collega dresseren borden in de keuken van de Opperdash-foodtruck",
    alt_tuin="Chef Elias Nys ruikt aan verse tijm in een zonnige tuin",
    k1="Culinair.<br>Gezond.<br>Mediterraan.", k_seizoen="Welkom bij Opperdash",
    p1=["Mijn naam is Elias. Ik ben chef en oprichter van Opperdash. Ik serveer culinaire, gezonde gerechten met mediterrane invloeden.",
        "Ik werk uitsluitend met whole foods en pure producten, op het ritme van het seizoen. Dat doe ik vanuit de foodtruck of in cateringvorm."],
    alt_visie="Elias Nys in Opperdash-schort met een bord van de catering", k2="Mijn visie",
    p2=["Opperdash groeit vanuit een passie voor gezondheid en een liefde voor smaak. Ik sta voor gerechten met intense smaken die ook gezond zijn voor het lichaam."],
    k3="Wat klanten zeggen", functie="CEO van", vertaald="",
    quote="We hebben Opperdash uitgenodigd voor een personeelsevenement bij 3E, en dat was een heel fijne ervaring. De gerechten waren gezond, smaakvol en met zorg gebracht. Je merkt dat Elias veel aandacht heeft voor kwaliteit, service en de juiste energie op zo’n moment. Ik zou Opperdash zeker aanraden aan andere bedrijven.",
    k4="Catering voor bedrijven",
    p4="Een bedrijfslunch, teamevent of personeelsfeest: ik kom met de foodtruck, zet een buffet of verzorg catering in de vorm die bij je event past. De basis blijft dezelfde: smaakvolle gerechten die ook gezond zijn voor het lichaam.",
    alt_bedr="Culinair gerecht met mediterrane invloeden op een keramisch bord", b_truck="Foodtruck", b_cat="Catering",
    alt_k_truck="De foodtruck van Opperdash serveert gasten op een bedrijfsevent", k_truck="Vanuit de foodtruck kook en serveer ik ter plaatse, van een bedrijfslunch tot een groot event met tot 250 gasten. Altijd op keramiek met echt bestek.",
    alt_k_cat="Bruschetta met tomaat en verse basilicum op keramiek, van het buffet van Opperdash", k_cat="Een culinair buffet, catering aan tafel of een walking dinner. Altijd op keramiek en met echt bestek."),
 "en": dict(titel="Corporate catering and food truck from Leuven | Opperdash",
    desc="Culinary catering, buffets and a food truck for staff parties, team events and company lunches. Nourishing dishes with Mediterranean influences, from Leuven.",
    h1="Opperdash: culinary corporate catering, buffets and food truck for events, from Leuven, Belgium",
    alt_hero="Chef Elias Nys and a colleague plating dishes in the Opperdash food truck kitchen",
    alt_tuin="Chef Elias Nys smelling fresh thyme in a sunny garden",
    k1="Culinary.<br>Healthy.<br>Mediterranean.", k_seizoen="Welcome to Opperdash",
    p1=["My name is Elias. I am the chef and founder of Opperdash. I serve culinary, healthy dishes with Mediterranean influences.",
        "I work exclusively with whole foods and pure produce, in step with the seasons. I do this from the food truck or as catering."],
    alt_visie="Elias Nys in an Opperdash apron holding a plate from the catering", k2="My vision",
    p2=["Opperdash grows out of a passion for health and a love of flavour. I stand for dishes with intense flavours that are also healthy for the body."],
    k3="What clients say", functie="CEO of", vertaald="Translated from Dutch",
    quote="We invited Opperdash for a staff event at 3E, and it was a really pleasant experience. The dishes were healthy, full of flavour and served with care. You can tell Elias pays close attention to quality, service and the right energy for the occasion. I would certainly recommend Opperdash to other companies.",
    k4="Catering for companies",
    p4="A company lunch, team event or staff party: I bring the food truck, set up a buffet or cater in the format that suits your event. The base stays the same: flavourful dishes that are also healthy for the body.",
    alt_bedr="Culinary dish with Mediterranean influences on a ceramic plate", b_truck="Food truck", b_cat="Catering",
    alt_k_truck="The Opperdash food truck serving guests at a company event", k_truck="From the food truck I cook and serve on site, from a company lunch to a large event of up to 250 guests. Always on ceramic with real cutlery.",
    alt_k_cat="Bruschetta with tomato and fresh basil on ceramic, from the Opperdash buffet", k_cat="A culinary buffet, seated catering or a walking dinner. Always on ceramic and with real cutlery."),
 "fr": dict(titel="Traiteur d’entreprise et food truck depuis Louvain | Opperdash",
    desc="Traiteur culinaire, buffet et food truck pour fêtes du personnel, événements d’équipe et lunchs d’entreprise. Des plats nourrissants aux influences méditerranéennes.",
    h1="Opperdash : traiteur d’entreprise culinaire, buffet et food truck pour vos événements, depuis Louvain",
    alt_hero="Le chef Elias Nys et un collègue dressent des assiettes dans la cuisine du food truck Opperdash",
    alt_tuin="Le chef Elias Nys sent du thym frais dans un jardin ensoleillé",
    k1="Culinaire.<br>Sain.<br>Méditerranéen.", k_seizoen="Bienvenue chez Opperdash",
    p1=["Je m’appelle Elias. Je suis chef et fondateur d’Opperdash. Je sers des plats culinaires et sains aux influences méditerranéennes.",
        "Je travaille uniquement des aliments bruts et des produits purs, au rythme des saisons. Je le fais depuis le food truck ou en formule traiteur."],
    alt_visie="Elias Nys en tablier Opperdash tenant une assiette du service traiteur", k2="Ma vision",
    p2=["Opperdash naît d’une passion pour la santé et d’un amour du goût. Je défends des plats aux saveurs intenses, qui sont aussi sains pour le corps."],
    k3="Ce que disent mes clients", functie="CEO de", vertaald="Traduit du néerlandais",
    quote="Nous avons invité Opperdash pour un événement du personnel chez 3E, et ce fut une très belle expérience. Les plats étaient sains, savoureux et servis avec soin. On sent qu’Elias accorde beaucoup d’attention à la qualité, au service et à la bonne énergie du moment. Je recommande vivement Opperdash à d’autres entreprises.",
    k4="Traiteur pour entreprises",
    p4="Un lunch d’entreprise, un événement d’équipe ou une fête du personnel : je viens avec le food truck, j’installe un buffet ou j’assure le traiteur dans la formule qui convient à votre événement. La base reste la même : des plats savoureux qui sont aussi sains pour le corps.",
    alt_bedr="Plat culinaire aux influences méditerranéennes sur une assiette en céramique", b_truck="Food truck", b_cat="Traiteur",
    alt_k_truck="Le food truck Opperdash sert des invités lors d’un événement d’entreprise", k_truck="Depuis le food truck, je cuisine et je sers sur place, d’un lunch d’entreprise à un grand événement jusqu’à 250 invités. Toujours en céramique avec de vrais couverts.",
    alt_k_cat="Bruschetta à la tomate et au basilic frais sur céramique, du buffet Opperdash", k_cat="Un buffet culinaire, un service à table ou un walking dinner. Toujours en céramique et avec de vrais couverts."),
}
# ============================================================ CATERING
CAT = {
 "nl": dict(titel="Catering voor bedrijven: buffet en walking dinner | Opperdash",
    desc="Bedrijfscatering voor je personeelsfeest, teamevent of receptie: een culinair buffet, walking dinner of catering aan tafel. Huisbereid en op keramiek geserveerd.",
    crumb="Catering", alt_hero="Bruschetta met tomaat en verse basilicum op keramiek, van het buffet van Opperdash",
    h1="Catering &amp;<br>buffet", lead="Een royaal buffet met voedzame culinaire gerechten met mediterrane invloeden. Huisbereid en klaar om te serveren.",
    alt_buf="Perziken worden gegrild op een grillpan voor de catering van Opperdash", k1="Culinair buffet",
    p1=["Elk seizoen stel ik een buffet samen met mediterrane invloeden. Het seizoen bepaalt wat er op tafel komt: ik kook met groenten die op dat moment op hun best zijn.",
        "Ik maak alles zelf en serveer het buffet warm of koud. Ik dek de tafel volledig, met tafellaken en versiering, en presenteer de gerechten in moderne schalen. Je gasten eten van keramiek met echt bestek.",
        "Ik kom ter plaatse en zorg voor de opbouw en de opruim."],
    k2="Drie manieren om te cateren",
    blokken=[("Buffet", "Een licht of uitgebreid buffet, aan te vullen met hapjes en desserts. Je hebt enkel tafels nodig en één stopcontact."),
             ("Aan tafel", "Ik kook in de keuken op je locatie en serveer aan tafel. Van een sterk hoofdgerecht tot een volledig menu met hapjes, voorgerecht en dessert."),
             ("Walking dinner", "Kleine koude en warme gerechten die na elkaar uit de keuken komen. Je gasten eten staand. Kies vijf of zeven gerechten.")],
    alt_beeld="Gesneden rundvlees met geroosterde paprika en kruiden op een keramisch bord",
    kaart_alt=["Een culinair gerecht met mediterrane invloeden in een keramische schaal", "Bruschetta op een bord aan tafel, tussen glazen en gasten", "Twee gerechten van Opperdash worden aan gasten gegeven"],
    alt_cap="Gerechten van Opperdash klaar om te serveren op een bedrijfsevent", k3="Capaciteit",
    p3=["Ik stem mijn team af op het aantal gasten en de gewenste timing. Zo wordt iedereen op tijd bediend.",
        "Het definitieve aantal gasten en eventuele allergieën geef je mij uiterlijk vijf werkdagen voor het event door."],
    k4="Veelgestelde vragen over catering",
    faq=[("Wat brengt Opperdash mee?", "Keramisch servies, echt bestek en de presentatie van het buffet in mooie serveerschalen. Ik bouw op en ruim achteraf alles op. Tafels en stoelen kan ik in de offerte opnemen."),
         ("Wat heb je nodig voor een buffet?", "Tafels om het buffet op te presenteren en één normaal stopcontact."),
         ("Kan je in de keuken op onze locatie koken?", "Ja. Voor catering aan tafel en een walking dinner kook ik ter plaatse. Daarvoor is een volledig uitgeruste keuken nodig met oven, kookvuur, voldoende koelruimte en werkruimte. Zaalpersoneel kan ik op aanvraag toevoegen."),
         ("Hou je rekening met allergieën?", "Ja. Geef allergieën en het definitieve aantal gasten uiterlijk vijf werkdagen voor het event door. Dan hou ik er in de bereiding rekening mee."),
         ("Volgt het menu het seizoen?", "Ja. Mijn menu verandert met het seizoen. Producten kies ik op smaak, herkomst en seizoen."),
         ("Kan je ook dranken voorzien?", "Ja. Ik kan huisgemaakte limonade, mocktails en plat of bruisend water voorzien.")],
    svc="Catering en buffet", svc_desc="Culinair buffet, catering aan tafel en walking dinner met mediterrane invloeden voor bedrijven en events."),
 "en": dict(titel="Corporate catering: buffets and walking dinners | Opperdash",
    desc="Corporate catering for your staff party, team event or reception: a culinary buffet, walking dinner or seated catering. Homemade and served on ceramic.",
    crumb="Catering", alt_hero="Bruschetta with tomato and fresh basil on ceramic, from the Opperdash buffet",
    h1="Catering &amp;<br>buffets", lead="A generous buffet of nourishing culinary dishes with Mediterranean influences. Homemade and ready to serve.",
    alt_buf="Peaches being grilled on a griddle pan for Opperdash catering", k1="Culinary buffet",
    p1=["Every season I put together a buffet with Mediterranean influences. The season decides what goes on the table: I cook with vegetables that are at their best at that moment.",
        "I make everything myself and serve the buffet warm or cold. I dress the table completely, with a tablecloth and decoration, and present the dishes in modern serving dishes. Your guests eat from ceramic plates with real cutlery.",
        "I come to your venue and take care of the setup and the clearing."],
    k2="Three ways to cater",
    blokken=[("Buffet", "A light or extended buffet, with optional appetisers and desserts. All you need is tables and one power socket."),
             ("Seated", "I cook in the kitchen at your venue and serve at the table. From one strong main course to a full menu with appetisers, starter and dessert."),
             ("Walking dinner", "Small cold and warm dishes that come out of the kitchen one after another. Your guests eat standing up. Choose five or seven dishes.")],
    alt_beeld="Sliced beef with roasted peppers and herbs on a ceramic plate",
    kaart_alt=["A culinary dish with Mediterranean influences in a ceramic bowl", "Bruschetta on a plate at the table, between glasses and guests", "Two Opperdash dishes being handed to guests"],
    alt_cap="Opperdash dishes ready to be served at a company event", k3="Capacity",
    p3=["I match my team to the number of guests and the timing you want, so everyone is served on time.",
        "Please confirm the final number of guests and any allergies at least five working days before the event."],
    k4="Catering FAQ",
    faq=[("What does Opperdash bring?", "Ceramic tableware, real cutlery and the buffet presentation in beautiful serving dishes. I set up and clear everything away afterwards. Tables and chairs can be included in the quote."),
         ("What do you need for a buffet?", "Tables to present the buffet on and one standard power socket."),
         ("Can you cook in the kitchen at our venue?", "Yes. For seated catering and walking dinners I cook on site. This requires a fully equipped kitchen with an oven, hob, enough cold storage and work space. Serving staff can be added on request."),
         ("Do you take allergies into account?", "Yes. Let me know about allergies and the final number of guests at least five working days before the event, and I will take them into account."),
         ("Does the menu follow the seasons?", "Yes. My menu changes with the season. I choose produce for taste, origin and season."),
         ("Can you provide drinks?", "Yes. I can provide homemade lemonade, mocktails and still or sparkling water.")],
    svc="Catering and buffets", svc_desc="Culinary buffets, seated catering and walking dinners with Mediterranean influences for companies and events."),
 "fr": dict(titel="Traiteur pour entreprises : buffet et walking dinner | Opperdash",
    desc="Traiteur pour votre fête du personnel, événement d’équipe ou réception : buffet culinaire, walking dinner ou service à table. Fait maison, servi en céramique.",
    crumb="Traiteur", alt_hero="Bruschetta à la tomate et au basilic frais sur céramique, du buffet Opperdash",
    h1="Traiteur &amp;<br>buffet", lead="Un buffet généreux de plats culinaires et nourrissants aux influences méditerranéennes. Fait maison et prêt à servir.",
    alt_buf="Des pêches grillées sur une poêle-gril pour le traiteur Opperdash", k1="Un buffet culinaire",
    p1=["À chaque saison, je compose un buffet aux influences méditerranéennes. La saison décide de ce qui arrive sur la table : je cuisine les légumes qui sont alors à leur meilleur.",
        "Je prépare tout moi-même et je sers le buffet chaud ou froid. Je dresse entièrement la table, avec nappe et décoration, et je présente les mets dans des plats de service modernes. Vos invités mangent dans de la céramique avec de vrais couverts.",
        "Je viens sur place et m’occupe de l’installation et du rangement."],
    k2="Trois formules",
    blokken=[("Buffet", "Un buffet léger ou complet, à compléter avec des bouchées et des desserts. Il vous faut seulement des tables et une prise électrique."),
             ("À table", "Je cuisine dans la cuisine de votre lieu et sers à table. D’un plat principal fort à un menu complet avec bouchées, entrée et dessert."),
             ("Walking dinner", "De petits plats froids et chauds qui sortent de la cuisine l’un après l’autre. Vos invités mangent debout. Choisissez cinq ou sept plats.")],
    alt_beeld="Bœuf tranché, poivrons rôtis et herbes sur une assiette en céramique",
    kaart_alt=["Un plat culinaire aux influences méditerranéennes dans un bol en céramique", "Bruschetta sur une assiette à table, entre verres et convives", "Deux plats Opperdash remis à des invités"],
    alt_cap="Plats Opperdash prêts à être servis lors d’un événement d’entreprise", k3="Capacité",
    p3=["J’adapte mon équipe au nombre d’invités et à l’horaire souhaité, pour que chacun soit servi à temps.",
        "Communiquez-moi le nombre définitif d’invités et les éventuelles allergies au plus tard cinq jours ouvrables avant l’événement."],
    k4="Questions fréquentes",
    faq=[("Qu’apporte Opperdash ?", "La vaisselle en céramique, de vrais couverts et la présentation du buffet dans de beaux plats de service. J’installe tout et je range après. Tables et chaises peuvent être incluses dans le devis."),
         ("De quoi avez-vous besoin pour un buffet ?", "De tables pour présenter le buffet et d’une prise électrique standard."),
         ("Pouvez-vous cuisiner dans la cuisine de notre lieu ?", "Oui. Pour le service à table et le walking dinner, je cuisine sur place. Il faut une cuisine entièrement équipée avec four, feux de cuisson, assez d’espace frigorifique et de plan de travail. Du personnel de salle peut être ajouté sur demande."),
         ("Tenez-vous compte des allergies ?", "Oui. Communiquez-moi les allergies et le nombre définitif d’invités au plus tard cinq jours ouvrables avant l’événement, et j’en tiens compte en cuisine."),
         ("Le menu suit-il les saisons ?", "Oui. Mon menu change avec la saison. Je choisis mes produits pour leur goût, leur origine et leur saison."),
         ("Pouvez-vous fournir des boissons ?", "Oui. Je peux prévoir de la limonade maison, des mocktails et de l’eau plate ou pétillante.")],
    svc="Traiteur et buffet", svc_desc="Buffet culinaire, service à table et walking dinner aux influences méditerranéennes pour entreprises et événements."),
}
for L in TALEN:
    t = CAT[L]
    kaart_foto = [("aanpak-buffet-groot.webp", 1920, 1183), ("home-visie.webp", 962, 641), ("aanpak-cases.webp", 1440, 960)]
    blokken = "".join(f'<article class="fotokaart"><div class="fotokaart__beeld">{img(f, alt, w, h, sizes="(max-width: 800px) 100vw, 33vw")}</div>'
                      f'<div class="fotokaart__tekst"><h3>{a}</h3><p>{b}</p></div></article>'
                      for (a, b), (f, w, h), alt in zip(t["blokken"], kaart_foto, t["kaart_alt"]))
    pagina("catering", L, t["titel"], t["desc"], f'''
<section class="hero">
  {img("catering-sfeer.webp", t["alt_hero"], 1920, 1275, lazy=False)}
  <div class="container"><div class="hero__tekst">
    <h1>{t["h1"]}</h1>
    <p>{t["lead"]}</p>
  </div></div>
</section>

<section class="sectie sectie--linnen">
  <div class="container tekstblok">
      <h2>{t["k1"]}</h2>
      {"".join(f"<p>{p}</p>" for p in t["p1"])}
      <div class="knoppen"><a class="knop knop--salie knop--klein" href="{url("off_cat", L)}">{C[L]["boek_cat"]}</a></div>
  </div>
</section>


<section class="sectie">
  <div class="container">
    <h2 class="midden">{t["k2"]}</h2>
    <div class="fotokaarten">{blokken}</div>
  </div>
</section>

<section class="sectie sectie--split sectie--zand">
  <div class="duo">
    <div class="duo__tekst">
      <h2 class="zwaar">{t["k3"]}</h2>
      {"".join(f"<p>{p}</p>" for p in t["p3"])}
      <div class="knoppen"><a class="knop knop--vol knop--klein" href="{url("off_cat", L)}">{C[L]["boek_cat"]}</a></div>
    </div>
    <div class="duo__beeld">{img("verhaal-doel-groot.webp", t["alt_beeld"], 1920, 1280, sizes="(max-width: 800px) 100vw, 50vw")}</div>
  </div>
</section>

<section class="sectie">
  <div class="container">
    <h2 class="midden">{t["k4"]}</h2>
    {faq_html(t["faq"])}
  </div>
</section>
{slotband(L)}
''', hero="catering-sfeer.webp", ogbeeld="og-catering.jpg", ogalt=t["alt_hero"],
       schema=[breadcrumbs("catering", L, t["crumb"]), faq_schema(t["faq"]),
               {"@type": "Service", "name": t["svc"], "serviceType": "Catering", "provider": {"@id": ORG_ID},
                "areaServed": {"@type": "Country", "name": "Belgium"}, "description": t["svc_desc"]}])

# ============================================================ FOODTRUCK
TRUCK = {
 "nl": dict(titel="Foodtruck huren voor je bedrijf of event | Opperdash",
    desc="Huur de foodtruck van Opperdash voor je personeelsfeest, teamevent of feest: voedzame culinaire gerechten met mediterrane invloeden, vers geserveerd op keramiek.",
    crumb="Foodtruck", alt_hero="De foodtruck van Opperdash serveert gasten op een bedrijfsevent",
    h1="De foodtruck<br>staat voor je klaar", lead="Ik breng de keuken van Opperdash naar je bedrijf, teamevent of feest. Ook dranken kan ik voorzien.",
    alt_ger="Elias Nys aan het werk in de foodtruck van Opperdash", k1="Zin gekregen?",
    p1=["Vanuit de foodtruck serveer ik voedzame culinaire gerechten met mediterrane invloeden. Ik kook met seizoensproducten en dresseer ieder bord ter plaatse.",
        "Je gasten eten van keramiek met echt bestek. Kies enkel een hoofdgerecht of vul aan met hapjes en dessert."],
    alt_sfeer="Gerecht met rundvlees, verse groenten en kruiden uit de foodtruck van Opperdash",
    alt_cap="Twee koks van Opperdash dresseren borden in de foodtruck", k2="Capaciteit", badge="Tot<br>250<br>gasten",
    p2="Van een bedrijfslunch tot een groot event met tot 250 gasten: ik stem crew en service af op het aantal gasten en de gewenste serveertijd.",
    k3="Praktisch over de foodtruck",
    faq=[("Voor hoeveel gasten kan de foodtruck koken?", "Tot 250 gasten."),
         ("Wat heb je nodig voor de foodtruck?", "Een standplaats van 3 bij 3 meter en twee normale stopcontacten op een apart circuit."),
         ("Wat is inbegrepen?", "Keramisch servies, echt bestek, de volledige opbouw en afbraak en de bediening vanuit de foodtruck."),
         ("Wat kunnen we kiezen?", "Je kiest enkel een hoofdgerecht of vult aan met hapjes en dessert. Het menu volgt het seizoen."),
         ("Kan je ook dranken voorzien?", "Ja. Ik kan huisgemaakte limonade, mocktails en plat of bruisend water voorzien.")],
    svc="Foodtruck voor bedrijven en events", svc_desc="Voedzame culinaire gerechten met mediterrane invloeden, vers geserveerd vanuit de foodtruck op keramiek met echt bestek."),
 "en": dict(titel="Food truck hire for companies and events | Opperdash",
    desc="Hire the Opperdash food truck for your staff party, team event or celebration: nourishing culinary dishes with Mediterranean influences, served fresh on ceramic.",
    crumb="Food truck", alt_hero="The Opperdash food truck serving guests at a company event",
    h1="The food truck<br>is ready for you", lead="I bring the Opperdash kitchen to your company, team event or party. I can provide drinks too.",
    alt_ger="Elias Nys at work in the Opperdash food truck", k1="Feeling hungry?",
    p1=["From the food truck I serve nourishing culinary dishes with Mediterranean influences. I cook with seasonal produce and plate every dish on site.",
        "Your guests eat from ceramic plates with real cutlery. Choose a main course only, or add appetisers and dessert."],
    alt_sfeer="Dish with beef, fresh vegetables and herbs from the Opperdash food truck",
    alt_cap="Two Opperdash cooks plating dishes in the food truck", k2="Capacity", badge="Up to<br>250<br>guests",
    p2="From a company lunch to a large event of up to 250 guests: I match crew and service to the number of guests and the serving time you want.",
    k3="Food truck essentials",
    faq=[("How many guests can the food truck serve?", "Up to 250 guests."),
         ("What do you need for the food truck?", "A 3 by 3 metre pitch and two standard power sockets on a separate circuit."),
         ("What is included?", "Ceramic tableware, real cutlery, full setup and breakdown, and service from the food truck."),
         ("What can we choose?", "Choose a main course only, or add appetisers and dessert. The menu follows the season."),
         ("Can you provide drinks?", "Yes. I can provide homemade lemonade, mocktails and still or sparkling water.")],
    svc="Food truck for companies and events", svc_desc="Nourishing culinary dishes with Mediterranean influences, served fresh from the food truck on ceramic with real cutlery."),
 "fr": dict(titel="Louer un food truck pour votre entreprise | Opperdash",
    desc="Louez le food truck Opperdash pour votre fête du personnel, événement d’équipe ou fête : des plats culinaires et nourrissants aux influences méditerranéennes, servis en céramique.",
    crumb="Food truck", alt_hero="Le food truck Opperdash sert des invités lors d’un événement d’entreprise",
    h1="Le food truck<br>vous attend", lead="J’apporte la cuisine d’Opperdash dans votre entreprise, à votre événement d’équipe ou à votre fête. Je peux aussi prévoir les boissons.",
    alt_ger="Elias Nys au travail dans le food truck Opperdash", k1="Envie de goûter ?",
    p1=["Depuis le food truck, je sers des plats culinaires et nourrissants aux influences méditerranéennes. Je cuisine des produits de saison et dresse chaque assiette sur place.",
        "Vos invités mangent dans de la céramique avec de vrais couverts. Choisissez uniquement un plat principal, ou ajoutez des bouchées et un dessert."],
    alt_sfeer="Plat au bœuf, légumes frais et herbes du food truck Opperdash",
    alt_cap="Deux cuisiniers d’Opperdash dressent des assiettes dans le food truck", k2="Capacité", badge="Jusqu’à<br>250<br>invités",
    p2="D’un lunch d’entreprise à un grand événement jusqu’à 250 invités : j’adapte l’équipe et le service au nombre d’invités et à l’heure de service souhaitée.",
    k3="Infos pratiques",
    faq=[("Pour combien d’invités ?", "Jusqu’à 250 invités."),
         ("De quoi avez-vous besoin pour le food truck ?", "D’un emplacement de 3 mètres sur 3 et de deux prises électriques standard sur un circuit séparé."),
         ("Qu’est-ce qui est inclus ?", "La vaisselle en céramique, de vrais couverts, l’installation et le démontage complets, et le service depuis le food truck."),
         ("Que pouvons-nous choisir ?", "Uniquement un plat principal, ou un menu complété de bouchées et d’un dessert. Le menu suit la saison."),
         ("Pouvez-vous fournir des boissons ?", "Oui. Je peux prévoir de la limonade maison, des mocktails et de l’eau plate ou pétillante.")],
    svc="Food truck pour entreprises et événements", svc_desc="Des plats culinaires et nourrissants aux influences méditerranéennes, servis frais depuis le food truck en céramique avec de vrais couverts."),
}
for L in TALEN:
    t = TRUCK[L]
    pagina("foodtruck", L, t["titel"], t["desc"], f'''
<section class="hero">
  {img("foodtruck-hero.webp", t["alt_hero"], 1698, 1132, lazy=False)}
  <div class="container"><div class="hero__tekst">
    <h1>{t["h1"]}</h1>
    <p>{t["lead"]}</p>
  </div></div>
</section>

<section class="sectie sectie--linnen">
  <div class="container tekstblok">
      <h2>{t["k1"]}</h2>
      {"".join(f"<p>{p}</p>" for p in t["p1"])}
      <div class="knoppen"><a class="knop knop--salie knop--klein" href="{url("off_truck", L)}">{C[L]["boek_truck"]}</a></div>
  </div>
</section>

<section class="sectie sectie--split sectie--zand">
  <div class="duo">
    <div class="duo__beeld">{img("foodtruck-sfeer.webp", t["alt_sfeer"], 1698, 1132, sizes="(max-width: 800px) 100vw, 50vw")}<span class="badge" aria-hidden="true">{t["badge"]}</span></div>
    <div class="duo__tekst">
      <h2 class="zwaar">{t["k2"]}</h2>
      <p>{t["p2"]}</p>
      <div class="knoppen"><a class="knop knop--vol knop--klein" href="{url("off_truck", L)}">{C[L]["boek_truck"]}</a></div>
    </div>
  </div>
</section>

<section class="sectie">
  <div class="container">
    <h2 class="midden">{t["k3"]}</h2>
    {faq_html(t["faq"])}
  </div>
</section>
{slotband(L)}
''', hero="foodtruck-hero.webp", ogbeeld="og-foodtruck.jpg", ogalt=t["alt_hero"],
       schema=[breadcrumbs("foodtruck", L, t["crumb"]), faq_schema(t["faq"]),
               {"@type": "Service", "name": t["svc"], "serviceType": "Food truck catering", "provider": {"@id": ORG_ID},
                "areaServed": {"@type": "Country", "name": "Belgium"}, "description": t["svc_desc"]}])

# ============================================================ ONZE AANPAK
AANPAK = {
 "nl": dict(titel="Mijn aanpak voor catering op maat | Opperdash",
    desc="Een gesprek, een menu op maat en een zorgeloze dag. Eén vast aanspreekpunt en heldere afspraken. Zo verzorgt Opperdash de catering van je bedrijf of event.",
    crumb="Mijn aanpak", alt_hero="Een kok van Opperdash dresseert gerechten op keramiek", alt_bord="Een gerecht van Opperdash met bulgur en rodekoolsla op een keramisch bord", h1="Zo pak ik het aan.", lead="Eerst een gesprek, dan een menu op maat. Op de dag zelf zorg ik voor al de rest, van servies tot eventueel meubilair, en laat ik alles proper achter.", k1="Zo ga ik te werk",
    stappen=[("Eerst een gesprek", "We maken kennis. Ik luister naar je wensen en naar wat voor jou belangrijk is op het evenement."),
             ("Menu en offerte op maat", "Je krijgt een menu en een offerte op maat. Hapjes, voorgerecht en hoofdgerecht, of enkel een sterk hoofdgerecht? Dat bespreken we samen."),
             ("Zorgeloos", "Op de dag zelf open je enkel de deuren en voorzie je elektriciteit. Ik zorg voor al de rest, van servies tot eventueel meubilair, en laat alles proper achter.")],
    boek="Boek Opperdash", alt_sfeer="Menukaart van Opperdash tussen verse tomaten en basilicum",
    alt_truck="Elias Nys kookt in de foodtruck van Opperdash", k2="Foodtruck", p2="Voedzame culinaire gerechten, vers geserveerd vanuit de foodtruck.", b_truck="Foodtruck",
    v_titel="Voordelen van werken<br>met Opperdash",
    voordelen=[("Een vast aanspreekpunt", "Van offerte tot service op het evenement: je kan voor alles bij mij, Elias, terecht."),
               ("Op maat", "Elke offerte stel ik samen met jou op."),
               ("Persoonlijk", "Je spreekt rechtstreeks met mij. Zo weet je altijd waar je aan toe bent."),
               ("Duidelijke prijzen", "Geen verrassingen achteraf: heldere afspraken en één overzichtelijke totaalprijs bij de start."),
               ("Getraind eigen team", "Altijd dezelfde kwaliteit, ook bij grote hoeveelheden.")],
    alt_buf="Buffet met mediterrane gerechten van Opperdash", c_kop="Cases", c_tekst="Een kijk achter de schermen van enkele events die ik verzorgde: voor wie ik kookte, wat er op het bord kwam en hoe ik het aanpakte.", c_knop="Cases", alt_cases="Twee gerechten van Opperdash worden aan de foodtruck aan gasten gegeven", k3="Buffet", p3="Een culinair buffet met mediterrane invloeden, op keramiek en met echt bestek.", b_cat="Catering"),
 "en": dict(titel="How I work: tailored catering from start to finish | Opperdash",
    desc="A conversation, a tailored menu and a carefree day. One point of contact and clear agreements. This is how Opperdash caters your company or event.",
    crumb="How I work", alt_hero="An Opperdash cook plating dishes on ceramic", alt_bord="An Opperdash dish with bulgur and red cabbage slaw on a ceramic plate", h1="This is how I work.", lead="First a conversation, then a tailored menu. On the day itself I take care of everything else, from tableware to furniture if needed, and leave everything clean.", k1="How I work",
    stappen=[("First a conversation", "We get to know each other. I listen to your wishes and to what matters to you at the event."),
             ("A tailored menu and quote", "You receive a menu and a quote made to measure. Appetisers, starter and main course, or one strong main course? We decide together."),
             ("Carefree", "On the day itself, all you do is open the doors and provide electricity. I take care of everything else, from tableware to furniture if needed, and leave everything clean.")],
    boek="Book Opperdash", alt_sfeer="Opperdash menu card among fresh tomatoes and basil",
    alt_truck="Elias Nys cooking in the Opperdash food truck", k2="Food truck", p2="Nourishing culinary dishes, served fresh from the food truck.", b_truck="Food truck",
    v_titel="Why work<br>with Opperdash",
    voordelen=[("One point of contact", "From quote to service at the event, you can come to me, Elias, for everything."),
               ("Tailored", "I draw up every quote together with you."),
               ("Personal", "You talk to me directly, so you always know where you stand."),
               ("Clear pricing", "No surprises afterwards: clear agreements and one transparent total price from the start."),
               ("My own trained team", "Consistent quality, even for large numbers.")],
    alt_buf="Buffet of Mediterranean dishes by Opperdash", c_kop="Cases", c_tekst="A look behind the scenes of some of the events I catered: who I cooked for, what ended up on the plate and how I approached it.", c_knop="Cases", alt_cases="Two Opperdash dishes being handed to guests at the food truck", k3="Buffet", p3="A culinary buffet with Mediterranean influences, on ceramic and with real cutlery.", b_cat="Catering"),
 "fr": dict(titel="Mon approche : un traiteur sur mesure | Opperdash",
    desc="Un échange, un menu sur mesure et une journée sans souci. Un seul interlocuteur et des accords clairs. Voici comment Opperdash organise votre traiteur.",
    crumb="Mon approche", alt_hero="Un cuisinier d’Opperdash dresse des plats en céramique", alt_bord="Un plat d’Opperdash avec boulgour et salade de chou rouge dans une assiette en céramique", h1="Voilà comment je travaille.", lead="D’abord un échange, puis un menu sur mesure. Le jour même, je m’occupe de tout le reste, de la vaisselle au mobilier si nécessaire, et je laisse tout propre derrière moi.", k1="Ma façon de travailler",
    stappen=[("D’abord un échange", "Nous faisons connaissance. J’écoute vos souhaits et ce qui compte pour vous lors de l’événement."),
             ("Un menu et un devis sur mesure", "Vous recevez un menu et un devis sur mesure. Bouchées, entrée et plat, ou uniquement un plat principal fort ? Nous en discutons ensemble."),
             ("Sans souci", "Le jour même, vous n’avez qu’à ouvrir les portes et à prévoir l’électricité. Je m’occupe de tout le reste, de la vaisselle au mobilier si nécessaire, et je laisse tout propre derrière moi.")],
    boek="Réservez", alt_sfeer="Carte du menu Opperdash parmi des tomates fraîches et du basilic",
    alt_truck="Elias Nys cuisine dans le food truck Opperdash", k2="Food truck", p2="Des plats culinaires et nourrissants, servis frais depuis le food truck.", b_truck="Food truck",
    v_titel="Les avantages<br>d’Opperdash",
    voordelen=[("Un seul interlocuteur", "Du devis au service le jour J, vous pouvez tout me demander, à moi, Elias."),
               ("Sur mesure", "J’établis chaque devis avec vous."),
               ("Personnel", "Vous parlez directement avec moi et savez toujours où vous en êtes."),
               ("Des prix clairs", "Pas de surprise après coup : des accords clairs et un prix total transparent dès le départ."),
               ("Ma propre équipe formée", "Une qualité constante, même pour de grandes quantités.")],
    alt_buf="Buffet de plats méditerranéens d’Opperdash", c_kop="Références", c_tekst="Les coulisses de quelques événements que j’ai servis : pour qui j’ai cuisiné, ce qui s’est retrouvé dans l’assiette et comment je m’y suis pris.", c_knop="Références", alt_cases="Deux plats Opperdash remis à des invités au food truck", k3="Buffet", p3="Un buffet culinaire aux influences méditerranéennes, en céramique et avec de vrais couverts.", b_cat="Traiteur"),
}
# Waarom mensen voor Opperdash kiezen (Mijn aanpak). Vijf punten van Elias (14/11/2026), elk met een eigen icoon:
# smaak en gezond, seizoen en lokaal, keramiek met echt bestek, zorgeloos, vast aanspreekpunt.
ANDERS = {
 "nl": dict(kop="Waarom kiezen mensen voor Opperdash?", alt="Een gerecht van Opperdash in een donkere keramische kom",
            punten=["Intense smaken, gezond voor het lichaam", "Seizoensgebonden en lokale ingrediënten","Altijd op keramiek met echt bestek", "Volledig ontzorgd, van voorbereiding tot afronding", "Ik ben je vaste aanspreekpunt"]),
 "en": dict(kop="Why do people choose Opperdash?", alt="An Opperdash dish in a dark ceramic bowl",
            punten=["Intense flavours, healthy for the body", "Seasonal and local ingredients","Always on ceramic with real cutlery", "Fully taken care of, from preparation to wrap-up", "I am your single point of contact"]),
 "fr": dict(kop="Pourquoi choisit-on Opperdash ?", alt="Un plat d’Opperdash dans un bol en céramique foncée",
            punten=["Des saveurs intenses, saines pour le corps", "Des ingrédients locaux et de saison","Toujours en céramique avec de vrais couverts", "Tout est pris en charge, de la préparation au rangement", "Je suis votre interlocuteur unique"]),
}
_ICOON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{}</svg>'
# Zelfde volgorde als de punten: vlam, blad, bestek, vinkje in cirkel, persoon.
ANDERS_ICONEN = [
    _ICOON.format('<path d="M8.5 14.5A2.5 2.5 0 0 0 11 12c0-1.38-.5-2-1-3-1.072-2.143-.224-4.054 2-6 .5 2.5 2 4.9 4 6.5 2 1.6 3 3.5 3 5.5a7 7 0 1 1-14 0c0-1.153.433-2.294 1-3a2.5 2.5 0 0 0 2.5 2.5z"/>'),
    _ICOON.format('<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>'),
    _ICOON.format('<path d="M3 2v7c0 1.1.9 2 2 2h4a2 2 0 0 0 2-2V2"/><path d="M7 2v20"/><path d="M21 15V2a5 5 0 0 0-5 5v6c0 1.1.9 2 2 2h3Zm0 0v7"/>'),
    _ICOON.format('<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>'),
    _ICOON.format('<circle cx="12" cy="8" r="5"/><path d="M20 21a8 8 0 0 0-16 0"/>'),
]


def keuze_blok(L, klasse="sectie"):
    """Twee fotokaarten: foodtruck en catering (home en Mijn aanpak)."""
    t = HOME[L]
    return f'''<section class="{klasse}">
  <div class="container">
    <div class="keuze">
      <article class="keuze__item">
        <a class="keuze__beeld" href="{url("foodtruck", L)}" tabindex="-1" aria-hidden="true">{img("foodtruck-hero.webp", t["alt_k_truck"], 1698, 1132, sizes="(max-width: 800px) 100vw, 50vw")}</a>
        <p>{t["k_truck"]}</p>
        <a class="knop knop--klein" href="{url("foodtruck", L)}">{t["b_truck"]}</a>
      </article>
      <article class="keuze__item">
        <a class="keuze__beeld" href="{url("catering", L)}" tabindex="-1" aria-hidden="true">{img("catering-sfeer.webp", t["alt_k_cat"], 1920, 1275, sizes="(max-width: 800px) 100vw, 50vw")}</a>
        <p>{t["k_cat"]}</p>
        <a class="knop knop--klein" href="{url("catering", L)}">{t["b_cat"]}</a>
      </article>
    </div>
  </div>
</section>'''


def anders_blok(L):
    a = ANDERS[L]
    punten = "".join(f"<li>{icoon}<span>{x}</span></li>" for icoon, x in zip(ANDERS_ICONEN, a["punten"]))
    return f'''<section class="sectie anders">
  <div class="container">
    <div class="anders__vlak">
      <h2 class="anders__kop">{a["kop"]}</h2>
      <div class="anders__bord">{img("verhaal-elias.webp", a["alt"], 962, 641, sizes="(max-width: 800px) 70vw, 36vw")}</div>
    </div>
    <ul class="anders__punten">{punten}</ul>
  </div>
</section>'''


for L in TALEN:
    t = AANPAK[L]
    stappen = "".join(f'<li class="stap"><span class="stap__nr" aria-hidden="true">{i}</span><h3>{a}</h3><p>{b}</p></li>'
                      for i, (a, b) in enumerate(t["stappen"], 1))
    pagina("aanpak", L, t["titel"], t["desc"], f'''
<section class="hero">
  {img("aanpak-hero-bord.webp", t["alt_bord"], 1920, 1280, lazy=False)}
  <div class="container hero__tekst"><h1>{t["h1"]}</h1><p>{t["lead"]}</p></div>
</section>

{band(L)}

{anders_blok(L)}

<section class="sectie sectie--eco">
  <div class="container midden">
    <h2 class="kop-groot">{t["k1"]}</h2>
    <ol class="stappen">{stappen}</ol>
    <a class="knop knop--groen stappen__knop" href="{url("contact", L)}">{t["boek"]}</a>
  </div>
</section>

<div class="beeld">{img("aanpak-sfeer.webp", t["alt_sfeer"], 1698, 1132)}</div>

<section class="sectie sectie--linnen">
  <div class="container duo">
    <div class="duo__beeld">{img("aanpak-cases.webp", t["alt_cases"], 1440, 960, sizes="(max-width: 800px) 100vw, 50vw")}</div>
    <div class="duo__tekst">
      <h2>{t["c_kop"]}</h2>
      <p>{t["c_tekst"]}</p>
      <div class="knoppen"><a class="knop knop--vol" href="{url("cases", L)}">{t["c_knop"]}</a></div>
    </div>
  </div>
</section>

{keuze_blok(L)}
''', hero="aanpak-hero-bord.webp", ogbeeld="og-aanpak.jpg", ogalt=t["alt_hero"], schema=[breadcrumbs("aanpak", L, t["crumb"])])

# ============================================================ ONS VERHAAL
VERHAAL = {
 "nl": dict(titel="Mijn verhaal: Elias Nys, chef en oprichter | Opperdash",
    desc="Elias Nys kookte in de fine dining en liep stage in San Sebastián. Met Opperdash kookt hij voedzame culinaire gerechten met mediterrane invloeden.",
    crumb="Mijn verhaal", alt_hero="Elias Nys serveert gasten vanuit de foodtruck van Opperdash",
    alt_foto="Een gast krijgt een gerecht van Opperdash aangereikt aan de foodtruck", h1="Het verhaal achter<br>Opperdash",
    alt_el="Een gerecht van Opperdash in een donkere keramische kom", alt_tuin="Chef Elias Nys proeft van verse kruiden in een tuin met lavendel", k1="Wie zit er<br>achter Opperdash?",
    p1=["Ik ben Elias Nys, chef, ondernemer en oprichter van Opperdash. In mijn keuken zijn kwaliteit en gezondheid even belangrijk, met intense smaken en een verfijnde presentatie als hoofddoel.",
        "Na mijn opleiding Lichamelijke Opvoeding koos ik voor de horeca. Ik volgde de opleidingen Restauranthouder en Horecamanagement en deed mijn ervaring op in de fine dining. Ik werkte meerdere jaren bij restaurant d’Artagnan en liep stage bij restaurant Arenberg in Leuven.",
        "In 2024 trok ik vier maanden naar Spanje en werkte daar in het vijfsterrenhotel Maria Cristina. Ik werd verliefd op de puurheid van de mediterrane keuken. Die inspiratie verwerk ik nu in de gerechten van Opperdash."],
    alt_med="Bruschetta met tomaat en basilicum, een mediterraan gerecht van Opperdash", k2="Mediterrane inspiratie",
    p2=["De mediterrane keuken draait om pure producten, olijfolie, kruiden en het seizoen. Daar vertrek ik van. Mijn gerechten dragen invloeden uit onder meer Spanje, Griekenland en Italië. Ook mijn eigen creaties volgen die principes.",
        "Ik kook met extra vierge olijfolie van Arbequina-olijven, frituur niets en werk zonder geraffineerde suiker, geraffineerde olie of additieven. Zo bereid ik zowel vegetarische als niet-vegetarische gerechten."],
    k3="Waar het begon", alt_begin="Verse paprika, groenten en kruiden naast een snijplank met het logo van Opperdash",
    p3=["Opperdash begon als fitnessfoodtruck. Daar ben ik in de diepte gaan kijken naar wat echt goed is voor het lichaam.",
        "Daaruit kwam één keuze: geen additieven, geen geraffineerde olie en geen geraffineerde suiker. Wat overblijft, zijn whole foods en pure producten.",
        "Met die producten kook ik zoals ik het in de fine dining en in San Sebastián leerde. Ik haal het maximum aan smaak uit elk product, hou het herkenbaar en werk gerechten af met verschillende garnituren, kleuren en texturen. Die combinatie van culinair vakmanschap en gezond eten maakt Opperdash anders."],
    job="Chef en oprichter"),
 "en": dict(titel="About Elias Nys, chef and founder | Opperdash",
    desc="Elias Nys trained in fine dining and in a five-star hotel in San Sebastián. With Opperdash he cooks nourishing culinary dishes with Mediterranean influences.",
    crumb="My story", alt_hero="Elias Nys serving guests from the Opperdash food truck",
    alt_foto="A guest is handed an Opperdash dish at the food truck", h1="The story behind<br>Opperdash",
    alt_el="An Opperdash dish in a dark ceramic bowl", alt_tuin="Chef Elias Nys tasting fresh herbs in a garden with lavender", k1="Who is behind<br>Opperdash?",
    p1=["I am Elias Nys, chef, entrepreneur and founder of Opperdash. In my kitchen, quality and health matter equally, with intense flavour and refined presentation as the main goal.",
        "After studying Physical Education, I chose hospitality. I trained in Restaurant Ownership and Hospitality Management and gained my experience in fine dining. I worked for several years at restaurant d’Artagnan and did an internship at restaurant Arenberg in Leuven.",
        "In 2024 I spent four months in Spain, working at the five-star Hotel Maria Cristina. I fell in love with the purity of Mediterranean cooking, and I now bring that inspiration into the dishes of Opperdash."],
    alt_med="Bruschetta with tomato and basil, a Mediterranean dish by Opperdash", k2="Mediterranean inspiration",
    p2=["Mediterranean cooking is about pure produce, olive oil, herbs and the season. That is where I start. My dishes carry influences from Spain, Greece and Italy, among others, and my own creations follow the same principles.",
        "I cook with extra virgin olive oil from Arbequina olives, never deep-fry and work without refined sugar, refined oils or additives. That is how I prepare both vegetarian and non-vegetarian dishes."],
    k3="Where it started", alt_begin="Fresh peppers, vegetables and herbs next to a chopping board with the Opperdash logo",
    p3=["Opperdash started out as a fitness food truck. That is where I began looking closely at what is truly good for the body.",
        "That led to one choice: no additives, no refined oils and no refined sugar. What remains are whole foods and pure produce.",
        "I cook with that produce the way I learned in fine dining and in San Sebastián. I draw the most flavour out of every product, keep it recognisable and finish dishes with different garnishes, colours and textures. That combination of culinary craft and healthy food is what sets Opperdash apart."],
    job="Chef and founder"),
 "fr": dict(titel="Elias Nys, chef et fondateur d’Opperdash | Opperdash",
    desc="Elias Nys s’est formé en haute cuisine et dans un hôtel cinq étoiles à Saint-Sébastien. Avec Opperdash, il cuisine des plats culinaires et nourrissants aux influences méditerranéennes.",
    crumb="Mon histoire", alt_hero="Elias Nys sert des invités depuis le food truck Opperdash",
    alt_foto="Un invité reçoit un plat Opperdash au food truck", h1="L’histoire<br>d’Opperdash",
    alt_el="Un plat d’Opperdash dans un bol en céramique foncée", alt_tuin="Le chef Elias Nys goûte des herbes fraîches dans un jardin avec de la lavande", k1="Qui se cache derrière<br>Opperdash ?",
    p1=["Je suis Elias Nys, chef, entrepreneur et fondateur d’Opperdash. Dans ma cuisine, la qualité et la santé comptent autant l’une que l’autre, avec des saveurs intenses et une présentation soignée comme objectif principal.",
        "Après des études d’éducation physique, j’ai choisi l’horeca. J’ai suivi les formations de restaurateur et de gestion hôtelière, puis acquis mon expérience dans la haute cuisine. J’ai travaillé plusieurs années au restaurant d’Artagnan et effectué un stage au restaurant Arenberg à Louvain.",
        "En 2024, je suis parti quatre mois en Espagne et j’ai travaillé à l’hôtel cinq étoiles Maria Cristina. Je suis tombé amoureux de la pureté de la cuisine méditerranéenne, et j’intègre aujourd’hui cette inspiration dans les plats d’Opperdash."],
    alt_med="Bruschetta à la tomate et au basilic, un plat méditerranéen d’Opperdash", k2="Inspiration méditerranéenne",
    p2=["La cuisine méditerranéenne repose sur des produits purs, l’huile d’olive, les herbes et la saison. C’est mon point de départ. Mes plats portent des influences d’Espagne, de Grèce et d’Italie notamment, et mes propres créations suivent les mêmes principes.",
        "Je cuisine à l’huile d’olive vierge extra d’olives Arbequina, sans aucune friture, sans sucre raffiné, huile raffinée ni additifs. C’est ainsi que je prépare des plats végétariens comme non végétariens."],
    k3="Là où tout a commencé", alt_begin="Poivrons, légumes et herbes fraîches à côté d’une planche à découper avec le logo d’Opperdash",
    p3=["Opperdash a commencé comme food truck fitness. C’est là que j’ai étudié de près ce qui est vraiment bon pour le corps.",
        "Il en est sorti un choix : pas d’additifs, pas d’huile raffinée et pas de sucre raffiné. Ce qui reste, ce sont des aliments bruts et des produits purs.",
        "Je cuisine ces produits comme je l’ai appris dans la haute cuisine et à Saint-Sébastien. J’en tire un maximum de goût, je garde chaque produit reconnaissable et je termine les plats avec différentes garnitures, couleurs et textures. C’est cette combinaison de savoir-faire culinaire et d’alimentation saine qui rend Opperdash différent."],
    job="Chef et fondateur"),
}
for L in TALEN:
    t = VERHAAL[L]
    pagina("verhaal", L, t["titel"], t["desc"], f'''
<section class="hero">
  {img("verhaal-hero-truck.webp", t["alt_foto"], 1920, 1329, lazy=False)}
  <div class="container hero__tekst"><h1>{t["h1"]}</h1></div>
</section>


<section class="sectie sectie--linnen">
  <div class="container duo">
    <div class="duo__beeld duo__beeld--hoog">{img("verhaal-elias-tuin.webp", t["alt_tuin"], 853, 1280)}</div>
    <div class="duo__tekst">
      <h2>{t["k1"]}</h2>
      {"".join(f"<p>{p}</p>" for p in t["p1"])}
    </div>
  </div>
</section>

<section class="sectie">
  <div class="container duo duo--begin">
    <div class="duo__tekst">
      <h2>{t["k3"]}</h2>
      {"".join(f"<p>{p}</p>" for p in t["p3"])}
    </div>
    <div class="duo__beeld duo__beeld--vierkant">{img("verhaal-hero.webp", t["alt_begin"], 1920, 1235, sizes="(max-width: 800px) 100vw, 50vw")}</div>
  </div>
</section>

<section class="sectie sectie--split sectie--zand">
  <div class="duo duo--omgekeerd">
    <div class="duo__beeld">{img("home-visie.webp", t["alt_med"], 962, 641)}</div>
    <div class="duo__tekst">
      <h2>{t["k2"]}</h2>
      {"".join(f"<p>{p}</p>" for p in t["p2"])}
    </div>
  </div>
</section>
{slotband(L)}
''', hero="verhaal-hero-truck.webp", ogbeeld="og-verhaal.jpg", ogalt=t["alt_hero"],
       schema=[breadcrumbs("verhaal", L, t["crumb"]),
               {"@type": "AboutPage", "url": SITE + url("verhaal", L), "about": {"@id": ORG_ID}},
               {"@type": "Person", "name": "Elias Nys", "jobTitle": t["job"], "worksFor": {"@id": ORG_ID},
                "sameAs": ["https://www.linkedin.com/in/elias-nys-a01702294/"]}])


# ============================================================ FORMULIEREN
def veld(naam, label, type_="text", verplicht=False, vol=False, ph="", textarea=False, auto=""):
    req = " required" if verplicht else ""
    ster = ' <span class="verplicht" aria-hidden="true">*</span>' if verplicht else ""
    php = f' placeholder="{ph}"' if ph else ""
    ac = f' autocomplete="{auto}"' if auto else ""
    ctrl = (f'<textarea id="{naam}" name="{naam}"{req}{php}></textarea>' if textarea
            else f'<input id="{naam}" name="{naam}" type="{type_}"{req}{php}{ac}>')
    return f'<div{" class=\"vol\"" if vol else ""}><label for="{naam}">{label}{ster}</label>{ctrl}</div>'


def formulier(naam, L, onderwerp, velden):
    return f'''<form class="formulier" name="{naam}" method="POST" action="{url("bedankt", L)}" data-netlify="true" netlify-honeypot="bot-field">
  <input type="hidden" name="form-name" value="{naam}">
  <input type="hidden" name="subject" value="{onderwerp}">
  <input type="hidden" name="taal" value="{L.upper()}">
  <p class="verborgen"><label>{C[L]["niet_invullen"]} <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
  {"".join(velden)}
  <div class="vol midden formulier__verstuur"><button class="knop knop--groen" type="submit">{C[L]["verstuur"]}</button></div>
</form>'''


LAB = {
 "nl": dict(naam="Je naam", vnaam="Voornaam + Naam", tel="Telefoonnummer", mail="Je e-mail", bedrijf="Je bedrijf", onderwerp="Onderwerp", vraag="Je vraag",
            datum="Datum event", locatie="Locatie", aantal="Aantal personen", event="Naam event", uitleg="Beetje uitleg",
            ph_cat="Hey! Wij zoeken voor ons bedrijfsevenement een culinaire catering!", ph_truck="Hey! Wij zoeken een foodtruck voor onze verjaardag/trouw/festival in de avond!"),
 "en": dict(naam="Your name", vnaam="First and last name", tel="Phone number", mail="Your email", bedrijf="Your company", onderwerp="Subject", vraag="Your question",
            datum="Event date", locatie="Location", aantal="Number of guests", event="Event name", uitleg="Tell me a bit more",
            ph_cat="Hi! We are looking for culinary catering for our company event.", ph_truck="Hi! We are looking for a food truck for our birthday, wedding or festival in the evening."),
 "fr": dict(naam="Votre nom", vnaam="Prénom et nom", tel="Téléphone", mail="Votre e-mail", bedrijf="Votre entreprise", onderwerp="Objet", vraag="Votre question",
            datum="Date de l’événement", locatie="Lieu", aantal="Nombre de personnes", event="Nom de l’événement", uitleg="Quelques détails",
            ph_cat="Bonjour ! Nous cherchons un traiteur culinaire pour notre événement d’entreprise.", ph_truck="Bonjour ! Nous cherchons un food truck pour notre anniversaire, mariage ou festival en soirée."),
}
CONTACT = {
 "nl": dict(titel="Contact: catering of foodtruck aanvragen | Opperdash", desc="Neem contact op met Opperdash voor catering, een buffet of de foodtruck. Mail elias@opperdash.be, bel +32 470 32 63 32 of stuur je vraag via het formulier.",
            crumb="Contact", h1="Neem contact op", p="Vertel me over je event of stel je vraag. Ik antwoord binnen 24 uur.", vh="Contactformulier"),
 "en": dict(titel="Get in touch about catering or the food truck | Opperdash", desc="Contact Opperdash for catering, a buffet or the food truck. Email elias@opperdash.be, call +32 470 32 63 32 or send your question using the form.",
            crumb="Contact", h1="Get in touch", p="Tell me about your event or ask your question. I reply within 24 hours. I speak Dutch, English and French.", vh="Contact form"),
 "fr": dict(titel="Contact : traiteur ou food truck | Opperdash", desc="Contactez Opperdash pour un traiteur, un buffet ou le food truck. Écrivez à elias@opperdash.be, appelez le +32 470 32 63 32 ou utilisez le formulaire.",
            crumb="Contact", h1="Contactez-moi", p="Parlez-moi de votre événement ou posez votre question. Je réponds dans les 24 heures. Je parle français, néerlandais et anglais.", vh="Formulaire de contact"),
}
for L in TALEN:
    t, l = CONTACT[L], LAB[L]
    pagina("contact", L, t["titel"], t["desc"], f'''
<section class="sectie sectie--eco">
  <div class="container midden">
    <h1>{t["h1"]}</h1>
    <p>{t["p"]}</p>
    <p class="contactinfo"><a href="mailto:elias@opperdash.be">elias@opperdash.be</a><br><a href="tel:+32470326332">+32 470 32 63 32</a></p>
  </div>
</section>
<section class="sectie">
  <div class="container">
    <h2 class="visueel-verborgen">{t["vh"]}</h2>
    {formulier("contact", L, "Nieuw bericht via opperdash.be (" + L.upper() + ")", [
        veld("naam", l["naam"], verplicht=True, auto="name"),
        veld("telefoon", l["tel"], "tel", auto="tel"),
        veld("email", l["mail"], "email", verplicht=True, auto="email"),
        veld("bedrijf", l["bedrijf"], auto="organization"),
        veld("onderwerp", l["onderwerp"], verplicht=True, vol=True),
        veld("vraag", l["vraag"], verplicht=True, vol=True, textarea=True)])}
  </div>
</section>
''', schema=[breadcrumbs("contact", L, t["crumb"]), {"@type": "ContactPage", "url": SITE + url("contact", L), "about": {"@id": ORG_ID}}])

OFF = {
 "off_cat": {
  "nl": dict(titel="Offerte aanvragen voor catering of buffet | Opperdash", desc="Vraag een offerte aan voor een culinair buffet, catering aan tafel of een walking dinner. Vertel me datum, locatie en aantal gasten.",
             crumb="Offerte catering", h1="Offerte aanvragen", p="Vertel me wat je plant: de datum, de locatie, het aantal gasten en het soort moment. Ik neem binnen de 24 uur contact met je op.", vh="Offerteformulier catering"),
  "en": dict(titel="Request a quote for catering or a buffet | Opperdash", desc="Request a quote for a culinary buffet, seated catering or a walking dinner. Tell me the date, location and number of guests.",
             crumb="Catering quote", h1="Request a quote", p="Tell me what you are planning: the date, the location, the number of guests and the kind of occasion. I will get back to you within 24 hours.", vh="Catering quote form"),
  "fr": dict(titel="Demander un devis traiteur ou buffet | Opperdash", desc="Demandez un devis pour un buffet culinaire, un service à table ou un walking dinner. Indiquez la date, le lieu et le nombre d’invités.",
             crumb="Devis traiteur", h1="Demander un devis", p="Dites-moi ce que vous préparez : la date, le lieu, le nombre d’invités et le type d’événement. Je vous recontacte dans les 24 heures.", vh="Formulaire de devis traiteur")},
 "off_truck": {
  "nl": dict(titel="Foodtruck aanvragen voor je event | Opperdash", desc="Vraag een voorstel op maat aan voor de foodtruck van Opperdash. Ik bekijk locatie, aantal gasten en timing en bezorg je een duidelijke offerte.",
             crumb="Foodtruck aanvragen", h1="Foodtruck aanvragen", p="Vraag een voorstel op maat voor je event. Ik neem binnen de 24 uur contact met je op.", vh="Aanvraagformulier foodtruck"),
  "en": dict(titel="Book the food truck for your event | Opperdash", desc="Request a tailored proposal for the Opperdash food truck. I look at location, number of guests and timing and send you a clear quote.",
             crumb="Book the food truck", h1="Book the food truck", p="Request a tailored proposal for your event. I will get back to you within 24 hours.", vh="Food truck request form"),
  "fr": dict(titel="Réserver le food truck pour votre événement | Opperdash", desc="Demandez une proposition sur mesure pour le food truck Opperdash. J’étudie le lieu, le nombre d’invités et l’horaire et vous envoie un devis clair.",
             crumb="Réserver le food truck", h1="Réserver le food truck", p="Demandez une proposition sur mesure pour votre événement. Je vous recontacte dans les 24 heures.", vh="Formulaire de réservation food truck")},
}
# Wat er gebeurt na een aanvraag. Alleen stappen die al op de site staan (formulier, 24 uur, Mijn aanpak).
OFF_STAPPEN = {
 "nl": ("Zo gaat het verder", [
    ("Je aanvraag", "Vul het formulier in. Vertel me de datum, de locatie, het aantal gasten en het soort moment."),
    ("Binnen 24 uur", "Ik neem binnen de 24 uur contact met je op."),
    ("Een voorstel op maat", "Ik luister naar je wensen, je gasten en het moment, en doe een voorstel dat daarbij past."),
    ("Zorgeloos", "Op de dag zelf open je enkel de deuren en voorzie je elektriciteit. Ik zorg voor al de rest, van servies tot eventueel meubilair.")]),
 "en": ("Next steps", [
    ("Your request", "Fill in the form. Tell me the date, the location, the number of guests and the kind of occasion."),
    ("Within 24 hours", "I will get back to you within 24 hours."),
    ("A tailored proposal", "I listen to your wishes, your guests and the occasion, and make a proposal that fits."),
    ("Carefree", "On the day itself, all you do is open the doors and provide electricity. I take care of everything else, from tableware to furniture if needed.")]),
 "fr": ("La suite", [
    ("Votre demande", "Remplissez le formulaire. Indiquez-moi la date, le lieu, le nombre d’invités et le type d’événement."),
    ("Dans les 24 heures", "Je vous recontacte dans les 24 heures."),
    ("Une proposition sur mesure", "J’écoute vos souhaits, vos invités et le moment, puis je fais une proposition adaptée."),
    ("Sans souci", "Le jour même, vous n’avez qu’à ouvrir les portes et à prévoir l’électricité. Je m’occupe de tout le reste, de la vaisselle au mobilier si nécessaire.")]),
}


def off_stappen(L):
    kop, stappen = OFF_STAPPEN[L]
    lijst = "".join(f'<li><span class="volgorde__nr" aria-hidden="true">{i}</span><div><h3>{a}</h3><p>{b}</p></div></li>' for i, (a, b) in enumerate(stappen, 1))
    return f'''<aside class="offerte__stappen">
        <h2 class="kop-klein">{kop}</h2>
        <ol class="volgorde">{lijst}</ol>
      </aside>'''


for page, formnaam, onderwerp, verplicht_extra, ph in [
        ("off_cat", "offerte-catering", "Nieuwe offerteaanvraag catering via opperdash.be", True, "ph_cat"),
        ("off_truck", "offerte-foodtruck", "Nieuwe aanvraag foodtruck via opperdash.be", False, "ph_truck")]:
    for L in TALEN:
        t, l = OFF[page][L], LAB[L]
        pagina(page, L, t["titel"], t["desc"], f'''
<section class="sectie sectie--linnen offerte">
  <div class="container">
    <div class="offerte__kop">
      <h1>{t["h1"]}</h1>
      <p>{t["p"]}</p>
    </div>
    <div class="offerte__raster">
      <div class="offerte__form">
        <h2 class="visueel-verborgen">{t["vh"]}</h2>
        {formulier(formnaam, L, onderwerp + " (" + L.upper() + ")", [
        veld("naam", l["vnaam"], verplicht=True, auto="name"),
        veld("telefoon", l["tel"], "tel", verplicht=verplicht_extra, auto="tel"),
        veld("email", l["mail"], "email", verplicht=True, auto="email"),
        veld("bedrijf", l["bedrijf"], auto="organization"),
        veld("datum", l["datum"], "date"),
        veld("locatie", l["locatie"], verplicht=verplicht_extra),
        veld("aantal_personen", l["aantal"], "number", verplicht=verplicht_extra),
        veld("naam_event", l["event"], verplicht=True),
        veld("uitleg", l["uitleg"], verplicht=True, vol=True, textarea=True, ph=l[ph])])}
      </div>
      {off_stappen(L)}
    </div>
  </div>
</section>
''', ogbeeld=("og-catering.jpg" if page == "off_cat" else "og-foodtruck.jpg"), ogalt=t["titel"].split(" | ")[0], schema=[breadcrumbs(page, L, t["crumb"])])

BEDANKT = {
 "nl": ("Bedankt voor je bericht | Opperdash", "Bedankt!", "Je bericht is verstuurd. Ik neem binnen de 24 uur contact met je op.", "Ga naar de startpagina"),
 "en": ("Thank you for your message | Opperdash", "Thank you!", "Your message has been sent. I will get back to you within 24 hours.", "Go to the home page"),
 "fr": ("Merci pour votre message | Opperdash", "Merci !", "Votre message a bien été envoyé. Je vous recontacte dans les 24 heures.", "Retour à l’accueil"),
}
NIETGEVONDEN = {
 "nl": ("Pagina niet gevonden | Opperdash", "Pagina niet gevonden", 'Deze pagina bestaat niet (meer). Bekijk de <a href="/catering">catering</a>, de <a href="/foodtruck">foodtruck</a> of <a href="/contact">neem contact op</a>.', "Ga naar de startpagina"),
 "en": ("Page not found | Opperdash", "Page not found", 'This page does not exist (anymore). Have a look at the <a href="/en/catering">catering</a>, the <a href="/en/food-truck">food truck</a> or <a href="/en/contact">get in touch</a>.', "Go to the home page"),
 "fr": ("Page introuvable | Opperdash", "Page introuvable", 'Cette page n’existe pas (ou plus). Découvrez le <a href="/fr/traiteur">service traiteur</a>, le <a href="/fr/food-truck">food truck</a> ou <a href="/fr/contact">contactez-moi</a>.', "Retour à l’accueil"),
}
for L in TALEN:
    ti, h, p, k = BEDANKT[L]
    pagina("bedankt", L, ti, p, f'''
<section class="sectie sectie--zwart sectie--vol">
  <div class="container midden">
    <h1>{h}</h1>
    <p>{p}</p>
    <a class="knop knop--vol" href="{url("home", L)}">{k}</a>
  </div>
</section>''', index=False)
    ti, h, p, k = NIETGEVONDEN[L]
    pagina("404", L, ti, h, f'''
<section class="sectie sectie--zwart sectie--vol">
  <div class="container midden">
    <h1>{h}</h1>
    <p>{p}</p>
    <a class="knop knop--vol" href="{url("home", L)}">{k}</a>
  </div>
</section>''', index=False)

# ============================================================ OFFERTE TEKENEN
# De klant opent de link uit zijn draaiboek of de meetingchat, bv. /offerte-tekenen?klant=Asmodee&bedrag=4250
# (optioneel ook &nr=,  &event=, &datum=JJJJ-MM-DD, &uur=, &locatie=, &personen=, &formule= en &pdf=https://...).
# Zonder klant of bedrag toont de pagina geen formulier: een klant tekent nooit een blanco offerte.
# De links maakt draaiboek-evenement automatisch per draaiboek (zie die skill); /offerte-link is de handmatige terugval.
# Verzenden gaat naar het Netlify-formulier "offerte-tekenen"; de mails komen uit netlify/functions/submission-created.
# Links maken: /offerte-link (interne hulppagina, niet gelinkt, noindex).
TEKENEN = {
 "nl": dict(titel="Offerte tekenen | Opperdash", desc="Teken je offerte van Opperdash online.", h1="Offerte tekenen",
            p="Kijk je offerte na, vink aan dat je akkoord gaat en zet je naam eronder. Daarna stuur ik je de getekende offerte en het draaiboek per mail.",
            offerte="Offerte", klant="Voor", event="Event", bedrag="Totaal excl. btw", pdf="Bekijk de offerte (pdf)",
            ev_kop="Het event", datum="Datum", uur="Uur", locatie="Locatie", personen="Aantal personen", formule="Formule", personen_tekst="ca. {n} personen",
            leeg="Deze link bevat geen offerte. Gebruik de link uit je offerte of mail naar elias@opperdash.be.", naam="Voornaam en naam", functie="Functie", mail="Je e-mail", mail_hint="Hier stuur ik de getekende offerte naartoe.",
            hand="Teken hier", optioneel="(niet verplicht)", hand_hint="Met je vinger of muis.", hand_vak="Handtekeningvak", wis="Wissen",
            akkoord="Ik ga akkoord met deze offerte en de algemene voorwaarden die erin staan. Ik mag dit namens mijn organisatie bevestigen.",
            knop="Offerte tekenen", bezig="Even geduld…", noot="Als bewijs van je akkoord bewaar ik je naam, functie, e-mail, het tijdstip en je IP-adres.",
            fout="Het versturen lukte niet. Probeer het opnieuw of mail naar elias@opperdash.be.",
            noscript="Zet JavaScript aan om je offerte te tekenen, of bevestig per mail naar elias@opperdash.be.",
            klaar_h="Getekend, bedankt!", klaar_p="Ik heb je akkoord ontvangen op {tijd}. De getekende offerte en het draaiboek stuur ik je naar {email}.",
            klaar_p2="Ik stuur je binnenkort de voorschotfactuur.", terug="Naar de startpagina", locale="nl-BE"),
 "en": dict(titel="Sign your quote | Opperdash", desc="Sign your Opperdash quote online.", h1="Sign your quote",
            p="Check your quote, tick that you agree and add your name. I will then email you the signed quote and the event plan.",
            offerte="Quote", klant="For", event="Event", bedrag="Total excl. VAT", pdf="View the quote (PDF)",
            ev_kop="The event", datum="Date", uur="Time", locatie="Location", personen="Guests", formule="Format", personen_tekst="approx. {n} guests",
            leeg="This link does not contain a quote. Please use the link in your quote or email elias@opperdash.be.", naam="First and last name", functie="Job title", mail="Your email", mail_hint="I will send the signed quote to this address.",
            hand="Sign here", optioneel="(optional)", hand_hint="With your finger or mouse.", hand_vak="Signature box", wis="Clear",
            akkoord="I agree to this quote and the general terms and conditions it contains. I am authorised to confirm this on behalf of my organisation.",
            knop="Sign the quote", bezig="One moment…", noot="As proof of your agreement, I keep your name, job title, email, the time and your IP address.",
            fout="Sending failed. Please try again or email elias@opperdash.be.",
            noscript="Turn on JavaScript to sign your quote, or confirm by email to elias@opperdash.be.",
            klaar_h="Signed, thank you!", klaar_p="I received your approval on {tijd}. I will send the signed quote and the event plan to {email}.",
            klaar_p2="I will send you the deposit invoice shortly.", terug="Go to the home page", locale="en-GB"),
 "fr": dict(titel="Signer votre devis | Opperdash", desc="Signez votre devis Opperdash en ligne.", h1="Signer votre devis",
            p="Vérifiez votre devis, cochez votre accord et indiquez votre nom. Je vous envoie ensuite le devis signé et le déroulé par e-mail.",
            offerte="Devis", klant="Pour", event="Événement", bedrag="Total hors TVA", pdf="Voir le devis (PDF)",
            ev_kop="L’événement", datum="Date", uur="Heure", locatie="Lieu", personen="Invités", formule="Formule", personen_tekst="env. {n} personnes",
            leeg="Ce lien ne contient pas de devis. Utilisez le lien de votre devis ou écrivez à elias@opperdash.be.", naam="Prénom et nom", functie="Fonction", mail="Votre e-mail", mail_hint="J’envoie le devis signé à cette adresse.",
            hand="Signez ici", optioneel="(facultatif)", hand_hint="Avec le doigt ou la souris.", hand_vak="Zone de signature", wis="Effacer",
            akkoord="J’accepte ce devis et les conditions générales qu’il contient. Je suis habilité(e) à le confirmer au nom de mon organisation.",
            knop="Signer le devis", bezig="Un instant…", noot="Comme preuve de votre accord, je conserve votre nom, votre fonction, votre e-mail, l’heure et votre adresse IP.",
            fout="L’envoi n’a pas abouti. Réessayez ou écrivez à elias@opperdash.be.",
            noscript="Activez JavaScript pour signer votre devis, ou confirmez par e-mail à elias@opperdash.be.",
            klaar_h="Signé, merci !", klaar_p="J’ai bien reçu votre accord le {tijd}. Je vous envoie le devis signé et le déroulé à {email}.",
            klaar_p2="Je vous envoie prochainement la facture d’acompte.", terug="Retour à l’accueil", locale="fr-BE"),
}
for L in TALEN:
    t = TEKENEN[L]
    js = json.dumps({k: t[k] for k in ("knop", "bezig", "klaar_p", "locale", "ev_kop", "personen_tekst")}, ensure_ascii=False)
    samenvatting = "".join(f'<div data-rij="{k}"><dt>{t[k]}</dt><dd data-veld="{k}"></dd></div>' for k in ("offerte", "klant", "bedrag"))
    eventdetails = "".join(f'<div data-rij="{k}"><dt>{t[k]}</dt><dd data-veld="{k}"></dd></div>' for k in ("datum", "uur", "locatie", "personen", "formule"))
    pagina("tekenen", L, t["titel"], t["desc"], f'''
<section class="sectie sectie--zwart">
  <div class="container midden">
    <h1>{t["h1"]}</h1>
    <p>{t["p"]}</p>
  </div>
</section>
<section class="sectie">
  <div class="container teken">
    <noscript><p class="teken__fout">{t["noscript"]}</p></noscript>
    <p class="teken__fout midden" id="teken-leeg" hidden>{t["leeg"]}</p>
    <div class="teken__overzicht" id="teken-overzicht" hidden>
      <dl class="teken__offerte">{samenvatting}</dl>
      <section class="teken__event" id="teken-event" aria-labelledby="teken-event-kop">
        <p class="teken__eventlabel" id="teken-event-label">{t["ev_kop"]}</p>
        <h2 class="teken__eventnaam" id="teken-event-kop" data-veld="event">{t["ev_kop"]}</h2>
        <dl class="teken__details">{eventdetails}</dl>
      </section>
      <p class="teken__pdf" data-rij="pdf"><a data-veld="pdf" href="#" target="_blank" rel="noopener">{t["pdf"]}</a></p>
    </div>
    <form class="formulier" id="teken-formulier" name="offerte-tekenen" method="POST" action="{url("bedankt", L)}" data-netlify="true" netlify-honeypot="bot-field">
      <input type="hidden" name="form-name" value="offerte-tekenen">
      <input type="hidden" name="taal" value="{L.upper()}">
      <input type="hidden" name="offertenummer">
      <input type="hidden" name="klant">
      <input type="hidden" name="bedrag">
      <input type="hidden" name="event">
      <input type="hidden" name="datum">
      <input type="hidden" name="uur">
      <input type="hidden" name="locatie">
      <input type="hidden" name="personen">
      <input type="hidden" name="formule">
      <input type="hidden" name="pdf">
      <input type="hidden" name="pagina">
      <input type="hidden" name="handtekening">
      <p class="verborgen"><label>{C[L]["niet_invullen"]} <input name="bot-field" tabindex="-1" autocomplete="off"></label></p>
      {veld("naam", t["naam"], verplicht=True, auto="name")}
      {veld("functie", t["functie"], verplicht=True, auto="organization-title")}
      <div class="vol"><label for="email">{t["mail"]} <span class="verplicht" aria-hidden="true">*</span></label><input id="email" name="email" type="email" required autocomplete="email"><p class="teken__hint">{t["mail_hint"]}</p></div>
      <div class="vol">
        <span class="label" id="hand-label">{t["hand"]} <span class="teken__optioneel">{t["optioneel"]}</span></span>
        <div class="teken__vlak"><canvas id="teken-canvas" role="img" aria-label="{t["hand_vak"]}"></canvas><button type="button" class="teken__wis" id="teken-wis">{t["wis"]}</button></div>
        <p class="teken__hint">{t["hand_hint"]}</p>
      </div>
      <div class="vol teken__akkoord"><label><input type="checkbox" name="akkoord" value="{t["akkoord"]}" required><span>{t["akkoord"]}</span></label></div>
      <p class="vol teken__fout" id="teken-fout" role="alert" hidden>{t["fout"]}</p>
      <div class="vol midden">
        <button class="knop knop--vol" type="submit">{t["knop"]}</button>
        <p class="teken__hint">{t["noot"]}</p>
      </div>
    </form>
    <div class="teken__klaar midden" id="teken-klaar" hidden>
      <h2 tabindex="-1">{t["klaar_h"]}</h2>
      <p id="teken-klaar-tekst"></p>
      <p>{t["klaar_p2"]}</p>
      <a class="knop knop--vol" href="{url("home", L)}">{t["terug"]}</a>
    </div>
    <script type="application/json" id="teken-tekst">{js}</script>
  </div>
</section>
<script src="/assets/js/offerte-tekenen.js?v={versie("assets/js/offerte-tekenen.js")}" defer></script>''', index=False, ogalt=t["titel"].split(" | ")[0] + " | Opperdash")

# Interne hulppagina voor Elias: maakt de tekenlink voor een offerte. Alleen NL, niet gelinkt, noindex.
pagina("offerte_link", "nl", "Tekenlink maken | Opperdash", "Interne hulppagina.", f'''
<section class="sectie sectie--zwart">
  <div class="container midden">
    <h1>Tekenlink maken</h1>
    <p>Vul de gegevens van de offerte in en kopieer de link. Alle velden met een * zijn nodig, zodat de klant ziet wat hij tekent. Schrijf event, uur, locatie en formule in de taal van de klant. Normaal maakt de draaiboekskill deze link automatisch; deze pagina is de handmatige terugval. Plak de link in de meetingchat.</p>
  </div>
</section>
<section class="sectie">
  <div class="container teken">
    <form class="formulier" id="link-maker" data-paden='{json.dumps({T.upper(): url("tekenen", T) for T in TALEN})}'>
      {veld("lm_klant", "Klant (bedrijf)", verplicht=True, ph="bv. Asmodee")}
      {veld("lm_bedrag", "Totaal excl. btw", verplicht=True, ph="bv. 4.250,00")}
      {veld("lm_event", "Naam van het event", verplicht=True, ph="bv. Personeelsfeest")}
      {veld("lm_datum", "Datum", "date", verplicht=True)}
      {veld("lm_uur", "Uur", verplicht=True, ph="bv. 12u tot 14u")}
      {veld("lm_locatie", "Locatie", verplicht=True, ph="bv. kantoor, Mechelen")}
      {veld("lm_personen", "Aantal personen", "number", verplicht=True, ph="bv. 60")}
      {veld("lm_formule", "Formule", verplicht=True, ph="bv. Licht buffet")}
      {veld("lm_pdf", "Link naar de pdf (niet verplicht)", "url", ph="bv. https://www.canva.com/...")}
      <div><label for="lm_taal">Taal van de klant</label><select id="lm_taal"><option value="NL">Nederlands</option><option value="EN">Engels</option><option value="FR">Frans</option></select></div>
      <div class="vol"><label for="lm_uit">Tekenlink</label><input id="lm_uit" readonly placeholder="Vul eerst alle velden met een * in"></div>
      <div class="vol midden knoppen knoppen--midden">
        <button class="knop knop--vol" type="button" id="lm_kopieer">Kopieer link</button>
        <a class="knop" id="lm_open" href="#">Open als klant</a>
      </div>
    </form>
  </div>
</section>
<script src="/assets/js/offerte-tekenen.js?v={versie("assets/js/offerte-tekenen.js")}" defer></script>''', index=False, ogalt="Opperdash")

# ============================================================ CASES
# Nieuwe case na een event: voeg bovenaan CASES_LIJST een blok toe in NL, EN en FR.
# publiceren=False: de case verschijnt alleen in de conceptpreview (python -I bouw.py --concept),
# nooit op de echte site. Zet pas op True na akkoord van Elias.
# formule: "truck" of "cat" (bepaalt de knop onderaan). Beelden staan in public/assets/img/.
CASES_LIJST = []
ZICHTBARE_CASES = [c for c in CASES_LIJST if c["publiceren"] or CONCEPT]
for c in ZICHTBARE_CASES:
    PAD["case_" + c["id"]] = {L: PAD["cases"][L] + c[L]["slug"] for L in TALEN}

# Korte cases: alleen een kaart op de cases-pagina (foto, bedrijf, wat we serveerden), zonder eigen pagina.
# Nieuwste eerst. nb verschijnt alleen in de conceptpreview, als extra uitleg in de conceptband.
KORTE_CASES = [
 dict(id="asmodee", publiceren=True, nb="", beeld=("case-asmodee.webp", 1200, 800),
      nl=dict(naam="Asmodee", meta="Foodtruck · Kortenberg · ± 160 gasten", alt="De rode foodtruck van Opperdash ’s avonds bij Asmodee, met twee koks aan het werk",
              tekst="Voor de showroomavond serveerde ik citroen-tijm kippendij of curryseitan met kruidige bulgur, geroosterde pompoen, champignonduxelles, rodekoolsalade en za’atar-yoghurt."),
      en=dict(naam="Asmodee", meta="Food truck · Kortenberg · ± 160 guests", alt="The red Opperdash food truck in the evening at Asmodee, with two cooks at work",
              tekst="For their showroom evening I served lemon-thyme chicken thigh or curried seitan with herby bulgur, roasted pumpkin, mushroom duxelles, red cabbage salad and za’atar yoghurt."),
      fr=dict(naam="Asmodee", meta="Food truck · Kortenberg · ± 160 invités", alt="Le food truck rouge d’Opperdash en soirée chez Asmodee, avec deux cuisiniers au travail",
              tekst="Pour leur soirée showroom, j’ai servi de la cuisse de poulet citron-thym ou du seitan au curry, avec boulgour aux herbes, potiron rôti, duxelles de champignons, salade de chou rouge et yaourt au za’atar.")),
 dict(id="xandres", publiceren=True, nb="", beeld=("case-xandres.webp", 1200, 800),
      nl=dict(naam="Xandres", meta="Foodtruck · Destelbergen · ± 50 gasten", alt="Elias en een collega van Opperdash aan de ontvangstbalie van Xandres",
              tekst="Voor het jubilarisfeest serveerde ik lemon-pepper chicken en curryseitan, met huisbereide limonades en pinda-chocotaart. Bijna 50 medewerkers aten binnen 30 minuten en gingen daarna terug aan het werk."),
      en=dict(naam="Xandres", meta="Food truck · Destelbergen · ± 50 guests", alt="Elias and an Opperdash colleague at the Xandres reception desk",
              tekst="For their anniversary celebration I served lemon-pepper chicken and curried seitan, with homemade lemonades and peanut chocolate tart. Almost 50 employees ate within 30 minutes and went straight back to work."),
      fr=dict(naam="Xandres", meta="Food truck · Destelbergen · ± 50 invités", alt="Elias et un collègue d’Opperdash à l’accueil de Xandres",
              tekst="Pour la fête des jubilaires, j’ai servi du poulet citron-poivre et du seitan au curry, avec des limonades maison et une tarte chocolat cacahuète. Près de 50 collaborateurs ont mangé en 30 minutes avant de reprendre le travail.")),
 dict(id="kul", publiceren=True, nb="", beeld=("case-kul.webp", 1200, 800),
      nl=dict(naam="KU Leuven", meta="Foodtruck · Leuven · 26 gasten", alt="Pulled beef met spitskool-appelslaw en lente-ui in een witte keramische kom",
              tekst="Een bedankmoment voor de collega’s na het academiejaar. Twee amuses, pulled beef met spitskool-appelslaw of gegrilde perzik met burrata, en daarna rosé chateaubriand of curryseitan met parelcouscous en ratatouille. Met huisgemaakte limonades en pinda-chocotaart."),
      en=dict(naam="KU Leuven", meta="Food truck · Leuven · 26 guests", alt="Pulled beef with pointed cabbage and apple slaw and spring onion in a white ceramic bowl",
              tekst="A thank-you to colleagues at the end of the academic year. Two amuse-bouches, pulled beef with pointed cabbage and apple slaw or grilled peach with burrata, then pink chateaubriand or curried seitan with pearl couscous and ratatouille. With homemade lemonades and peanut chocolate tart."),
      fr=dict(naam="KU Leuven", meta="Food truck · Louvain · 26 invités", alt="Effiloché de bœuf, salade de chou pointu et pomme et oignon nouveau dans un bol en céramique blanche",
              tekst="Un moment pour remercier les collègues à la fin de l’année académique. Deux amuse-bouches, effiloché de bœuf avec une salade de chou pointu et pomme ou pêche grillée et burrata, puis chateaubriand rosé ou seitan au curry avec couscous perlé et ratatouille. Avec des limonades maison et une tarte chocolat cacahuète.")),
 dict(id="3p", publiceren=True, nb="", beeld=("case-3p.webp", 1200, 800),
      nl=dict(naam="3P", meta="Foodtruck · ± 40 gasten", alt="Elias werkt een gerecht af in de foodtruck van Opperdash",
              tekst="Lunch voor het hele team: kip met citroen en peper of seitancurry, met kruidige bulgur, gegrilde courgette, kerstomaten met rodewijnazijn, een yoghurt-komkommersalade en een licht pittige hummusdressing."),
      en=dict(naam="3P", meta="Food truck · ± 40 guests", alt="Elias finishing a dish in the Opperdash food truck",
              tekst="Lunch for the whole team: lemon-pepper chicken or seitan curry, with spiced bulgur, grilled courgette, cherry tomatoes with red wine vinegar, a yoghurt and cucumber salad and a lightly spicy hummus dressing."),
      fr=dict(naam="3P", meta="Food truck · ± 40 invités", alt="Elias termine un plat dans le food truck Opperdash",
              tekst="Un lunch pour toute l’équipe : poulet citron-poivre ou curry de seitan, avec boulgour épicé, courgette grillée, tomates cerises au vinaigre de vin rouge, une salade yaourt-concombre et une sauce houmous légèrement relevée.")),
 dict(id="couleur-cafe", publiceren=True, nb="", beeld=("case-couleur-cafe.webp", 1200, 800),
      nl=dict(naam="Couleur Café", meta="Foodtruck · Festival · Brussel", alt="De tent van Opperdash met gasten",
              tekst="Een festivalweekend aan het Atomium in Brussel. Kippendij of seitancurry met krieltjes, zoete aardappel, komkommer, radijs, feta en hummus. Zonder rundvlees en zonder ingevlogen producten."),
      en=dict(naam="Couleur Café", meta="Food truck · Festival · Brussels", alt="The Opperdash tent with guests",
              tekst="A festival weekend at the Atomium in Brussels. Chicken thigh or seitan curry with baby potatoes, sweet potato, cucumber, radish, feta and hummus. No beef and no air-freighted produce."),
      fr=dict(naam="Couleur Café", meta="Food truck · Festival · Bruxelles", alt="La tente Opperdash avec des invités",
              tekst="Un week-end de festival à l’Atomium, à Bruxelles. Cuisse de poulet ou curry de seitan avec pommes grenaille, patate douce, concombre, radis, feta et houmous. Sans bœuf et sans produits importés par avion.")),
 dict(id="veritas", publiceren=True, nb="", beeld=("case-veritas.webp", 962, 641),
      nl=dict(naam="Veritas", meta="Foodtruck · Kontich · ± 100 gasten", alt="Elias aan de toonbank van de foodtruck van Opperdash",
              tekst="Lunch voor zo’n 100 medewerkers, in twee shifts. Kippendij of seitancurry met zoete aardappel, krieltjes, boontjes, rode biet, feta en hummus."),
      en=dict(naam="Veritas", meta="Food truck · Kontich · ± 100 guests", alt="Elias at the counter of the Opperdash food truck",
              tekst="Lunch for around 100 employees, in two sittings. Chicken thigh or seitan curry with sweet potato, baby potatoes, green beans, beetroot, feta and hummus."),
      fr=dict(naam="Veritas", meta="Food truck · Kontich · ± 100 invités", alt="Elias au comptoir du food truck Opperdash",
              tekst="Un lunch pour une centaine de collaborateurs, en deux services. Cuisse de poulet ou curry de seitan avec patate douce, pommes grenaille, haricots verts, betterave, feta et houmous.")),
]
# Conceptcases en interne notities staan in concepten.py naast dit script. Dat bestand staat NIET in git
# (de repo is openbaar) en wordt alleen lokaal ingeladen; zonder dat bestand bouwt de site gewoon zonder concepten.
_CONCEPT_BESTAND = os.path.join(os.path.dirname(os.path.abspath(__file__)), "concepten.py")
if os.path.exists(_CONCEPT_BESTAND):
    import runpy as _runpy
    _c = _runpy.run_path(_CONCEPT_BESTAND)
    CASES_LIJST = _c.get("CASES_LIJST", []) + CASES_LIJST
    KORTE_CASES = KORTE_CASES + _c.get("KORTE_CASES", [])
    for _k in KORTE_CASES:
        _k["nb"] = _c.get("NOTITIES", {}).get(_k["id"], _k.get("nb", ""))
ZICHTBARE_KORT = [k for k in KORTE_CASES if k["publiceren"] or CONCEPT]
ZICHTBARE_CASES = [c for c in CASES_LIJST if c["publiceren"] or CONCEPT]

# ============================================================ HOME (wegschrijven)
# Staat hier, na de cases, zodat de homepage de drie nieuwste gepubliceerde korte cases kan tonen.
HOME_CASES = {"nl": "Voor wie ik kookte", "en": "Who I cooked for", "fr": "Pour qui j’ai cuisiné"}
for L in TALEN:
    t = HOME[L]
    vert = f'<figcaption class="citaat__noot">{t["vertaald"]}</figcaption>' if t["vertaald"] else ""
    home_cases = "".join(f'''
      <article class="kookte__item">
        <a class="kookte__beeld" href="{url("cases", L)}" tabindex="-1" aria-hidden="true">{img(k["beeld"][0], k[L]["alt"], k["beeld"][1], k["beeld"][2], sizes="(max-width: 800px) 100vw, 33vw")}</a>
        <h3><a href="{url("cases", L)}">{k[L]["naam"]}</a></h3>
        <p>{k[L]["meta"]}</p>
      </article>''' for k in [k for k in KORTE_CASES if k["publiceren"]][:3])
    pagina("home", L, t["titel"], t["desc"], f'''
<section class="hero hero--home">
  {img("home-elias-tuin.webp", t["alt_tuin"], 1280, 853, lazy=False)}
  <div class="container hero__tekst">
    <h1 class="visueel-verborgen">{t["h1"]}</h1>
    <p class="hero__kop">{t["k1"]}</p>
    <div class="knoppen">
      <a class="knop knop--groen knop--klein" href="{url("foodtruck", L)}">{t["b_truck"]}</a>
      <a class="knop knop--accent knop--klein" href="{url("catering", L)}">{t["b_cat"]}</a>
    </div>
  </div>
</section>

<section class="sectie sectie--linnen">
  <div class="container kopblok">
    <h2 class="kop-groot">{t["k_seizoen"]}</h2>
    <div class="kopblok__tekst">{"".join(f"<p>{p}</p>" for p in t["p1"])}</div>
  </div>
</section>

<section class="sectie sectie--split">
  <div class="duo">
    <div class="duo__beeld">{img("catering-capaciteit.webp", t["alt_visie"], 962, 641)}</div>
    <div class="duo__tekst">
      <h2>{t["k2"]}</h2>
      {"".join(f"<p>{p}</p>" for p in t["p2"])}
    </div>
  </div>
</section>


<section class="sectie sectie--eco">
  <div class="container">
    <h2 class="kop-groot">{t["k3"]}</h2>
    <figure class="citaat citaat--groot">
      {img("testimonial-3e.webp", "Stef Goossens, CEO 3E", 480, 480)}
      <div>
        <blockquote>“{t["quote"]}”</blockquote>
        <figcaption><span class="citaat__naam">Stef Goossens</span><span class="citaat__functie">{t["functie"]} <a href="https://www.linkedin.com/company/3e/" target="_blank" rel="noopener">3E</a></span>{vert}</figcaption>
      </div>
    </figure>
  </div>
</section>

{keuze_blok(L, "sectie sectie--linnen")}

<section class="sectie">
  <div class="container">
    <h2 class="kop-groot">{HOME_CASES[L]}</h2>
    <div class="kookte">{home_cases}</div>
    <div class="knoppen cases-knop"><a class="knop" href="{url("cases", L)}">{AANPAK[L]["c_knop"]}</a></div>
  </div>
</section>
''', ogbeeld="og-home.jpg", ogalt=t["alt_hero"], schema=[org(L), {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Opperdash",
                      "inLanguage": ["nl-BE", "en", "fr-BE"], "publisher": {"@id": ORG_ID}}])

for c in ZICHTBARE_CASES:
    PAD["case_" + c["id"]] = {L: PAD["cases"][L] + c[L]["slug"] for L in TALEN}

CASES = {
 "nl": dict(titel="Cases: catering en foodtruck op bedrijfsevents | Opperdash",
            desc="Bekijk enkele events die Opperdash verzorgde: personeelsfeesten, teamevents en bedrijfslunches met foodtruck of buffet. Wat ik serveerde en hoe ik het aanpakte.",
            leeg_desc="Binnenkort toon ik hier events die Opperdash verzorgde voor bedrijven en privéfeesten.",
            crumb="Cases", h1="Cases", alt_hero="Bruschetta met tomaat en basilicum op een bord, tussen gasten aan tafel",
            intro="Een kijk achter de schermen van enkele events die ik verzorgde: voor wie ik kookte, wat er op het bord kwam en hoe ik het aanpakte.",
            leeg="Deze pagina komt binnenkort. Hier toon ik straks events die ik verzorgde voor bedrijven en privéfeesten.",
            p2="Benieuwd wat ik voor jouw event kan doen?", b1="Catering", b2="Contact",
            meer="Lees de case", terug="Alle cases", k_vraag="De vraag", k_menu="Wat ik serveerde", k_aanpak="Hoe ik het aanpakte",
            cta="Ook zo’n event in gedachten?", gasten="gasten", truck="Foodtruck", cat="Catering",
            concept="Concept: niet gepubliceerd. Gegevens tussen [ ] nog te bevestigen."),
 "en": dict(titel="Cases: catering and food truck at company events | Opperdash",
            desc="See some of the events Opperdash catered: staff parties, team events and company lunches with the food truck or a buffet. What I served and how I did it.",
            leeg_desc="Coming soon: events Opperdash catered for companies and private parties.",
            crumb="Cases", h1="Cases", alt_hero="Bruschetta with tomato and basil on a plate, between guests at a table",
            intro="A look behind the scenes of some of the events I catered: who I cooked for, what ended up on the plate and how I approached it.",
            leeg="This page is coming soon. Here I will show events I catered for companies and private parties.",
            p2="Curious what I can do for your event?", b1="Catering", b2="Contact",
            meer="Read the case", terug="All cases", k_vraag="The brief", k_menu="What I served", k_aanpak="How I did it",
            cta="Planning an event like this?", gasten="guests", truck="Food truck", cat="Catering",
            concept="Draft: not published. Details in [ ] still to be confirmed."),
 "fr": dict(titel="Références : traiteur et food truck en entreprise | Opperdash",
            desc="Découvrez quelques événements servis par Opperdash : fêtes du personnel, événements d’équipe et lunchs d’entreprise, en food truck ou en buffet.",
            leeg_desc="Bientôt : les événements qu’Opperdash a servis pour des entreprises et des fêtes privées.",
            crumb="Références", h1="Références", alt_hero="Bruschetta à la tomate et au basilic sur une assiette, entre des convives à table",
            intro="Les coulisses de quelques événements que j’ai servis : pour qui j’ai cuisiné, ce qui s’est retrouvé dans l’assiette et comment je m’y suis pris.",
            leeg="Cette page arrive bientôt. Vous y découvrirez les événements que j’ai servis pour des entreprises et des fêtes privées.",
            p2="Envie de savoir ce que je peux faire pour votre événement ?", b1="Traiteur", b2="Contact",
            meer="Lire la référence", terug="Toutes les références", k_vraag="La demande", k_menu="Ce que j’ai servi", k_aanpak="Mon approche",
            cta="Un événement de ce type en tête ?", gasten="invités", truck="Food truck", cat="Traiteur",
            concept="Brouillon : non publié. Les éléments entre [ ] restent à confirmer."),
}
PIJL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
PIJL_TERUG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M19 12H5M11 6l-6 6 6 6"/></svg>'


def case_meta(c, L):
    t = CASES[L]
    gasten = dict(c[L]["feiten"]).get({"nl": "Gasten", "en": "Guests", "fr": "Invités"}[L], "")
    return f'{t["truck"] if c["formule"] == "truck" else t["cat"]} · {gasten} {t["gasten"]}'


def concept_band(c, L):
    return "" if c["publiceren"] else f'<p class="concept-band">{" ".join(filter(None, [CASES[L]["concept"], c.get("nb")]))}</p>'


for L in TALEN:
    t = CASES[L]
    if not ZICHTBARE_CASES and not ZICHTBARE_KORT:
        pagina("cases", L, t["titel"], t["leeg_desc"], f'''
<section class="sectie sectie--zwart sectie--vol">
  <div class="container midden">
    <h1>{t["h1"]}</h1>
    <p>{t["leeg"]}</p>
    <p>{t["p2"]}</p>
    <div class="knoppen knoppen--midden">
      <a class="knop knop--vol" href="{url("catering", L)}">{t["b1"]}</a>
      <a class="knop" href="{url("contact", L)}">{t["b2"]}</a>
    </div>
  </div>
</section>''', index=False)
        continue

    kaarten = "".join(f'''
      <article class="case-kaart">
        <div class="case-kaart__beeld">{img(c["beeld"][0], c[L]["alt"], c["beeld"][1], c["beeld"][2], sizes="(max-width: 800px) 100vw, 50vw")}</div>
        <div class="case-kaart__tekst">
          {concept_band(c, L)}<p class="case-kaart__meta">{case_meta(c, L)}</p>
          <h2 class="case-kaart__titel"><a class="case-kaart__link" href="{url("case_" + c["id"], L)}">{c[L]["titel"]}</a></h2>
          <p>{c[L]["kaart"]}</p>
          <span class="case-kaart__meer" aria-hidden="true">{t["meer"]} {PIJL}</span>
        </div>
      </article>''' for c in ZICHTBARE_CASES)
    kort = "".join(f'''
      <article class="case-kaart case-kaart--kort">
        <div class="case-kaart__beeld">{img(k["beeld"][0], k[L]["alt"], k["beeld"][1], k["beeld"][2], sizes="(max-width: 800px) 100vw, 50vw")}</div>
        <div class="case-kaart__tekst">
          {concept_band(k, L)}<p class="case-kaart__meta">{k[L]["meta"]}</p>
          <h2 class="case-kaart__titel">{k[L]["naam"]}</h2>
          <p>{k[L]["tekst"]}</p>
        </div>
      </article>''' for k in ZICHTBARE_KORT)
    pagina("cases", L, t["titel"], t["desc"], f'''
<section class="hero">
  {img("cases-hero.webp", t["alt_hero"], 1920, 1280, lazy=False)}
  <div class="container"><div class="hero__tekst">
    <h1>{t["h1"]}</h1>
    <p>{t["intro"]}</p>
  </div></div>
</section>
<section class="sectie">
  <div class="container cases-raster">{kort}{kaarten}
  </div>
</section>
<section class="sectie sectie--groen">
  <div class="container cta">
    <h2>{t["cta"]}</h2>
    <div class="knoppen cta__knoppen">
      <a class="knop knop--linnen" href="{url("off_cat", L)}">{C[L]["boek_cat"]}</a>
      <a class="knop" href="{url("off_truck", L)}">{C[L]["boek_truck"]}</a>
    </div>
  </div>
</section>''', hero="cases-hero.webp", index=not CONCEPT or any(c["publiceren"] for c in CASES_LIJST + KORTE_CASES),
           schema=[breadcrumbs("cases", L, t["crumb"]),
                   {"@type": "ItemList", "itemListElement": [
                       {"@type": "ListItem", "position": i, "url": SITE + url("case_" + c["id"], L), "name": c[L]["titel"]}
                       for i, c in enumerate(ZICHTBARE_CASES, 1)]}])

    for c in ZICHTBARE_CASES:
        d = c[L]
        page = "case_" + c["id"]
        feiten = "".join(f"<div><dt>{a}</dt><dd>{b}</dd></div>" for a, b in d["feiten"])
        menu = "".join(f"<li>{m}</li>" for m in d["menu"])
        knop = (f'<a class="knop knop--linnen" href="{url("off_truck", L)}">{C[L]["boek_truck"]}</a>' if c["formule"] == "truck"
                else f'<a class="knop knop--linnen" href="{url("off_cat", L)}">{C[L]["boek_cat"]}</a>')
        quote = (f'''
<section class="sectie">
  <div class="container">
    <figure class="citaat">
      <blockquote>“{d["quote"]}”</blockquote>
      <figcaption class="citaat__naam">{d["quote_wie"]}</figcaption>
    </figure>
  </div>
</section>''' if d.get("quote") else "")
        pagina(page, L, d["seo"], d["desc"], f'''
<section class="hero case-hero">
  {img(c["beeld"][0], d["alt"], c["beeld"][1], c["beeld"][2], lazy=False)}
  <div class="container case-hero__terug"><a class="terug" href="{url("cases", L)}" data-terug>{PIJL_TERUG} {t["terug"]}</a></div>
  <div class="container"><div class="hero__tekst">
    {concept_band(c, L)}<p class="case-hero__meta">{case_meta(c, L)}</p>
    <h1 class="case-hero__titel">{d["titel"]}</h1>
    <p>{d["kaart"]}</p>
  </div></div>
</section>

<section class="feiten">
  <div class="container"><dl class="feiten__lijst">{feiten}</dl></div>
</section>

<section class="sectie sectie--split">
  <div class="duo">
    <div class="duo__tekst">
      <h2>{t["k_vraag"]}</h2>
      {"".join(f"<p>{p}</p>" for p in d["vraag"])}
    </div>
    <div class="duo__beeld duo__beeld--hoog">{img(c["beeld2"][0], d["alt2"], c["beeld2"][1], c["beeld2"][2])}</div>
  </div>
</section>

<section class="sectie">
  <div class="container case-blokken">
    <div class="praktisch__blok">
      <h2 class="kop-klein">{t["k_menu"]}</h2>
      <ul class="case-menu">{menu}</ul>
    </div>
    <div class="praktisch__blok">
      <h2 class="kop-klein">{t["k_aanpak"]}</h2>
      {"".join(f"<p>{p}</p>" for p in d["aanpak"])}
    </div>
  </div>
</section>
{quote}
<section class="sectie sectie--groen">
  <div class="container cta">
    <h2>{t["cta"]}</h2>
    <div class="knoppen cta__knoppen">{knop}<a class="knop" href="{url("cases", L)}" data-terug>{t["terug"]}</a></div>
  </div>
</section>''', index=c["publiceren"], hero=c["beeld"][0], ogalt=d["alt"],
               schema=[{"@type": "BreadcrumbList", "itemListElement": [
                           {"@type": "ListItem", "position": 1, "name": C[L]["home"], "item": SITE + url("home", L)},
                           {"@type": "ListItem", "position": 2, "name": t["crumb"], "item": SITE + url("cases", L)},
                           {"@type": "ListItem", "position": 3, "name": d["titel"], "item": SITE + url(page, L)}]},
                       {"@type": "Article", "headline": d["titel"], "description": d["desc"], "inLanguage": HTML_LANG[L],
                        "image": SITE + "/assets/img/" + c["beeld"][0], "datePublished": c["datum"],
                        "author": {"@id": ORG_ID}, "publisher": {"@id": ORG_ID}, "mainEntityOfPage": SITE + url(page, L)}])

# ============================================================ VEELGESTELDE VRAGEN
# Alleen feiten die in Context/Product.md en Context/brand.md bevestigd zijn.
FAQ = {
 "nl": dict(titel="Veelgestelde vragen over catering en foodtruck | Opperdash",
    desc="Antwoorden op wat klanten mij vaak vragen: formules, allergieën, wat ik meebreng, wat ik nodig heb op locatie, de offerte en de betaling.",
    crumb="Veelgestelde vragen", h1="Meest gestelde vragen",
    intro="Hier vind je antwoorden op wat klanten mij vaak vragen. Staat je vraag er niet bij? Neem gerust contact op.",
    groepen=[
     ("Het aanbod", [
      ("Wat biedt Opperdash aan?", ["Ik kook voedzame culinaire gerechten met mediterrane invloeden. Je kiest uit vier formules:",
       [("Foodtruck:", "hoofdgerechten, efficiënt geserveerd vanuit de truck."),
        ("Buffet:", "gerechten mooi gepresenteerd in schalen, waar je gasten zelf van nemen."),
        ("Catering aan tafel:", "een menu van meerdere gangen, aan tafel geserveerd."),
        ("Walking dinner:", "meerdere kleine gerechten die je gasten staand eten.")],
       "Elke formule kan je aanvullen met hapjes, desserts en dranken."]),
      ("Wat is het verschil tussen de foodtruck en een buffet?", "Bij de foodtruck dresseer ik ieder bord ter plaatse en serveer ik vanuit de truck. Bij een buffet presenteer ik de gerechten in mooie serveerschalen en nemen je gasten zelf."),
      ("Kan je in de keuken op onze locatie koken?", "Ja. Voor catering aan tafel en een walking dinner kook ik ter plaatse. Daarvoor raad ik een volledig uitgeruste keuken aan, met oven, kookvuur, voldoende koelruimte en werkruimte. Is er geen keuken op je locatie? Dan denk ik graag mee en bekijken we samen wat mogelijk is."),
      ("Voor wie kook je?", "Voor bedrijven, teamevents, personeelsfeesten en privéfeesten."),
     ]),
     ("Het eten", [
      ("Wat maakt je gerechten anders?", "Op veel events kies je tussen burgers, frieten en pizza, of een lichte salade. Ik kook wat daartussen ontbreekt: gerechten met intense, diepe smaken die ook voedzaam zijn."),
      ("Verandert het menu?", "Ja, mijn menu volgt het seizoen. Producten kies ik op smaak, herkomst en seizoen."),
      ("Zijn er vegetarische of vegan gerechten?", "Ja. Ik bereid zowel vegetarische als niet-vegetarische gerechten, en vegan is mogelijk. Geef je wensen mee bij je aanvraag."),
      ("Hou je rekening met allergieën?", "Ja. Geef allergieën uiterlijk vijf werkdagen voor het event door, samen met het definitieve aantal gasten. Dan hou ik er in de bereiding rekening mee."),
      ("Kan het ook met vis in plaats van vlees?", "Ja, vis is mogelijk in plaats van vlees, tegen een meerprijs."),
      ("Kan je ook dranken voorzien?", "Ja. Ik kan huisgemaakte limonade, mocktails en plat of bruisend water voorzien."),
     ]),
     ("Praktisch", [
      ("Wat breng je mee?", "Keramisch servies en echt bestek. Tafels en stoelen kan ik in de offerte opnemen, en zaalpersoneel kan op aanvraag."),
      ("Wat heb je nodig op locatie?", [[
       ("Foodtruck:", "een standplaats van 3 bij 3 meter en twee normale stopcontacten op een apart circuit."),
       ("Buffet:", "tafels en één normaal stopcontact."),
       ("Catering aan tafel of walking dinner:", "ik raad een volledig uitgeruste keuken aan. Is die er niet, dan denk ik graag mee.")]]),
      ("Waar ben je actief?", "Ik kook vanuit Leuven en kom naar je locatie, overal in België. De verplaatsing reken ik per kilometer, heen en terug."),
     ]),
     ("Offerte en betaling", [
      ("Hoe vraag ik een offerte aan?", "Via het offerteformulier voor catering of foodtruck, per mail of telefonisch. Ik bekijk je wensen en stel de offerte samen met jou op."),
      ("Wat staat er in een offerte?", "De prijs per persoon voor de gekozen gerechten, een vaste opstartkost en de verplaatsing. Alle prijzen zijn exclusief btw."),
      ("Hoe werkt de betaling?", "Bij bevestiging betaal je een voorschot van 20% van de totaalfactuur, met een minimum van € 500. Het voorschot betaal je uiterlijk vijf werkdagen voor het event."),
      ("Tot wanneer kan ik het aantal gasten aanpassen?", "Het definitieve aantal gasten geef je uiterlijk vijf werkdagen voor het event door."),
     ]),
    ], slot="Nog een vraag?", b1="Neem contact op", b2="Vraag offerte aan"),
 "en": dict(titel="Frequently asked questions about the catering | Opperdash",
    desc="Answers to what clients often ask me: formats, allergies, what I bring, what I need on site, the quote and payment.",
    crumb="FAQ", h1="Frequently asked questions",
    intro="Here you will find answers to what clients often ask me. Can’t find your question? Feel free to get in touch.",
    groepen=[
     ("What I offer", [
      ("What does Opperdash offer?", ["I cook nourishing culinary dishes with Mediterranean influences. You choose from four formats:",
       [("Food truck:", "main courses, served efficiently from the truck."),
        ("Buffet:", "dishes beautifully presented in serving dishes, where your guests help themselves."),
        ("Seated catering:", "a menu of several courses, served at the table."),
        ("Walking dinner:", "several small dishes that your guests eat standing up.")],
       "Every format can be extended with appetisers, desserts and drinks."]),
      ("What is the difference between the food truck and a buffet?", "With the food truck I plate every dish on site and serve from the truck. With a buffet I present the dishes in beautiful serving dishes and your guests help themselves."),
      ("Can you cook in the kitchen at our venue?", "Yes. For seated catering and walking dinners I cook on site. I recommend a fully equipped kitchen, with an oven, hob, enough cold storage and work space. No kitchen at your venue? I am happy to think along and look at what is possible together."),
      ("Who do you cook for?", "For companies, team events, staff parties and private parties."),
     ]),
     ("The food", [
      ("What makes your dishes different?", "At many events you choose between burgers, fries and pizza, or a light salad. I cook what is missing in between: dishes with intense, deep flavours that are also nourishing."),
      ("Does the menu change?", "Yes, my menu follows the seasons. I choose produce for taste, origin and season."),
      ("Do you have vegetarian or vegan dishes?", "Yes. I prepare both vegetarian and non-vegetarian dishes, and vegan is possible. Let me know your wishes in your request."),
      ("Do you take allergies into account?", "Yes. Let me know about allergies at least five working days before the event, together with the final number of guests, and I will take them into account."),
      ("Can you serve fish instead of meat?", "Yes, fish is possible instead of meat, at an extra cost."),
      ("Can you provide drinks?", "Yes. I can provide homemade lemonade, mocktails and still or sparkling water."),
     ]),
     ("Practical", [
      ("What do you bring?", "Ceramic tableware and real cutlery. Tables and chairs can be included in the quote, and serving staff is available on request."),
      ("What do you need on site?", [[
       ("Food truck:", "a 3 by 3 metre pitch and two standard power sockets on a separate circuit."),
       ("Buffet:", "tables and one standard power socket."),
       ("Seated catering or walking dinner:", "I recommend a fully equipped kitchen. If there is none, I am happy to think along.")]]),
      ("Where do you work?", "I cook from Leuven and come to your venue, anywhere in Belgium. Travel is charged per kilometre, there and back."),
     ]),
     ("Quote and payment", [
      ("How do I request a quote?", "Use the quote form for catering or the food truck, or contact me by email or phone. I look at your wishes and put the quote together with you."),
      ("What is in a quote?", "The price per person for the chosen dishes, a fixed start-up fee and travel. All prices exclude VAT."),
      ("How does payment work?", "On confirmation you pay a deposit of 20% of the total invoice, with a minimum of €500. The deposit is due no later than five working days before the event."),
      ("Until when can I change the number of guests?", "Please confirm the final number of guests no later than five working days before the event."),
     ]),
    ], slot="Another question?", b1="Get in touch", b2="Request a quote"),
 "fr": dict(titel="Questions fréquentes sur le service traiteur | Opperdash",
    desc="Les réponses à ce que mes clients demandent souvent : formules, allergies, ce que j’apporte, ce qu’il faut sur place, le devis et le paiement.",
    crumb="Questions fréquentes", h1="Questions fréquentes",
    intro="Vous trouverez ici les réponses aux questions que mes clients posent souvent. Votre question n’y figure pas ? N’hésitez pas à me contacter.",
    groepen=[
     ("L’offre", [
      ("Que propose Opperdash ?", ["Je cuisine des plats culinaires et nourrissants aux influences méditerranéennes. Vous choisissez parmi quatre formules :",
       [("Food truck :", "des plats principaux, servis efficacement depuis le truck."),
        ("Buffet :", "des mets joliment présentés dans des plats de service, où vos invités se servent eux-mêmes."),
        ("Service à table :", "un menu de plusieurs services, servi à table."),
        ("Walking dinner :", "plusieurs petits plats que vos invités mangent debout.")],
       "Chaque formule peut être complétée de bouchées, de desserts et de boissons."]),
      ("Quelle différence entre le food truck et un buffet ?", "Avec le food truck, je dresse chaque assiette sur place et je sers depuis le truck. Avec un buffet, je présente les mets dans de beaux plats de service et vos invités se servent eux-mêmes."),
      ("Pouvez-vous cuisiner dans la cuisine de notre lieu ?", "Oui. Pour le service à table et le walking dinner, je cuisine sur place. Je recommande une cuisine entièrement équipée, avec four, feux de cuisson, assez d’espace frigorifique et de plan de travail. Pas de cuisine sur votre lieu ? Je réfléchis volontiers avec vous à ce qui est possible."),
      ("Pour qui cuisinez-vous ?", "Pour les entreprises, les événements d’équipe, les fêtes du personnel et les fêtes privées."),
     ]),
     ("La cuisine", [
      ("Qu’est-ce qui rend vos plats différents ?", "Lors de nombreux événements, on choisit entre burgers, frites et pizza, ou une salade légère. Je cuisine ce qui manque entre les deux : des plats aux saveurs intenses et profondes, qui sont aussi nourrissants."),
      ("Le menu change-t-il ?", "Oui, mon menu suit les saisons. Je choisis mes produits pour leur goût, leur origine et leur saison."),
      ("Proposez-vous des plats végétariens ou végans ?", "Oui. Je prépare des plats végétariens comme non végétariens, et le végan est possible. Indiquez vos souhaits dans votre demande."),
      ("Tenez-vous compte des allergies ?", "Oui. Communiquez-moi les allergies au plus tard cinq jours ouvrables avant l’événement, avec le nombre définitif d’invités, et j’en tiens compte en cuisine."),
      ("Est-ce possible avec du poisson plutôt que de la viande ?", "Oui, le poisson est possible à la place de la viande, avec un supplément."),
      ("Pouvez-vous fournir des boissons ?", "Oui. Je peux prévoir de la limonade maison, des mocktails et de l’eau plate ou pétillante."),
     ]),
     ("Infos pratiques", [
      ("Qu’apportez-vous ?", "La vaisselle en céramique et de vrais couverts. Tables et chaises peuvent être incluses dans le devis, et du personnel de salle est possible sur demande."),
      ("De quoi avez-vous besoin sur place ?", [[
       ("Food truck :", "un emplacement de 3 mètres sur 3 et deux prises électriques standard sur un circuit séparé."),
       ("Buffet :", "des tables et une prise électrique standard."),
       ("Service à table ou walking dinner :", "je recommande une cuisine entièrement équipée. S’il n’y en a pas, je réfléchis volontiers avec vous.")]]),
      ("Où travaillez-vous ?", "Je cuisine depuis Louvain et viens jusqu’à vous, partout en Belgique. Le déplacement est facturé au kilomètre, aller et retour."),
     ]),
     ("Devis et paiement", [
      ("Comment demander un devis ?", "Via le formulaire de devis pour le traiteur ou le food truck, par e-mail ou par téléphone. J’étudie vos souhaits et j’établis le devis avec vous."),
      ("Que contient un devis ?", "Le prix par personne pour les plats choisis, des frais de démarrage fixes et le déplacement. Tous les prix s’entendent hors TVA."),
      ("Comment se passe le paiement ?", "À la confirmation, vous payez un acompte de 20 % de la facture totale, avec un minimum de 500 €. L’acompte est à régler au plus tard cinq jours ouvrables avant l’événement."),
      ("Jusqu’à quand puis-je modifier le nombre d’invités ?", "Communiquez le nombre définitif d’invités au plus tard cinq jours ouvrables avant l’événement."),
     ]),
    ], slot="Une autre question ?", b1="Contactez-moi", b2="Demander un devis"),
}
for L in TALEN:
    t = FAQ[L]
    alle = [vr for _, vragen in t["groepen"] for vr in vragen]
    anker = lambda g: "".join(c if c.isalnum() else "-" for c in g.lower()).strip("-")
    blokken = "".join(f'<h2 class="faq__groep" id="{anker(g)}">{g}</h2>{faq_html(vragen)}' for g, vragen in t["groepen"])
    groepen_nav = "".join(f'<a href="#{anker(g)}">{g}</a>' for g, _ in t["groepen"])
    pagina("faq", L, t["titel"], t["desc"], f'''
<section class="sectie sectie--linnen faq-sectie">
  <div class="container">
    <div class="offerte__kop">
      <h1>{t["h1"]}</h1>
      <p>{t["intro"]}</p>
    </div>
    <div class="faq-raster">
      <nav class="faq-nav" aria-label="{t["h1"]}">{groepen_nav}</nav>
      <div class="faq-pagina">
        {blokken}
      </div>
    </div>
  </div>
</section>
<section class="slotband">
  <div class="container slotband__binnen">
    <h2>{t["slot"]}</h2>
    <div class="knoppen">
      <a class="knop knop--groen" href="{url("contact", L)}">{t["b1"]}</a>
      <a class="knop" href="{url("off_cat", L)}">{t["b2"]}</a>
    </div>
  </div>
</section>''', schema=[breadcrumbs("faq", L, t["crumb"]), faq_schema(alle)])

# ============================================================ SITEMAP
INDEX_PAGES = ["home", "catering", "foodtruck", "aanpak", "verhaal", "faq", "contact", "off_cat", "off_truck"]
if any(c["publiceren"] for c in CASES_LIJST + KORTE_CASES):
    INDEX_PAGES += ["cases"] +["case_" + c["id"] for c in CASES_LIJST if c["publiceren"]]
prio = {"home": "1.0", "catering": "0.9", "foodtruck": "0.9", "cases": "0.7"}

# Oude losse cases-pagina's (vóór de cases-map van 20 oktober 2026) opruimen, anders botsen ze met cases/.
for oud in ["cases.html", "en/cases.html", "fr/references.html"]:
    if os.path.exists(os.path.join(OUT, oud)):
        os.remove(os.path.join(OUT, oud))
with open(os.path.join(OUT, "sitemap.xml"), "w", encoding="utf-8", newline="\n") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n')
    for p in INDEX_PAGES:
        for L in TALEN:
            alts = "".join(f'\n    <xhtml:link rel="alternate" hreflang="{HTML_LANG[T]}" href="{SITE}{url(p, T)}"/>' for T in TALEN)
            alts += f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{url(p, "nl")}"/>'
            f.write(f"  <url>\n    <loc>{SITE}{url(p, L)}</loc>{alts}\n    <lastmod>{DATUM}</lastmod>\n    <priority>{prio.get(p, '0.6')}</priority>\n  </url>\n")
    f.write("</urlset>\n")
print("klaar: pagina's en sitemap geschreven naar", OUT)
