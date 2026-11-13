// Draait automatisch bij elke goedgekeurde formulierinzending (Netlify-event "submission-created").
// Stuurt een gestylede mail via de one.com-mailbox van Opperdash.
// Nodig in Netlify (Project configuration > Environment variables, scope Functions):
//   ONECOM_SMTP_PASS  wachtwoord van de mailbox (geheim)
// Optioneel: ONECOM_SMTP_USER (standaard elias@opperdash.be), FORM_MAIL_TO (standaard elias@opperdash.be)
import nodemailer from "nodemailer"
import { maakMail, maakTekenMails } from "./mail-template.mts"
import { getStore } from "@netlify/blobs"

const VERBORGEN = new Set(["form-name", "subject", "bot-field", "ip", "user_agent", "referrer"])

export default async (req: Request) => {
  const { payload } = await req.json()
  const formulier: string = payload?.form_name ?? payload?.data?.["form-name"] ?? "onbekend"
  const data: Record<string, string> = {}
  for (const [k, v] of Object.entries(payload?.data ?? {})) if (!VERBORGEN.has(k)) data[k] = String(v ?? "")

  const gebruiker = Netlify.env.get("ONECOM_SMTP_USER") || "elias@opperdash.be"
  const wachtwoord = Netlify.env.get("ONECOM_SMTP_PASS")
  const ontvanger = Netlify.env.get("FORM_MAIL_TO") || "elias@opperdash.be"
  if (!wachtwoord) {
    console.warn("ONECOM_SMTP_PASS ontbreekt: gestylede formuliermail niet verstuurd.")
    return new Response("geen wachtwoord ingesteld", { status: 200 })
  }

  const aangemaakt = payload?.created_at ?? new Date().toISOString()
  const transport = nodemailer.createTransport({
    host: "send.one.com",
    port: 465,
    secure: true,
    auth: { user: gebruiker, pass: wachtwoord },
  })

  // Getekende offerte: alleen een bewijsmail voor Elias. De klant krijgt geen automatische kopie:
  // de getekende offerte en het draaiboek gaan mee in de na-meetingmail (skill meeting-verwerken).
  if (formulier === "offerte-tekenen") {
    // Handtekening privé bewaren (Netlify Blobs) zodat ze later achteraan het draaiboek kan; de link staat alleen in Elias' bewijsmail.
    let handtekeningUrl = ""
    const png = String(data.handtekening ?? "")
    if (/^data:image\/png;base64,[A-Za-z0-9+/=]+$/.test(png) && png.length < 400000) {
      try {
        const sleutel = crypto.randomUUID()
        const bytes = Uint8Array.from(Buffer.from(png.split(",")[1], "base64"))
        await getStore("handtekeningen").set(sleutel, bytes, { metadata: { klant: String(data.klant ?? ""), aangemaakt } })
        handtekeningUrl = `https://www.opperdash.be/.netlify/functions/handtekening?id=${sleutel}`
      } catch (fout) {
        console.error("Handtekening niet bewaard:", fout)
      }
    }
    const meta = { ip: String(payload?.data?.ip ?? ""), toestel: String(payload?.data?.user_agent ?? ""), handtekeningUrl }
    const { intern } = maakTekenMails(data, aangemaakt, payload?.id ?? "", meta)
    await transport.sendMail({
      from: { name: "Opperdash website", address: gebruiker },
      to: ontvanger,
      replyTo: intern.antwoordAan,
      subject: intern.onderwerp,
      html: intern.html,
      text: intern.tekst,
      attachments: intern.bijlagen,
    })
    console.log(`Offerte getekend: ${data.klant || "zonder klant"} (${payload?.id ?? "zonder id"})`)
    return new Response("ok")
  }

  const mail = maakMail(formulier, data, aangemaakt, payload?.id ?? "")
  await transport.sendMail({
    from: { name: "Opperdash website", address: gebruiker },
    to: ontvanger,
    replyTo: mail.antwoordAan,
    subject: mail.onderwerp,
    html: mail.html,
    text: mail.tekst,
  })
  console.log(`Formuliermail verstuurd: ${formulier} (${payload?.id ?? "zonder id"})`)
  return new Response("ok")
}
