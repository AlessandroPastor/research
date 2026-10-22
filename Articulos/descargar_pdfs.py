"""Descarga los PDF de acceso abierto de los estudios de la revisión y los ordena por carpetas.

Fuentes (todas abiertas): OpenAlex (ubicaciones de acceso abierto) y, como respaldo, Semantic Scholar.
Solo se guarda un archivo si realmente es un PDF. Lo que no se encuentre se lista en
Articulos/PDF/FALTANTES.csv con la carpeta y el nombre de archivo que debe tener.

Carpetas:
  01_semillas, 02_trabajos_base, 03_aumentacion, 04_bert_transformers, 05_llm,
  06_ml_dl_clasico, 07_revisiones

Uso:  python Articulos/descargar_pdfs.py          (se puede volver a ejecutar: no repite descargas)
"""
import csv
import json
import os
import re
import sys
import time
import unicodedata
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.dirname(os.path.abspath(__file__))
PDF = os.path.join(BASE, "PDF")
UA = {"User-Agent": "Mozilla/5.0 (tesis-nfr; descarga de acceso abierto)"}

SEMILLAS = {"10.48084/etasr.14313", "10.1007/s00766-025-00451-8", "10.1109/access.2025.3570359"}
BASE_TRABAJOS = [  # (clave corta, DOI)
    ("ClelandHuang2007_NFR", "10.1007/s00766-007-0045-1"),
    ("Kurtanovic2017_SupervisedML", "10.1109/RE.2017.82"),
    ("Dalpiaz2019_Interpretable", "10.1109/RE.2019.00025"),
    ("Hey2020_NoRBERT", "10.1109/RE48521.2020.00028"),
    ("Alhoshan2023_ZeroShot", "10.1016/j.infsof.2023.107202"),
    ("Devlin2019_BERT", "10.18653/v1/N19-1423"),
    ("Chawla2002_SMOTE", "10.1613/jair.953"),
    ("Batista2004_SMOTETomek", "10.1145/1007730.1007735"),
    ("Wei2019_EDA", "10.18653/v1/D19-1670"),
    ("Morris2020_TextAttack", "10.18653/v1/2020.emnlp-demos.16"),
    ("Rahimi2021_TwoPhase", "10.3390/e23101264"),
]


def plano(s, n=40):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "", s.title())[:n]


def nombre(i, autores, anio, titulo):
    ape = plano(autores.split(",")[0].split(";")[0].split()[0] if autores else "Anon", 20)
    pal = [w for w in re.findall(r"[A-Za-z0-9]+", titulo) if len(w) > 3][:4]
    return f"{i}_{ape}{anio}_{plano(' '.join(pal), 40)}.pdf"


def obtener(url, timeout=40):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def candidatos(doi):
    urls = []
    try:
        w = json.loads(obtener("https://api.openalex.org/works/doi:" + urllib.parse.quote(doi)))
        locs = [w.get("best_oa_location")] + (w.get("locations") or [])
        for l in locs:
            if l and l.get("is_oa") and l.get("pdf_url"):
                urls.append(l["pdf_url"])
    except Exception:
        pass
    try:
        s = json.loads(obtener("https://api.semanticscholar.org/graph/v1/paper/DOI:" + urllib.parse.quote(doi)
                               + "?fields=openAccessPdf,externalIds"))
        if (s.get("openAccessPdf") or {}).get("url"):
            urls.append(s["openAccessPdf"]["url"])
        arx = (s.get("externalIds") or {}).get("ArXiv")
        if arx:
            urls.append(f"https://arxiv.org/pdf/{arx}")
    except Exception:
        pass
    # Páginas de los artículos de acceso abierto: buscar la etiqueta estándar citation_pdf_url
    paginas = ["https://doi.org/" + doi]
    try:
        paginas += [l["landing_page_url"] for l in (w.get("locations") or [])
                    if l and l.get("is_oa") and l.get("landing_page_url")]
    except Exception:
        pass
    for p in paginas:
        try:
            html = obtener(p).decode("utf-8", "ignore")
            m = re.search(r'<meta[^>]+name=["\']citation_pdf_url["\'][^>]+content=["\']([^"\']+)', html, re.I) \
                or re.search(r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']citation_pdf_url', html, re.I)
            if m:
                urls.append(urllib.parse.urljoin(p, m.group(1)))
            a = re.search(r'arnumber[=/"]+(\d{6,})', html)  # IEEE: visor de PDF
            if "ieee" in p.lower() or a:
                if a:
                    urls.append(f"https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber={a.group(1)}")
        except Exception:
            continue
    if doi.startswith("10.1007/"):
        urls.append(f"https://link.springer.com/content/pdf/{doi}.pdf")
    vistos, out = set(), []
    for u in urls:
        if u not in vistos:
            vistos.add(u)
            out.append(u)
    return out


def descargar(doi, ruta):
    if os.path.exists(ruta):
        return "ya estaba"
    for u in candidatos(doi):
        try:
            datos = obtener(u)
            if datos[:5] == b"%PDF-":
                with open(ruta, "wb") as fh:
                    fh.write(datos)
                return "ok"
        except Exception:
            continue
        finally:
            time.sleep(0.5)
    return None


# --- Lista de documentos con su carpeta -----------------------------------------
docs = []
with open(os.path.join(BASE, "incluidos.csv"), encoding="utf-8-sig") as fh:
    for r in csv.DictReader(fh):
        doi = r["doi"].lower()
        if doi in SEMILLAS:
            carpeta = "01_semillas"
        elif r["aumento"] or r["desbalance"] == "True" and r["aumento"]:
            carpeta = "03_aumentacion"
        elif r["enfoque"] == "LLM":
            carpeta = "05_llm"
        elif r["enfoque"] == "Transformer":
            carpeta = "04_bert_transformers"
        else:
            carpeta = "06_ml_dl_clasico"
        docs.append((r["id"], doi, carpeta, r["titulo"], r["anio"], r.get("autores", "")))

autores = {}
for b in ["S1", "S2", "S3", "S4"]:
    with open(os.path.join(BASE, "SCUPUS", f"{b}.csv"), encoding="utf-8-sig") as fh:
        for x in csv.DictReader(fh):
            autores.setdefault(x["DOI"].lower(), x["Authors"])

with open(os.path.join(BASE, "cribado.csv"), encoding="utf-8-sig") as fh:
    for r in csv.DictReader(fh):
        if r["decision"] == "CE4":
            docs.append((r["id"], r["doi"].lower(), "07_revisiones", r["titulo"], r["anio"], ""))
for clave, doi in BASE_TRABAJOS:
    docs.append(("B", doi.lower(), "02_trabajos_base", clave, "", ""))

# --- Descarga --------------------------------------------------------------------
faltan, n_ok = [], 0
for i, doi, carpeta, titulo, anio, _ in docs:
    os.makedirs(os.path.join(PDF, carpeta), exist_ok=True)
    archivo = (f"{titulo}.pdf" if i == "B" else nombre(i, autores.get(doi, ""), anio, titulo))
    ruta = os.path.join(PDF, carpeta, archivo)
    res = descargar(doi, ruta) if doi else None
    if res:
        n_ok += 1
    else:
        faltan.append([carpeta, archivo, i, titulo, doi, f"https://doi.org/{doi}" if doi else ""])
    print(f"{'OK ' if res else '-- '} {carpeta}/{archivo}")

with open(os.path.join(PDF, "FALTANTES.csv"), "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.writer(fh)
    w.writerow(["carpeta", "nombre_de_archivo", "id", "titulo", "doi", "enlace"])
    w.writerows(sorted(faltan))
print(f"\nDescargados: {n_ok} de {len(docs)}. Faltan {len(faltan)} -> Articulos/PDF/FALTANTES.csv")
