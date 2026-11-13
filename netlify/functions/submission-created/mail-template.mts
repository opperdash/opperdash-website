// Opmaak van de formuliermails in de Opperdash-huisstijl.
// Wordt gebruikt door submission-created.mts en door het voorbeeldscript.

type Velden = Record<string, string>

type FormulierConfig = {
  titel: string
  intro: string
  kern: string[]        // velden die bovenaan als blokjes verschijnen
  details: string[]     // velden in de gegevenstabel
  bericht: string       // veld met de vrije tekst
  onderwerp: (d: Velden) => string
}

const LABELS: Record<string, string> = {
  naam: "Naam",
  email: "E-mail",
  telefoon: "Telefoon",
  bedrijf: "Bedrijf",
  onderwerp: "Onderwerp",
  vraag: "Vraag",
  datum: "Datum event",
  locatie: "Locatie",
  aantal_personen: "Aantal personen",
  naam_event: "Naam event",
  uitleg: "Uitleg",
}

const TALEN: Record<string, string> = { NL: "Nederlands", EN: "Engels", FR: "Frans" }

const FORMULIEREN: Record<string, FormulierConfig> = {
  "offerte-catering": {
    titel: "Nieuwe offerteaanvraag catering",
    intro: "Er kwam een offerteaanvraag voor catering binnen via opperdash.be.",
    kern: ["datum", "aantal_personen", "locatie"],
    details: ["naam", "bedrijf", "email", "telefoon", "naam_event"],
    bericht: "uitleg",
    onderwerp: (d) => ["Offerte catering", d.naam_event || d.naam, d.aantal_personen && `${d.aantal_personen} pers.`, d.datum && datumKort(d.datum)].filter(Boolean).join(" · "),
  },
  "offerte-foodtruck": {
    titel: "Nieuwe aanvraag foodtruck",
    intro: "Er kwam een aanvraag voor de foodtruck binnen via opperdash.be.",
    kern: ["datum", "aantal_personen", "locatie"],
    details: ["naam", "bedrijf", "email", "telefoon", "naam_event"],
    bericht: "uitleg",
    onderwerp: (d) => ["Foodtruck", d.naam_event || d.naam, d.aantal_personen && `${d.aantal_personen} pers.`, d.datum && datumKort(d.datum)].filter(Boolean).join(" · "),
  },
  contact: {
    titel: "Nieuw bericht via de website",
    intro: "Er kwam een bericht binnen via het contactformulier op opperdash.be.",
    kern: [],
    details: ["naam", "bedrijf", "email", "telefoon", "onderwerp"],
    bericht: "vraag",
    onderwerp: (d) => ["Nieuw bericht", d.onderwerp, d.naam].filter(Boolean).join(" · "),
  },
}

// Palet van 12/11/2026 (Context/brand.md): vooral wit en zwart, kleur alleen in kleine details
const KLEUR = {
  zwart: "#100E0A",   // Offblack: koppen, kop van de mail
  wit: "#FFFFFF",
  linnen: "#F4F3E8",  // Soft linen: achtergrond, blokjes, berichtvak
  zand: "#E6DDC8",    // Warm sand: taalnoot
  ecogroen: "#DBE5D7",// Eco-green: voet
  pine: "#154C40",    // Pine teal: knop, berichtlijn
  tennis: "#EBFE72",  // Tennis ball: tekst op de pine teal-knop
  tekst: "#100E0A",
  grijs: "#5E5B55",
  lijn: "#E2E0DA",
  stippel: "#C8C5BD",
}
const KOP = "'Teko','Arial Narrow','Helvetica Neue',Arial,sans-serif"
const TEKST = "'Lato','Helvetica Neue',Arial,sans-serif"

function esc(s: string): string {
  return String(s ?? "")
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;").replace(/'/g, "&#39;")
}

function datumLang(iso: string): string {
  const d = new Date(`${iso}T12:00:00`)
  if (Number.isNaN(d.getTime())) return iso
  return new Intl.DateTimeFormat("nl-BE", { weekday: "long", day: "numeric", month: "long", year: "numeric" }).format(d)
}

function datumKort(iso: string): string {
  const d = new Date(`${iso}T12:00:00`)
  if (Number.isNaN(d.getTime())) return iso
  return new Intl.DateTimeFormat("nl-BE", { day: "numeric", month: "short", year: "numeric" }).format(d)
}

function tijdstip(iso: string): string {
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return ""
  return new Intl.DateTimeFormat("nl-BE", { dateStyle: "full", timeStyle: "short", timeZone: "Europe/Brussels" }).format(d)
}

function waarde(veld: string, v: string): string {
  if (!v) return `<span style="color:${KLEUR.grijs};">niet ingevuld</span>`
  if (veld === "email") return `<a href="mailto:${esc(v)}" style="color:${KLEUR.zwart};font-weight:700;">${esc(v)}</a>`
  if (veld === "telefoon") return `<a href="tel:${esc(v.replace(/[^\d+]/g, ""))}" style="color:${KLEUR.zwart};font-weight:700;">${esc(v)}</a>`
  if (veld === "datum") return esc(datumLang(v))
  return esc(v)
}

function knop(href: string, label: string, achtergrond: string, kleur: string): string {
  return `<td style="padding:0 8px 8px 0;"><a href="${esc(href)}" style="display:inline-block;background:${achtergrond};color:${kleur};font-family:${KOP};font-size:20px;line-height:1;letter-spacing:.5px;text-transform:uppercase;text-decoration:none;padding:13px 22px 10px;border-radius:8px;">${label}</a></td>`
}

export type Bijlage = { filename: string; path: string; cid: string }
export type Mail = { onderwerp: string; html: string; tekst: string; antwoordAan?: string; aan?: string; bijlagen?: Bijlage[] }

export function maakMail(formulier: string, data: Velden, aangemaakt: string, id: string): Mail {
  const cfg = FORMULIEREN[formulier] ?? {
    titel: `Nieuwe inzending: ${formulier}`, intro: "Er kwam een formulier binnen via opperdash.be.",
    kern: [], details: Object.keys(LABELS).filter((k) => k in data), bericht: "", onderwerp: () => `Nieuwe inzending ${formulier}`,
  }
  const d: Velden = {}
  for (const [k, v] of Object.entries(data ?? {})) d[k] = typeof v === "string" ? v.trim() : String(v ?? "")

  const taal = (d.taal || "NL").toUpperCase()
  const voornaam = (d.naam || "").split(" ")[0] || "de klant"
  const onderwerp = cfg.onderwerp(d) + (taal !== "NL" ? ` [${taal}]` : "")

  const kernBlokken = cfg.kern.length
    ? `<tr><td style="padding:4px 32px 8px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>${cfg.kern
        .map((k) => `<td width="${Math.floor(100 / cfg.kern.length)}%" valign="top" style="padding:0 4px;"><div style="background:${KLEUR.linnen};border-radius:10px;padding:14px 12px;text-align:center;">
          <div style="font-family:${TEKST};font-size:12px;color:${KLEUR.zwart};text-transform:uppercase;letter-spacing:.8px;font-weight:700;">${LABELS[k]}</div>
          <div style="font-family:${KOP};font-size:24px;line-height:1.1;color:${KLEUR.zwart};font-weight:600;margin-top:4px;">${d[k] ? esc(k === "datum" ? datumKort(d[k]) : d[k]) : "–"}</div>
        </div></td>`).join("")}</tr></table></td></tr>`
    : ""

  const rijen = cfg.details
    .map((k) => `<tr>
        <td valign="top" style="padding:11px 0;border-bottom:1px solid ${KLEUR.lijn};font-family:${TEKST};font-size:14px;color:${KLEUR.grijs};width:38%;">${LABELS[k] ?? esc(k)}</td>
        <td valign="top" style="padding:11px 0;border-bottom:1px solid ${KLEUR.lijn};font-family:${TEKST};font-size:16px;color:${KLEUR.tekst};">${waarde(k, d[k])}</td>
      </tr>`).join("")

  const bericht = cfg.bericht && d[cfg.bericht]
    ? `<tr><td style="padding:8px 32px 4px;">
        <div style="font-family:${KOP};font-size:22px;color:${KLEUR.zwart};text-transform:uppercase;font-weight:600;margin:0 0 8px;">${LABELS[cfg.bericht]}</div>
        <div style="background:${KLEUR.linnen};border-left:4px solid ${KLEUR.pine};border-radius:6px;padding:16px 18px;font-family:${TEKST};font-size:16px;line-height:1.55;color:${KLEUR.tekst};">${esc(d[cfg.bericht]).replace(/\r?\n/g, "<br>")}</div>
      </td></tr>`
    : ""

  const knoppen: string[] = []
  if (d.email) knoppen.push(knop(`mailto:${d.email}?subject=${encodeURIComponent("Re: " + onderwerp)}`, `Antwoord ${esc(voornaam)}`, KLEUR.pine, KLEUR.tennis))
  if (d.telefoon) knoppen.push(knop(`tel:${d.telefoon.replace(/[^\d+]/g, "")}`, "Bel", KLEUR.zwart, KLEUR.wit))

  const taalNoot = taal !== "NL"
    ? `<tr><td style="padding:0 32px 8px;"><div style="background:${KLEUR.zand};border-radius:8px;padding:10px 14px;font-family:${TEKST};font-size:14px;color:${KLEUR.tekst};">Deze aanvraag kwam via de <strong>${TALEN[taal] ?? taal}e</strong> website. Antwoord bij voorkeur in het ${TALEN[taal] ?? taal}.</div></td></tr>`
    : ""

  const html = `<!doctype html>
<html lang="nl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light only"><title>${esc(onderwerp)}</title>
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Teko:wght@500;600&display=swap" rel="stylesheet">
</head>
<body style="margin:0;padding:0;background:${KLEUR.linnen};">
<div style="display:none;max-height:0;overflow:hidden;">${esc(cfg.intro)}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:${KLEUR.linnen};"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;background:${KLEUR.wit};border-radius:16px;overflow:hidden;">
  <tr><td align="center" style="background:${KLEUR.zwart};padding:26px 24px 22px;">
    <img src="https://www.opperdash.be/assets/img/email-logo-wit.png" width="180" height="37" alt="Opperdash" style="display:block;border:0;">
  </td></tr>
    <tr><td style="padding:28px 32px 6px;">
    <div style="font-family:${KOP};font-size:34px;line-height:1;color:${KLEUR.zwart};text-transform:uppercase;font-weight:600;">${esc(cfg.titel)}</div>
    <p style="font-family:${TEKST};font-size:15px;color:${KLEUR.grijs};margin:10px 0 14px;">${esc(cfg.intro)}</p>
  </td></tr>
  ${taalNoot}
  ${kernBlokken}
  <tr><td style="padding:10px 32px 18px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0">${rijen}</table></td></tr>
  ${bericht}
  <tr><td style="padding:20px 32px 26px;"><table role="presentation" cellpadding="0" cellspacing="0"><tr>${knoppen.join("")}</tr></table></td></tr>
  <tr><td style="background:${KLEUR.ecogroen};padding:16px 32px;font-family:${TEKST};font-size:12px;line-height:1.6;color:${KLEUR.zwart};">
    Ontvangen ${esc(tijdstip(aangemaakt))} · formulier <strong>${esc(formulier)}</strong> · taal ${esc(taal)}<br>
    Antwoorden op deze mail gaan rechtstreeks naar ${d.email ? esc(d.email) : "de afzender"}. <a href="https://app.netlify.com/projects/opperdash/forms" style="color:${KLEUR.zwart};">Alle aanvragen in Netlify</a>${id ? ` · ref. ${esc(id.slice(-6))}` : ""}
  </td></tr>
</table>
</td></tr></table>
</body></html>`

  const tekst = [
    cfg.titel.toUpperCase(), "", cfg.intro, taal !== "NL" ? `Taal: ${TALEN[taal] ?? taal}` : "", "",
    ...cfg.kern.concat(cfg.details).map((k) => `${LABELS[k] ?? k}: ${k === "datum" && d[k] ? datumLang(d[k]) : d[k] || "niet ingevuld"}`),
    "", cfg.bericht ? `${LABELS[cfg.bericht]}:\n${d[cfg.bericht] || ""}` : "",
    "", `Ontvangen ${tijdstip(aangemaakt)}`,
  ].filter((r) => r !== undefined).join("\n")

  return { onderwerp, html, tekst, antwoordAan: d.email || undefined }
}

// ============================================================ OFFERTE TEKENEN
// Formulier "offerte-tekenen": alleen een mail voor Elias met het bewijs (tijdstip, IP, toestel, handtekening).
// De klant krijgt de getekende offerte via de na-meetingmail; de taallabels hieronder dienen voor de eventgegevens.

type TekenTaal = {
  locale: string; wat: (nr: string, event: string) => string; onderwerp: (w: string) => string; titel: string; groet: (v: string) => string
  intro: (w: string) => string; volgende: string; slot: string; pdf: string
  labels: Record<"offerte" | "klant" | "event" | "datum" | "uur" | "locatie" | "personen" | "formule" | "bedrag" | "naam" | "tijd" | "akkoord" | "handtekening", string>
}

const TEKEN: Record<string, TekenTaal> = {
  NL: {
    locale: "nl-BE", wat: (nr, ev) => nr ? `offerte ${nr}` : ev ? `de offerte voor ${ev}` : "de offerte", onderwerp: (w) => `Kopie: je akkoord op ${w}`, titel: "Offerte getekend", groet: (v) => `Dag ${v},`,
    intro: (w) => `Bedankt. Ik heb je akkoord op ${w} goed ontvangen. Hieronder vind je wat je bevestigd hebt.`,
    volgende: "Ik stuur je binnenkort de voorschotfactuur. Heb je nog een vraag? Antwoord gewoon op deze mail.", slot: "Tot snel,", pdf: "Bekijk de offerte",
    labels: { offerte: "Offerte", klant: "Voor", event: "Event", datum: "Datum", uur: "Uur", locatie: "Locatie", personen: "Aantal personen", formule: "Formule", bedrag: "Totaal excl. btw", naam: "Getekend door", tijd: "Getekend op", akkoord: "Akkoord", handtekening: "Handtekening" },
  },
  EN: {
    locale: "en-GB", wat: (nr, ev) => nr ? `quote ${nr}` : ev ? `the quote for ${ev}` : "the quote", onderwerp: (w) => `Copy: your approval of ${w}`, titel: "Quote signed", groet: (v) => `Hi ${v},`,
    intro: (w) => `Thank you. I have received your approval of ${w}. Below is what you confirmed.`,
    volgende: "I will send you the deposit invoice shortly. Any questions? Just reply to this email.", slot: "See you soon,", pdf: "View the quote",
    labels: { offerte: "Quote", klant: "For", event: "Event", datum: "Date", uur: "Time", locatie: "Location", personen: "Guests", formule: "Format", bedrag: "Total excl. VAT", naam: "Signed by", tijd: "Signed on", akkoord: "Agreement", handtekening: "Signature" },
  },
  FR: {
    locale: "fr-BE", wat: (nr, ev) => nr ? `devis ${nr}` : ev ? `le devis pour ${ev}` : "le devis", onderwerp: (w) => `Copie : votre accord sur ${w}`, titel: "Devis signé", groet: (v) => `Bonjour ${v},`,
    intro: (w) => `Merci. J’ai bien reçu votre accord sur ${w}. Vous trouverez ci-dessous ce que vous avez confirmé.`,
    volgende: "Je vous envoie prochainement la facture d’acompte. Une question ? Répondez simplement à cet e-mail.", slot: "À bientôt,", pdf: "Voir le devis",
    labels: { offerte: "Devis", klant: "Pour", event: "Événement", datum: "Date", uur: "Heure", locatie: "Lieu", personen: "Invités", formule: "Formule", bedrag: "Total hors TVA", naam: "Signé par", tijd: "Signé le", akkoord: "Accord", handtekening: "Signature" },
  },
}

const HANDTEKENING_CID = "handtekening@opperdash.be"
// Eventgegevens uit de tekenlink, zoals de klant ze op de pagina zag
const EVENTVELDEN = ["datum", "uur", "locatie", "personen", "formule"] as const

function tijdstipTaal(iso: string, locale: string, seconden = false): string {
  const d = new Date(iso)
  if (Number.isNaN(d.getTime())) return iso
  return new Intl.DateTimeFormat(locale, { dateStyle: "full", timeStyle: seconden ? "medium" : "short", timeZone: "Europe/Brussels" }).format(d)
}

function rij(label: string, inhoud: string): string {
  return `<tr>
        <td valign="top" style="padding:11px 0;border-bottom:1px solid ${KLEUR.lijn};font-family:${TEKST};font-size:14px;color:${KLEUR.grijs};width:38%;">${esc(label)}</td>
        <td valign="top" style="padding:11px 0;border-bottom:1px solid ${KLEUR.lijn};font-family:${TEKST};font-size:16px;color:${KLEUR.tekst};">${inhoud}</td>
      </tr>`
}

function blokjes(items: [string, string][]): string {
  return `<tr><td style="padding:4px 32px 8px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0"><tr>${items
    .map(([l, v]) => `<td width="${Math.floor(100 / items.length)}%" valign="top" style="padding:0 4px;"><div style="background:${KLEUR.linnen};border-radius:10px;padding:14px 12px;text-align:center;">
          <div style="font-family:${TEKST};font-size:12px;color:${KLEUR.zwart};text-transform:uppercase;letter-spacing:.8px;font-weight:700;">${esc(l)}</div>
          <div style="font-family:${KOP};font-size:24px;line-height:1.1;color:${KLEUR.zwart};font-weight:600;margin-top:4px;">${v ? esc(v) : "–"}</div>
        </div></td>`).join("")}</tr></table></td></tr>`
}

function omhulsel(lang: string, onderwerp: string, voorvertoning: string, inhoud: string, voet: string): string {
  return `<!doctype html>
<html lang="${lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light only"><title>${esc(onderwerp)}</title>
<link href="https://fonts.googleapis.com/css2?family=Lato:wght@400;700&family=Teko:wght@500;600&display=swap" rel="stylesheet">
</head>
<body style="margin:0;padding:0;background:${KLEUR.linnen};">
<div style="display:none;max-height:0;overflow:hidden;">${esc(voorvertoning)}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:${KLEUR.linnen};"><tr><td align="center" style="padding:24px 12px;">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:600px;background:${KLEUR.wit};border-radius:16px;overflow:hidden;">
  <tr><td align="center" style="background:${KLEUR.zwart};padding:26px 24px 22px;">
    <img src="https://www.opperdash.be/assets/img/email-logo-wit.png" width="180" height="37" alt="Opperdash" style="display:block;border:0;">
  </td></tr>
    ${inhoud}
  <tr><td style="background:${KLEUR.ecogroen};padding:16px 32px;font-family:${TEKST};font-size:12px;line-height:1.6;color:${KLEUR.zwart};">${voet}</td></tr>
</table>
</td></tr></table>
</body></html>`
}

function handtekeningBlok(label: string, aanwezig: boolean, leeg: string): string {
  const inhoud = aanwezig
    ? `<img src="cid:${HANDTEKENING_CID}" width="300" alt="${esc(label)}" style="display:inline-block;max-width:100%;height:auto;border:0;">`
    : esc(leeg)
  return `<tr><td style="padding:8px 32px 4px;">
        <div style="font-family:${KOP};font-size:22px;color:${KLEUR.zwart};text-transform:uppercase;font-weight:600;margin:0 0 8px;">${esc(label)}</div>
        <div style="background:${KLEUR.wit};border:1px dashed ${KLEUR.stippel};border-radius:8px;padding:10px;text-align:center;font-family:${TEKST};font-size:14px;color:${KLEUR.grijs};">${inhoud}</div>
      </td></tr>`
}

// handtekeningUrl: privélink naar de png in Netlify Blobs; meeting-verwerken zet daarmee de akkoordpagina achteraan het draaiboek
export type TekenMeta = { ip: string; toestel: string; handtekeningUrl?: string }

export function maakTekenMails(data: Velden, aangemaakt: string, id: string, meta: TekenMeta): { intern: Mail } {
  const d: Velden = {}
  for (const [k, v] of Object.entries(data ?? {})) d[k] = typeof v === "string" ? v.trim() : String(v ?? "")
  const taal = TEKEN[(d.taal || "NL").toUpperCase()] ? (d.taal || "NL").toUpperCase() : "NL"
  // Offertenummer is niet verplicht: zonder nummer herkennen we de offerte aan event en klant
  const nr = d.offertenummer || ""
  const bestand = (nr || d.klant || "offerte").replace(/[^A-Za-z0-9-]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 40) || "offerte"
  const voornaam = (d.naam || "").split(" ")[0]
  const pdf = /^https:\/\//i.test(d.pdf) ? d.pdf : ""
  // De handtekening gaat als bijlage (cid) mee: Gmail toont geen data:-beelden in de mail zelf.
  const png = /^data:image\/png;base64,[A-Za-z0-9+/=]+$/.test(d.handtekening) && d.handtekening.length < 400000 ? d.handtekening : ""
  const bijlagen: Bijlage[] = png ? [{ filename: `handtekening-${bestand}.png`, path: png, cid: HANDTEKENING_CID }] : []
  const link = (href: string, tekst: string) => `<a href="${esc(href)}" style="color:${KLEUR.zwart};font-weight:700;">${esc(tekst)}</a>`

  // Mail voor Elias
  const onderwerp = ["Offerte getekend", nr, d.klant, d.event, d.bedrag].filter(Boolean).join(" · ") + (taal !== "NL" ? ` [${taal}]` : "")
  const intro = `${d.naam || "De klant"}${d.functie ? ` (${d.functie})` : ""} tekende ${TEKEN.NL.wat(nr, d.event)}${d.klant ? ` (${d.klant})` : ""} via opperdash.be.`
  const getekend = new Intl.DateTimeFormat("nl-BE", { day: "numeric", month: "short", year: "numeric", timeZone: "Europe/Brussels" }).format(new Date(aangemaakt))
  const rijen = [
    rij("Klant", esc(d.klant || "niet ingevuld")),
    d.event ? rij("Event", esc(d.event)) : "",
    ...EVENTVELDEN.filter((k) => d[k]).map((k) => rij(TEKEN.NL.labels[k], esc(d[k]))),
    rij("Naam", esc(d.naam)),
    rij("Functie", esc(d.functie)),
    rij("E-mail", d.email ? link(`mailto:${d.email}`, d.email) : "niet ingevuld"),
    rij("Akkoord", esc(d.akkoord || "niet aangevinkt")),
    rij("Tijdstip", esc(tijdstipTaal(aangemaakt, "nl-BE", true))),
    rij("IP-adres", esc(meta.ip || "onbekend")),
    rij("Toestel", `<span style="font-size:13px;color:${KLEUR.grijs};">${esc(meta.toestel || "onbekend")}</span>`),
    rij("Taal", esc(TALEN[taal] ?? taal)),
    pdf ? rij("Offerte", link(pdf, "pdf openen")) : "",
    meta.handtekeningUrl ? rij("Handtekening-bestand", link(meta.handtekeningUrl, "png openen")) : "",
  ].join("")
  const knoppen = d.email ? knop(`mailto:${d.email}?subject=${encodeURIComponent("Re: " + TEKEN.NL.wat(nr, d.event))}`, `Antwoord ${esc(voornaam || "klant")}`, KLEUR.pine, KLEUR.tennis) : ""
  const internHtml = omhulsel("nl", onderwerp, intro, `
  <tr><td style="padding:28px 32px 6px;">
    <div style="font-family:${KOP};font-size:34px;line-height:1;color:${KLEUR.zwart};text-transform:uppercase;font-weight:600;">Offerte getekend</div>
    <p style="font-family:${TEKST};font-size:15px;color:${KLEUR.grijs};margin:10px 0 14px;">${esc(intro)}</p>
  </td></tr>
  ${blokjes([nr ? ["Offerte", nr] : ["Klant", d.klant], ["Totaal excl. btw", d.bedrag], ["Getekend", getekend]])}
  <tr><td style="padding:10px 32px 18px;"><table role="presentation" width="100%" cellpadding="0" cellspacing="0">${rijen}</table></td></tr>
  ${handtekeningBlok("Handtekening", !!png, "Geen handtekening getekend. Naam, functie en akkoordvinkje zijn ingevuld.")}
  <tr><td style="padding:20px 32px 6px;"><table role="presentation" cellpadding="0" cellspacing="0"><tr>${knoppen}</tr></table></td></tr>
  <tr><td style="padding:0 32px 26px;font-family:${TEKST};font-size:14px;color:${KLEUR.tekst};">Volgende stap: zeg <strong>meeting klaar ${esc(voornaam || d.klant || "[naam]")}</strong>. Dan staat de na-meetingmail met de getekende offerte en het draaiboek als concept klaar${d.email ? ` voor ${esc(d.email)}` : ""}. De klant kreeg nog geen kopie. Daarna start <strong>evenement-bevestigd</strong>.</td></tr>`,
    `Ontvangen ${esc(tijdstip(aangemaakt))} · formulier <strong>offerte-tekenen</strong> · taal ${esc(taal)}<br>
    Bewaar deze mail als bewijs. De inzending staat ook in <a href="https://app.netlify.com/projects/opperdash/forms" style="color:${KLEUR.zwart};">Netlify</a>${id ? ` · ref. ${esc(id.slice(-6))}` : ""}`)
  const internTekst = [
    "OFFERTE GETEKEND", "", intro, "",
    nr ? `Offerte: ${nr}` : "", `Klant: ${d.klant || "niet ingevuld"}`, d.event ? `Event: ${d.event}` : "",
    ...EVENTVELDEN.filter((k) => d[k]).map((k) => `${TEKEN.NL.labels[k]}: ${d[k]}`), `Totaal excl. btw: ${d.bedrag || "niet in de link"}`,
    `Naam: ${d.naam}`, `Functie: ${d.functie}`, `E-mail: ${d.email}`, `Akkoord: ${d.akkoord || "niet aangevinkt"}`,
    `Tijdstip: ${tijdstipTaal(aangemaakt, "nl-BE", true)}`, `IP-adres: ${meta.ip || "onbekend"}`, `Toestel: ${meta.toestel || "onbekend"}`,
    `Handtekening: ${png ? "zie bijlage" : "niet getekend"}`, meta.handtekeningUrl ? `Handtekening-bestand: ${meta.handtekeningUrl}` : "", pdf ? `Offerte: ${pdf}` : "",
  ].filter(Boolean).join("\n")
  const intern: Mail = { onderwerp, html: internHtml, tekst: internTekst, antwoordAan: d.email || undefined, bijlagen }

  return { intern }
}
