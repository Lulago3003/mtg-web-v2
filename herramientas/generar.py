"""Arma el sitio de MTG en español (raíz) y en inglés (carpeta en/).

Las plantillas de fuente/ llevan el texto de los dos idiomas así: [[español||english]].
Los catálogos salen de datos/*.json. Las páginas de cada línea de producto salen de
fuente/_linea.html, una por línea.

Uso:  python3 herramientas/generar.py            (vista previa, con noindex)
      python3 herramientas/generar.py --publicar (sin noindex ni aviso, para mtglobalpa.com)
"""
import html
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import quote

RAIZ = Path(__file__).resolve().parent.parent
PUBLICAR = "--publicar" in sys.argv
# cambia en cada armado para que el navegador no use una hoja de estilos vieja
VERSION = str(int(time.time()))
DOMINIO = "https://mtglobalpa.com/"

WA = "50768873065"
WA_VISIBLE = "+507 6887-3065"
CORREO = "administrativo@mtglobalpa.com"
INSTAGRAM = "https://www.instagram.com/metatecglobal/"
MAPA = "https://maps.app.goo.gl/wtqi5NnLH8ZkPtXU7"


def leer(nombre):
    return json.loads((RAIZ / "datos" / nombre).read_text(encoding="utf-8"))


RELOJES = leer("relojes.json")
RELOJES_EN = leer("relojes_en.json")
PRODUCTOS = leer("productos.json")["productos"]
LINEAS = leer("lineas.json")["lineas"]
LINEA = {l["id"]: l for l in LINEAS}

e = html.escape

# ---------------------------------------------------------------- idioma

MARCA_IDIOMA = re.compile(r"\[\[(.*?)\|\|(.*?)\]\]", re.S)


def idioma(texto, L):
    return MARCA_IDIOMA.sub(lambda m: m.group(1) if L == "es" else m.group(2), texto)


def wa(texto=None):
    return f"https://wa.me/{WA}" + (f"?text={quote(texto)}" if texto else "")


# ---------------------------------------------------------------- iconos y dibujos

ICONO = {
    "wa": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M20.5 11.6a8.6 8.6 0 0 1-12.7 7.6L3 20.5l1.3-4.6a8.6 8.6 0 1 1 16.2-4.3z"/><path d="M9 8.6c.3 2.6 2.4 4.9 5.2 5.7l1.2-1.3 1.8.9-.4 1.7c-4.4.2-8.6-3.9-8.5-8.3l1.7-.4.8 1.8z" stroke-width="1.4"/></svg>',
    "flecha": '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M2 4l4 4 4-4"/></svg>',
    "menu": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>',
    "cerrar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
    "luna": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4 8.5 8.5 0 1 0 20 14.5z"/></svg>',
    "buscar": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-4-4"/></svg>',
    "correo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/></svg>',
    "reloj": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "mapa": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
    "instagram": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
    "instalacion": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.7 6.3a4 4 0 0 0 5 5L12 19l-4-4z"/><path d="M8 15l-4 4"/><path d="M14.7 6.3L17 4l3 3-2.3 2.3"/></svg>',
    "soporte": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 14v-2a8 8 0 0 1 16 0v2"/><rect x="3" y="14" width="4" height="6" rx="1.5"/><rect x="17" y="14" width="4" height="6" rx="1.5"/><path d="M19 20a3 3 0 0 1-3 2h-3"/></svg>',
    "mantenimiento": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/></svg>',
    "calibracion": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 18a8 8 0 1 1 16 0"/><path d="M12 18l4-6"/><path d="M4 18h16"/></svg>',
    "sitio": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l-6 18M12 3l6 18M8.5 14h7M7.3 17.5h9.4"/><circle cx="12" cy="3" r="1"/></svg>',
    "llave": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="7" width="18" height="13" rx="2"/><path d="M8 7V5a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2M3 12h18"/></svg>',
    "energia": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" aria-hidden="true"><path d="M13 2L4 14h7l-1 8 9-12h-7z"/></svg>',
}

DIBUJO = {
    "gabinete": '<svg viewBox="0 0 120 160" aria-hidden="true"><rect x="10" y="6" width="100" height="148" rx="6" fill="#1b2a44"/><rect x="18" y="16" width="84" height="116" rx="3" fill="#2a3d5e"/><g fill="#5b9bef"><rect x="24" y="24" width="72" height="9" rx="2"/><rect x="24" y="38" width="72" height="9" rx="2"/><rect x="24" y="52" width="72" height="9" rx="2"/></g><g fill="#8fa6c6"><rect x="24" y="68" width="72" height="9" rx="2"/><rect x="24" y="82" width="72" height="9" rx="2"/><rect x="24" y="96" width="72" height="9" rx="2"/><rect x="24" y="110" width="72" height="14" rx="2"/></g><g fill="#7dbb42"><circle cx="88" cy="28.5" r="2"/><circle cx="88" cy="42.5" r="2"/><circle cx="88" cy="56.5" r="2"/></g><rect x="18" y="138" width="84" height="8" rx="2" fill="#2a3d5e"/></svg>',
    "contenedor": '<svg viewBox="0 0 200 120" aria-hidden="true"><rect x="8" y="20" width="184" height="86" rx="4" fill="#1b2a44"/><g stroke="#2f4568" stroke-width="4"><path d="M24 24v78M40 24v78M56 24v78M72 24v78M88 24v78M104 24v78M120 24v78"/></g><rect x="134" y="30" width="48" height="66" rx="3" fill="#2a3d5e"/><g fill="#5b9bef"><rect x="140" y="38" width="36" height="6" rx="1.5"/><rect x="140" y="48" width="36" height="6" rx="1.5"/><rect x="140" y="58" width="36" height="6" rx="1.5"/></g><g fill="#8fa6c6"><rect x="140" y="68" width="36" height="6" rx="1.5"/><rect x="140" y="78" width="36" height="6" rx="1.5"/></g><rect x="8" y="106" width="184" height="6" fill="#0f1b2e"/></svg>',
    "cargador": '<svg viewBox="0 0 120 160" aria-hidden="true"><rect x="28" y="8" width="64" height="96" rx="12" fill="#1b2a44"/><rect x="40" y="22" width="40" height="26" rx="4" fill="#2a3d5e"/><path d="M62 26l-10 12h7l-2 8 10-12h-7z" fill="#7dbb42"/><circle cx="60" cy="78" r="9" fill="#2a3d5e"/><path d="M60 104c0 20-24 18-24 36v12" fill="none" stroke="#1b2a44" stroke-width="6" stroke-linecap="round"/><rect x="26" y="146" width="20" height="10" rx="3" fill="#1b2a44"/></svg>',
}


def ruta(img, R):
    """Las fotos guardadas en el sitio llevan el prefijo de la carpeta del idioma; las externas no."""
    return img if img.startswith("http") else R + img


def figura_producto(p, R):
    """Foto del fabricante o, si no hay, un dibujo. Si la foto no carga, sitio.js pone un respaldo."""
    if p.get("img"):
        return f'<img src="{e(ruta(p["img"], R))}" alt="{e(p["marca"])} {e(p["nombre"])}" loading="lazy" data-respaldo="{e(p["marca"])} · {e(p["nombre"])}">'
    return DIBUJO.get(p.get("dibujo", "gabinete"), DIBUJO["gabinete"])


# ---------------------------------------------------------------- piezas comunes

def cabeza(meta, archivo, L, R):
    titulo, descripcion = meta["titulo"], meta["descripcion"]
    ruta_es = DOMINIO + ("" if archivo == "index.html" else archivo)
    ruta_en = DOMINIO + "en/" + ("" if archivo == "index.html" else archivo)
    robots = "" if PUBLICAR else '<meta name="robots" content="noindex, nofollow">\n'
    return f"""<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
{robots}<title>{e(titulo)}</title>
<meta name="description" content="{e(descripcion)}">
<link rel="canonical" href="{ruta_es if L == 'es' else ruta_en}">
<link rel="alternate" hreflang="es" href="{ruta_es}">
<link rel="alternate" hreflang="en" href="{ruta_en}">
<meta property="og:type" content="website">
<meta property="og:title" content="{e(titulo)}">
<meta property="og:description" content="{e(descripcion)}">
<meta property="og:url" content="{ruta_es if L == 'es' else ruta_en}">
<meta property="og:image" content="{DOMINIO}img/logo-mtg.png">
<meta property="og:locale" content="{'es_PA' if L == 'es' else 'en_US'}">
<meta name="theme-color" content="#0c2340">
<link rel="icon" href="{R}img/logo-mtg.png" type="image/png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Red+Hat+Display:wght@500;600;700;800&family=Red+Hat+Text:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="{R}css/estilo.css?v={VERSION}">
<script>try{{if(localStorage.getItem("mtg-tema")==="oscuro")document.documentElement.setAttribute("data-tema","oscuro")}}catch(e){{}}</script>"""


def barra_superior(archivo, L, R):
    otro = f"en/{archivo}" if L == "es" else f"../{archivo}"
    selector = (
        f'<span>ES</span><a href="{otro}" hreflang="en" lang="en">EN</a>' if L == "es"
        else f'<a href="{otro}" hreflang="es" lang="es">ES</a><span>EN</span>'
    )
    aviso = "" if PUBLICAR else '<div class="aviso-vista-previa">[[Vista previa del rediseño. Todavía no está publicada en mtglobalpa.com.||Redesign preview. Not yet published on mtglobalpa.com.]]</div>\n'
    return f"""{aviso}<div class="barra-sup">
  <div class="envoltura">
    <span class="barra-sup-lema">[[Telecomunicaciones, energía y seguridad en Panamá desde 2008||Telecom, energy and safety in Panama since 2008]]</span>
    <div class="barra-sup-acciones">
      <a href="{wa()}">WhatsApp<span class="barra-sup-numero"> {WA_VISIBLE}</span></a>
      <a class="barra-sup-correo" href="mailto:{CORREO}">{CORREO}</a>
      <span class="idioma" aria-label="[[Idioma||Language]]">{selector}</span>
      <button type="button" class="tema-boton" data-tema-boton aria-pressed="false">{ICONO['luna']}<span class="tema-texto">[[Modo oscuro||Dark mode]]</span></button>
    </div>
  </div>
</div>"""


UNIDADES = [
    ("medidor.html", "[[Residencial||Residential]]", "[[Casas y apartamentos: vea qué equipo sube la factura y cuide a la familia.||Homes and apartments: see which appliance drives the bill and look after your family.]]",
     [("medidor.html", "[[Medidor Inteligente||Smart Meter]]"), ("medidor.html#planes", "[[Planes desde USD 150||Plans from USD 150]]"), ("relojes.html", "[[Relojes GPS para la familia||GPS watches for the family]]")]),
    ("medidor.html", "[[Comercial||Commercial]]", "[[Locales, oficinas y edificios: consumo por área, cableado y Wi-Fi.||Shops, offices and buildings: usage by area, cabling and Wi-Fi.]]",
     [("medidor.html", "[[Medidor para negocios||Smart Meter for business]]"), ("data-centers.html", "[[Cableado estructurado y Wi-Fi||Structured cabling and Wi-Fi]]"), ("servicios.html#mantenimiento", "[[Mantenimiento||Maintenance]]")]),
    ("servicios.html#calidad-energia", "[[Industrial||Industrial]]", "[[Plantas y talleres: calidad de energía, equipos de medición y protección de carga.||Plants and workshops: power quality, test equipment and cargo protection.]]",
     [("servicios.html#calidad-energia", "[[Calidad de energía||Power quality]]"), ("catalogo.html", "[[Equipos de prueba||Test equipment]]"), ("shockwatch.html", "[[Detectores de impacto||Impact indicators]]")]),
    ("fibra-optica.html", "[[Telecomunicaciones||Telecommunications]]", "[[Operadores e ISP: fibra, RF, torres y antenas, con instalación.||Operators and ISPs: fiber, RF, towers and antennas, installed.]]",
     [("fibra-optica.html", "[[Fibra óptica||Fiber optics]]"), ("rf-cobertura.html", "[[RF y cobertura||RF and coverage]]"), ("prose.html", "[[Antenas camufladas PROSE||PROSE camouflaged antennas]]")]),
    ("data-centers.html", "Data centers", "[[KHIPU, racks, cableado y energía para centros de datos.||KHIPU, racks, cabling and power for data centers.]]",
     [("data-centers.html", "[[Data centers KHIPU||KHIPU data centers]]"), ("monitoreo-redes.html", "[[Monitoreo de redes||Network monitoring]]"), ("servicios.html#llave-en-mano", "[[Proyectos llave en mano||Turnkey projects]]")]),
    ("servicios.html#calidad-energia", "[[Calidad de energía||Power quality]]", "[[Estudios, armónicos, energía reactiva y respaldo.||Studies, harmonics, reactive power and backup.]]",
     [("servicios.html#calidad-energia", "[[Estudios de calidad de energía||Power quality studies]]"), ("medidor.html", "[[Medición por circuito||Per-circuit metering]]"), ("index.html#contacto", "[[Solicitar un estudio||Request a study]]")]),
]


def tiles_productos(R):
    """Los accesos visuales a cada línea: menú Productos, banda de portada y catálogo."""
    t = []
    for l in LINEAS:
        foto = f'<img src="{e(ruta(l["foto"], R))}" alt="" loading="lazy">' if l["foto"] else DIBUJO[l.get("dibujo", "gabinete")]
        t.append((l["archivo"], f'[[{l["nombre"]["es"]}||{l["nombre"]["en"]}]]', f'[[{l["corto"]["es"]}||{l["corto"]["en"]}]]', foto, ""))
    t.append(("medidor.html", "[[Medidor Inteligente||Smart Meter]]", "[[Consumo por circuito en su celular||Per-circuit usage on your phone]]",
              f'<img src="{R}img/fotos/tablero-con-pinzas.jpg" alt="" loading="lazy">', "foto-real"))
    t.append(("relojes.html", "[[Relojes GPS||GPS watches]]", f"[[{len(RELOJES['modelos'])} modelos, desde USD {min(m['precio'] for m in RELOJES['modelos'])}||{len(RELOJES['modelos'])} models, from USD {min(m['precio'] for m in RELOJES['modelos'])}]]",
              f'<img src="{R}img/relojes/k-h05g-azul.png" alt="" loading="lazy">', "acero"))
    t.append(("shockwatch.html", "[[Detectores de impacto||Impact indicators]]", "[[Etiquetas ShockWatch para su carga||ShockWatch labels for your cargo]]",
              f'<img src="{R}video/poster-shockwatch.jpg" alt="" loading="lazy">', "foto-real"))
    return t


def cabecera(archivo, L, R):
    actual = ' aria-current="page"'
    mega = "".join(
        f'<div class="mega-col"><h3><a href="{h}">{n}</a></h3><p>{d}</p><ul>'
        + "".join(f'<li><a href="{a}">{b}</a></li>' for a, b in links) + "</ul></div>"
        for h, n, d, links in UNIDADES
    )
    prods = "".join(
        f'<a href="{a}"><span class="mini {c}">{f}</span><span><strong>{n}</strong><span>{d}</span></span></a>'
        for a, n, d, f, c in tiles_productos(R)
    )
    en_productos = archivo in [l["archivo"] for l in LINEAS] + ["catalogo.html", "shockwatch.html", "prose.html"]

    def enlace(a, texto):
        return f'<div class="menu-item"><a class="menu-enlace" href="{a}"{actual if a == archivo else ""}>{texto}</a></div>'

    return f"""<a class="salto" href="#contenido">[[Saltar al contenido||Skip to content]]</a>
{barra_superior(archivo, L, R)}
<header class="cabecera">
  <div class="envoltura">
    <a class="logo" href="index.html"><img src="{R}img/logo-mtg.png" alt="Meta Technology Global, [[inicio||home]]" width="605" height="239"></a>
    <button type="button" class="menu-movil-boton" aria-expanded="false" aria-controls="menu-principal" data-menu-movil>{ICONO['menu']}[[Menú||Menu]]</button>
    <nav class="menu" id="menu-principal" aria-label="[[Principal||Main]]">
      <div class="menu-item">
        <button type="button" class="menu-enlace" aria-expanded="false" aria-controls="panel-unidades" data-panel>[[Unidades de negocio||Business units]] {ICONO['flecha']}</button>
        <div class="panel-menu" id="panel-unidades"><div class="envoltura"><div class="mega">{mega}</div></div></div>
      </div>
      <div class="menu-item">
        <button type="button" class="menu-enlace" aria-expanded="false" aria-controls="panel-productos" data-panel{actual if en_productos else ""}>[[Productos||Products]] {ICONO['flecha']}</button>
        <div class="panel-menu" id="panel-productos"><div class="envoltura"><div class="productos-menu">{prods}</div>
          <div class="panel-pie"><a href="catalogo.html">[[Ver el catálogo completo||See the full catalog]]</a><a href="prose.html">[[Antenas camufladas PROSE||PROSE camouflaged antennas]]</a><a href="catalogo.html#catalogos-pdf">[[Catálogos en PDF||PDF catalogs]]</a></div>
        </div></div>
      </div>
      {enlace("medidor.html", "[[Medidor Inteligente||Smart Meter]]")}
      {enlace("relojes.html", "[[Relojes GPS||GPS watches]]")}
      {enlace("servicios.html", "[[Servicios||Services]]")}
      {enlace("index.html#nosotros", "[[Nosotros||About]]")}
      {enlace("index.html#contacto", "[[Contacto||Contact]]")}
      <a class="boton boton-wa cta-movil" href="{wa()}">{ICONO['wa']}WhatsApp {WA_VISIBLE}</a>
    </nav>
    <a class="boton boton-azul cabecera-cta" href="catalogo.html">[[Cotizar equipos||Request a quote]]</a>
  </div>
</header>"""


def pie(L, R):
    lineas = "".join(f'<li><a href="{l["archivo"]}">[[{l["nombre"]["es"]}||{l["nombre"]["en"]}]]</a></li>' for l in LINEAS)
    return f"""<footer class="pie">
  <div class="envoltura">
    <div class="pie-grilla">
      <div>
        <span class="pie-logo"><img src="{R}img/logo-mtg.png" alt="Meta Technology Global" width="605" height="239"></span>
        <p>[[Empresa panameña de telecomunicaciones, energía y seguridad. En el sector desde 2008 y como Meta Technology Global desde 2022.||Panamanian telecom, energy and safety company. In the industry since 2008, and as Meta Technology Global since 2022.]]</p>
        <p>[[San Francisco, Ciudad de Panamá.||San Francisco, Panama City.]] <a href="{MAPA}">[[Cómo llegar||Directions]]</a></p>
      </div>
      <div>
        <h2>[[Productos||Products]]</h2>
        <ul>{lineas}<li><a href="medidor.html">[[Medidor Inteligente||Smart Meter]]</a></li><li><a href="relojes.html">[[Relojes GPS||GPS watches]]</a></li><li><a href="shockwatch.html">[[Detectores de impacto||Impact indicators]]</a></li></ul>
      </div>
      <div>
        <h2>[[Empresa||Company]]</h2>
        <ul><li><a href="servicios.html">[[Servicios||Services]]</a></li><li><a href="prose.html">[[Antenas PROSE||PROSE antennas]]</a></li><li><a href="catalogo.html">[[Catálogo||Catalog]]</a></li><li><a href="index.html#nosotros">[[Nosotros||About]]</a></li><li><a href="index.html#preguntas">[[Preguntas frecuentes||FAQ]]</a></li></ul>
      </div>
      <div>
        <h2>[[Contacto||Contact]]</h2>
        <ul>
          <li><a href="{wa()}">WhatsApp {WA_VISIBLE}</a></li>
          <li><a href="mailto:{CORREO}">{CORREO}</a></li>
          <li><a href="{INSTAGRAM}">Instagram @metatecglobal</a></li>
          <li>[[Lunes a viernes, 8:00 a.m. a 5:00 p.m.||Monday to Friday, 8:00 a.m. to 5:00 p.m.]]</li>
        </ul>
      </div>
    </div>
    <div class="pie-final"><span>© 2026 Meta Technology Global. [[Precios en dólares de los Estados Unidos.||Prices in US dollars.]]</span><span>[[Las marcas mencionadas pertenecen a sus fabricantes.||Brand names belong to their manufacturers.]]</span></div>
  </div>
</footer>"""


def flotantes(L, R):
    opciones = [
        ("[[Medidor Inteligente||Smart Meter]]", "[[Hola, quiero información del Medidor Inteligente.||Hello, I'd like information about the Smart Meter.]]"),
        ("[[Relojes GPS||GPS watches]]", "[[Hola, me interesan los relojes GPS.||Hello, I'm interested in the GPS watches.]]"),
        ("[[Fibra, RF y equipos||Fiber, RF and equipment]]", "[[Hola, necesito una cotización de equipos de telecomunicaciones.||Hello, I need a quote for telecom equipment.]]"),
        ("[[Otra consulta||Something else]]", "[[Hola, tengo una consulta.||Hello, I have a question.]]"),
    ]
    items = "".join(f'<li><a href="{{{{WA:{t}}}}}">{n}</a></li>' for n, t in opciones)
    return f"""<div class="barra-cotizar" data-barra-cotizar hidden>
  <span data-barra-texto></span>
  <button type="button" class="boton boton-borde-claro" data-abrir-comparar hidden>[[Comparar||Compare]]</button>
  <button type="button" class="boton boton-blanco" data-abrir-cotizar>[[Ver cotización||View quote]]</button>
</div>
<div class="cajon" data-cajon="cotizar" role="dialog" aria-modal="true" aria-labelledby="cotizar-titulo">
  <div class="cajon-panel">
    <div class="cajon-cabeza"><h2 id="cotizar-titulo">[[Su cotización||Your quote]]</h2><button type="button" class="cerrar" data-cerrar aria-label="[[Cerrar||Close]]">{ICONO['cerrar']}</button></div>
    <div class="cajon-cuerpo"><ul class="lista-cotizar" data-lista-cotizar></ul></div>
    <div class="cajon-pie">
      <p class="formulario-nota">[[Se abre WhatsApp con la lista lista para enviar. Le respondemos con precio y tiempo de entrega.||WhatsApp opens with the list ready to send. We reply with price and lead time.]]</p>
      <a class="boton boton-wa" data-enviar-cotizar href="{wa()}">{ICONO['wa']}[[Enviar por WhatsApp||Send via WhatsApp]]</a>
      <button type="button" class="boton boton-borde" data-vaciar>[[Vaciar la lista||Clear the list]]</button>
    </div>
  </div>
</div>
<div class="cajon" data-cajon="comparar" role="dialog" aria-modal="true" aria-labelledby="comparar-titulo">
  <div class="cajon-panel ancho">
    <div class="cajon-cabeza"><h2 id="comparar-titulo">[[Comparar equipos||Compare equipment]]</h2><button type="button" class="cerrar" data-cerrar aria-label="[[Cerrar||Close]]">{ICONO['cerrar']}</button></div>
    <div class="cajon-cuerpo" data-tabla-comparar></div>
  </div>
</div>
<div class="wa-flotante">
  <div class="wa-menu" id="wa-menu" data-wa-menu>
    <p>[[¿Sobre qué nos escribe?||What is it about?]]</p>
    <ul>{items}</ul>
    <small>WhatsApp {WA_VISIBLE}. [[Lunes a viernes, 8:00 a.m. a 5:00 p.m.||Monday to Friday, 8:00 a.m. to 5:00 p.m.]]</small>
  </div>
  <button type="button" class="wa-boton" aria-expanded="false" aria-controls="wa-menu" aria-label="[[Escribir por WhatsApp||Message us on WhatsApp]]" data-wa-boton>{ICONO['wa']}</button>
</div>"""


def textos_js(L):
    t = {
        "es": {
            "agregar": "Agregar a cotización", "agregado": "En la cotización", "productos1": "1 producto", "productosN": "{n} productos",
            "barra1": "1 equipo en su cotización", "barraN": "{n} equipos en su cotización", "comparar": "Comparar ({n})",
            "modelos1": "1 modelo", "modelosN": "{n} modelos", "existencia": "en existencia", "enColor": "en color",
            "relojWa": "Hola, me interesa el reloj {modelo}{color} de USD {precio}. ¿Está disponible?",
            "cotizarWa": "Hola, quiero cotizar estos equipos:", "cotizarCierre": "¿Me pueden enviar precio y tiempo de entrega?",
            "buscarWa": "Hola, ¿tienen disponible {q}?", "quitar": "Quitar", "vacia": "Todavía no agregó equipos. Use el botón «Agregar a cotización» en el catálogo.",
            "compararMax": "Puede comparar hasta 3 equipos a la vez.", "marca": "Marca", "linea": "Línea", "desc": "Para qué sirve",
            "specs": "Características", "disp": "Disponibilidad", "stock": "Disponible en Panamá", "pedido": "Bajo pedido",
            "formFalta": "Escriba su nombre y un teléfono o WhatsApp para poder responderle.",
            "formWa": "Hola, soy {nombre}. Me interesa {tipo}.\n{mensaje}\nTeléfono: {tel}{correo}", "formCorreo": "\nCorreo: {correo}",
            "temaClaro": "Modo claro", "temaOscuro": "Modo oscuro",
        },
        "en": {
            "agregar": "Add to quote", "agregado": "In your quote", "productos1": "1 product", "productosN": "{n} products",
            "barra1": "1 item in your quote", "barraN": "{n} items in your quote", "comparar": "Compare ({n})",
            "modelos1": "1 model", "modelosN": "{n} models", "existencia": "in stock", "enColor": "in",
            "relojWa": "Hello, I'm interested in the {modelo} watch{color} at USD {precio}. Is it available?",
            "cotizarWa": "Hello, I'd like a quote for this equipment:", "cotizarCierre": "Could you send me price and lead time?",
            "buscarWa": "Hello, do you have {q} available?", "quitar": "Remove", "vacia": "You haven't added anything yet. Use the “Add to quote” button in the catalog.",
            "compararMax": "You can compare up to 3 items at a time.", "marca": "Brand", "linea": "Line", "desc": "What it's for",
            "specs": "Features", "disp": "Availability", "stock": "Available in Panama", "pedido": "Made to order",
            "formFalta": "Please enter your name and a phone or WhatsApp number so we can reply.",
            "formWa": "Hello, I'm {nombre}. I'm interested in {tipo}.\n{mensaje}\nPhone: {tel}{correo}", "formCorreo": "\nEmail: {correo}",
            "temaClaro": "Light mode", "temaOscuro": "Dark mode",
        },
    }[L]
    lineas = {l["id"]: l["nombre"][L] for l in LINEAS}
    raiz = "" if L == "es" else "../"
    return f'<script>window.MTG={json.dumps({"wa": WA, "idioma": L, "raiz": raiz, "t": t, "lineas": lineas}, ensure_ascii=False)};</script>'


# ---------------------------------------------------------------- catálogo de equipos

def tarjeta_producto(p, L, R):
    linea = LINEA[p["linea"]]["nombre"][L]
    buscar = " ".join([p["marca"], p["nombre"], p["desc"]["es"], p["desc"]["en"], *p["specs"]["es"], *p["specs"]["en"],
                       LINEA[p["linea"]]["nombre"]["es"], LINEA[p["linea"]]["nombre"]["en"]]).lower()
    datos = {
        "id": p["id"], "marca": p["marca"], "nombre": p["nombre"], "img": p.get("img", ""), "dibujo": p.get("dibujo", ""),
        "linea": linea, "desc": p["desc"][L], "specs": p["specs"][L], "disp": p["disp"],
    }
    insignia = '<span class="insignia">[[Más solicitado||Most requested]]</span>' if p.get("popular") else ""
    oficial = '<span class="oficial">[[Distribuidor oficial||Official distributor]]</span>' if p.get("oficial") else ""
    disp = ('<span class="disponible stock">[[Disponible en Panamá||Available in Panama]]</span>' if p["disp"] == "stock"
            else '<span class="disponible pedido">[[Bajo pedido||Made to order]]</span>')
    specs = "".join(f"<li>{e(s)}</li>" for s in p["specs"][L])
    return f"""<article class="producto" data-producto="{e(p['id'])}" data-linea="{p['linea']}" data-marca="{e(p['marca'])}" data-buscar="{e(buscar)}" data-datos='{e(json.dumps(datos, ensure_ascii=False))}'>
  <div class="producto-foto">{insignia}{figura_producto(p, R)}</div>
  <div class="producto-cuerpo">
    <p class="producto-marca">{e(p['marca'])}{oficial}</p>
    <h3>{e(p['nombre'])}</h3>
    <p class="producto-desc">{e(p['desc'][L])}</p>
    <ul class="producto-specs">{specs}</ul>
    {disp}
    <div class="producto-acciones">
      <button type="button" class="boton boton-borde boton-cotizar" aria-pressed="false" data-cotizar>[[Agregar a cotización||Add to quote]]</button>
      <label class="comparar"><input type="checkbox" data-comparar> [[Comparar||Compare]]</label>
    </div>
  </div>
</article>"""


def productos_html(L, R, filtro=None, solo_portada=False):
    ps = [p for p in PRODUCTOS if (filtro is None or p["linea"] == filtro) and (not solo_portada or p.get("portada"))]
    return "\n".join(tarjeta_producto(p, L, R) for p in ps)


def filtros_catalogo(L):
    lineas = ['<button type="button" class="ficha" aria-pressed="true" data-filtro-linea="todas">[[Todas||All]] <span class="n">%d</span></button>' % len(PRODUCTOS)]
    for l in LINEAS:
        n = sum(1 for p in PRODUCTOS if p["linea"] == l["id"])
        lineas.append(f'<button type="button" class="ficha" aria-pressed="false" data-filtro-linea="{l["id"]}">[[{l["nombre"]["es"]}||{l["nombre"]["en"]}]] <span class="n">{n}</span></button>')
    marcas = sorted({p["marca"] for p in PRODUCTOS}, key=str.lower)
    bm = ['<button type="button" class="ficha" aria-pressed="true" data-filtro-marca="todas">[[Todas||All]]</button>']
    bm += [f'<button type="button" class="ficha" aria-pressed="false" data-filtro-marca="{e(m)}">{e(m)}</button>' for m in marcas]
    return "\n".join(lineas), "\n".join(bm)


def lineas_tarjetas(L, R, excluir=None):
    out = []
    for archivo, n, d, foto, clase in tiles_productos(R):
        if archivo == excluir:
            continue
        out.append(f'<a class="linea-tarjeta" href="{archivo}"><span class="linea-foto {clase}">{foto}</span><span><h3>{n}</h3><p>{d}</p></span></a>')
    return "\n".join(out)


def banda_lineas(R):
    return "\n".join(
        f'<li><a href="{a}"><span class="banda-foto {c}">{f}</span><strong>{n}</strong><span>{d}</span></a></li>'
        for a, n, d, f, c in tiles_productos(R)
    )


def marcas_franja():
    destino = {"PROSE": "prose.html", "KHIPU": "data-centers.html"}
    marcas = ["EXFO", "N-TEST", "PROSE", "KHIPU", "CRFS", "Bird", "PROMAX", "AEM", "GL Communications", "Emporia"]
    out = []
    for m in marcas:
        href = destino.get(m) or ("medidor.html" if m == "Emporia" else f"catalogo.html?marca={quote(m)}")
        out.append(f'<li><a href="{href}">{e(m)}</a></li>')
    return "\n".join(out)


# ---------------------------------------------------------------- relojes

def reloj_textos(m, L):
    if L == "es":
        return m["nombre"], m["funciones"], m.get("nota")
    tr = RELOJES_EN["modelos"].get(m["modelo"], {})
    return tr.get("nombre", m["nombre"]), tr.get("funciones", m["funciones"]), tr.get("nota", m.get("nota"))


def categoria_nombre(cid, L):
    c = next(c for c in RELOJES["categorias"] if c["id"] == cid)
    return c["nombre"] if L == "es" else RELOJES_EN["categorias"][cid]


def color_nombre(c, L):
    return c if L == "es" else RELOJES_EN["colores"].get(c, c)


ORDEN_CAT = [c["id"] for c in RELOJES["categorias"]]
MODELOS = sorted(RELOJES["modelos"], key=lambda m: (ORDEN_CAT.index(m["categoria"]), m["precio"], m["modelo"]))


def tarjeta_reloj(m, L, R):
    cat = next(c for c in RELOJES["categorias"] if c["id"] == m["categoria"])
    nombre, funciones, nota = reloj_textos(m, L)
    primero = m["colores"][0]
    varios = len(m["colores"]) > 1
    color_txt = (f" en color {primero['color'].lower()}" if L == "es" else f" in {color_nombre(primero['color'], L).lower()}") if varios else ""
    texto_wa = (f"Hola, me interesa el reloj {m['modelo']}{color_txt} de USD {m['precio']}. ¿Está disponible?" if L == "es"
                else f"Hello, I'm interested in the {m['modelo']} watch{color_txt} at USD {m['precio']}. Is it available?")
    if varios:
        botones = "".join(
            f'<button type="button" class="muestra" data-m="{e(c["color"])}" data-nombre="{e(color_nombre(c["color"], L))}" data-foto="{R}img/relojes/{e(c["foto"])}" '
            f'data-existencias="{c["existencias"]}" aria-pressed="{"true" if i == 0 else "false"}" aria-label="{e(color_nombre(c["color"], L))}"></button>'
            for i, c in enumerate(m["colores"])
        )
        muestras = f'<div class="colores">{botones}<span class="colores-nombre">{e(color_nombre(primero["color"], L))}</span></div>'
    else:
        muestras = f'<div class="colores"><span class="colores-nombre">[[Color||Color]]: {e(color_nombre(primero["color"], L).lower())}</span></div>'
    datos = ["[[Necesita una SIM con datos y llamadas.||Needs a SIM with data and calls.]]" if m["conexion"] == "sim"
             else "[[Se conecta a su celular por Bluetooth. No lleva SIM.||Connects to your phone by Bluetooth. No SIM needed.]]"]
    if m.get("app"):
        datos.append(f"[[App gratuita||Free app]]: {e(m['app'])}")
    notas = []
    if nota:
        notas.append(e(nota))
    if m.get("salud"):
        notas.append("[[Las mediciones de salud son de referencia. No es un equipo médico.||Health readings are for reference. This is not a medical device.]]")
    if m.get("por_confirmar"):
        notas.append("[[Le enviamos la ficha técnica completa por WhatsApp.||We'll send you the full spec sheet on WhatsApp.]]")
    alt_color = color_nombre(primero["color"], L).lower()
    return f"""<article class="reloj" data-categoria="{cat['id']}" data-color="{cat['color']}" data-modelo="{e(m['modelo'])}" data-precio="{m['precio']}">
  <div class="reloj-foto">
    <span class="reloj-cat"><span class="manga"></span>{e(categoria_nombre(cat['id'], L))}</span>
    <img src="{R}img/relojes/{e(primero['foto'])}" alt="{e(m['modelo'])}, {e(alt_color)}" loading="lazy">
  </div>
  <div class="reloj-cuerpo">
    <div><p class="reloj-modelo">{e(m['modelo'])}</p><h3>{e(nombre)}</h3></div>
    <div class="precio-fila"><span class="precio"><small>USD</small>{m['precio']}</span><span class="existencias">{primero['existencias']} [[en existencia||in stock]]</span></div>
    {muestras}
    <ul class="funciones">{''.join(f'<li>{e(f)}</li>' for f in funciones)}</ul>
    <p class="reloj-datos">{''.join(f'<span>{d}</span>' for d in datos)}</p>
    {''.join(f'<p class="nota">{n}</p>' for n in notas)}
    <a class="boton boton-wa" href="{e(wa(texto_wa))}">{ICONO['wa']}[[Pedir por WhatsApp||Order on WhatsApp]]</a>
  </div>
</article>"""


def filtros_relojes(L):
    partes = [f'<button type="button" class="ficha" data-filtro="todos" aria-pressed="true">[[Todos||All]] <span class="n">{len(MODELOS)}</span></button>']
    for c in RELOJES["categorias"]:
        n = sum(1 for m in MODELOS if m["categoria"] == c["id"])
        partes.append(f'<button type="button" class="ficha" data-filtro="{c["id"]}" data-color="{c["color"]}" aria-pressed="false"><span class="manga"></span>{e(categoria_nombre(c["id"], L))} <span class="n">{n}</span></button>')
    return "\n".join(partes)


def grupos_relojes(L, R):
    fotos = {"ninos": "k-h05g-azul.png", "mayores": "e-v28c-negro.png", "salud": "s-f3.png", "mascotas": "p-fa58p.png"}
    out = []
    for c in RELOJES["categorias"]:
        ms = [m for m in MODELOS if m["categoria"] == c["id"]]
        desde = min(m["precio"] for m in ms)
        if L == "es":
            txt = f"1 modelo, USD {desde}" if len(ms) == 1 else f"{len(ms)} modelos, desde USD {desde}"
        else:
            txt = f"1 model, USD {desde}" if len(ms) == 1 else f"{len(ms)} models, from USD {desde}"
        out.append(f'<a class="grupo" href="relojes.html#{c["id"]}" data-color="{c["color"]}"><span class="grupo-foto"><img src="{R}img/relojes/{fotos[c["id"]]}" alt="" loading="lazy"></span>'
                   f'<span class="grupo-texto"><strong><span class="manga"></span>{e(categoria_nombre(c["id"], L))}</strong><span>{txt}</span></span></a>')
    return "\n".join(out)


def jsonld_relojes(L):
    items = []
    for i, m in enumerate(MODELOS, 1):
        nombre, funciones, _ = reloj_textos(m, L)
        items.append({"@type": "ListItem", "position": i, "item": {
            "@type": "Product", "name": f"{m['modelo']}, {nombre}", "sku": m["modelo"],
            "image": f"{DOMINIO}img/relojes/{m['colores'][0]['foto']}", "description": "; ".join(funciones),
            "offers": {"@type": "Offer", "price": f"{m['precio']:.2f}", "priceCurrency": "USD", "availability": "https://schema.org/InStock",
                       "seller": {"@type": "Organization", "name": "Meta Technology Global"}}}})
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@type": "ItemList", "itemListElement": items}, ensure_ascii=False) + "</script>"


# ---------------------------------------------------------------- páginas de línea

def bloques_linea(l, L, R):
    foto = (f'<div class="cabeza-foto"><img src="{e(ruta(l["foto"], R))}" alt="" data-respaldo="{e(l["nombre"][L])}"></div>' if l["foto"]
            else f'<div class="cabeza-foto">{DIBUJO[l.get("dibujo", "gabinete")]}</div>')
    pdf = (f'<a class="boton boton-borde-claro" href="{e(l["pdf"])}">{e(l["pdf_nombre"][L])}</a>' if l["pdf"] else "")
    otras = "".join(f'<a href="{o["archivo"]}">{e(o["nombre"][L])}</a>' for o in LINEAS if o["id"] != l["id"])
    texto_wa = (f"Hola, me interesa la línea de {l['nombre']['es'].lower()}. Necesito cotizar:" if L == "es"
                else f"Hello, I'm interested in your {l['nombre']['en'].lower()} line. I need a quote for:")
    return {
        "{{L_NOMBRE}}": e(l["nombre"][L]),
        "{{L_CORTO}}": e(l["corto"][L]),
        "{{L_DESC}}": e(l["desc"][L]),
        "{{L_FOTO}}": foto,
        "{{L_MARCAS}}": "".join(f"<span>{e(m)}</span>" for m in l["marcas"]),
        "{{L_ITEMS}}": "".join(f"<li>{e(i)}</li>" for i in l["items"][L]),
        "{{L_PRODUCTOS}}": productos_html(L, R, filtro=l["id"]),
        "{{L_PDF}}": pdf,
        "{{L_OTRAS}}": otras + f'<a href="medidor.html">[[Medidor Inteligente||Smart Meter]]</a>',
        "{{L_WA}}": e(wa(texto_wa)),
        "{{L_PROSE}}": ('<p class="seccion-intro">[[Vea también las <a href="prose.html">antenas camufladas PROSE</a>, que se integran al aspecto del edificio.||See also the <a href="prose.html">PROSE camouflaged antennas</a>, which blend into the building.]]</p>'
                        if l["id"] in ("infra", "rf") else ""),
    }


# ---------------------------------------------------------------- armado

FRONT = re.compile(r"<!--meta\s*(.*?)-->\s*", re.S)


def leer_meta(texto, L):
    m = FRONT.search(texto)
    meta = {}
    for linea in m.group(1).strip().splitlines():
        clave, valor = linea.split(":", 1)
        es, en = [x.strip() for x in valor.split("||")]
        meta[clave.strip()] = es if L == "es" else en
    return meta, FRONT.sub("", texto, count=1)


def construir(texto, archivo, L, extra=None):
    R = "" if L == "es" else "../"
    meta, texto = leer_meta(texto, L)
    if extra:
        for k, v in extra.items():
            meta = {mk: mv.replace(k, v) for mk, mv in meta.items()}
    lin_botones, marca_botones = filtros_catalogo(L)
    reemplazos = {
        "{{CABEZA}}": cabeza(meta, archivo, L, R),
        "{{CABECERA}}": cabecera(archivo, L, R),
        "{{PIE}}": pie(L, R),
        "{{FLOTANTES}}": flotantes(L, R),
        "{{SCRIPTS}}": textos_js(L) + f'\n<script src="{R}js/sitio.js?v={VERSION}" defer></script>',
        "{{BANDA_LINEAS}}": banda_lineas(R),
        "{{MARCAS}}": marcas_franja(),
        "{{PRODUCTOS_POPULARES}}": productos_html(L, R, solo_portada=True),
        "{{PRODUCTOS_TODOS}}": productos_html(L, R),
        "{{PRODUCTOS_PROSE}}": "\n".join(tarjeta_producto(p, L, R) for p in PRODUCTOS if p["marca"] == "PROSE"),
        "{{FILTROS_LINEA}}": lin_botones,
        "{{FILTROS_MARCA}}": marca_botones,
        "{{LINEAS_TARJETAS}}": lineas_tarjetas(L, R),
        "{{TOTAL_PRODUCTOS}}": str(len(PRODUCTOS)),
        "{{RELOJES_CATALOGO}}": "\n".join(tarjeta_reloj(m, L, R) for m in MODELOS),
        "{{RELOJES_FILTROS}}": filtros_relojes(L),
        "{{RELOJES_GRUPOS}}": grupos_relojes(L, R),
        "{{RELOJES_JSONLD}}": jsonld_relojes(L),
        "{{RELOJES_TOTAL}}": str(len(MODELOS)),
        "{{RELOJES_DESDE}}": str(min(m["precio"] for m in MODELOS)),
        "{{CATALOGOS_PDF}}": "".join(
            f'<li><a href="{e(l["pdf"])}">{e(l["pdf_nombre"][L])}</a></li>' for l in LINEAS if l["pdf"]
        ) + f'<li><a href="{R}img/prose/prose-camouflage-catalog.pdf">[[Antenas camufladas PROSE (PDF)||PROSE camouflaged antennas (PDF)]]</a></li>',
        "{{WA}}": wa(),
        "{{WA_VISIBLE}}": WA_VISIBLE,
        "{{CORREO}}": CORREO,
        "{{MAPA}}": MAPA,
        "{{INSTAGRAM}}": INSTAGRAM,
        "{{R}}": R,
    }
    reemplazos.update({f"{{{{ICONO_{k.upper()}}}}}": v for k, v in ICONO.items()})
    reemplazos.update({f"{{{{DIBUJO_{k.upper()}}}}}": v for k, v in DIBUJO.items()})
    if extra:
        reemplazos.update(extra)
    for clave, valor in reemplazos.items():
        texto = texto.replace(clave, valor)
    texto = idioma(texto, L)
    # enlaces de WhatsApp con mensaje: {{WA:mensaje}}
    texto = re.sub(r"\{\{WA:(.*?)\}\}", lambda m: e(wa(html.unescape(m.group(1)))), texto, flags=re.S)
    if "{{" in texto or "[[" in texto:
        resto = re.findall(r"(\{\{.*?\}\}|\[\[.{0,40})", texto)[:3]
        raise SystemExit(f"{L}/{archivo}: quedaron marcadores sin reemplazar: {resto}")
    return texto


def main():
    (RAIZ / "en").mkdir(exist_ok=True)
    plantillas = sorted(p for p in (RAIZ / "fuente").glob("*.html") if not p.name.startswith("_"))
    plantilla_linea = (RAIZ / "fuente" / "_linea.html").read_text(encoding="utf-8")
    for L in ("es", "en"):
        destino = RAIZ if L == "es" else RAIZ / "en"
        for p in plantillas:
            (destino / p.name).write_text(construir(p.read_text(encoding="utf-8"), p.name, L), encoding="utf-8")
        for l in LINEAS:
            extra = bloques_linea(l, L, "" if L == "es" else "../")
            (destino / l["archivo"]).write_text(construir(plantilla_linea, l["archivo"], L, extra), encoding="utf-8")
        print(L, "listo:", len(plantillas) + len(LINEAS), "páginas")


if __name__ == "__main__":
    main()
