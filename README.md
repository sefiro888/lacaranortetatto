# La Cara Norte Custom Tattoo · demostración web

Demo para **La Cara Norte Custom Tattoo** (C. Posadera Aldonza, 3 · 24007 León · barrio de La Palomera).
Web estática de 31 páginas, sin dependencias. Verla en local: `npx serve -l 5174 .` y abrir http://localhost:5174 (o abrir `index.html`).

> Es una **demo no oficial**: lleva una etiqueta «Demo», `noindex`, y los textos legales son borradores con datos «Pendiente».

## Páginas
| Página | Contenido |
|---|---|
| `index.html` | Portada: muro animado de trabajos + logo, marquee, estudio, estilos, equipo, buscador «¿qué artista?», galería, reseñas Google, proceso, horario en vivo y mapa |
| `tatuajes.html` | Neotradicional/anime, realismo, fine line, cover up, graffiti, guest spots, FAQ |
| `piercing.html` | Servicios de Paulix, galería con visor, cuidados |
| `equipo.html` | Los 4 artistas + buscador + guest spots |
| `luis-santos.html` · `guille-martink.html` · `maria.html` · `paulix.html` | Página propia por artista con portfolio y botón de cita por WhatsApp |
| `neotradicional.html` · `anime.html` · `realismo.html` · `blackwork-dotwork.html` · `fine-line.html` · `tatuajes-pequenos.html` · `cover-up.html` · `graffiti.html` | Una página por estilo de tatuaje: qué lo define, cuándo encaja, preguntas, quién lo hace y galería |
| `piercing-orejas.html` · `piercing-ombligo.html` · `gemas-dentales.html` · `joyeria.html` · `otros-piercings.html` | Una página por servicio de piercing: opciones, cicatrización orientativa, preguntas y galería |
| `belly-painting.html` · `tienda.html` | Nuevo servicio de belly painting; totebag, camisetas y tarjetas regalo (datos de los destacados de Instagram) |
| `galeria.html` | 42 trabajos con filtros y lightbox (teclado y swipe) |
| `estudio.html` | Historia, valores, extras (tarjetas regalo, merch, belly painting), reseñas |
| `primera-vez.html` | Proceso, preparación, cuidados y FAQ |
| `contacto.html` | Solicitud de cita → abre WhatsApp con el mensaje escrito, horario, mapa |
| `aviso-legal.html` · `privacidad.html` · `cookies.html` · `404.html` | Legales (borrador) y error |

## Regenerar
Las páginas se generan con `python _build/build.py` (contenido en `_build/data.py`). CSS en `assets/css/styles.css`, JS en `assets/js/main.js`.

## Datos verificados (07/10/2026)
- Google Maps: 5,0 ★ (120 reseñas), dirección, tel. 987 62 62 30, «amigable con LGBTQ+».
- WhatsApp 613 07 58 89 (el del propio negocio), correo lacaranortetattoo@gmail.com.
- Horario: L–V 10:00–18:00; julio y agosto solo con cita (mensaje automático de WhatsApp).
- Equipo y especialidades: bios y destacados de Instagram de @luiss.tattoo, @guillemartink, @aybar.rabya (María) y @paulix.piercing.

## Pendiente de confirmar con el cliente
Ver `ASSETS.md` (permisos de fotos) y `DESIGN.md` (textos genéricos que conviene validar: higiene, belly painting, merchandising, cuidados).

## Reels
Se cargan solo al pulsar play (`data-reel` en `assets/js/main.js`). Reel de Luis (DeJxzXMOQ5G): portada, `luis-santos.html`, `neotradicional.html`. Reel de Guille (DZNYtoqNHEg): portada, `guille-martink.html`, `realismo.html`. Se definen en `REELS` de `_build/build.py`.
