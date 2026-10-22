"""Agrega a Articulos/PDF/FALTANTES.csv el tipo de acceso (OpenAlex) y el enlace directo a la versión libre.

Orden del archivo resultante: primero los de acceso abierto (se descargan en el navegador, sin cuenta),
luego los de pago (requieren el acceso institucional de la UPeU).

Uso:  python Articulos/clasificar_faltantes.py
"""
import csv
import json
import os
import sys
import urllib.parse
import urllib.request

sys.stdout.reconfigure(encoding="utf-8")
ARCH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "PDF", "FALTANTES.csv")
ABIERTO = {"gold", "hybrid", "green", "diamond", "bronze"}

filas = list(csv.DictReader(open(ARCH, encoding="utf-8-sig")))
for r in filas:
    r["acceso"], r["enlace_libre"] = "de pago (UPeU)", ""
    if not r["doi"]:
        r["acceso"] = "sin DOI (buscar por título)"
        continue
    try:
        req = urllib.request.Request("https://api.openalex.org/works/doi:" + urllib.parse.quote(r["doi"]),
                                     headers={"User-Agent": "Mozilla/5.0"})
        w = json.load(urllib.request.urlopen(req, timeout=30))
    except Exception:
        continue
    oa = w.get("open_access") or {}
    if oa.get("oa_status") in ABIERTO:
        r["acceso"] = "abierto (navegador, sin cuenta)"
        loc = w.get("best_oa_location") or {}
        r["enlace_libre"] = loc.get("pdf_url") or loc.get("landing_page_url") or oa.get("oa_url") or r["enlace"]

orden = {"abierto (navegador, sin cuenta)": 0, "de pago (UPeU)": 1, "sin DOI (buscar por título)": 2}
filas.sort(key=lambda r: (orden[r["acceso"]], r["carpeta"], r["nombre_de_archivo"]))
campos = ["acceso", "carpeta", "nombre_de_archivo", "enlace_libre", "enlace", "titulo", "doi", "id"]
with open(ARCH, "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.DictWriter(fh, fieldnames=campos, extrasaction="ignore")
    w.writeheader()
    w.writerows(filas)

from collections import Counter
print(Counter(r["acceso"] for r in filas))
