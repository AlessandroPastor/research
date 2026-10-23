"""Segundo intento de descarga de los PDF de acceso abierto que faltan (estado "Acceso abierto" en
Articulos/PDF/INDICE_ARTICULOS.xlsx).

Para cada estudio prueba, en orden: el enlace libre del índice, la meta etiqueta citation_pdf_url de la página
de la editorial o del repositorio, las ubicaciones de OpenAlex, el openAccessPdf de Semantic Scholar y arXiv.
Solo guarda el archivo si empieza con %PDF y si la primera página contiene la mayor parte del título.

Uso:  python Articulos/descargar_abiertos.py            (todos los pendientes)
      python Articulos/descargar_abiertos.py 231 344    (solo esos)
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import time
import unicodedata
import urllib.parse
import urllib.request

from openpyxl import load_workbook

BASE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(BASE, "PDF")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/126.0 Safari/537.36")


REVISTAS_MDPI = {"app": "applsci", "fi": "futureinternet", "info": "information"}


def abridor():
    """Archivo de cookies compartido entre las peticiones de un mismo estudio."""
    fh = tempfile.NamedTemporaryFile(suffix=".txt", delete=False)
    fh.close()
    return fh.name


def bajar(cookies, url, timeout=45):
    """Descarga con curl (algunas editoriales rechazan el cliente HTTP de Python)."""
    salida = tempfile.NamedTemporaryFile(delete=False)
    salida.close()
    r = subprocess.run(["curl", "-s", "-L", "--max-time", str(timeout), "-A", UA,
                        "-H", "Accept: text/html,application/pdf,*/*;q=0.8", "-H", "Accept-Language: en-US,en;q=0.9",
                        "-b", cookies, "-c", cookies, "-o", salida.name, "-w", "%{http_code} %{url_effective}", url],
                       capture_output=True, text=True)
    datos = open(salida.name, "rb").read()
    os.remove(salida.name)
    codigo, _, final = r.stdout.partition(" ")
    if r.returncode or not codigo.startswith("2"):
        raise IOError(f"HTTP {codigo or r.returncode}")
    return datos, final


def palabras(s):
    s = unicodedata.normalize("NFKC", s).lower()  # separa ligaduras como ﬁ
    return [w for w in re.sub(r"[^a-z0-9 ]", " ", s).split() if len(w) > 3]


def coincide(datos, titulo):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as fh:
        fh.write(datos)
        ruta = fh.name
    try:
        txt = subprocess.run(["pdftotext", "-l", "2", "-enc", "UTF-8", ruta, "-"], capture_output=True).stdout
        txt = " ".join(palabras(txt.decode("utf-8", "ignore")))
    finally:
        os.remove(ruta)
    t = palabras(titulo)
    return sum(1 for w in t if w in txt) / max(1, len(t)) >= 0.8


def meta_pdf(html, url_base):
    h = html.decode("utf-8", "ignore")
    m = re.search(r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)', h, re.I) or \
        re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']citation_pdf_url', h, re.I)
    if m:
        return [urllib.parse.urljoin(url_base, m.group(1).replace("&amp;", "&"))]
    # repositorios DSpace / Pure: primer enlace a un .pdf o a /bitstream/
    return [urllib.parse.urljoin(url_base, x.replace("&amp;", "&")) for x in
            re.findall(r'href=["\']([^"\']*(?:/bitstream/[^"\']+|/files/[^"\']+\.pdf|\.pdf)[^"\']*)["\']', h, re.I)][:3]


def candidatos(o, doi, enlace, titulo):
    vistos = []

    def add(u):
        if u and u not in vistos:
            vistos.append(u)
            return True
        return False

    # Rutas directas de editoriales cuya página bloquea la descarga automática
    m = re.match(r"10\.3390/([a-z]+)(\d{2})(\d{2})(\d+)$", doi.lower())
    if m:
        revista = REVISTAS_MDPI.get(m.group(1), m.group(1))
        nombre = f"{revista}-{m.group(2)}-{int(m.group(4)):05d}"
        u = f"https://mdpi-res.com/d_attachment/{revista}/{nombre}/article_deploy/{nombre}.pdf"
        if add(u):
            yield u
    if doi.lower().startswith("10.1109/"):
        try:
            r = subprocess.run(["curl", "-s", "-I", "-A", UA, f"https://doi.org/{doi}"], capture_output=True, text=True)
            ar = re.search(r"/document/(\d+)", r.stdout)
            if ar:
                u = f"https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber={ar.group(1)}&ref="
                if add(u):
                    yield u
        except Exception:
            pass
    for u in (enlace, f"https://doi.org/{doi}" if doi else None):
        if add(u):
            yield u
    try:
        w = json.loads(bajar(o, "https://api.openalex.org/works/doi:" + urllib.parse.quote(doi))[0])
        for loc in w.get("locations", []):
            for u in (loc.get("pdf_url"), loc.get("landing_page_url")):
                if add(u):
                    yield u
    except Exception:
        pass
    try:
        s = json.loads(bajar(o, "https://api.semanticscholar.org/graph/v1/paper/DOI:" + urllib.parse.quote(doi)
                             + "?fields=openAccessPdf,externalIds")[0])
        u = (s.get("openAccessPdf") or {}).get("url")
        if add(u):
            yield u
        arx = (s.get("externalIds") or {}).get("ArXiv")
        if arx and add(f"https://arxiv.org/pdf/{arx}"):
            yield f"https://arxiv.org/pdf/{arx}"
    except Exception:
        pass


def intentar(doi, enlace, titulo, destino):
    o = abridor()
    for u in candidatos(o, doi, enlace, titulo):
        for paso in range(2):  # la página puede llevar a otra con el PDF
            try:
                datos, final = bajar(o, u)
            except Exception as e:
                print(f"      x {u[:90]} ({str(e)[:40]})")
                break
            if datos[:5] == b"%PDF-":
                if coincide(datos, titulo):
                    os.makedirs(os.path.dirname(destino), exist_ok=True)
                    open(destino, "wb").write(datos)
                    return final
                print(f"      x {u[:90]} (PDF de otro artículo)")
                break
            siguientes = meta_pdf(datos, final)
            if not siguientes:
                break
            u = siguientes[0]
        time.sleep(1)
    return None


ws = load_workbook(os.path.join(PDF, "INDICE_ARTICULOS.xlsx"))["Estudios"]
pedidos = set(sys.argv[1:])
ok, fallos = [], []
for fila in ws.iter_rows(min_row=2):
    v = [c.value for c in fila]
    if v[7] != "Acceso abierto (navegador)" or (pedidos and str(v[0]) not in pedidos):
        continue
    destino = os.path.join(PDF, v[9])
    enlace = fila[8].hyperlink.target if fila[8].hyperlink else ""
    print(f"#{v[0]} {v[2][:70]}")
    fuente = intentar(v[12], enlace, v[2], destino)
    if fuente:
        print(f"   OK desde {fuente[:90]}")
        ok.append(v[0])
    else:
        print("   NO se pudo")
        fallos.append((v[0], v[2], enlace))

print(f"\nDescargados {len(ok)}: {ok}")
print(f"Sin descargar {len(fallos)}:")
for i, t, e in fallos:
    print(f"  #{i} {t[:80]} -> {e}")
