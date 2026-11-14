"""Filmeffect voor de foto's van de Opperdash-website.

Alle foto's op de site hebben dezelfde bewerking (voorbeeld van Elias, 14/11/2026):
1. lichte ontverzadiging en meer contrast (diepere schaduwen en middentonen);
2. warme crèmetint in de lichte tinten, per foto afgestemd op hoe warm het wit al is;
3. vignet: de hoeken zijn donkerder;
4. zwart-witkorrel.

De maten staan in foto_effect.json en zijn uitgemeten op de voorbeeldfoto.

Gebruik (vanuit de map Website, met het ORIGINEEL van de foto als bron):

    python foto_effect.py pad/naar/origineel.jpg case-klant.webp
    python foto_effect.py pad/naar/origineel.jpg case-klant.webp --breedte 1200

Het resultaat komt in public/assets/img/, samen met een gsm-versie (-m.webp, 960 px) als de foto
breder is dan 960 px. Draai daarna `python -I bouw.py`.

Belangrijk: pas het effect nooit toe op een foto die het al heeft. De foto's in public/assets/img/
zijn al bewerkt; het script weigert die als bron.
"""
import argparse, json, os, sys, zlib
import numpy as np
from PIL import Image, ImageOps

HIER = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(HIER, "public", "assets", "img")
_M = json.load(open(os.path.join(HIER, "foto_effect.json"), encoding="utf-8"))
RASTER = np.array(_M["raster"])
KROMMEN = [np.array(k) for k in _M["krommen"]]
MATRIX = np.array(_M["matrix"])                 # lichte ontverzadiging; grijs blijft grijs
VIGNET = _M["vignet"]
TOON = (KROMMEN[0] + KROMMEN[1]) / 2            # neutrale toonkromme
TINT = [np.where(TOON > 0.03, k / np.maximum(TOON, 1e-6), 1.0) for k in KROMMEN]   # warme tint per kanaal

KWALITEIT = 70            # webp-kwaliteit: houdt 94 tot 98% van de korrel en beperkt het gewicht
KORREL = 3.7 / 255        # sterkte van de korrel in de middentonen (afgesteld op het korrelvoorbeeld van Elias, 14/11/2026)
KORREL_ZACHT = 1.5        # verzachting van de korrel in px (bij 1920 px breed): hoger = grover en zachter
REF_BREEDTE = 1920        # de korrel is gemeten op een foto van 1920 px breed
WIT_VOOR, WIT_NA = 0.958, 0.854   # blauw/rood in het wit van de voorbeeldfoto, voor en na
MAX_WARM = 1.3            # heel koele foto's niet verder dan dit opwarmen
GSM_BREEDTE = 960


def warmte(img):
    """Hoe sterk de warme tint moet zijn: 1 = zoals de voorbeeldfoto, 0 = de foto is al warm genoeg."""
    p = (np.asarray(img.convert("RGB"), dtype=np.float64) / 255).reshape(-1, 3)
    lum = p @ [0.2126, 0.7152, 0.0722]
    sat = (p.max(1) - p.min(1)) / (p.max(1) + 1e-6)
    m = (lum > np.quantile(lum, 0.92)) & (sat < 0.35) & (lum > 0.45)
    if m.mean() < 0.015:      # geen duidelijk wit in de foto: neem de standaardsterkte
        return 1.0
    wit = p[m].mean(0)
    return float(np.clip((wit[2] / wit[0] - WIT_NA) / (WIT_VOOR - WIT_NA), 0, MAX_WARM))


def korrel(img, naam):
    w, h = img.size
    rng = np.random.default_rng(zlib.crc32(naam.encode()))
    # Kleinere foto's krijgen dezelfde korrel, mee verkleind: zo oogt ze op elke foto even fijn.
    wn = max(w, REF_BREEDTE); hn = round(wn * h / w)
    n = rng.standard_normal((hn, wn))
    r = max(2, int(np.ceil(3 * KORREL_ZACHT)))
    k = np.exp(-np.arange(-r, r + 1) ** 2 / (2 * KORREL_ZACHT ** 2)); k /= k.sum()   # verzachting: bepaalt hoe grof de korrel is
    n = sum(kk * np.roll(n, d, 0) for kk, d in zip(k, range(-r, r + 1)))
    n = sum(kk * np.roll(n, d, 1) for kk, d in zip(k, range(-r, r + 1)))
    n /= n.std()
    if (wn, hn) != (w, h):
        n = np.asarray(Image.fromarray(n.astype(np.float32), mode="F").resize((w, h), Image.BOX), dtype=np.float64)
    x = np.asarray(img.convert("RGB"), dtype=np.float64) / 255
    l = x @ [0.2126, 0.7152, 0.0722]
    amp = KORREL * np.sqrt(np.clip(4 * l * (1 - l), 0, 1)) * np.minimum(1, (l / 0.2) ** 0.25)
    y = np.clip(x + (n * amp)[..., None], 0, 1)
    return Image.fromarray((y * 255 + 0.5).astype(np.uint8))


def film(img, naam, s):
    """Het volledige effect op één foto. `naam` bepaalt het korrelpatroon, `s` de warmte."""
    x = np.clip((np.asarray(img.convert("RGB"), dtype=np.float64) / 255) @ MATRIX.T, 0, 1)
    y = np.stack([np.interp(x[..., c], RASTER, TOON) * np.interp(x[..., c], RASTER, TINT[c]) ** s for c in range(3)], -1)
    h, w = y.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    r2 = (((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2) / 2      # 0 in het midden, 1 in de hoek
    y = np.clip(y * (1 + VIGNET[1] * r2 + VIGNET[2] * r2 ** 2)[..., None], 0, 1)
    return korrel(Image.fromarray((y * 255 + 0.5).astype(np.uint8)), naam)


def bewaar(img, naam, s):
    pad = os.path.join(IMG_DIR, naam)
    film(img, naam, s).save(pad, "WEBP", quality=KWALITEIT, method=6)
    print(f"{naam}: {img.width} x {img.height} px, warmte {s:.2f}, {os.path.getsize(pad) // 1024} kB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Zet het Opperdash-filmeffect op een nieuwe foto.")
    ap.add_argument("bron", help="het origineel van de foto (zonder effect)")
    ap.add_argument("naam", help="bestandsnaam op de site, bv. case-klant.webp")
    ap.add_argument("--breedte", type=int, help="verklein de foto eerst tot deze breedte in px")
    a = ap.parse_args()
    if os.path.commonpath([os.path.abspath(a.bron), IMG_DIR]) == IMG_DIR:
        sys.exit("De foto's in public/assets/img/ hebben het effect al. Geef het origineel als bron.")
    if not a.naam.endswith(".webp") or a.naam.endswith("-m.webp"):
        sys.exit("Geef een naam die eindigt op .webp (en niet op -m.webp).")
    img = ImageOps.exif_transpose(Image.open(a.bron)).convert("RGB")
    if a.breedte and img.width > a.breedte:
        img = img.resize((a.breedte, round(a.breedte * img.height / img.width)), Image.LANCZOS)
    s = warmte(img)
    bewaar(img, a.naam, s)
    if img.width > GSM_BREEDTE:
        gsm = img.resize((GSM_BREEDTE, round(GSM_BREEDTE * img.height / img.width)), Image.LANCZOS)
        bewaar(gsm, a.naam.replace(".webp", "-m.webp"), s)
