#!/bin/zsh
# Publica la web en mtglobalpa.com.
# Arma la versión final (sin aviso de vista previa ni noindex) en una carpeta aparte,
# la copia al repositorio mtg-pagina-web y la sube. Cloudflare la despliega sola en uno o dos minutos.
# Uso:  zsh herramientas/publicar.sh "Qué cambió"
set -e
MENSAJE=${1:-"Actualiza la web de MTG"}
ORIGEN=$(cd "$(dirname "$0")/.." && pwd)
TMP=$(mktemp -d)
rsync -a --exclude .git --exclude .claude "$ORIGEN/" "$TMP/obra/"
(cd "$TMP/obra" && python3 herramientas/generar.py --publicar)
git clone -q https://github.com/Lulago3003/mtg-pagina-web.git "$TMP/oficial"
cp "$TMP/obra/"*.html "$TMP/obra/sitemap.xml" "$TMP/obra/robots.txt" "$TMP/oficial/"
rsync -a "$TMP/obra/en" "$TMP/obra/css" "$TMP/obra/js" "$TMP/obra/img" "$TMP/obra/video" "$TMP/oficial/"
cd "$TMP/oficial"
git add -A
if git diff --cached --quiet; then echo "No hay cambios para publicar."; exit 0; fi
git commit -q -m "$MENSAJE"
git push -q origin main
echo "Publicado: $(git rev-parse --short HEAD). En uno o dos minutos se ve en https://mtglobalpa.com/"
