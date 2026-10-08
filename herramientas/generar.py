"""Arma las páginas del sitio de MTG.

Lee las plantillas de fuente/, les pone la cabecera y el pie comunes, y construye
el catálogo de relojes desde datos/relojes.json. Escribe los .html en la raíz.

Uso:  python3 herramientas/generar.py            (vista previa, con noindex)
      python3 herramientas/generar.py --publicar (sin noindex, para mtglobalpa.com)
"""
import html
import json
import sys
from pathlib import Path
from urllib.parse import quote

RAIZ = Path(__file__).resolve().parent.parent
PUBLICAR = "--publicar" in sys.argv

DATOS = json.loads((RAIZ / "datos" / "relojes.json").read_text(encoding="utf-8"))
WA = DATOS["whatsapp"]
CATEGORIAS = {c["id"]: c for c in DATOS["categorias"]}
ORDEN_CAT = [c["id"] for c in DATOS["categorias"]]
MODELOS = sorted(DATOS["modelos"], key=lambda m: (ORDEN_CAT.index(m["categoria"]), m["precio"], m["modelo"]))

e = html.escape

ICONO_WA = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linejoin="round" aria-hidden="true"><path d="M20.5 11.6a8.6 8.6 0 0 1-12.7 7.6L3 20.5'
    'l1.3-4.6a8.6 8.6 0 1 1 16.2-4.3z"/><path d="M9 8.6c.3 2.6 2.4 4.9 5.2 5.7l1.2-1.3 1.8.9'
    '-.4 1.7c-4.4.2-8.6-3.9-8.5-8.3l1.7-.4.8 1.8z" stroke-width="1.4"/></svg>'
)

# En el teléfono se oculta la segunda parte del nombre para que el menú quepa
PAGINAS = [
    ("medidor.html", "Medidor", " Inteligente"),
    ("relojes.html", "Relojes", " GPS"),
    ("telecom.html", "Telecom", " y equipos"),
]


def wa(texto=None):
    if not texto:
        return f"https://wa.me/{WA}"
    return f"https://wa.me/{WA}?text={quote(texto)}"


def cabeza_comun():
    robots = '' if PUBLICAR else '<meta name="robots" content="noindex, nofollow">\n'
    return (
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        f'{robots}'
        '<meta name="theme-color" content="#1b2433">\n'
        '<link rel="icon" href="img/logo-mtg.png" type="image/png">\n'
        '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,100..900&display=swap">\n'
        '<link rel="stylesheet" href="css/estilo.css">'
    )


def cabecera(archivo):
    aviso = '' if PUBLICAR else (
        '<div class="aviso-vista-previa">Vista previa del rediseño. Todavía no está publicada en mtglobalpa.com.</div>\n'
    )
    actual = ' aria-current="page"'
    enlaces = "\n".join(
        f'      <a href="{a}"{actual if a == archivo else ""}>{n}<span class="nav-extra">{extra}</span></a>'
        for a, n, extra in PAGINAS
    )
    return f"""{aviso}<a class="salto" href="#contenido">Saltar al contenido</a>
<header class="cabecera">
  <div class="envoltura">
    <a class="logo" href="index.html"><img src="img/logo-mtg.png" alt="Meta Technology Global, inicio" width="605" height="239"></a>
    <nav class="menu" aria-label="Principal">
{enlaces}
      <a href="#contacto">Contacto</a>
    </nav>
    <a class="boton boton-wa" href="{wa()}">{ICONO_WA}<span class="wa-largo">WhatsApp 6887-3065</span><span class="wa-corto">WhatsApp</span></a>
  </div>
</header>"""


def pie():
    return f"""<footer class="pie" id="contacto">
  <div class="envoltura">
    <div class="pie-grilla">
      <div>
        <span class="pie-logo"><img src="img/logo-mtg.png" alt="Meta Technology Global" width="605" height="239"></span>
        <p>Empresa panameña. Trabajamos en telecomunicaciones desde 2008, y como Meta Technology Global desde 2022.</p>
        <p>San Francisco, Ciudad de Panamá</p>
      </div>
      <div>
        <h2>Contacto</h2>
        <ul>
          <li>WhatsApp: <a href="{wa()}">+507 6887-3065</a></li>
          <li>Correo: <a href="mailto:administrativo@mtglobalpa.com">administrativo@mtglobalpa.com</a></li>
          <li>Instagram: <a href="https://www.instagram.com/metatecglobal/">@metatecglobal</a></li>
          <li>Lunes a viernes, de 8:00 a.m. a 5:00 p.m.</li>
        </ul>
      </div>
      <div>
        <h2>Páginas</h2>
        <ul>
          <li><a href="index.html">Inicio</a></li>
          <li><a href="medidor.html">Medidor Inteligente</a></li>
          <li><a href="relojes.html">Relojes GPS</a></li>
          <li><a href="telecom.html">Telecom y equipos</a></li>
        </ul>
      </div>
    </div>
    <p class="pie-final">© 2026 Meta Technology Global. Precios en dólares de los Estados Unidos.</p>
  </div>
</footer>"""


def tarjeta(m):
    cat = CATEGORIAS[m["categoria"]]
    primero = m["colores"][0]
    varios = len(m["colores"]) > 1
    texto_wa = (
        f"Hola, me interesa el reloj {m['modelo']}"
        + (f" en color {primero['color'].lower()}" if varios else "")
        + f" de USD {m['precio']}. ¿Está disponible?"
    )

    muestras = ""
    if varios:
        botones = "".join(
            f'<button type="button" class="muestra" data-m="{e(c["color"])}" data-foto="img/relojes/{e(c["foto"])}" '
            f'data-existencias="{c["existencias"]}" aria-pressed="{"true" if i == 0 else "false"}" '
            f'aria-label="Color {e(c["color"].lower())}"></button>'
            for i, c in enumerate(m["colores"])
        )
        muestras = f'<div class="colores">{botones}<span class="colores-nombre">{e(primero["color"])}</span></div>'
    else:
        muestras = f'<div class="colores"><span class="colores-nombre">Color {e(primero["color"].lower())}</span></div>'

    funciones = "".join(f"<li>{e(f)}</li>" for f in m["funciones"])

    datos = []
    if m["conexion"] == "sim":
        datos.append("Necesita una SIM con datos y llamadas.")
    else:
        datos.append("Se conecta a su celular por Bluetooth. No lleva SIM.")
    if m.get("app"):
        datos.append(f"App gratuita: {e(m['app'])}")
    datos_html = "".join(f"<span>{d}</span>" for d in datos)

    notas = []
    if m.get("nota"):
        notas.append(e(m["nota"]))
    if m.get("salud"):
        notas.append("Las mediciones de salud son de referencia. No es un equipo médico.")
    if m.get("por_confirmar"):
        notas.append("Le enviamos la ficha técnica completa por WhatsApp.")
    notas_html = "".join(f'<p class="nota">{n}</p>' for n in notas)

    return f"""<article class="reloj" data-categoria="{cat['id']}" data-color="{cat['color']}" data-modelo="{e(m['modelo'])}" data-precio="{m['precio']}">
  <div class="reloj-foto">
    <span class="reloj-cat"><span class="manga"></span>{e(cat['nombre'])}</span>
    <img src="img/relojes/{e(primero['foto'])}" alt="{e(m['modelo'])} en color {e(primero['color'].lower())}" loading="lazy">
  </div>
  <div class="reloj-cuerpo">
    <div>
      <p class="reloj-modelo">{e(m['modelo'])}</p>
      <h3>{e(m['nombre'])}</h3>
    </div>
    <div class="precio-fila">
      <span class="precio"><small>USD</small>{m['precio']}</span>
      <span class="existencias">{primero['existencias']} en existencia</span>
    </div>
    {muestras}
    <ul class="funciones">{funciones}</ul>
    <p class="reloj-datos">{datos_html}</p>
    {notas_html}
    <a class="boton boton-wa" href="{wa(texto_wa)}">{ICONO_WA}Pedir por WhatsApp</a>
  </div>
</article>"""


def filtros():
    total = len(MODELOS)
    partes = [f'<button type="button" class="filtro" data-filtro="todos" aria-pressed="true">Todos <span class="n">{total}</span></button>']
    for c in DATOS["categorias"]:
        n = sum(1 for m in MODELOS if m["categoria"] == c["id"])
        partes.append(
            f'<button type="button" class="filtro" data-filtro="{c["id"]}" data-color="{c["color"]}" aria-pressed="false">'
            f'<span class="manga"></span>{e(c["nombre"])} <span class="n">{n}</span></button>'
        )
    return "\n".join(partes)


def grupos():
    """Los cuatro accesos de la portada, con la foto más representativa de cada categoría."""
    fotos = {"ninos": "k-h05g-azul.png", "mayores": "e-v28c-negro.png", "salud": "s-f3.png", "mascotas": "p-fa58p.png"}
    salida = []
    for c in DATOS["categorias"]:
        ms = [m for m in MODELOS if m["categoria"] == c["id"]]
        desde = min(m["precio"] for m in ms)
        cuantos = "1 modelo" if len(ms) == 1 else f"{len(ms)} modelos"
        precio = f"USD {desde}" if len(ms) == 1 else f"desde USD {desde}"
        salida.append(
            f'<a class="grupo" href="relojes.html#{c["id"]}" data-color="{c["color"]}">'
            f'<span class="grupo-foto"><img src="img/relojes/{fotos[c["id"]]}" alt="" loading="lazy"></span>'
            f'<span class="grupo-texto"><strong><span class="manga"></span>{e(c["nombre"])}</strong>'
            f'<span>{cuantos}, {precio}</span></span></a>'
        )
    return "\n".join(salida)


def jsonld_relojes():
    items = []
    for i, m in enumerate(MODELOS, 1):
        items.append({
            "@type": "ListItem", "position": i,
            "item": {
                "@type": "Product",
                "name": f"{m['modelo']} · {m['nombre']}",
                "sku": m["modelo"],
                "image": f"https://mtglobalpa.com/img/relojes/{m['colores'][0]['foto']}",
                "description": "; ".join(m["funciones"]),
                "offers": {
                    "@type": "Offer", "price": f"{m['precio']:.2f}", "priceCurrency": "USD",
                    "availability": "https://schema.org/InStock",
                    "seller": {"@type": "Organization", "name": "Meta Technology Global"},
                },
            },
        })
    datos = {"@context": "https://schema.org", "@type": "ItemList", "itemListElement": items}
    return '<script type="application/ld+json">' + json.dumps(datos, ensure_ascii=False) + "</script>"


def desde(categoria=None):
    ms = [m for m in MODELOS if categoria is None or m["categoria"] == categoria]
    return min(m["precio"] for m in ms)


def main():
    reemplazos = {
        "{{CABEZA}}": cabeza_comun(),
        "{{PIE}}": pie(),
        "{{CATALOGO}}": "\n".join(tarjeta(m) for m in MODELOS),
        "{{FILTROS}}": filtros(),
        "{{GRUPOS}}": grupos(),
        "{{JSONLD_RELOJES}}": jsonld_relojes(),
        "{{TOTAL_RELOJES}}": str(len(MODELOS)),
        "{{DESDE_RELOJES}}": str(desde()),
        "{{WA}}": wa(),
        "{{WA_NUMERO}}": WA,
        "{{ICONO_WA}}": ICONO_WA,
    }
    for fuente in sorted((RAIZ / "fuente").glob("*.html")):
        texto = fuente.read_text(encoding="utf-8")
        texto = texto.replace("{{CABECERA}}", cabecera(fuente.name))
        # enlaces de WhatsApp con texto: {{WA:mensaje}}
        while "{{WA:" in texto:
            ini = texto.index("{{WA:")
            fin = texto.index("}}", ini)
            texto = texto[:ini] + e(wa(texto[ini + 5:fin])) + texto[fin + 2:]
        for clave, valor in reemplazos.items():
            texto = texto.replace(clave, valor)
        if "{{" in texto:
            raise SystemExit(f"{fuente.name}: quedó un marcador sin reemplazar")
        (RAIZ / fuente.name).write_text(texto, encoding="utf-8")
        print("listo", fuente.name)


if __name__ == "__main__":
    main()
