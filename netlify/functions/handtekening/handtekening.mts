// Geeft een bewaarde handtekening (png) terug voor de akkoordpagina achteraan het draaiboek.
// Alleen met de willekeurige sleutel uit Elias' bewijsmail; geen lijst, geen zoekfunctie, niet indexeerbaar.
import { getStore } from "@netlify/blobs"

const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/

export default async (req: Request): Promise<Response> => {
  const kop = { "Cache-Control": "no-store", "X-Robots-Tag": "noindex, nofollow" }
  const id = new URL(req.url).searchParams.get("id") ?? ""
  if (req.method !== "GET" || !UUID.test(id)) return new Response("Niet gevonden", { status: 404, headers: kop })
  const png = await getStore("handtekeningen").get(id, { type: "arrayBuffer" })
  if (!png) return new Response("Niet gevonden", { status: 404, headers: kop })
  return new Response(png, { headers: { ...kop, "Content-Type": "image/png" } })
}
