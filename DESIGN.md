# Concepto de diseño

**Idea:** «tinta, cobre y carbón». Un estudio oscuro y editorial donde el trabajo real de los cuatro artistas es el protagonista; el cobre del logotipo sirve de acento y las secciones blancas actúan como «hoja de flash».

## Paleta (la que pidió el cliente)
| Token | Hex | Uso |
|---|---|---|
| `--black` | #0e0e10 | Hero, portfolio, pie |
| `--anthracite` | #2a2d32 | Cabecera, secciones alternas, buscador |
| `--copper` / `--copper-light` | #bf7440 / #e29c68 | Acento, botones, detalles. El logo original (dorado) se ha reteñido a cobre con `_build/make_logo.py` para respetar la paleta |
| `--white` | #f7f5f1 | Secciones claras y texto |
| `--green` | #9ccf86 | **Solo toque**: estado «abierto», viñetas de hoja, helechos decorativos, banda de ambiente, borde del pie, sellos |

## Tipografía
Oswald (títulos, mayúsculas) · Cormorant Garamond cursiva (acentos, eco del logo) · Inter (texto).

## Métodos reutilizados de otras demos
Barra superior con **abierto/cerrado en hora de Madrid**, marquee, splash de logo (una vez por sesión), reveal on scroll, contadores, **buscador «¿qué artista?»**, formulario que abre WhatsApp, galería filtrable con lightbox, CTA fija en móvil, enlace «saltar al contenido», `aria-current`, `prefers-reduced-motion`, 404 y legales borrador, `noindex` + etiqueta Demo.

## Textos genéricos a validar con el cliente
Higiene («material de un solo uso»), belly painting (pintura sobre barriga de embarazada), merchandising, tarjetas regalo, pautas de cuidados y fecha de apertura 2021 (sale del logotipo).

## Ritmo de secciones (portada)
Negro (hero) → blanco → antracita → blanco → antracita → negro → blanco → carbón → blanco → antracita → negro. Así los cuatro colores pesan parecido y el verde aparece como detalle.
