# -*- coding: utf-8 -*-
"""Tarjeta 1200x630 para compartir por WhatsApp/redes: logo, nombre, datos y mosaico de trabajos."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
W, H = 1200, 630
bg = Image.new("RGB", (W, H), (28, 30, 34))
d = ImageDraw.Draw(bg)

# degradado antracita
for y in range(H):
    t = y / H
    c = (int(42 - 22 * t), int(45 - 24 * t), int(50 - 26 * t))
    d.line([(0, y), (W, y)], fill=c)

# mosaico de trabajos a la derecha (tres columnas inclinadas)
keys = ["luis-02", "guille-04", "maria-03", "paulix-10", "luis-08", "guille-08", "maria-05", "luis-03", "guille-06", "paulix-03", "luis-09", "maria-02"]
tiles = []
for k in keys:
    im = Image.open(os.path.join(root, "assets/img/ig", k + "-m.webp")).convert("RGB")
    tw = 210
    th = 280
    r = max(tw / im.width, th / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    x0, y0 = (im.width - tw) // 2, (im.height - th) // 2
    tiles.append(im.crop((x0, y0, x0 + tw, y0 + th)))
canvas = Image.new("RGB", (760, 900), (20, 21, 24))
cols = 3
for i, t in enumerate(tiles):
    c, r = i % cols, i // cols
    canvas.paste(t, (c * 226 + 10, r * 296 + 10 - (c % 2) * 90))
canvas = canvas.rotate(-7, resample=Image.BICUBIC, expand=True, fillcolor=(20, 21, 24))
bg.paste(canvas, (560, -150))

# velo para legibilidad
veil = Image.new("RGBA", (W, H), (0, 0, 0, 0))
vd = ImageDraw.Draw(veil)
for x in range(W):
    a = int(max(0, min(255, 248 - (x - 760) * 1.1))) if x > 760 else 248
    vd.line([(x, 0), (x, H)], fill=(16, 17, 19, a))
bg = Image.alpha_composite(bg.convert("RGBA"), veil).convert("RGB")
d = ImageDraw.Draw(bg)

# logo
logo = Image.open(os.path.join(root, "assets/img/logo/logo-transparent.png")).convert("RGBA").resize((300, 300), Image.LANCZOS)
disc = Image.new("RGBA", (300, 300), (0, 0, 0, 0))
ImageDraw.Draw(disc).ellipse((6, 6, 294, 294), fill=(8, 8, 9, 255))
disc = Image.alpha_composite(disc, logo)
bg.paste(disc, (70, 165), disc)

def font(names, size):
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except Exception:
            pass
    return ImageFont.load_default()

title = font(["C:/Windows/Fonts/bahnschrift.ttf", "C:/Windows/Fonts/arialbd.ttf"], 62)
sub = font(["C:/Windows/Fonts/georgiai.ttf", "C:/Windows/Fonts/timesi.ttf"], 36)
small = font(["C:/Windows/Fonts/bahnschrift.ttf", "C:/Windows/Fonts/arial.ttf"], 26)
tiny = font(["C:/Windows/Fonts/bahnschrift.ttf", "C:/Windows/Fonts/arial.ttf"], 22)
copper = (226, 156, 104)

x = 420
d.text((x, 150), "LA CARA NORTE", font=title, fill=(246, 244, 240))
d.text((x, 222), "CUSTOM TATTOO", font=title, fill=copper)
d.text((x, 305), "Tatuajes y piercing en León", font=sub, fill=(220, 222, 226))
d.line([(x, 372), (x + 90, 372)], fill=copper, width=3)
d.text((x, 392), "5,0 en Google · 120 reseñas", font=small, fill=(246, 244, 240))
d.text((x, 432), "Neotradicional · Realismo · Fine line", font=tiny, fill=(190, 194, 200))
d.text((x, 470), "C. Posadera Aldonza, 3 · León", font=tiny, fill=(190, 194, 200))
d.text((x, 504), "WhatsApp 613 07 58 89 · L–V 10–18 h", font=tiny, fill=(190, 194, 200))

# franja cobre-verde inferior
d.rectangle((0, H - 8, W, H), fill=copper)
d.rectangle((W - 260, H - 8, W, H), fill=(156, 207, 134))

bg.save(os.path.join(root, "assets/img/og-card.jpg"), "JPEG", quality=84, optimize=True)
print(os.path.getsize(os.path.join(root, "assets/img/og-card.jpg")) // 1024, "KB")
