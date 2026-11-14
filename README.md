# Opperdash-website

De website www.opperdash.be (Netlify), in NL (hoofdtaal), EN (`/en/`) en FR (`/fr/`).

## Hoe het werkt

- `bouw.py` is de enige bron voor teksten en opbouw van alle pagina's.
- `python -I bouw.py` schrijft de pagina's naar `public/`. Netlify publiceert `public/`.
- Stijl, scripts, lettertypes en beelden staan in `public/assets/`.
- Formuliermails komen uit `netlify/functions/`. Het mailwachtwoord staat als geheime variabele in Netlify, nooit in de code.

## Afspraken

- Een inhoudelijke wijziging gebeurt altijd in de drie talen.
- Werk op een aparte branch en bekijk eerst lokaal. Live gaat pas na akkoord van Elias.
- Draai na elke wijziging `python -I bouw.py` en commit `public/` mee. Netlify bouwt zelf niets: zonder bijgewerkte `public/` toont de voorbeeldlink niets nieuws.
- Open een pull request naar `main` (een draft mag ook). Pas dan maakt Netlify een voorbeeldlink, en alleen via een goedgekeurde pull request komt een wijziging op `main`.
- Kleur- en stijlregels: 90% zwart en wit, kleur alleen in kleine details (knoppen, band, kaartjes). Foto's raken elkaar nooit. Achter elke grote titel staat een punt.
- Nooit de DNS, nameservers of MX-records bij one.com wijzigen: de mail van opperdash.be loopt via one.com.

## Foto's

Alle foto's op de site hebben hetzelfde filmeffect: meer contrast, warme lichte tinten, donkerdere hoeken en korrel. Een nieuwe foto krijgt het zo, met het origineel als bron:

```bash
python foto_effect.py pad/naar/origineel.jpg case-klant.webp --breedte 1200
python -I bouw.py
```

- Het resultaat komt in `public/assets/img/`, met een gsm-versie (`-m.webp`) erbij.
- Pas het effect nooit toe op een foto die het al heeft. De foto's in `public/assets/img/` zijn al bewerkt.
- Het logo, de iconen en de deelbeelden (`og-*.jpg`) hebben het effect niet.

## Lokaal bekijken

```bash
python -I bouw.py
python -m http.server 8765 --directory public
```
