# -*- coding: utf-8 -*-
"""Generador estático de la demo de La Cara Norte. Ejecutar:  python _build/build.py"""
import os, html, urllib.parse
from PIL import Image
from data import SITE, W, ARTISTS, ORDER, REVIEWS
from servicios import SERVICES
from estilos import STYLES


import math, json


def fern():
    """Rama de helecho en SVG (decorativa), generada por código."""
    leaves = []
    for i in range(1, 26):
        t = i / 26
        # curva de Bézier cuadrática: (20,380) -> control (40,150) -> (190,10)
        x = (1 - t) ** 2 * 20 + 2 * (1 - t) * t * 40 + t ** 2 * 190
        y = (1 - t) ** 2 * 380 + 2 * (1 - t) * t * 150 + t ** 2 * 10
        dx = 2 * (1 - t) * (40 - 20) + 2 * t * (190 - 40)
        dy = 2 * (1 - t) * (150 - 380) + 2 * t * (10 - 150)
        ang = math.degrees(math.atan2(dy, dx))
        ln = 70 * (1 - t) ** 0.7 + 10
        for side in (-1, 1):
            leaves.append(f'<ellipse cx="{ln/2:.1f}" cy="0" rx="{ln/2:.1f}" ry="{3.2 + 2.2*(1-t):.1f}" transform="translate({x:.1f} {y:.1f}) rotate({ang + side*58:.1f})"/>')
    return ('<svg class="leaf-deco %s" viewBox="0 -20 260 420" aria-hidden="true" fill="currentColor"><path d="M20 380Q40 150 190 10" fill="none" stroke="currentColor" stroke-width="3"/>' + "".join(leaves) + '</svg>')


def leaves(pos="tr"):
    return fern() % pos


SITE_URL = "https://sefiro888.github.io/lacaranortetatto/"


def jsonld():
    d = {
        "@context": "https://schema.org", "@type": "TattooParlor",
        "name": "La Cara Norte Custom Tattoo", "image": SITE_URL + "assets/img/og-card.jpg", "url": SITE_URL,
        "telephone": "+34613075889", "email": SITE["mail"],
        "address": {"@type": "PostalAddress", "streetAddress": "C. Posadera Aldonza, 3", "postalCode": "24007", "addressLocality": "León", "addressCountry": "ES"},
        "geo": {"@type": "GeoCoordinates", "latitude": 42.6092943, "longitude": -5.5674665},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "10:00", "closes": "18:00"}],
        "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "120"},
        "sameAs": [SITE["ig"], SITE["fb"]],
    }
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>'


ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
IMG = "assets/img/ig/"
_sizes = {}


def size(key):
    if key not in _sizes:
        with Image.open(os.path.join(ROOT, IMG, key + ".webp")) as im:
            _sizes[key] = im.size
    return _sizes[key]


def src(key):
    """Miniatura (960 px) para tarjetas, carruseles y muros."""
    return IMG + key + "-m.webp"


def full(key):
    """Versión completa (1920 px) para marcos grandes, cabeceras y visor."""
    return IMG + key + ".webp"


def alt(key):
    return html.escape(W[key][0], quote=True)


def img(key, cls="", lazy=True, extra="", big=False):
    w, h = size(key)
    return f'<img src="{full(key) if big else src(key)}" alt="{alt(key)}" width="{w}" height="{h}"{" loading=\"lazy\"" if lazy else ""}{(" class=\"" + cls + "\"") if cls else ""} {extra}>'


REELS = {
    "luis": {"id": "DeJxzXMOQ5G", "owner": "luis", "poster": "luis-04", "title": "Proyecto brazo finalizado", "artist": "Luis Santos", "ig": "luiss.tattoo",
             "text": "Un brazo completo con dragón y máscaras, terminado en La Cara Norte."},
    "serpiente": {"id": None, "owner": "luis", "poster": "luis-04", "title": "Serpiente japonesa", "artist": "Luis Santos", "ig": "luiss.tattoo",
                  "text": "Cuatro días seguidos de sesión: serpiente japonesa en rojo y negro, hecha en La Cara Norte."},
    "hannya": {"id": None, "owner": "luis", "poster": "luis-04", "title": "Brazo japonés", "artist": "Luis Santos", "ig": "luiss.tattoo",
               "text": "Manga japonesa en gris con máscara hannya, templo y geisha, hecha en La Cara Norte."},
    "anubis": {"id": None, "owner": "guille", "poster": "guille-07", "title": "Anubis", "artist": "Guille Martink", "ig": "guillemartink",
               "text": "Manga en black & grey con Anubis, pirámides y ojo de Horus. Un piezote de realismo hecho en La Cara Norte."},
    "lovehate": {"id": None, "owner": "guille", "poster": "guille-07", "title": "L.O.V.E and H.A.T.E", "artist": "Guille Martink", "ig": "guillemartink",
                 "text": "Proyecto de brazo en realismo: retrato, billetes y cartas en gris, hecho en La Cara Norte."},
    "guille": {"id": "DZNYtoqNHEg", "owner": "guille", "poster": "guille-07", "title": "Amortiwow", "artist": "Guille Martink", "ig": "guillemartink",
               "text": "Realismo a color: un amortiguador que parece salir de la pierna."},
}


def reel(k, tilt=""):
    r = REELS[k]
    w, h = size(r["poster"])
    poster = src(r["poster"])
    pp = f"assets/video/reel-{k}-poster.jpg"
    if os.path.exists(os.path.join(ROOT, pp)):
        poster, (w, h) = pp, (540, 960)
    vid = f"assets/video/reel-{k}.mp4"
    vattr = f' data-video="{vid}"' if os.path.exists(os.path.join(ROOT, vid)) else ""
    link = f'https://www.instagram.com/{r["ig"]}/reel/{r["id"]}/' if r["id"] else f'https://www.instagram.com/{r["ig"]}/'
    ring = "PLAY REEL · PLAY REEL · PLAY REEL · "
    return f'''<figure class="reel {tilt}" data-reel="{r["id"] or ""}"{vattr}>
  <div class="phone">
    <span class="phone-notch" aria-hidden="true"></span>
    <span class="reel-credit"><b>{r["artist"]}</b><i>@{r["ig"]}</i></span>
    <button type="button" class="reel-play" aria-label="Reproducir el reel: {r["title"]}">
      <img src="{poster}" alt="" width="{w}" height="{h}" loading="lazy">
      <span class="reel-ring" aria-hidden="true"><svg viewBox="0 0 120 120"><defs><path id="rc{k}" d="M60,60 m-46,0 a46,46 0 1,1 92,0 a46,46 0 1,1 -92,0"/></defs><text><textPath href="#rc{k}">{ring}</textPath></text></svg><i><svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg></i></span>
      <span class="reel-eq" aria-hidden="true"><b></b><b></b><b></b><b></b></span>
      <span class="reel-meta"><em><i class="rec"></i> Reel</em><strong>{r["title"]}</strong><small>@{r["ig"]}</small></span>
    </button>
  </div>
  <figcaption><strong class="reel-by">Tatuaje de <a href="{ARTISTS[r["owner"]]["slug"]}.html">{r["artist"]}</a></strong><span>{r["text"]}</span>
    <a class="link-arrow" href="{link}" target="_blank" rel="noopener">Ver en Instagram</a>
    {"" if vattr else '<small>Se abre en una ventana grande con el reproductor de Instagram (servicio de terceros).</small>'}</figcaption>
</figure>'''


def reel_section(owner, limit=None):
    a = ARTISTS[owner]
    keys = [k for k, r in REELS.items() if r["owner"] == owner][:limit]
    many = len(keys) > 1
    tilts = ["tilt-l", "tilt-r", "tilt-l"]
    phones = "".join(reel(k, tilts[i % 3] if many else "tilt-l") for i, k in enumerate(keys))
    head = f'''<p class="eyebrow">En movimiento</p><h2 class="split-words">El trabajo de {a["short"]}, <span class="serif accent">en vídeo</span></h2>
      <p class="lead">{"Reels recientes" if many else "Un reel reciente"} de su perfil de Instagram. Pulsa play y {"míralos" if many else "míralo"} sin salir de la web.</p>
      <a class="btn btn-ghost" href="https://www.instagram.com/{a["ig"]}/" target="_blank" rel="noopener">{ICON["ig"]} @{a["ig"]}</a>'''
    if many:
        return f'''
<section class="sec reel-sec grain has-leaves">
  <span class="reel-bg-text" aria-hidden="true">REEL</span>
  <div class="wrap">
    <div class="sec-head center reveal">{head}</div>
    <div class="reel-duo reel-row">{phones}</div>
  </div>
</section>'''
    return f'''
<section class="sec reel-sec grain has-leaves">
  <span class="reel-bg-text" aria-hidden="true">REEL</span>
  <div class="wrap split">
    <div class="reveal">{head}</div>
    <div class="reveal d1" style="display:flex;justify-content:center">{phones}</div>
  </div>
</section>'''


def wa(text=""):
    q = ("?text=" + urllib.parse.quote(text)) if text else ""
    return f"https://wa.me/{SITE['wa']}{q}"


# ---------- Iconos ----------
ICON = {
    "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15l-1.4 5 5.2-1.4A10 10 0 1 0 12 2zm0 1.8a8.2 8.2 0 1 1-4.2 15.3l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 0 1 12 3.8zM8.6 7.5c-.2 0-.5.1-.7.4-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.2 5 4.4 2.4 1 2.9.8 3.4.7.5 0 1.7-.7 1.9-1.4.2-.7.2-1.3.2-1.4-.1-.1-.3-.2-.6-.4l-1.9-.9c-.3-.1-.5-.1-.7.1l-.9 1.1c-.2.2-.3.2-.6.1-.3-.1-1.2-.4-2.3-1.4-.8-.8-1.4-1.700-1.600-2-.2-.3 0-.4.1-.6l.4-.5.3-.4c.1-.2 0-.3 0-.5l-.9-2.100c-.2-.5-.4-.5-.6-.5z"/></svg>',
    "fb": '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M13.5 21v-7.5h2.6l.4-3h-3V8.600c0-.9.3-1.500 1.500-1.500h1.600V4.400c-.3 0-1.200-.1-2.300-.1-2.300 0-3.800 1.400-3.800 3.900v2.300H7.900v3h2.600V21z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
    "phone": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M5 4h4l2 5-2.500 1.500a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 21s7-6.100 7-11.500A7 7 0 0 0 5 9.500C5 14.900 12 21 12 21z"/><circle cx="12" cy="9.500" r="2.500"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "info": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><circle cx="12" cy="12" r="9"/><path d="M12 11v6M12 7.500v.1"/></svg>',
    "pen": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 20l1-4L16.500 4.500a2.100 2.100 0 0 1 3 3L8 19z"/><path d="M14 7l3 3"/></svg>',
    "gem": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M6 3h12l4 6-10 12L2 9z"/><path d="M2 9h20M9 3l-2 6 5 12 5-12-2-6"/></svg>',
    "leaf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M5 19C5 10 11 5 20 4c0 9-5 15-14 15z"/><path d="M5 19c3-5 6-8 11-11"/></svg>',
    "gift": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="8" width="18" height="4"/><path d="M5 12v9h14v-9M12 8v13M12 8c-3 0-5-1-5-3s3-2 5 3c2-5 5-5 5-3s-2 3-5 3z"/></svg>',
    "shirt": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M8 3L3 6l2 4 3-1v12h8V9l3 1 2-4-5-3c-.5 2-2 3-4 3s-3.500-1-4-3z"/></svg>',
    "spray": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="7" y="9" width="8" height="12" rx="1.500"/><path d="M9 9V6h4v3M11 3v3M18 6h.1M20 4h.1M20 8h.1"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 3l8 3v6c0 5-3.500 8-8 9-4.500-1-8-4-8-9V6z"/><path d="M8.500 12l2.500 2.500 4.500-5"/></svg>',
    "heart": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M12 20s-8-4.600-8-10.500A4.500 4.500 0 0 1 12 7a4.500 4.500 0 0 1 8 2.500C20 15.400 12 20 12 20z"/></svg>',
    "rev": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M4 5h16v11H9l-5 4z"/></svg>',
    "arrow": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
    "down": '<svg viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M1 3l4 4 4-4"/></svg>',
}

NAV = [
    ("tatuajes.html", "Tatuajes"),
    ("piercing.html", "Piercing"),
    ("equipo.html", "Equipo"),
    ("galeria.html", "Galería"),
    ("estudio.html", "Estudio"),
    ("primera-vez.html", "Tu primera vez"),
    ("contacto.html", "Contacto"),
]
TEAM_PAGES = {a["slug"] + ".html" for a in ARTISTS.values()}
SERVICE_PAGES = {s["slug"] + ".html" for s in SERVICES}
STUDIO_ITEMS = [("estudio.html", "El estudio", "Historia, valores y ambiente"), ("belly-painting.html", "Belly painting", "Pintura sobre la tripa de embarazada"), ("tienda.html", "Tienda y tarjetas regalo", "Totebag, camisetas y regalos")]
STUDIO_PAGES = {h for h, _, _ in STUDIO_ITEMS}
STYLE_PAGES = {s["slug"] + ".html" for s in STYLES}


def header(current):
    links = []
    for href, label in NAV:
        if href == "equipo.html":
            cur = current == "equipo.html" or current in TEAM_PAGES
            dd = "".join(
                f'<a href="{a["slug"]}.html"{" aria-current=\"page\"" if current == a["slug"] + ".html" else ""}><b>{a["name"]}</b><small>{a["role"]}</small></a>'
                for a in (ARTISTS[k] for k in ORDER)
            )
            links.append(
                f'<div class="nav-dd{" has-current" if cur else ""}"><button type="button" aria-haspopup="true">Equipo{ICON["down"]}</button>'
                f'<div class="dd-menu"><a href="equipo.html"><b>Todo el equipo</b><small>Conócelos a los cuatro</small></a>{dd}</div></div>'
            )
        elif href == "estudio.html":
            cur = current in STUDIO_PAGES
            dd = "".join(f'<a href="{h}"{" aria-current=\"page\"" if current == h else ""}><b>{t}</b><small>{d}</small></a>' for h, t, d in STUDIO_ITEMS)
            links.append(
                f'<div class="nav-dd{" has-current" if cur else ""}"><button type="button" aria-haspopup="true">Estudio{ICON["down"]}</button>'
                f'<div class="dd-menu">{dd}</div></div>'
            )
        elif href == "tatuajes.html":
            cur = current == "tatuajes.html" or current in STYLE_PAGES
            dd = "".join(
                f'<a href="{s["slug"]}.html"{" aria-current=\"page\"" if current == s["slug"] + ".html" else ""}><b>{s["nav"]}</b><small>{s["kicker"]}</small></a>'
                for s in STYLES
            )
            links.append(
                f'<div class="nav-dd{" has-current" if cur else ""}"><button type="button" aria-haspopup="true">Tatuajes{ICON["down"]}</button>'
                f'<div class="dd-menu" style="min-width:300px"><a href="tatuajes.html"><b>Todos los estilos</b><small>Elige el tuyo</small></a>{dd}</div></div>'
            )
        elif href == "piercing.html":
            cur = current == "piercing.html" or current in SERVICE_PAGES
            dd = "".join(
                f'<a href="{s["slug"]}.html"{" aria-current=\"page\"" if current == s["slug"] + ".html" else ""}><b>{s["nav"]}</b><small>{s["kicker"]}</small></a>'
                for s in SERVICES
            )
            links.append(
                f'<div class="nav-dd{" has-current" if cur else ""}"><button type="button" aria-haspopup="true">Piercing{ICON["down"]}</button>'
                f'<div class="dd-menu"><a href="piercing.html"><b>Todo el piercing</b><small>Servicios y galería</small></a>{dd}</div></div>'
            )
        else:
            links.append(f'<a href="{href}"{" aria-current=\"page\"" if current == href else ""}>{label}</a>')
    mob = ['<a href="index.html"%s>Inicio</a>' % (' aria-current="page"' if current == "index.html" else "")]
    for href, label in NAV:
        mob.append(f'<a href="{href}"{" aria-current=\"page\"" if current == href else ""}>{label}</a>')
        if href == "equipo.html":
            for k in ORDER:
                a = ARTISTS[k]
                mob.append(f'<a class="sub" href="{a["slug"]}.html">{a["name"]}</a>')
        if href == "estudio.html":
            for h, t, d in STUDIO_ITEMS[1:]:
                mob.append(f'<a class="sub" href="{h}">{t}</a>')
        if href == "tatuajes.html":
            for s in STYLES:
                mob.append(f'<a class="sub" href="{s["slug"]}.html">{s["nav"]}</a>')
        if href == "piercing.html":
            for s in SERVICES:
                mob.append(f'<a class="sub" href="{s["slug"]}.html">{s["nav"]}</a>')
    return f'''
<div class="top-bar"><div class="top-bar-inner">
  <span class="open-status" data-open-status><span class="status-dot" aria-hidden="true"></span><span class="status-text">Horario</span></span>
  <span class="top-sep hide-sm">·</span>
  <a class="hide-sm" href="{SITE["maps"]}" target="_blank" rel="noopener">{SITE["addr"]}</a>
  <span class="top-sep hide-sm">·</span>
  <a href="{wa()}" target="_blank" rel="noopener">WhatsApp {SITE["wa_pretty"]}</a>
  <span class="top-sep">·</span>
  <span>★ 5,0 · 120 reseñas en Google</span>
  <span class="demo-tag">Demo</span>
</div></div>
<header class="site-header"><div class="wrap header-inner">
  <a href="index.html" class="brand" aria-label="La Cara Norte — inicio"><img src="assets/img/logo/logo-512.png" alt="" width="54" height="54"><span class="brand-text"><span class="brand-name">La Cara Norte</span><span class="brand-sub">Custom Tattoo</span></span></a>
  <nav class="main-nav" aria-label="Principal">{"".join(links)}</nav>
  <div class="header-cta"><a class="btn btn-primary" href="contacto.html#cita">Pedir cita</a><button class="nav-toggle" id="navToggle" aria-expanded="false" aria-controls="mobileNav" aria-label="Abrir menú"><span></span><span></span><span></span></button></div>
</div>
<nav class="mobile-nav" id="mobileNav" aria-label="Menú móvil">{"".join(mob)}<a class="btn btn-wa" href="{wa("Hola, quería pedir cita en La Cara Norte.")}" target="_blank" rel="noopener">{ICON["wa"]} Escribir por WhatsApp</a></nav>
</header>'''


def footer():
    return f'''
<footer class="site-footer"><div class="wrap">
  <div class="footer-grid">
    <div>
      <img class="footer-logo" src="assets/img/logo/logo-512.png" alt="La Cara Norte Custom Tattoo — desde 2021" width="130" height="130" loading="lazy">
      <p>Estudio de tatuajes y piercing en el barrio de La Palomera, León. Tatuaje a medida, piercing y graffiti desde 2021.</p>
      <div class="socials">
        <a href="{SITE["ig"]}" target="_blank" rel="noopener" aria-label="Instagram">{ICON["ig"]}</a>
        <a href="{SITE["fb"]}" target="_blank" rel="noopener" aria-label="Facebook">{ICON["fb"]}</a>
        <a href="{wa()}" target="_blank" rel="noopener" aria-label="WhatsApp">{ICON["wa"]}</a>
        <a href="mailto:{SITE["mail"]}" aria-label="Correo">{ICON["mail"]}</a>
      </div>
    </div>
    <div><h4>Estudio</h4><a href="tatuajes.html">Tatuajes</a>{"".join(f'<a href="{s["slug"]}.html" style="padding-left:14px;font-size:.86rem">· {s["nav"]}</a>' for s in STYLES)}<a href="piercing.html">Piercing y gemas</a>{"".join(f'<a href="{s["slug"]}.html" style="padding-left:14px;font-size:.86rem">· {s["nav"]}</a>' for s in SERVICES)}<a href="galeria.html">Galería</a><a href="estudio.html">El estudio</a><a href="belly-painting.html" style="padding-left:14px;font-size:.86rem">· Belly painting</a><a href="tienda.html" style="padding-left:14px;font-size:.86rem">· Tienda y tarjetas regalo</a><a href="primera-vez.html">Tu primera vez</a><a href="contacto.html">Contacto</a></div>
    <div><h4>Equipo</h4>{"".join(f'<a href="{ARTISTS[k]["slug"]}.html">{ARTISTS[k]["name"]}</a>' for k in ORDER)}</div>
    <div><h4>Visítanos</h4>
      <p>{SITE["addr"]}</p>
      <p>Lunes a viernes · 10:00 – 18:00<br>Julio y agosto: solo con cita previa.</p>
      <a href="{wa()}" target="_blank" rel="noopener">WhatsApp {SITE["wa_pretty"]}</a>
      <a href="tel:{SITE["tel"]}">Tel. {SITE["tel_pretty"]}</a>
      <a href="mailto:{SITE["mail"]}">{SITE["mail"]}</a>
    </div>
  </div>
  <div class="footer-bottom">
    <span>© <span data-year>2026</span> La Cara Norte Custom Tattoo · Demostración web no oficial</span>
    <nav aria-label="Legal"><a href="aviso-legal.html">Aviso legal</a><a href="privacidad.html">Privacidad</a><a href="cookies.html">Cookies</a></nav>
  </div>
</div></footer>
<div class="mobile-cta" role="region" aria-label="Pedir cita"><a class="btn btn-wa" href="{wa("Hola, quería pedir cita en La Cara Norte.")}" target="_blank" rel="noopener">{ICON["wa"]} WhatsApp</a><a class="btn btn-primary" href="contacto.html#cita">Pedir cita</a></div>
'''


def page(fname, title, desc, body, og_img="logo/logo-original", extra_head="", pre=""):
    full_title = title if title.startswith("La Cara Norte") else f"{title} · La Cara Norte Custom Tattoo León"
    og = f"assets/img/{og_img}.jpg" if og_img.endswith("original") else src(og_img)
    doc = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(full_title)}</title>
<meta name="description" content="{html.escape(desc, quote=True)}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#0b0b0c">
<meta property="og:type" content="website"><meta property="og:locale" content="es_ES"><meta property="og:site_name" content="La Cara Norte Custom Tattoo">
<meta property="og:url" content="{SITE_URL}{"" if fname == "index.html" else fname}">
<meta property="og:title" content="{html.escape(full_title, quote=True)}"><meta property="og:description" content="{html.escape(desc, quote=True)}">
<meta property="og:image" content="{SITE_URL}assets/img/og-card.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="La Cara Norte Custom Tattoo: tatuajes y piercing en León">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{html.escape(full_title, quote=True)}"><meta name="twitter:description" content="{html.escape(desc, quote=True)}"><meta name="twitter:image" content="{SITE_URL}assets/img/og-card.jpg">
<link rel="icon" type="image/png" href="assets/img/logo/favicon.png"><link rel="apple-touch-icon" href="assets/img/logo/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500;1,600&family=Inter:wght@400;500;600;700&family=Oswald:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/styles.css?v=3">
{jsonld()}
{extra_head}
</head>
<body>
<a class="skip-link" href="#contenido">Saltar al contenido</a>
{pre}
{header(fname)}
<main id="contenido">
{body}
</main>
{footer()}
<script src="assets/js/main.js?v=3" defer></script>
</body>
</html>
'''
    with open(os.path.join(ROOT, fname), "w", encoding="utf-8") as f:
        f.write(doc)
    print("ok", fname, len(doc) // 1024, "KB")


def page_hero(crumb, h1, lead, hero_key, extra="", eyebrow=""):
    return f'''
<section class="page-hero grain">
  {f'<div class="page-hero-bg">{img(hero_key, lazy=False, big=True)}</div>' if hero_key else ''}
  <div class="wrap">
    <p class="crumbs"><a href="index.html">Inicio</a><span>/</span>{crumb}</p>
    {f'<p class="eyebrow">{eyebrow}</p>' if eyebrow else ''}
    <h1 class="split-words">{h1}</h1>
    <p class="lead">{lead}</p>
    {extra}
  </div>
</section>'''


def marquee(items):
    one = "".join(f"<span>{i}</span>" for i in items)
    return f'<div class="marquee" aria-hidden="true"><div class="marquee-track"><div class="marquee-set">{one}</div><div class="marquee-set">{one}</div></div></div>'


def cta_final(title="Cuéntanos tu idea", text="Escríbenos por WhatsApp con tu referencia, la zona del cuerpo y el tamaño aproximado. Te respondemos dentro del horario del estudio.", keys=None):
    keys = keys or ["luis-03", "guille-04", "maria-03", "paulix-03", "luis-02", "guille-06"]
    bg = "".join(img(k, extra='aria-hidden="true"').replace('alt="' + alt(k) + '"', 'alt=""') for k in keys)
    return f'''
<section class="final-cta">
  <div class="bg" style="display:grid;grid-template-columns:repeat({len(keys)},1fr);opacity:.55">{bg}</div>
  <div class="wrap reveal">
    <p class="eyebrow">Pide tu cita</p>
    <h2>{title}</h2>
    <p class="lead">{text}</p>
    <div class="btn-row">
      <a class="btn btn-wa" href="{wa("Hola, quería pedir cita en La Cara Norte.")}" target="_blank" rel="noopener">{ICON["wa"]} WhatsApp</a>
      <a class="btn btn-ghost" href="contacto.html#cita">Rellenar solicitud</a>
    </div>
  </div>
</section>'''


def shots(keys, group, cap=True):
    out = []
    for k in keys:
        a, artist, cat = W[k]
        w, h = size(k)
        out.append(
            f'<button type="button" class="shot" data-full="{full(k)}" data-cat="{cat}" data-artist="{artist}" data-cap="{html.escape(artist, quote=True)}" aria-label="Ampliar: {html.escape(a, quote=True)}">'
            f'<img src="{src(k)}" data-full="{full(k)}" alt="{alt(k)}" width="{w}" height="{h}" loading="lazy"></button>'
        )
    return "".join(out)


def hours_table():
    rows = [("Lunes", 1, "10:00 – 18:00"), ("Martes", 2, "10:00 – 18:00"), ("Miércoles", 3, "10:00 – 18:00"), ("Jueves", 4, "10:00 – 18:00"), ("Viernes", 5, "10:00 – 18:00"), ("Sábado", 6, "Cerrado"), ("Domingo", 0, "Cerrado")]
    return '<table class="hours"><tbody>' + "".join(f'<tr data-hours-row="{n}"><td>{d}</td><td>{h}</td></tr>' for d, n, h in rows) + "</tbody></table>"


def reviews_block(n=3, light=True):
    cards = "".join(
        f'<figure class="card review reveal d{i % 3}" style="margin:0"><div class="stars" aria-label="5 estrellas">★★★★★</div><q>«{html.escape(t)}»</q><cite>{html.escape(a)} · {html.escape(s)}</cite></figure>'
        for i, (t, a, s) in enumerate(REVIEWS[:n])
    )
    return cards


def finder():
    opts = [
        ("Color y personajes", "Neotradicional, neojaponés, anime…", "luis", "un tatuaje de color (neotradicional, japonés o anime)", "luis-08", "Color saturado, línea firme y personajes con mucha vida: es lo que mejor se le da a Luis."),
        ("Realismo y retrato", "Black & grey, retratos, piezas grandes", "guille", "un tatuaje realista o en black & grey", "guille-08", "Volumen, contraste y retratos. Guille es nuestro especialista en realismo y piezas completas."),
        ("Fine line y detalles", "Línea fina, flores, símbolos pequeños", "maria", "un tatuaje fine line o dotwork", "maria-03", "Trazo delicado y composiciones limpias. María es ideal para piezas finas y para un primer tatuaje."),
        ("Piercing o gemas", "Orejas, nariz, ombligo, gemas dentales", "paulix", "un piercing o gemas dentales", "paulix-03", "Paulix se encarga de piercings y joyería, con marcado previo y composición de orejas."),
        ("Cover up", "Tapar o reformar un tatuaje antiguo", "luis", "un cover up", "luis-01", "Luis y Guille trabajan cover ups. Cuéntanos tu caso con una foto y te orientamos."),
        ("No lo tengo claro", "Quiero ver opciones y que me aconsejen", "maria", "pedir consejo sobre mi idea", "maria-02", "Escríbenos con lo que tengas en mente y te decimos con quién encaja mejor."),
    ]
    btns = ""
    for title, sub, k, topic, im, why in opts:
        a = ARTISTS[k]
        btns += f'<button type="button" class="opt" aria-pressed="false" data-name="{a["name"]}" data-href="{a["slug"]}.html" data-img="{src(im)}" data-topic="{topic}" data-why="{html.escape(why, quote=True)}"><b>{title}</b><small>{sub}</small></button>'
    return f'''
<div class="finder reveal" data-finder>
  <p class="eyebrow">Encuentra a tu artista</p>
  <h3>¿Qué tienes en mente?</h3>
  <div class="finder-opts">{btns}</div>
  <div class="finder-result" aria-live="polite">
    <img class="fr-img" src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==" alt="" width="150" height="200">
    <div><p class="num">Te recomendamos a</p><h3 class="fr-name"></h3><p class="fr-why"></p>
      <div class="btn-row"><a class="btn btn-primary fr-link" href="#">Ver su trabajo</a><a class="btn btn-wa fr-wa" href="#" target="_blank" rel="noopener">{ICON["wa"]} Pedir cita</a></div></div>
  </div>
</div>'''


def artist_card(k, light=False):
    a = ARTISTS[k]
    return f'''<article class="artist-card reveal">
  <a class="ph" href="{a["slug"]}.html" aria-label="Ver a {a["name"]}">{img(a["card"])}</a>
  <div class="body"><h3>{a["name"]}</h3><p class="role">{a["role"]}</p><p>{a["teaser"]}</p>
  <a class="link-arrow more" href="{a["slug"]}.html">Ver su trabajo {ICON["arrow"].replace("<svg", '<svg width="16" height="16"')}</a></div>
</article>'''


# ============================================================
# PÁGINAS
# ============================================================
def build_index():
    wall_keys = ["luis-02", "guille-04", "maria-03", "paulix-03", "luis-08", "guille-08", "maria-05", "paulix-01", "luis-03", "guille-06",
                 "maria-02", "luis-09", "guille-09", "paulix-10", "luis-05", "guille-12", "maria-09", "luis-06", "guille-05", "paulix-07",
                 "luis-04", "maria-01", "luis-01", "guille-11", "maria-04", "paulix-04", "studio-09", "guille-02", "maria-10"]
    cols = [wall_keys[i::5][:6] for i in range(5)]
    wall = ""
    for c in cols:
        one = "".join(img(k, lazy=False).replace('alt="' + alt(k) + '"', 'alt=""') for k in c)
        wall += f'<div class="hero-col" aria-hidden="true">{one}{one}</div>'
    pre = '<div class="splash" aria-hidden="true"><img src="assets/img/logo/logo-transparent.png" alt="" width="300" height="300"></div>'
    arrow = ICON["arrow"].replace("<svg", '<svg width="16" height="16"')
    hero = f"""
<section class="hero grain">
  <div class="hero-wall">{wall}</div>
  <div class="wrap hero-inner">
    <div>
      <div class="hero-badges"><span class="stamp">Estudio en León · La Palomera</span><span class="pill">Desde 2021</span></div>
      <h1>Tinta a medida,<br>piel con carácter<em>Custom tattoo &amp; graffiti en el barrio de La Palomera</em></h1>
      <p class="lead">Un estudio con cuatro artistas y cuatro maneras de entender la piel: neotradicional, realismo, fine line y piercing. Todo diseñado contigo, de principio a fin.</p>
      <div class="btn-row">
        <a class="btn btn-primary" href="contacto.html#cita">Pedir cita</a>
        <a class="btn btn-ghost" href="galeria.html">Ver trabajos</a>
      </div>
      <div class="hero-stats">
        <div><b data-count="5.0">5,0</b><span>★ en Google</span></div>
        <div><b data-count="120">120</b><span>reseñas</span></div>
        <div><b data-count="4">4</b><span>artistas</span></div>
        <div><b>2021</b><span>abrimos</span></div>
      </div>
    </div>
    <div class="hero-logo"><img src="assets/img/logo/logo-transparent.png" alt="Logotipo de La Cara Norte Custom Tattoo, desde 2021" width="1000" height="1000"></div>
  </div>
  <span class="scroll-cue" aria-hidden="true"></span>
</section>"""
    mq = marquee(["★ 5,0 en Google", "120 reseñas", "Tatuaje a medida", "Neotradicional", "Realismo", "Fine line", "Piercing y gemas", "Cover up", "Graffiti", "León · La Palomera"])
    intro = f"""
<section class="sec on-light has-leaves">
  {leaves("tr")}
  <div class="wrap split">
    <div class="reveal frame-stack"><div class="frame">{img("luis-03", big=True)}</div>{img("maria-03", "b")}</div>
    <div class="reveal d1">
      <p class="eyebrow">El estudio</p>
      <h2 class="split-words">Cada pieza empieza en una <span class="serif accent">conversación</span></h2>
      <p class="lead">En La Cara Norte no hay catálogo cerrado. Escuchamos tu idea, la dibujamos contigo y la llevamos a la piel con el artista cuyo estilo mejor la defiende. Tatuaje, piercing y graffiti bajo el mismo techo, en pleno barrio de La Palomera.</p>
      <ul class="leaf-list" style="margin:0 0 30px;color:#3b4047">
        <li>Diseño personalizado, nunca plantillas</li>
        <li>Cuatro especialidades, un solo estudio</li>
        <li>Trato cercano: así lo cuentan nuestros clientes</li>
        <li>Espacio amigable con el colectivo LGBTQ+</li>
      </ul>
      <a class="link-arrow" href="estudio.html">Conoce el estudio {arrow}</a>
    </div>
  </div>
</section>"""
    styles = f"""
<section class="sec sec-anth grain">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Lo que hacemos</p><h2 class="split-words">Estilos para todas las pieles</h2><p class="lead">Del color más intenso a la línea más fina. Elige tu estilo y descubre quién lo trabaja.</p></div>
    <div class="grid g4">
      <a class="style-card reveal" href="tatuajes.html#neotradicional">{img("luis-02")}<div class="in"><span class="num">01</span><h3>Neotradicional &amp; anime</h3><p>Color, línea firme y personajes con alma.</p><span class="pill">Luis Santos</span></div></a>
      <a class="style-card reveal d1" href="tatuajes.html#realismo">{img("guille-09")}<div class="in"><span class="num">02</span><h3>Realismo &amp; black&nbsp;grey</h3><p>Retratos, volumen y piezas completas.</p><span class="pill">Guille Martink</span></div></a>
      <a class="style-card reveal d2" href="tatuajes.html#fineline">{img("maria-05")}<div class="in"><span class="num">03</span><h3>Fine line &amp; dotwork</h3><p>Delicadeza, flores y símbolos pequeños.</p><span class="pill">María</span></div></a>
      <a class="style-card reveal d3" href="piercing.html">{img("paulix-10")}<div class="in"><span class="num">04</span><h3>Piercing &amp; gemas</h3><p>Orejas, ombligo y joyería en oro.</p><span class="pill green">Paulix</span></div></a>
    </div>
  </div>
</section>"""
    team = f"""
<section class="sec on-light has-leaves">
  {leaves("bl")}
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">El equipo</p><h2 class="split-words">Cuatro artistas, <span class="serif accent">un mismo cuidado</span></h2><p class="lead">Cada uno con su estilo, su portfolio y su manera de trabajar. Entra en su página para ver más trabajos y pedirles cita.</p></div>
    <div class="grid g4">{"".join(artist_card(k) for k in ORDER)}</div>
  </div>
</section>"""
    find = f"""
<section class="sec sec-anth grain"><div class="wrap" style="max-width:1000px">{finder()}</div></section>"""
    carousel_keys = ["luis-02", "guille-06", "maria-05", "paulix-10", "luis-08", "guille-05", "maria-03", "luis-09", "guille-08", "paulix-01", "luis-05", "maria-02"]
    items = "".join(f'<a href="galeria.html" draggable="false">{img(k)}<span class="cap">{W[k][1]}</span></a>' for k in carousel_keys)
    gallery = f"""
<section class="sec sec-dark" style="overflow:hidden">
  <div class="wrap"><div class="sec-head reveal"><p class="eyebrow">Portfolio</p><h2 class="split-words">Trabajos <span class="serif accent">reales</span>, sin filtros</h2><p class="lead">Arrastra para ver más. La galería completa tiene filtros por estilo y visor ampliado.</p></div></div>
  <div class="hscroll" aria-label="Carrusel de trabajos">{items}</div>
  <div class="wrap"><p style="margin-top:20px"><a class="btn btn-primary" href="galeria.html">Ver la galería completa</a></p></div>
</section>"""
    reels = f"""
<section class="sec reel-sec grain">
  <span class="reel-bg-text" aria-hidden="true">REELS</span>
  <div class="wrap">
    <div class="sec-head center reveal"><p class="eyebrow">En movimiento</p><h2 class="split-words">Piezas reales, <span class="serif accent">en vídeo</span></h2><p class="lead">Reels de nuestros artistas. Pulsa play y míralos sin salir de la web.</p></div>
    <div class="reel-duo reel-row">{reel("serpiente", "tilt-l")}{reel("anubis", "tilt-r")}{reel("hannya", "tilt-l")}{reel("lovehate", "tilt-r")}</div>
  </div>
</section>"""
    mas = f"""
<section class="sec on-light has-leaves">
  {leaves("tr")}
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Y además</p><h2 class="split-words">Más que <span class="serif accent">tatuajes</span></h2><p class="lead">Un par de cosas que quizá no esperabas encontrar en un estudio de tatuajes.</p></div>
    <div class="grid g3">
      <a class="card reveal" href="belly-painting.html"><div class="ico">{ICON["heart"]}</div><span class="stamp" style="margin-bottom:14px">Nuevo servicio</span><h3>Belly painting</h3><p style="margin:0 0 14px;color:#4a4f57">Pintura artística sobre la tripa de embarazada: un recuerdo único.</p><span class="link-arrow">Ver más</span></a>
      <a class="card reveal d1" href="tienda.html#tarjetas"><div class="ico">{ICON["gift"]}</div><h3>Tarjetas regalo</h3><p style="margin:0 0 14px;color:#4a4f57">Regala tinta o piercing. Pídela por WhatsApp con el importe que quieras.</p><span class="link-arrow">Ver más</span></a>
      <a class="card reveal d2" href="tienda.html#merch"><div class="ico">{ICON["shirt"]}</div><h3>Merchandising</h3><p style="margin:0 0 14px;color:#4a4f57">Totebag y camisetas con el sello de La Cara Norte.</p><span class="link-arrow">Ver más</span></a>
    </div>
  </div>
</section>"""
    slides = "".join(
        f'<div class="testi-slide{" on" if i == 0 else ""}"><div class="stars" aria-hidden="true">★★★★★</div><q>«{html.escape(t)}»</q><cite>{html.escape(a)} · {html.escape(s)}</cite></div>'
        for i, (t, a, s) in enumerate(REVIEWS)
    )
    dots = "".join(f'<button type="button" aria-label="Reseña {i + 1}"{" class=on" if i == 0 else ""}></button>' for i in range(len(REVIEWS)))
    reviews = f"""
<section class="sec on-light has-leaves">
  {leaves("br")}
  <div class="wrap">
    <div class="rating-big reveal" style="justify-content:center"><b>5,0</b><div><div class="stars" aria-hidden="true">★★★★★</div><p style="margin:6px 0 0">120 opiniones en Google · <a class="link-arrow" style="padding-bottom:2px" href="{SITE["maps"]}" target="_blank" rel="noopener">Leerlas</a></p></div></div>
    <div class="testi reveal" data-testi><div class="testi-track">{slides}</div><div class="testi-dots">{dots}</div></div>
  </div>
</section>"""
    steps = """
<section class="sec sec-carbon grain">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Cómo trabajamos</p><h2 class="split-words">Del primer mensaje a <span class="serif accent">tu tatuaje</span></h2></div>
    <div class="steps">
      <div class="step reveal"><h3>Cuéntanos</h3><p>Escríbenos por WhatsApp con tu idea, referencias, zona y tamaño aproximado.</p></div>
      <div class="step reveal d1"><h3>Diseñamos</h3><p>El artista adecuado prepara una propuesta y te orienta sobre tiempo y presupuesto.</p></div>
      <div class="step reveal d2"><h3>Reservamos</h3><p>Fijamos día y hora dentro del horario del estudio. En julio y agosto, solo con cita.</p></div>
      <div class="step reveal d3"><h3>Tatuamos</h3><p>Sesión tranquila, material de un solo uso y consejos claros para cuidarlo después.</p></div>
    </div>
    <p style="margin-top:40px"><a class="link-arrow" href="primera-vez.html">Guía para tu primera vez</a></p>
  </div>
</section>"""
    ig_keys = ["luis-08", "maria-03", "guille-04", "paulix-03", "luis-02", "maria-02"]
    ig = f"""
<section class="sec sec-dark">
  <div class="wrap">
    <div class="split" style="margin-bottom:40px;align-items:end">
      <div class="reveal"><p class="eyebrow">Instagram</p><h2 class="split-words">@lacaranorte<span class="serif accent">.tattoo</span></h2></div>
      <div class="reveal d1"><p class="lead" style="margin:0 0 18px">2.464 seguidores y trabajo nuevo cada semana: tatuajes, piercings, huecos libres y visitas de artistas invitados.</p><a class="btn btn-ghost" href="{SITE["ig"]}" target="_blank" rel="noopener">{ICON["ig"]} Seguir en Instagram</a></div>
    </div>
    <div class="ig-grid reveal">{"".join(f'<a href="{SITE["ig"]}" target="_blank" rel="noopener" aria-label="Ver en Instagram">{img(k)}{ICON["ig"]}</a>' for k in ig_keys)}</div>
  </div>
</section>"""
    visit = f"""
<section class="sec sec-anth grain">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Visítanos</p><h2>En el corazón de <span class="serif accent">La Palomera</span></h2>
      <p class="lead">{SITE["addr"]}. Atendemos de lunes a viernes de 10:00 a 18:00. En julio y agosto, únicamente con cita previa.</p>
      {hours_table()}
      <div class="btn-row" style="margin-top:28px"><a class="btn btn-primary" href="{SITE["maps"]}" target="_blank" rel="noopener">Cómo llegar</a><a class="btn btn-ghost" href="contacto.html">Contacto</a></div>
    </div>
    <div class="map reveal d1"><iframe title="Mapa de La Cara Norte Custom Tattoo en León" src="{SITE["embed"]}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
  </div>
</section>"""
    body = hero + mq + intro + styles + team + find + gallery + reels + reviews + steps + mas + ig + visit + cta_final("Tu próxima pieza empieza aquí")
    page("index.html", "La Cara Norte Custom Tattoo — Estudio de tatuajes y piercing en León",
         "Estudio de tatuajes y piercing en León (La Palomera). Neotradicional, realismo, fine line, piercing y gemas dentales. 5,0 en Google. Pide cita por WhatsApp.",
         body, pre=pre)


def build_tatuajes():
    def block(id_, num, title, text, k, keys, rev=False, tags=()):
        a = ARTISTS[k]
        return f'''
<section class="sec {"on-light" if num % 2 == 0 else "sec-dark"} {"alt" if num % 2 == 0 and num > 2 else ""}" id="{id_}">
  <div class="wrap split {"rev" if rev else ""}">
    <div class="reveal"><div class="frame">{img(keys[0], big=True)}</div></div>
    <div class="reveal d1">
      <p class="eyebrow">Estilo 0{num}</p><h2>{title}</h2>
      <p class="lead">{text}</p>
      <div class="pills" style="margin:0 0 26px">{"".join(f'<span class="pill">{t}</span>' for t in tags)}</div>
      <div class="strip" style="grid-template-columns:repeat(3,1fr);margin-bottom:28px">{"".join(f'<a href="{a["slug"]}.html">{img(x)}</a>' for x in keys[1:4])}</div>
      <div class="btn-row"><a class="btn btn-primary" href="{a["slug"]}.html">Trabajos de {a["short"]}</a><a class="btn btn-ghost" href="{wa("Hola, me interesa " + a["topic"] + ".")}" target="_blank" rel="noopener">Consultar por WhatsApp</a></div>
    </div>
  </div>
</section>'''
    b = (
        block("neotradicional", 1, "Neotradicional, neojaponés & anime", "Contornos firmes, paletas intensas y mucha personalidad. Del lince al koi, de un personaje de anime a una escena completa: piezas que destacan a la primera y envejecen bien. Luis también se encarga de cover ups, blackout y piezas pequeñas.", "luis", ["luis-02", "luis-01", "luis-08", "luis-09"], False, ["Neotradicional", "Neojaponés", "Anime", "Cover up", "Blackout"]) +
        block("realismo", 2, "Realismo & black&nbsp;grey", "Retratos, piernas, espaldas y mangas con volumen, contraste y detalle fotográfico. Guille dibuja cada proyecto antes de tatuarlo y se mueve igual de bien en el gris que en el color.", "guille", ["guille-04", "guille-08", "guille-06", "guille-12"], True, ["Realismo", "Retrato", "Black & grey", "Black work", "Ilustración"]) +
        block("fineline", 3, "Fine line & dotwork", "Línea fina, puntillismo y composiciones respiradas. Flores, animales, letras, coordenadas y diseños pequeños que se sienten íntimos. María ofrece un trato muy cercano, ideal para primeras veces.", "maria", ["maria-03", "maria-05", "maria-02", "maria-09"], False, ["Fine line", "Dotwork", "Floral", "Minimalista", "Micro realismo"])
    )
    allstyles = f'''
<section class="sec sec-anth grain" id="estilos">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Profundiza</p><h2>Todos los <span class="serif accent">estilos</span></h2><p class="lead">Una página para cada estilo, con lo que lo define, cuándo encaja, preguntas frecuentes y quién lo hace.</p></div>
    <div class="grid g4">{"".join(f'<a class="style-card reveal d{i % 4}" href="{x["slug"]}.html">{img(x["card"])}<div class="in"><span class="num">0{i + 1}</span><h3>{x["nav"]}</h3><p>{x["card_text"]}</p><span class="pill">Ver más</span></div></a>' for i, x in enumerate(STYLES))}</div>
  </div>
</section>'''
    extra = f'''
<section class="sec sec-carbon">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Más cosas</p><h2>Cover up, graffiti <span class="serif accent">y colaboraciones</span></h2></div>
    <div class="grid g3">
      <div class="card reveal"><div class="ico">{ICON["pen"]}</div><h3>Cover up</h3><p style="color:#b9bdc4">¿Un tatuaje antiguo que ya no te representa? Mándanos una foto y te decimos si se puede reformar o tapar y con quién encaja mejor. <a class="accent" href="cover-up.html">Ver más</a>.</p></div>
      <div class="card reveal d1"><div class="ico">{ICON["spray"]}</div><h3>Graffiti</h3><p style="color:#b9bdc4">Somos «Custom Tattoo & Graffiti». Guille tiene un destacado de graffiti e ilustraciones en su Instagram. <a class="accent" href="graffiti.html">Ver más</a>.</p></div>
      <div class="card reveal d2"><div class="ico">{ICON["heart"]}</div><h3>Guest spots</h3><p style="color:#b9bdc4">Recibimos artistas invitados durante el año. Anunciamos las fechas en nuestro Instagram: síguenos para no perderte ninguna.</p></div>
    </div>
  </div>
</section>'''
    faq = f'''
<section class="sec on-light">
  <div class="wrap" style="max-width:900px">
    <div class="sec-head reveal"><p class="eyebrow">Antes de decidir</p><h2>Preguntas sobre tatuajes</h2></div>
    <div class="faq reveal">
      <details><summary>¿Cuánto cuesta un tatuaje?</summary><div class="ans">Depende del tamaño, el nivel de detalle, la zona y las horas de trabajo. Por eso presupuestamos cada pieza de forma personalizada: envíanos tu idea y te damos una cifra clara antes de reservar.</div></details>
      <details><summary>¿Puedo traer mi propio diseño?</summary><div class="ans">Por supuesto. Lo valoramos con el artista, ajustamos tamaño y composición a la zona del cuerpo y, si hace falta, lo adaptamos para que quede bien y envejezca mejor.</div></details>
      <details><summary>¿Hacéis tatuajes pequeños?</summary><div class="ans">Sí. Tanto Luis (Small), como María y Guille (Pequetattoos) trabajan piezas pequeñas. Mira las historias «Disponibles» de sus Instagram para huecos sueltos.</div></details>
      <details><summary>¿Qué pasa si quiero tapar un tatuaje?</summary><div class="ans">Hacemos cover up. Cada caso es distinto (color, tamaño, tinta anterior), así que lo mejor es que nos mandes una foto y te orientamos con honestidad.</div></details>
    </div>
  </div>
</section>'''
    body = page_hero("Tatuajes", "Tatuajes <span class='serif accent'>a medida</span>", "Neotradicional, realismo, fine line y más. Elige un estilo y conoce al artista que mejor lo defiende.", "luis-01", extra="") + allstyles + b + extra + faq + cta_final()
    page("tatuajes.html", "Tatuajes", "Tatuajes a medida en León: neotradicional, neojaponés, anime, realismo, black & grey, fine line y dotwork. Cover up y piezas pequeñas.", body, og_img="luis-02")


def build_piercing():
    main = [s for s in SERVICES if s["card"]]
    cards = "".join(f'<a class="style-card reveal d{i % 4}" href="{s["slug"]}.html">{img(s["card"])}<div class="in"><span class="num">0{i + 1}</span><h3>{s["nav"]}</h3><p>{s["card_text"]}</p><span class="pill green">Ver más</span></div></a>' for i, s in enumerate(main))
    more = "".join(f'<a class="card reveal d{i}" href="otros-piercings.html#{h.lower()}"><div class="ico">{ICON["gem"]}</div><h3>{h}</h3><p style="margin:0 0 14px;color:#b9bdc4">{d}</p><span class="link-arrow">Ver más</span></a>' for i, (h, d) in enumerate([
        ("Nariz", "Fosa nasal con joyería fina y colocación precisa."),
        ("Ceja", "Piercing de ceja con joya a medida de tu anatomía."),
        ("Microdermal", "Piezas de superficie para un toque diferente. Consulta zonas posibles."),
    ]))
    hero = page_hero("Piercing", "Piercing, <span class='serif' style='color:var(--green)'>joyería</span> y gemas", "De la primera perforación a una oreja completa: marcado, joyería fina y un seguimiento cercano de la mano de Paulix.", "paulix-03", eyebrow="Body piercing")
    body = f'''<div class="theme-green">{hero}
<section class="sec sec-dark grain">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Servicios</p><h2>Qué puedes hacerte</h2><p class="lead">Estos son los trabajos que Paulix muestra en su perfil. ¿Algo distinto? Escríbenos y lo vemos.</p></div>
    <div class="grid g4">{cards}</div>
    <div class="grid g3" style="margin-top:24px">{more}</div>
  </div>
</section>
<section class="sec on-light">
  <div class="wrap split">
    <div class="reveal"><p class="eyebrow">Cómo trabajamos</p><h2>Marcado previo, <span class="serif accent">joyería fina</span></h2>
      <p class="lead">Antes de perforar, marcamos y comprobamos contigo la colocación. Luego elegimos la joya que mejor encaja con tu anatomía y tu estilo.</p>
      <div class="grid g2" style="gap:16px;margin-bottom:28px">
        <div class="card"><div class="ico">{ICON["shield"]}</div><h3 style="font-size:1.2rem">Material estéril</h3><p style="margin:0;font-size:.92rem">Material de un solo uso y protocolo de higiene en cada perforación.</p></div>
        <div class="card"><div class="ico">{ICON["gem"]}</div><h3 style="font-size:1.2rem">Joyería</h3><p style="margin:0;font-size:.92rem">Piezas finas, incluyendo oro de 18K. Consulta disponibilidad.</p></div>
      </div>
      <a class="btn btn-primary" href="paulix.html">Conoce a Paulix</a></div>
    <div class="reveal d1"><div class="frame">{img("paulix-07", big=True)}</div></div>
  </div>
</section>
<section class="sec sec-carbon">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Galería</p><h2>Piercing en detalle</h2></div>
    <div class="masonry reveal" data-lightbox="pierc">{shots(ARTISTS["paulix"]["works"], "pierc")}</div>
  </div>
</section>
<section class="sec on-light alt">
  <div class="wrap" style="max-width:900px">
    <div class="sec-head reveal"><p class="eyebrow">Cuidados</p><h2>Cuida tu piercing</h2><p class="lead">Pautas generales habituales. Paulix te dará instrucciones concretas para tu perforación el día de tu cita.</p></div>
    <div class="faq reveal">
      <details><summary>Limpieza diaria</summary><div class="ans">Lávate las manos antes de tocar la zona y límpiala con suero fisiológico o el producto que te indiquen. Evita alcohol, agua oxigenada y pomadas no recomendadas.</div></details>
      <details><summary>¿Puedo girar o cambiar la joya?</summary><div class="ans">No la manipules ni la cambies hasta que cicatrice del todo. Si tienes dudas, escríbenos y lo revisamos.</div></details>
      <details><summary>Piscina, mar y sol</summary><div class="ans">Evita baños en piscinas, mar o jacuzzis durante la cicatrización y protege la zona del sol directo.</div></details>
      <details><summary>¿Cuánto tarda en cicatrizar?</summary><div class="ans">Depende de la zona y de cada persona. El cartílago suele tardar más que el lóbulo. Te informamos en la cita.</div></details>
    </div>
  </div>
</section>
{cta_final("Tu próximo piercing", "Escríbenos con la zona que te interesa y te decimos disponibilidad y opciones de joyería.", ["paulix-03", "paulix-01", "paulix-10", "paulix-07", "paulix-04", "paulix-06"])}
</div>'''
    page("piercing.html", "Piercing y gemas dentales", "Piercing en León: orejas, nariz, ombligo, ceja, microdermal y gemas dentales, con joyería en oro 18K. Paulix en La Cara Norte.", body, og_img="paulix-03")



def build_service(s):
    others = [x for x in SERVICES if x is not s]
    opts = "".join(
        f'<div class="card reveal d{i % 4}" id="{o[0].lower().split(" ")[0]}"><p class="num">0{i + 1}</p><h3>{o[0]}</h3><p style="margin:0;color:#b9bdc4">{o[1]}</p></div>'
        for i, o in enumerate(s["options"])
    )
    heal = "".join(f'<li><b>{h}.</b> {t}</li>' for h, t in s["heal"])
    faq = "".join(f'<details><summary>{q}</summary><div class="ans">{a}</div></details>' for q, a in s["faq"])
    paras = "".join(f"<p class=\"lead\">{t}</p>" for t in s["intro"])
    if s.get("no_photos"):
        gal = f'''<div class="card reveal" style="max-width:720px"><div class="ico">{ICON["ig"]}</div><h3>Ejemplos en Instagram</h3><p style="color:#b9bdc4">Los trabajos de nariz, ceja y microdermal están en el perfil de Paulix. Mientras actualizamos esta galería, puedes verlos aquí.</p><a class="btn btn-ghost" href="https://www.instagram.com/paulix.piercing/" target="_blank" rel="noopener">@paulix.piercing</a></div>'''
    else:
        gal = f'<div class="masonry reveal" data-lightbox="svc">{shots(s["gallery"], "svc")}</div>'
    rel = "".join(f'<a class="card reveal" href="{x["slug"]}.html"><p class="num">Piercing</p><h3>{x["nav"]}</h3><p style="margin:0 0 14px;color:#b9bdc4">{x["kicker"]}</p><span class="link-arrow">Ver más</span></a>' for x in others[:3])
    hero = page_hero(f'<a href="piercing.html">Piercing</a><span>/</span>{s["nav"]}', s["title"], s["lead"], s["hero"], eyebrow=s["kicker"],
                     extra=f'<div class="btn-row" style="margin-top:26px"><a class="btn btn-primary" href="{wa("Hola, me interesa " + s["topic"] + " en La Cara Norte.")}" target="_blank" rel="noopener">{ICON["wa"]} Consultar con Paulix</a><a class="btn btn-ghost" href="paulix.html">Conoce a Paulix</a></div>')
    body = f'''<div class="theme-green">{hero}
<section class="sec on-light has-leaves">
  {leaves("tr")}
  <div class="wrap split">
    <div class="reveal"><p class="eyebrow">De qué va</p><h2 class="split-words">Todo lo que conviene saber</h2>{paras}</div>
    <div class="reveal d1"><div class="frame">{img(s["hero"], big=True)}</div></div>
  </div>
</section>
<section class="sec sec-anth grain">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">{s["options_title"]}</p><h2>{s["nav"]} <span class="serif" style="color:var(--green)">en detalle</span></h2></div>
    <div class="grid g4">{opts}</div>
  </div>
</section>
<section class="sec on-light alt has-leaves">
  {leaves("bl")}
  <div class="wrap split">
    <div class="reveal"><p class="eyebrow">{s["heal_title"]}</p><h2>Cuidar bien para <span class="serif accent">que dure</span></h2>
      <p class="lead">Estos plazos y pautas son generales. Paulix te dará instrucciones concretas para tu caso el día de la cita.</p>
      <ul class="leaf-list" style="color:#3b4047">{heal}</ul></div>
    <div class="reveal d1"><div class="faq">{faq}</div></div>
  </div>
</section>
<section class="sec sec-carbon">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Galería</p><h2>Trabajos de {s["nav"].lower()}</h2></div>
    {gal}
  </div>
</section>
<section class="sec on-light">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Sigue explorando</p><h2>Más sobre piercing</h2></div>
    <div class="grid g3">{rel}</div>
  </div>
</section>
{cta_final("Pide tu cita de piercing", "Escríbenos con lo que tienes en mente y Paulix te dirá disponibilidad, opciones de joyería y plazos.", ["paulix-03", "paulix-01", "paulix-10", "paulix-07", "paulix-04", "paulix-06"])}
</div>'''
    page(s["slug"] + ".html", re_title(s), f'{re_title(s)} en La Cara Norte Custom Tattoo, León: qué es, opciones, cicatrización orientativa, preguntas frecuentes y cómo pedir cita con Paulix.', body, og_img=s["hero"])


def re_title(s):
    import re as _re
    return _re.sub(r"<[^>]+>", "", s["title"]).replace("  ", " ")



def build_style(s):
    a = ARTISTS[s["artist"]]
    others = [x for x in STYLES if x is not s]
    opts = "".join(
        f'<div class="card reveal d{i % 4}"><p class="num">0{i + 1}</p><h3>{o[0]}</h3><p style="margin:0;color:#b9bdc4">{o[1]}</p></div>'
        for i, o in enumerate(s["options"])
    )
    ideal = "".join(f'<li><b>{h}.</b> {t}</li>' for h, t in s["ideal"])
    faq = "".join(f'<details><summary>{q}</summary><div class="ans">{an}</div></details>' for q, an in s["faq"])
    paras = "".join(f"<p class=\"lead\">{t}</p>" for t in s["intro"])
    if s.get("no_photos"):
        gal = f'''<div class="card reveal" style="max-width:720px"><div class="ico">{ICON["ig"]}</div><h3>Ejemplos en Instagram</h3><p style="color:#b9bdc4">{s["no_photos_text"]}</p><a class="btn btn-ghost" href="https://www.instagram.com/{s["ig"]}/" target="_blank" rel="noopener">@{s["ig"]}</a></div>'''
    else:
        gal = f'<div class="masonry reveal" data-lightbox="sty">{shots(s["gallery"], "sty")}</div>'
    rel = "".join(f'<a class="style-card reveal d{i}" href="{x["slug"]}.html">{img(x["card"])}<div class="in"><span class="num">0{i + 1}</span><h3>{x["nav"]}</h3><p>{x["card_text"]}</p><span class="pill">Ver más</span></div></a>' for i, x in enumerate(others[:4]))
    hero = page_hero(f'<a href="tatuajes.html">Tatuajes</a><span>/</span>{s["nav"]}', s["title"], s["lead"], s["hero"], eyebrow=s["kicker"],
                     extra=f'<div class="btn-row" style="margin-top:26px"><a class="btn btn-primary" href="{wa("Hola, me interesa " + s["topic"] + " en La Cara Norte.")}" target="_blank" rel="noopener">{ICON["wa"]} Pedir cita</a><a class="btn btn-ghost" href="{a["slug"]}.html">Conoce a {a["short"]}</a></div>')
    body = f'''{hero}
<section class="sec on-light has-leaves">
  {leaves("tr")}
  <div class="wrap split">
    <div class="reveal"><p class="eyebrow">El estilo</p><h2 class="split-words">Todo lo que conviene saber</h2>{paras}</div>
    <div class="reveal d1"><div class="frame">{img(s["card"], big=True)}</div></div>
  </div>
</section>
<section class="sec sec-anth grain">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">{s["options_title"]}</p><h2>{s["nav"]} <span class="serif accent">en detalle</span></h2></div>
    <div class="grid g4">{opts}</div>
  </div>
</section>
<section class="sec on-light alt has-leaves">
  {leaves("bl")}
  <div class="wrap split">
    <div class="reveal"><p class="eyebrow">{s["ideal_title"]}</p><h2>Cuándo <span class="serif accent">encaja</span></h2>
      <ul class="leaf-list" style="color:#3b4047">{ideal}</ul></div>
    <div class="reveal d1"><div class="faq">{faq}</div></div>
  </div>
</section>
{reel_section(s["artist"], 1) if s["slug"] in ("neotradicional", "realismo") else ""}
<section class="sec sec-dark grain">
  <div class="wrap split">
    <div class="reveal"><p class="eyebrow">Quién lo hace</p><h2>{a["name"]}</h2><p class="role serif accent" style="font-size:1.4rem;margin:0 0 14px">{a["role"]}</p><p class="lead">{a["teaser"]}</p>
      <div class="btn-row"><a class="btn btn-primary" href="{a["slug"]}.html">Ver su portfolio</a><a class="btn btn-ghost" href="https://www.instagram.com/{a["ig"]}/" target="_blank" rel="noopener">@{a["ig"]}</a></div></div>
    <div class="reveal d1"><div class="frame">{img(a["card"], big=True)}</div></div>
  </div>
</section>
<section class="sec sec-carbon">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Galería</p><h2>Trabajos de {s["nav"].lower()}</h2></div>
    {gal}
  </div>
</section>
<section class="sec on-light">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Sigue explorando</p><h2>Más estilos</h2></div>
    <div class="grid g4">{rel}</div>
  </div>
</section>
{cta_final("Pide tu cita", "Cuéntanos tu idea, la zona del cuerpo y el tamaño aproximado. Con una foto de referencia, mejor.", (s["gallery"] * 6)[:6])}'''
    page(s["slug"] + ".html", re_title(s), f'{re_title(s)} en La Cara Norte Custom Tattoo, León: qué define el estilo, cuándo encaja, preguntas frecuentes y cómo pedir cita con {a["short"]}.', body, og_img=s["hero"])



def build_belly():
    hero = page_hero("Belly painting", "Belly <span class='serif accent'>painting</span>", "Un recuerdo único de tu embarazo: pintura artística sobre la tripa, con un diseño pensado para ti y para tu bebé.", None, eyebrow="Nuevo servicio",
                     extra=f'<div class="btn-row" style="margin-top:26px"><a class="btn btn-primary" href="{wa("Hola, me interesa el belly painting en La Cara Norte.")}" target="_blank" rel="noopener">{ICON["wa"]} Consultar</a><a class="btn btn-ghost" href="contacto.html#cita">Formulario de cita</a></div>')
    ideas = "".join(f'<div class="card reveal d{i % 4}"><p class="num">0{i + 1}</p><h3>{t}</h3><p style="margin:0;color:#b9bdc4">{d}</p></div>' for i, (t, d) in enumerate([
        ("Animales y flores", "Diseños tiernos con animalitos y flores, como el ciervo con flores moradas que se ve en su Instagram."),
        ("El nombre del bebé", "Puede incluir su nombre o iniciales con caligrafía a mano."),
        ("A tu medida", "Colores, motivos y estilo se hablan contigo antes de pintar."),
        ("Recuerdo con foto", "Una imagen para guardar o compartir: ideal para una sesión de fotos o un baby shower."),
    ]))
    faq = "".join(f'<details><summary>{q}</summary><div class="ans">{a}</div></details>' for q, a in [
        ("¿Es un tatuaje?", "No. Es pintura artística sobre la piel, no se tatúa: es temporal y se retira con el tiempo."),
        ("¿Es seguro durante el embarazo?", "Pregunta al estudio qué materiales utiliza, y consulta con tu matrona o médico si tienes dudas o la piel sensible."),
        ("¿Cuánto dura?", "Al ser pintura, no es permanente. El tiempo depende de tu piel y de los cuidados; te lo explican al hacerlo."),
        ("¿Cuándo es mejor hacerlo?", "Suele hacerse cuando la tripa ya está bien marcada. Cuéntanos de cuántas semanas estás y te orientamos."),
        ("¿Cuánto cuesta?", "Se presupuesta según el diseño. Escríbenos con tu idea y te lo decimos."),
    ])
    body = hero + f'''
<section class="sec on-light has-leaves">
  {leaves("tr")}
  <div class="wrap split">
    <div class="reveal"><p class="eyebrow">De qué va</p><h2 class="split-words">Arte para esta etapa tan especial</h2>
      <p class="lead">El belly painting convierte la tripa de embarazada en un pequeño lienzo. Es una forma bonita y distinta de celebrar el embarazo, y queda precioso en fotos.</p>
      <p class="lead">Es un servicio nuevo en La Cara Norte: lo anuncian en su Instagram como «Nuevo servicio». Para ver ejemplos reales, mira su destacado «Belly Painting».</p>
      <a class="btn btn-ghost" href="{SITE["ig"]}" target="_blank" rel="noopener">{ICON["ig"]} Ver en Instagram</a></div>
    <div class="reveal d1"><div class="card" style="text-align:center;padding:50px 30px;background:var(--carbon);border-color:transparent;color:var(--white)"><img src="assets/img/logo/logo-512.png" alt="Logotipo de La Cara Norte" width="200" height="200" style="margin:0 auto 18px;width:200px"><p class="serif accent" style="font-size:1.6rem;margin:0">Un recuerdo único</p></div></div>
  </div>
</section>
<section class="sec sec-anth grain">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Ideas</p><h2>Qué se puede <span class="serif accent">pintar</span></h2></div>
    <div class="grid g4">{ideas}</div>
  </div>
</section>
<section class="sec on-light alt">
  <div class="wrap" style="max-width:900px">
    <div class="sec-head reveal"><p class="eyebrow">Dudas</p><h2>Preguntas habituales</h2></div>
    <div class="faq reveal">{faq}</div>
  </div>
</section>''' + cta_final("Reserva tu belly painting", "Escríbenos con tus semanas de embarazo y lo que se te ocurre. Te contamos cómo hacerlo y cuándo.")
    page("belly-painting.html", "Belly painting en León", "Belly painting en León: pintura artística sobre la tripa de embarazada. Nuevo servicio de La Cara Norte Custom Tattoo.", body)


def build_tienda():
    hero = page_hero("Tienda", "Tienda y <span class='serif accent'>tarjetas regalo</span>", "Llévate un trozo de La Cara Norte o regala tinta a quien tú sabes.", None, eyebrow="Merchandising",
                     extra=f'<div class="btn-row" style="margin-top:26px"><a class="btn btn-primary" href="{wa("Hola, quería información sobre la tienda de La Cara Norte.")}" target="_blank" rel="noopener">{ICON["wa"]} Pedir por WhatsApp</a></div>')
    body = hero + f'''
<section class="sec on-light has-leaves" id="tarjetas">
  {leaves("tr")}
  <div class="wrap split">
    <div class="reveal"><p class="eyebrow">Tarjetas regalo</p><h2 class="split-words">Regala <span class="serif accent">tinta</span></h2>
      <p class="lead">Una tarjeta física, negra con el logo del estudio y una cinta roja, con un espacio para escribir el importe que quieras regalar. Sirve para un tatuaje o un piercing.</p>
      <ul class="leaf-list" style="color:#3b4047;margin-bottom:28px">
        <li>Eliges el importe.</li>
        <li>Se pide por WhatsApp o en el estudio.</li>
        <li>La persona elige artista y estilo cuando quiera, dentro de la disponibilidad.</li>
      </ul>
      <a class="btn btn-primary" href="{wa("Hola, quería una tarjeta regalo de La Cara Norte.")}" target="_blank" rel="noopener">{ICON["gift"]} Pedir una tarjeta regalo</a></div>
    <div class="reveal d1"><div class="card" style="text-align:center;padding:50px 30px;background:var(--carbon);border-color:transparent;color:var(--white)"><div class="ico" style="margin-inline:auto">{ICON["gift"]}</div><img src="assets/img/logo/logo-512.png" alt="" width="180" height="180" style="margin:0 auto 14px;width:180px"><p class="serif accent" style="font-size:1.5rem;margin:0">Tarjeta regalo</p></div></div>
  </div>
</section>
<section class="sec sec-anth grain" id="merch">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Merchandising</p><h2 class="split-words">Con el sello de <span class="serif accent">La Cara Norte</span></h2><p class="lead">Lo que han mostrado en su Instagram. Pregunta disponibilidad y tallas por WhatsApp.</p></div>
    <div class="grid g3">
      <div class="card reveal"><div class="ico">{ICON["shirt"]}</div><span class="stamp" style="margin-bottom:14px">Promo · 5 €</span><h3>Totebag «Primavera»</h3><p style="color:#b9bdc4">Bolsa de tela negra con ilustración blanca de La Cara Norte. En promoción a 5 € según su Instagram; confirma disponibilidad.</p><a class="link-arrow" href="{wa("Hola, quería una totebag de La Cara Norte.")}" target="_blank" rel="noopener">Pedir</a></div>
      <div class="card reveal d1"><div class="ico">{ICON["shirt"]}</div><h3>Camisetas</h3><p style="color:#b9bdc4">Camisetas nuevas con ilustraciones del estudio. Se piden por mensaje directo: «¿Quieres una? Mándanos un DM».</p><a class="link-arrow" href="{wa("Hola, quería una camiseta de La Cara Norte.")}" target="_blank" rel="noopener">Pedir</a></div>
      <div class="card reveal d2"><div class="ico">{ICON["spray"]}</div><h3>Próximas ediciones</h3><p style="color:#b9bdc4">El estudio saca ediciones por temporada. Síguelos en Instagram para enterarte primero.</p><a class="link-arrow" href="{SITE["ig"]}" target="_blank" rel="noopener">Instagram</a></div>
    </div>
  </div>
</section>
<section class="sec on-light">
  <div class="wrap" style="max-width:900px">
    <div class="sec-head reveal"><p class="eyebrow">Cómo pedir</p><h2>Es muy sencillo</h2></div>
    <ol class="leaf-list reveal" style="color:#3b4047"><li><b>Escríbenos</b> por WhatsApp o Instagram con lo que quieres.</li><li><b>Confirmamos</b> disponibilidad, talla y precio.</li><li><b>Lo recoges</b> en el estudio, en horario de lunes a viernes de 10:00 a 18:00.</li></ol>
  </div>
</section>''' + cta_final("¿Algo para ti o para regalar?")
    page("tienda.html", "Tienda y tarjetas regalo", "Totebag, camisetas y tarjetas regalo de La Cara Norte Custom Tattoo, León. Pídelo por WhatsApp.", body)


def build_equipo():
    hero = page_hero("Equipo", "Cuatro artistas, <span class='serif accent'>cuatro miradas</span>", "Conoce a quienes dan vida a tu idea. Cada uno tiene su portfolio, su estilo y su propia página.", "luis-03")
    team = f'<section class="sec sec-dark grain"><div class="wrap"><div class="grid g4">{"".join(artist_card(k) for k in ORDER)}</div></div></section>'
    guest = f'''
<section class="sec on-light">
  <div class="wrap split">
    <div class="reveal"><p class="eyebrow">Invitados</p><h2>Guest spots y <span class="serif accent">visitas</span></h2>
      <p class="lead">A lo largo del año pasan por el estudio tatuadores invitados. Lo anunciamos primero en Instagram, con fechas y estilo. Si quieres reservar con un invitado, escríbenos con tiempo: las agendas vuelan.</p>
      <a class="btn btn-primary" href="{SITE["ig"]}" target="_blank" rel="noopener">Seguir en Instagram</a></div>
    <div class="reveal d1"><div class="frame">{img("studio-02", big=True)}</div></div>
  </div>
</section>'''
    rows = "".join(
        f'<tr><td><a href="{ARTISTS[k]["slug"]}.html">{ARTISTS[k]["name"]}</a></td><td>{ARTISTS[k]["role"]}</td><td>{ARTISTS[k]["topic"].capitalize()}</td><td>{ARTISTS[k]["cities"]}</td><td><a class="accent" href="https://www.instagram.com/{ARTISTS[k]["ig"]}/" target="_blank" rel="noopener">@{ARTISTS[k]["ig"]}</a></td></tr>'
        for k in ORDER
    )
    compare = f'''
<section class="sec on-light alt has-leaves">
  {leaves("br")}
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">De un vistazo</p><h2>¿Quién hace <span class="serif accent">qué</span>?</h2></div>
    <div class="table-wrap reveal"><table class="compare"><thead><tr><th>Artista</th><th>Estilos</th><th>Ideal para</th><th>Dónde</th><th>Instagram</th></tr></thead><tbody>{rows}</tbody></table></div>
  </div>
</section>'''
    body = hero + team + compare + finder_section() + guest + cta_final()
    page("equipo.html", "El equipo", "Luis Santos, Guille Martink, María y Paulix: los cuatro artistas de La Cara Norte Custom Tattoo en León.", body, og_img="luis-03")


def finder_section():
    return f'<section class="sec sec-carbon"><div class="wrap" style="max-width:1000px">{finder()}</div></section>'


def build_artist(k):
    a = ARTISTS[k]
    others = [x for x in ORDER if x != k]
    feats = "".join(f'<span class="pill {"green" if k == "paulix" else ""}">{s}</span>' for s in a["styles"])
    hl = "".join(f'<span class="pill">{h}</span>' for h in a["hl"])
    theme = "theme-green" if k == "paulix" else ""
    hero = page_hero(f'<a href="equipo.html">Equipo</a><span>/</span>{a["name"]}', a["name"], a["role"].replace(" · ", " · "), a["hero"], extra=f'<div class="btn-row" style="margin-top:26px"><a class="btn btn-primary" href="{wa("Hola, me gustaría pedir cita con " + a["name"] + " en La Cara Norte.")}" target="_blank" rel="noopener">{ICON["wa"]} Pedir cita con {a["short"]}</a><a class="btn btn-ghost" href="https://www.instagram.com/{a["ig"]}/" target="_blank" rel="noopener">@{a["ig"]}</a></div>')
    body = f'''<div class="{theme}">{hero}
<section class="sec sec-dark grain">
  <div class="wrap split">
    <div class="reveal"><div class="frame">{img(a["card"], big=True)}</div></div>
    <div class="reveal d1">
      <p class="eyebrow">Sobre {a["short"]}</p><h2>{a["role"].split(" · ")[0]}, <span class="serif accent">a su manera</span></h2>
      <p class="lead">{a["intro"]}</p>
      <div class="tag-list" style="margin:0 0 24px"><div class="pills">{feats}</div></div>
      <div class="stat-row">
        <div><b>{len(a["styles"])}</b><span>Especialidades</span></div>
        <div><b>{len(a["works"])}</b><span>Trabajos aquí</span></div>
        <div><b>{a["followers"]}</b><span>Seguidores</span></div>
        <div><b>{a["cities"].split(" · ")[0]}</b><span>Base</span></div>
      </div>
      <p style="margin:0 0 14px"><a class="link-arrow" href="https://www.instagram.com/{a["ig"]}/" target="_blank" rel="noopener">@{a["ig"]} en Instagram</a></p>
      <p style="margin-top:14px;color:#aeb2b9;font-size:.95rem">{a["extra"]}</p>
    </div>
  </div>
</section>
{reel_section(k) if k in REELS else ""}
<section class="sec sec-carbon">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Portfolio</p><h2>Trabajos de {a["short"]}</h2><p class="lead">Fotos publicadas en su perfil de Instagram. Pulsa para ampliar.</p></div>
    <div class="masonry reveal" data-lightbox="{k}">{shots(a["works"], k)}</div>
    <div style="margin-top:40px"><p class="eyebrow">En su Instagram, además</p><div class="pills">{hl}</div></div>
  </div>
</section>
<section class="sec on-light has-leaves">
  {leaves("tr")}
  <div class="wrap split" style="margin-bottom:clamp(50px,8vw,90px)">
    <div class="reveal"><p class="eyebrow">Pedir cita con {a["short"]}</p><h2>Tres pasos, <span class="serif accent">sin complicaciones</span></h2>
      <ol class="leaf-list" style="color:#3b4047">
        <li><b>Escríbenos</b> por WhatsApp o desde el formulario indicando que quieres a {a["short"]}.</li>
        <li><b>Cuéntale tu idea</b>: referencias, zona del cuerpo y tamaño aproximado.</li>
        <li><b>Confirmamos fecha</b> dentro del horario del estudio (en julio y agosto, solo con cita).</li>
      </ol>
      <div class="btn-row" style="margin-top:28px"><a class="btn btn-primary" href="{wa("Hola, me gustaría pedir cita con " + a["name"] + " en La Cara Norte.")}" target="_blank" rel="noopener">{ICON["wa"]} Pedir cita con {a["short"]}</a><a class="btn btn-ghost" href="contacto.html#cita">Formulario</a></div>
    </div>
    <div class="reveal d1"><div class="frame">{img(a["works"][1] if len(a["works"]) > 1 else a["card"], big=True)}</div></div>
  </div>
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">El resto del equipo</p><h2>Conoce a los demás</h2></div>
    <div class="grid g3">{"".join(artist_card(x) for x in others)}</div>
  </div>
</section>
{cta_final("Pide cita con " + a["short"], "Cuéntanos tu idea, la zona del cuerpo y el tamaño aproximado. Con una foto de referencia, mejor.", a["works"][:6] if len(a["works"]) >= 6 else None)}
</div>'''
    page(a["slug"] + ".html", a["name"], f'{a["name"]} — {a["role"]} en La Cara Norte Custom Tattoo, León. Portfolio y cómo pedir cita.', body, og_img=a["hero"])


def build_galeria():
    order = []
    # intercalado para ritmo visual
    lists = [ARTISTS[k]["works"] for k in ORDER]
    for i in range(max(map(len, lists))):
        for l in lists:
            if i < len(l) and l[i] not in order:
                order.append(l[i])
    for k in W:
        if k not in order and W[k][2]:
            order.append(k)
    hero = page_hero("Galería", "Galería de <span class='serif accent'>trabajos</span>", f"{len(order)} piezas reales publicadas por nuestros artistas. Filtra por estilo y amplía cualquier foto.", "guille-04")
    body = hero + f'''
<section class="sec sec-dark">
  <div class="wrap">
    <div class="filters" role="group" aria-label="Filtrar por estilo">
      <button class="filter active" aria-pressed="true" data-filter="all">Todo</button>
      <button class="filter" aria-pressed="false" data-filter="color">Color · neotradicional · anime</button>
      <button class="filter" aria-pressed="false" data-filter="bng">Realismo · black & grey</button>
      <button class="filter" aria-pressed="false" data-filter="fine">Fine line · dotwork</button>
      <button class="filter" aria-pressed="false" data-filter="pierc">Piercing · gemas</button>
    </div>
    <div class="masonry" data-lightbox="all">{shots(order, "all")}</div>
    <p style="margin-top:44px;color:#aeb2b9">¿Quieres ver más? Todo el trabajo reciente está en <a class="accent" href="{SITE["ig"]}" target="_blank" rel="noopener">@lacaranorte.tattoo</a> y en los perfiles de cada artista.</p>
  </div>
</section>''' + cta_final()
    page("galeria.html", "Galería de tatuajes y piercing", "Galería de trabajos reales de La Cara Norte: neotradicional, anime, realismo, black & grey, fine line y piercing.", body, og_img="guille-04")


def build_estudio():
    hero = page_hero("El estudio", "Un estudio, <span class='serif accent'>muchas formas</span> de tinta", "Custom tattoo & graffiti en el barrio de La Palomera. Abrimos en 2021 con una idea simple: trabajar cada pieza como si fuera única.", "guille-10")
    vals = f'''
<section class="sec sec-dark grain">
  <div class="wrap split">
    <div class="reveal"><p class="eyebrow">Nuestra historia</p><h2>Desde 2021, en <span class="serif accent">La Palomera</span></h2>
      <p class="lead">La Cara Norte nació en León como un estudio de tatuaje a medida y con raíces en el graffiti. Hoy reunimos a cuatro artistas de estilos muy distintos (color, realismo, línea fina y piercing) que comparten una forma de trabajar: escuchar primero, diseñar contigo y cuidar cada detalle.</p>
      <p style="color:#aeb2b9">Nuestro estudio está en la calle Posadera Aldonza, 3. Si pasas por el barrio, ven a conocernos.</p></div>
    <div class="reveal d1 frame-stack"><div class="frame">{img("guille-06", big=True)}</div>{img("maria-09", "b")}</div>
  </div>
</section>
<section class="sec green-band has-leaves">
  {leaves("tr")}
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Ambiente</p><h2>Un sitio <span class="serif" style="color:var(--green)">tranquilo</span> para tatuarte</h2><p class="lead">Fachada de ladrillo, paredes grises con láminas enmarcadas, un espejo blanco ornamentado y alguna planta verde. Un espacio cuidado y sin prisas, con gente que te explica cada paso.</p><span class="stamp">Amigable con el colectivo LGBTQ+</span></div>
  </div>
</section>
<section class="sec on-light">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Lo que nos define</p><h2>Cómo trabajamos</h2></div>
    <div class="grid g3">
      <div class="card reveal"><div class="ico">{ICON["pen"]}</div><h3>Diseño a medida</h3><p>Nada de plantillas: cada tatuaje se dibuja a partir de tu idea y de tu piel.</p></div>
      <div class="card reveal d1"><div class="ico">{ICON["heart"]}</div><h3>Trato cercano</h3><p>Es lo que más repiten nuestras reseñas: sentirse cómodo, escuchado y tranquilo.</p></div>
      <div class="card reveal d2"><div class="ico">{ICON["shield"]}</div><h3>Higiene</h3><p>Material de un solo uso, superficies desinfectadas y explicaciones claras de los cuidados.</p></div>
      <div class="card reveal"><div class="ico">{ICON["spray"]}</div><h3>Raíz graffiti</h3><p>Nos gusta el color, el trazo y la calle. Es parte de nuestra identidad.</p></div>
      <div class="card reveal d1"><div class="ico">{ICON["leaf"]}</div><h3>Ambiente acogedor</h3><p>Un espacio tranquilo, amigable con el colectivo LGBTQ+ y pensado para primeras veces.</p></div>
      <div class="card reveal d2"><div class="ico">{ICON["gem"]}</div><h3>Piercing y gemas</h3><p>Perforaciones con marcado previo y joyería fina, además de gemas dentales.</p></div>
    </div>
  </div>
</section>
<section class="sec sec-anth grain">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Y además</p><h2>Más allá del tatuaje</h2></div>
    <div class="grid g4">
      <div class="card reveal"><div class="ico">{ICON["gift"]}</div><h3>Tarjetas regalo</h3><p style="color:#b9bdc4">Regala tinta o piercing a quien tú sabes. Pídenos tu tarjeta por WhatsApp. <a class="accent" href="tienda.html#tarjetas">Ver más</a>.</p></div>
      <div class="card reveal d1"><div class="ico">{ICON["shirt"]}</div><h3>Merchandising</h3><p style="color:#b9bdc4">Totebag «Primavera» y camisetas con el sello de La Cara Norte. <a class="accent" href="tienda.html#merch">Ver más</a>.</p></div>
      <div class="card reveal d2"><div class="ico">{ICON["pen"]}</div><h3>Belly painting</h3><p style="color:#b9bdc4">Nuevo servicio: pintura artística sobre la tripa de embarazada. <a class="accent" href="belly-painting.html">Ver más</a>.</p></div>
      <div class="card reveal d3"><div class="ico">{ICON["heart"]}</div><h3>Cover up</h3><p style="color:#b9bdc4">Reformamos o tapamos tatuajes antiguos. Cuéntanos tu caso con una foto.</p></div>
    </div>
  </div>
</section>
<section class="sec on-light alt">
  <div class="wrap">
    <div class="rating-big reveal"><b>5,0</b><div><div class="stars" aria-hidden="true">★★★★★</div><p style="margin:6px 0 0">120 opiniones en Google</p></div></div>
    <div class="grid g3">{reviews_block(6)}</div>
  </div>
</section>''' + cta_final("Ven a conocernos")
    body = hero + vals
    page("estudio.html", "El estudio", "Conoce La Cara Norte Custom Tattoo: estudio de tatuajes, piercing y graffiti en el barrio de La Palomera, León, abierto desde 2021.", body, og_img="guille-06")


def build_primera_vez():
    hero = page_hero("Tu primera vez", "Tu primera vez, <span class='serif accent'>sin nervios</span>", "Todo lo que conviene saber antes, durante y después de tu cita. Pensado para que llegues tranquilo y te lleves a casa un tatuaje que cuidar con cariño.", "maria-02")
    steps = '''
<section class="sec sec-dark grain">
  <div class="wrap">
    <div class="sec-head reveal"><p class="eyebrow">Paso a paso</p><h2>Cómo es el proceso</h2></div>
    <div class="steps">
      <div class="step reveal"><h3>1 · Escríbenos</h3><p>Por WhatsApp, Instagram o desde la web. Cuéntanos qué quieres, dónde y cuánto de grande. Adjunta referencias.</p></div>
      <div class="step reveal d1"><h3>2 · Propuesta</h3><p>El artista que mejor encaja te prepara una propuesta y te da una idea clara de tiempo y precio.</p></div>
      <div class="step reveal d2"><h3>3 · Cita</h3><p>Fijamos fecha dentro del horario del estudio (lunes a viernes de 10:00 a 18:00).</p></div>
      <div class="step reveal d3"><h3>4 · Sesión</h3><p>Repasamos el diseño, lo colocamos sobre tu piel y tatuamos con calma. Al final te explicamos los cuidados.</p></div>
    </div>
  </div>
</section>'''
    prep = f'''
<section class="sec on-light">
  <div class="wrap split">
    <div class="reveal"><p class="eyebrow">Antes de tu cita</p><h2>Prepárate <span class="serif accent">sin complicarte</span></h2>
      <ul class="leaf-list" style="color:#3b4047;font-size:1.02rem">
        <li><b>Come bien</b> y descansa la noche anterior.</li>
        <li><b>Hidrata la piel</b> los días previos y evita el sol en la zona.</li>
        <li><b>Evita el alcohol</b> el día antes y el mismo día.</li>
        <li><b>Ropa cómoda</b> que deje accesible la zona a tatuar.</li>
        <li><b>Avísanos</b> de alergias, medicación o cualquier condición de salud.</li>
        <li><b>Trae referencias</b> y tus dudas. Cuanto más claro, mejor sale.</li>
      </ul>
    </div>
    <div class="reveal d1"><div class="frame">{img("maria-09", big=True)}</div></div>
  </div>
</section>
<section class="sec sec-carbon">
  <div class="wrap split rev">
    <div class="reveal"><div class="frame">{img("luis-05", big=True)}</div></div>
    <div class="reveal d1"><p class="eyebrow">Después de tu cita</p><h2>Cuida tu <span class="serif accent">tatuaje</span></h2>
      <p class="lead">Estas son pautas generales habituales. Tu artista te dará instrucciones concretas para tu pieza el mismo día de la sesión.</p>
      <ul class="leaf-list" style="color:#cfd2d7">
        <li>Lava con agua tibia y jabón neutro, sin frotar, y seca a toquecitos.</li>
        <li>Aplica una capa fina de crema cicatrizante según te indiquen.</li>
        <li>No te rasques ni arranques costras.</li>
        <li>Evita sol directo, piscina, mar y saunas mientras cicatriza.</li>
        <li>Si notas algo raro (calor, pus, fiebre), escríbenos o consulta a un médico.</li>
      </ul>
    </div>
  </div>
</section>'''
    faq = '''
<section class="sec on-light alt">
  <div class="wrap" style="max-width:900px">
    <div class="sec-head reveal"><p class="eyebrow">Dudas frecuentes</p><h2>Preguntas habituales</h2></div>
    <div class="faq reveal">
      <details><summary>¿Duele?</summary><div class="ans">Depende de la zona, del tipo de trabajo y de cada persona. Las costillas o el esternón suelen molestar más que el antebrazo, por ejemplo. Una de nuestras clientas cuenta que «apenas ha dolido» con María. Te orientamos según tu caso.</div></details>
      <details><summary>¿Cuánto tarda una sesión?</summary><div class="ans">Una pieza pequeña puede resolverse en una hora; mangas, espaldas o piernas completas requieren varias sesiones. Lo concretamos al preparar tu propuesta.</div></details>
      <details><summary>¿Puedo venir sin cita?</summary><div class="ans">Lo mejor es escribir antes. De lunes a viernes de 10:00 a 18:00 atendemos consultas; en julio y agosto no atendemos visitas sin cita previa.</div></details>
      <details><summary>¿Y si soy menor de edad?</summary><div class="ans">Para menores es necesaria la autorización de madre, padre o tutor y el cumplimiento de la normativa vigente. Consúltanos antes de reservar.</div></details>
      <details><summary>¿Puedo tatuarme si estoy tomando medicación?</summary><div class="ans">Cuéntanoslo al pedir cita. Algunas medicaciones o condiciones requieren consultar antes con un profesional sanitario.</div></details>
      <details><summary>¿Cómo pago?</summary><div class="ans">Te informamos de las formas de pago al preparar tu propuesta. Escríbenos y te lo confirmamos.</div></details>
    </div>
  </div>
</section>'''
    body = hero + steps + prep + faq + cta_final("¿Lista o listo para empezar?")
    page("primera-vez.html", "Tu primera vez: guía y cuidados", "Guía para tu primer tatuaje o piercing en La Cara Norte León: cómo es el proceso, preparación, cuidados y preguntas frecuentes.", body, og_img="maria-02")


def build_contacto():
    hero = page_hero("Contacto", "Hablemos de <span class='serif accent'>tu idea</span>", "La forma más rápida de pedir cita es WhatsApp. También puedes rellenar este formulario y te abrimos el chat con todo ya escrito.", "luis-09")
    form = f'''
<section class="sec sec-dark grain" id="cita">
  <div class="wrap split" style="align-items:start">
    <div class="reveal">
      <p class="eyebrow">Solicitud de cita</p><h2>Cuéntanos <span class="serif accent">qué quieres</span></h2>
      <p class="lead">Rellena lo que sepas y pulsa el botón: se abrirá WhatsApp con tu mensaje listo. Después solo tienes que adjuntar tus fotos de referencia.</p>
      <div class="note">{ICON["info"]}<span>Julio y agosto: solo con cita previa. El resto del año atendemos de lunes a viernes de 10:00 a 18:00.</span></div>
      <p style="margin-top:28px"><b>Prefieres hablar</b></p>
      <p><a class="accent" href="{wa()}" target="_blank" rel="noopener">WhatsApp {SITE["wa_pretty"]}</a><br><a href="tel:{SITE["tel"]}">Teléfono {SITE["tel_pretty"]}</a><br><a href="mailto:{SITE["mail"]}">{SITE["mail"]}</a><br><a href="{SITE["ig"]}" target="_blank" rel="noopener">@lacaranorte.tattoo</a></p>
    </div>
    <form class="form reveal d1 card" data-wa-form>
      <div class="row"><div class="field"><label for="nombre">Tu nombre</label><input id="nombre" name="nombre" autocomplete="given-name" required></div>
      <div class="field"><label for="servicio">Servicio</label><select id="servicio" name="servicio" required><option>Tatuaje</option><option>Piercing</option><option>Gemas dentales</option><option>Cover up</option><option>Tarjeta regalo</option><option>Otra consulta</option></select></div></div>
      <div class="row"><div class="field"><label for="artista">Artista</label><select id="artista" name="artista"><option value="">Me da igual / aconsejadme</option><option>Luis Santos (neotradicional, anime)</option><option>Guille Martink (realismo, black & grey)</option><option>María (fine line, dotwork)</option><option>Paulix (piercing, gemas)</option></select></div>
      <div class="field"><label for="zona">Zona del cuerpo</label><input id="zona" name="zona" placeholder="Antebrazo, oreja…"></div></div>
      <div class="row"><div class="field"><label for="tamano">Tamaño aproximado</label><input id="tamano" name="tamano" placeholder="Ej. 10 cm"></div>
      <div class="field"><label for="fecha">¿Cuándo te viene bien?</label><input id="fecha" name="fecha" placeholder="Mañanas, octubre…"></div></div>
      <div class="field"><label for="idea">Tu idea</label><textarea id="idea" name="idea" placeholder="Cuéntanos qué quieres y qué significa para ti"></textarea><span class="hint">No se envía nada a ningún servidor: solo se abre WhatsApp con tu mensaje.</span></div>
      <button class="btn btn-wa" type="submit">{ICON["wa"]} Enviar por WhatsApp</button>
    </form>
  </div>
</section>'''
    info = f'''
<section class="sec on-light">
  <div class="wrap split">
    <div class="reveal">
      <p class="eyebrow">Visítanos</p><h2>Dónde <span class="serif accent">estamos</span></h2>
      <p class="lead">{SITE["addr"]}, barrio de La Palomera.</p>
      <p class="open-status" data-open-status style="color:var(--carbon);font-size:1rem;margin-bottom:18px"><span class="status-dot" aria-hidden="true"></span><span class="status-text">Horario</span></p>
      {hours_table()}
      <div class="note" style="margin-top:22px">{ICON["info"]}<span>Durante julio y agosto no atendemos visitas sin cita previa. Escríbenos para concertarla.</span></div>
      <div class="btn-row" style="margin-top:26px"><a class="btn btn-primary" href="{SITE["maps"]}" target="_blank" rel="noopener">Abrir en Google Maps</a><a class="btn btn-ghost" href="tel:{SITE["tel"]}">Llamar</a></div>
    </div>
    <div class="map reveal d1" style="filter:grayscale(.4)"><iframe title="Mapa de La Cara Norte Custom Tattoo" src="{SITE["embed"]}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" allowfullscreen></iframe></div>
  </div>
</section>
<section class="sec sec-carbon">
  <div class="wrap">
    <div class="grid g4">
      <a class="card reveal" href="{wa()}" target="_blank" rel="noopener"><div class="ico">{ICON["wa"]}</div><h3>WhatsApp</h3><p style="margin:0;color:#b9bdc4">{SITE["wa_pretty"]}<br>La vía más rápida.</p></a>
      <a class="card reveal d1" href="{SITE["ig"]}" target="_blank" rel="noopener"><div class="ico">{ICON["ig"]}</div><h3>Instagram</h3><p style="margin:0;color:#b9bdc4">@lacaranorte.tattoo<br>Trabajos y huecos libres.</p></a>
      <a class="card reveal d2" href="mailto:{SITE["mail"]}"><div class="ico">{ICON["mail"]}</div><h3>Correo</h3><p style="margin:0;color:#b9bdc4;word-break:break-all">{SITE["mail"]}</p></a>
      <a class="card reveal d3" href="tel:{SITE["tel"]}"><div class="ico">{ICON["phone"]}</div><h3>Teléfono</h3><p style="margin:0;color:#b9bdc4">{SITE["tel_pretty"]}<br>En horario de estudio.</p></a>
    </div>
  </div>
</section>
<section class="sec on-light alt">
  <div class="wrap" style="max-width:900px">
    <div class="sec-head reveal"><p class="eyebrow">Antes de escribir</p><h2>Respuestas rápidas</h2></div>
    <div class="faq reveal">
      <details><summary>¿Cuánto tardáis en responder?</summary><div class="ans">Respondemos lo antes posible dentro del horario de atención (lunes a viernes, 10:00 a 18:00).</div></details>
      <details><summary>¿Qué datos necesitáis para un presupuesto?</summary><div class="ans">Una referencia o idea, la zona del cuerpo, el tamaño aproximado y, si es un cover up, una foto del tatuaje actual.</div></details>
      <details><summary>¿Puedo venir directamente?</summary><div class="ans">Mejor escríbenos antes. En julio y agosto no atendemos visitas sin cita previa.</div></details>
    </div>
  </div>
</section>'''
    body = hero + form + info
    page("contacto.html", "Contacto y cita", "Pide cita en La Cara Norte Custom Tattoo, León: WhatsApp 613 07 58 89, calle Posadera Aldonza 3. Horario de lunes a viernes de 10:00 a 18:00.", body, og_img="luis-09")


def legal(fname, title, desc, inner):
    body = f'''
<section class="sec sec-dark"><div class="wrap legal">
<p class="crumbs"><a href="index.html">Inicio</a><span>/</span>{title}</p>
<h1 style="font-size:clamp(2.2rem,5vw,3.6rem)">{title}</h1>
<p class="note" style="margin:0 0 26px">{ICON["info"]}<span>Borrador de demostración. Los datos marcados como <span class="pend">Pendiente</span> deben ser completados por el titular antes de publicar la web.</span></p>
{inner}</div></section>'''
    page(fname, title, desc, body)


def build_legal():
    legal("aviso-legal.html", "Aviso legal", "Aviso legal de la web de La Cara Norte Custom Tattoo.", f'''
<h2>Titular del sitio web</h2>
<p>Denominación: La Cara Norte Custom Tattoo<br>Titular / razón social: <span class="pend">Pendiente</span><br>NIF / CIF: <span class="pend">Pendiente</span><br>Domicilio: {SITE["addr"]}<br>Correo: {SITE["mail"]}<br>Teléfono: {SITE["wa_pretty"]}</p>
<h2>Objeto</h2><p>Este sitio web es una <b>demostración</b> y presenta los servicios de tatuaje, piercing y graffiti del estudio. No constituye una oferta contractual.</p>
<h2>Propiedad intelectual</h2><p>El logotipo, nombre comercial e imágenes de trabajos pertenecen a sus respectivos autores (La Cara Norte y sus artistas) y se usan en esta demo con fines ilustrativos, pendientes de autorización expresa antes de su publicación definitiva.</p>
<h2>Responsabilidad</h2><p>La información sobre cuidados es orientativa y no sustituye el consejo del artista ni de un profesional sanitario.</p>
<h2>Legislación</h2><p>Este aviso se rige por la legislación española (LSSI-CE).</p>''')
    legal("privacidad.html", "Política de privacidad", "Política de privacidad de la web de La Cara Norte Custom Tattoo.", f'''
<h2>Responsable</h2><p>La Cara Norte Custom Tattoo, {SITE["addr"]}. Contacto: {SITE["mail"]}. Titular y NIF: <span class="pend">Pendiente</span>.</p>
<h2>Qué datos tratamos</h2><p>Esta web <b>no almacena datos</b> ni envía formularios a ningún servidor. El formulario de cita solo compone un mensaje y abre WhatsApp en tu dispositivo; a partir de ahí, el tratamiento lo rige la política de WhatsApp y la del estudio al atender tu consulta.</p>
<h2>Finalidad y base jurídica</h2><p>Atender tu consulta y gestionar tu cita (consentimiento / ejecución de medidas precontractuales).</p>
<h2>Derechos</h2><p>Puedes ejercer tus derechos de acceso, rectificación, supresión, oposición, limitación y portabilidad escribiendo a {SITE["mail"]}. También puedes reclamar ante la Agencia Española de Protección de Datos.</p>
<h2>Servicios de terceros</h2><p>Esta web carga tipografías de Google Fonts y un mapa de Google Maps, lo que puede implicar el envío de tu IP a Google. Los reels de Instagram solo se cargan cuando pulsas «play»; en ese momento Instagram (Meta) puede recibir tu IP y colocar cookies.</p>''')
    legal("cookies.html", "Política de cookies", "Política de cookies de la web de La Cara Norte Custom Tattoo.", '''
<h2>Cookies propias</h2><p>Esta web no instala cookies propias. Usa <code>sessionStorage</code> únicamente para no repetir la animación de entrada durante la misma visita.</p>
<h2>Cookies de terceros</h2><p>El mapa incrustado de Google Maps, las tipografías de Google Fonts y, solo si pulsas «play», los reels de Instagram pueden establecer o leer cookies propias de Google y de Meta. Puedes configurarlas o bloquearlas desde tu navegador.</p>
<h2>Cómo desactivarlas</h2><p>Consulta la ayuda de tu navegador (Chrome, Firefox, Safari, Edge) para borrar o bloquear cookies.</p>''')


def build_404():
    body = f'''
<section class="sec sec-dark grain" style="text-align:center;min-height:60vh;display:grid;place-items:center">
<div class="wrap"><img src="assets/img/logo/logo-transparent.png" alt="" width="180" height="180" style="margin:0 auto 20px;width:180px">
<p class="eyebrow">Error 404</p><h1 style="font-size:clamp(2.4rem,6vw,4.5rem)">Esta página <span class="serif accent">no existe</span></h1>
<p class="lead" style="margin:0 auto 30px">Quizá el enlace ha cambiado. Vuelve al inicio o escríbenos y te ayudamos.</p>
<div class="btn-row" style="justify-content:center"><a class="btn btn-primary" href="index.html">Volver al inicio</a><a class="btn btn-ghost" href="contacto.html">Contacto</a></div></div></section>'''
    page("404.html", "Página no encontrada", "La página que buscas no existe.", body)


if __name__ == "__main__":
    build_index()
    build_tatuajes()
    build_piercing()
    for _s in SERVICES:
        build_service(_s)
    for _s in STYLES:
        build_style(_s)
    build_equipo()
    build_belly()
    build_tienda()
    for k in ORDER:
        build_artist(k)
    build_galeria()
    build_estudio()
    build_primera_vez()
    build_contacto()
    build_legal()
    build_404()
