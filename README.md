# Web de Meta Technology Global, rediseño

Vista previa del rediseño de mtglobalpa.com. No toca el sitio en vivo (repo `mtg-pagina-web`).

## Páginas

- `index.html`: portada con el directorio de las tres líneas
- `medidor.html`: Medidor Inteligente, planes y precios
- `relojes.html`: catálogo de los 13 relojes con precio, existencias y funciones
- `telecom.html`: fibra, RF, data centers, equipos de prueba, PROSE

## Cambiar un precio, una existencia o una función de un reloj

1. Editar `datos/relojes.json`.
2. Correr `python3 herramientas/generar.py`.
3. Subir los cambios.

Los `.html` de la raíz se generan solos: los textos se editan en `fuente/` y se vuelve a correr el generador.

## Publicar en mtglobalpa.com

`python3 herramientas/generar.py --publicar` quita el aviso de vista previa y el `noindex`.
