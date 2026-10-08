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

`python3 herramientas/generar.py --publicar` quita el aviso de vista previa y el `noindex`.

## Fotos

- `img/fotos/` y `video/`: fotos y videos reales de MTG (salen de sus videos promocionales).
- `img/equipos/`: fotos oficiales de los fabricantes, guardadas en el sitio para no depender de sus servidores.
- `img/relojes/`: recortes de la lista de precios de los relojes.
- `img/prose/`: fotos del catálogo PROSE.
