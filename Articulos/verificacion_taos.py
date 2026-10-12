"""Verificación de la partición pública de TAOS (github.com/boulbaba1981/TAOS).

Descarga train.csv y test.csv del repositorio de Ben Ammar y Almatrafi (2025) y mide:
  - cuántos requerimientos de prueba aparecen también en entrenamiento (fuga de información);
  - cuántos requerimientos distintos hay realmente después de quitar duplicados;
  - la distribución de clases con y sin duplicados.

Dos textos se consideran el mismo requerimiento si coinciden tras pasar a minúsculas y quitar la
puntuación, las comillas y los espacios repetidos (en el repositorio, muchos aparecen una vez entre
comillas simples y otra sin ellas).

Uso:  python Articulos/verificacion_taos.py
"""
import io
import re
import sys
import urllib.request

import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
RAW = "https://raw.githubusercontent.com/boulbaba1981/TAOS/HEAD/{}"
CLASES = ["F", "US", "SE", "PE", "O", "LF", "SC", "A", "MN", "L", "FT", "PO"]


def leer(nombre):
    with urllib.request.urlopen(RAW.format(nombre), timeout=60) as r:
        return pd.read_csv(io.BytesIO(r.read()))


def normalizar(texto):
    return re.sub(r"\W+", " ", str(texto).lower()).strip()


tr, te = leer("train.csv"), leer("test.csv")
tr["n"], te["n"] = tr.text.map(normalizar), te.text.map(normalizar)

exactos = te.text.str.strip().isin(set(tr.text.str.strip())).sum()
fuga = te[te.n.isin(set(tr.n))]
etiqueta_tr = dict(zip(tr.n, tr.label))
misma = sum(etiqueta_tr[n] == l for n, l in zip(fuga.n, fuga.label))
print(f"Entrenamiento: {len(tr)}  Prueba: {len(te)}")
print(f"Prueba con texto idéntico en entrenamiento: {exactos}")
print(f"Prueba con el mismo requerimiento en entrenamiento (normalizado): {len(fuga)} "
      f"({len(fuga) / len(te):.1%}); con la misma etiqueta: {misma}")
print("  por clase:", fuga.label.value_counts().reindex(CLASES, fill_value=0).to_dict())

todo = pd.concat([tr, te])
unicos = todo.drop_duplicates("n")
contradictorios = (todo.groupby("n").label.nunique() > 1).sum()
print(f"\nRequerimientos distintos en las {len(todo)} filas: {len(unicos)} "
      f"({len(todo) - len(unicos)} filas duplicadas); con etiquetas contradictorias: {contradictorios}")
c0, c1 = todo.label.value_counts(), unicos.label.value_counts()
print("Clase  Con duplicados  Sin duplicados")
for k in CLASES:
    print(f"{k:5s} {c0.get(k, 0):14d} {c1.get(k, 0):15d}")
print(f"Razón F:PO  con duplicados (solo entrenamiento) = {tr.label.value_counts()['F'] / tr.label.value_counts()['PO']:.1f}:1"
      f"  |  sin duplicados = {c1['F'] / c1['PO']:.1f}:1")
