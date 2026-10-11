# Web de Meta Technology Global, rediseño

Vista previa del rediseño de mtglobalpa.com. No toca el sitio en vivo (repo `mtg-pagina-web`).
Tiene todo lo del sitio actual: unidades de negocio, catálogo con filtros, cotización y comparación,
servicios, PROSE, ShockWatch, Medidor Inteligente, relojes GPS, preguntas, contacto, inglés y modo oscuro.

## Páginas (en español en la raíz y en inglés en `en/`)

- `index.html`: portada
- `catalogo.html`: catálogo de equipos con buscador, filtros, cotización por WhatsApp y comparador
- `fibra-optica.html`, `rf-cobertura.html`, `infraestructura.html`, `data-centers.html`, `monitoreo-redes.html`: una por línea
- `medidor.html`: Medidor Inteligente, planes y precios
- `relojes.html`: los 13 relojes con precio, existencias y funciones
- `servicios.html`, `prose.html`, `shockwatch.html`

## Cómo se edita

- Precios, existencias o funciones de un reloj: `datos/relojes.json` (y `datos/relojes_en.json` para el inglés).
- Equipos del catálogo: `datos/productos.json`. Líneas de producto: `datos/lineas.json`.
- Textos de las páginas: `fuente/*.html`, con los dos idiomas así: `[[español||english]]`.

Después de editar, correr `python3 herramientas/generar.py` y subir los cambios.
Los `.html` de la raíz y de `en/` se generan solos: no se editan a mano.

## Publicar en mtglobalpa.com

La web oficial vive en el repositorio `mtg-pagina-web`: Cloudflare la despliega sola cada vez que se sube un cambio.
Para publicar lo que hay aquí:

    zsh herramientas/publicar.sh "Qué cambió"

El script arma la versión final (sin aviso de vista previa, sin `noindex`, con enlaces sin `.html`), la copia a
`mtg-pagina-web` y la sube. Este repositorio (`mtg-web-v2`) sigue siendo la vista previa en GitHub Pages.

Para volver a una versión anterior de la web oficial: `git revert` del commit correspondiente en `mtg-pagina-web`.
La página vieja de una sola hoja quedó en el commit `51c656f`.

## Fotos


- `img/fotos/` y `video/`: fotos y videos reales de MTG (salen de sus videos promocionales).
- `img/equipos/`: fotos oficiales de los fabricantes, guardadas en el sitio para no depender de sus servidores.
- `img/relojes/`: recortes de la lista de precios de los relojes.
- `img/prose/`: fotos del catálogo PROSE.
