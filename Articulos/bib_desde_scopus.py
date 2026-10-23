"""Añade a RSL/referencias_nfr.bib las entradas que faltan para los estudios del formulario de extracción.

Toma los metadatos de las exportaciones de Scopus (Articulos/SCUPUS/S*.csv). Las claves siguen el estilo
ApellidoAño-Palabra. Solo agrega estudios elegibles cuyo DOI aún no está en el .bib.

Uso:  python Articulos/bib_desde_scopus.py
"""
import csv
import json
import os
import re
import unicodedata

BASE = os.path.dirname(os.path.abspath(__file__))
BIB = os.path.join(BASE, "..", "RSL", "referencias_nfr.bib")
VACIAS = {"a", "an", "the", "on", "of", "for", "to", "and", "in", "with", "using", "from", "towards", "toward"}


def ascii(s):
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()


def esc(s):
    return s.replace("&", r"\&").replace("%", r"\%").replace("_", r"\_").replace("#", r"\#")


bib = open(BIB, encoding="utf-8").read()
en_bib = {d.lower().strip() for d in re.findall(r"doi\s*=\s*\{([^}]+)\}", bib, re.I)}
claves = set(re.findall(r"@\w+\{([^,]+),", bib))

scopus = {}
for s in ("S1", "S2", "S3", "S4"):
    with open(os.path.join(BASE, "SCUPUS", s + ".csv"), encoding="utf-8-sig") as fh:
        for f in csv.DictReader(fh):
            if f["DOI"]:
                scopus.setdefault(f["DOI"].lower().strip(), f)

incl = {f["id"]: f for f in csv.DictReader(open(os.path.join(BASE, "incluidos.csv"), encoding="utf-8-sig"))}
est = json.load(open(os.path.join(BASE, "extraccion", "extraccion_texto_completo.json"), encoding="utf-8"))["estudios"]

nuevas = []
for i in sorted(est, key=int):
    if est[i].get("Elegible tras texto completo") == "No":
        continue
    doi = incl[i]["doi"].lower().strip()
    if doi in en_bib or doi not in scopus:
        continue
    f = scopus[doi]
    nombres = [n.strip() for n in f["Author full names"].split(";") if n.strip()]
    autores = []
    for n in nombres:
        n = re.sub(r"\s*\(\d+\)$", "", n)
        autores.append(n)
    apellido = ascii(autores[0].split(",")[0]).replace(" ", "").replace("-", "")
    palabra = next(w for w in re.findall(r"[A-Za-z]+", ascii(f["Title"])) if w.lower() not in VACIAS)
    clave = f"{apellido}{f['Year']}-{palabra.capitalize()}"
    while clave in claves:
        clave += "b"
    claves.add(clave)
    es_conf = f["Document Type"] == "Conference paper"
    campos = [("author", " and ".join(autores)), ("title", f["Title"])]
    campos.append(("booktitle" if es_conf else "journal", f["Source title"]))
    campos.append(("year", f["Year"]))
    if f["Volume"]:
        campos.append(("volume", f["Volume"]))
    if f["Issue"] and not es_conf:
        campos.append(("number", f["Issue"]))
    if f["Page start"] and f["Page end"]:
        campos.append(("pages", f"{f['Page start']}--{f['Page end']}"))
    elif f["Art. No."]:
        campos.append(("pages", f["Art. No."]))
    campos.append(("doi", f["DOI"]))
    cuerpo = ",\n".join(f"  {k:<9} = {{{esc(v) if k not in ('doi', 'pages') else v}}}" for k, v in campos)
    tipo = "inproceedings" if es_conf else "article"
    nuevas.append(f"% [Scopus] id {i} del cribado\n@{tipo}{{{clave},\n{cuerpo},\n}}\n")
    print(i, clave)

if nuevas:
    with open(BIB, "a", encoding="utf-8") as fh:
        fh.write("\n" + "\n".join(nuevas))
print(len(nuevas), "entradas nuevas")
