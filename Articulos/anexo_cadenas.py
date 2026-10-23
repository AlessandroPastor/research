"""Genera RSL/anexo_cadenas.tex con las cadenas de búsqueda completas, tomadas de los archivos de fórmulas.

Uso:  python Articulos/anexo_cadenas.py
"""
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
SCOPUS = open(os.path.join(BASE, "FORMULAS_BUSQUEDA_SCOPUS.txt"), encoding="utf-8").read()
OTRAS = open(os.path.join(BASE, "FORMULAS_BUSQUEDA_WOS_IEEE_ACM.txt"), encoding="utf-8").read()
EJES = ["aumentación y desbalance", "BERT y transformers", "LLM como clasificador",
        "GitHub y auto-etiquetado"]


def cadena(texto):
    return r"\begin{flushleft}\ttfamily\scriptsize\detokenize{" + texto.strip() + r"}\end{flushleft}"


partes = [r"\section*{Anexo A. Cadenas de búsqueda completas}",
          r"\addcontentsline{toc}{section}{Anexo A. Cadenas de búsqueda completas}"]

scopus = [l for l in SCOPUS.splitlines() if l.startswith("TITLE-ABS-KEY")]
partes.append(r"\subsection*{Scopus (Advanced document search)}")
for k, c in enumerate(scopus[:4]):
    partes += [rf"\textbf{{S{k + 1}: {EJES[k]}.}}", cadena(c)]

wos = [l for l in OTRAS.splitlines() if l.startswith("TS=")]
partes.append(r"\subsection*{Web of Science Core Collection (Advanced search)}")
for k, c in enumerate(wos[:4]):
    partes += [rf"\textbf{{W{k + 1}: {EJES[k]}.}}", cadena(c)]

ieee = [l for l in OTRAS.splitlines() if l.startswith('("non-functional requirement*"')]
partes.append(r"\subsection*{IEEE Xplore (Command Search)}")
partes.append(r"Filtros aplicados en la interfaz: años 2017--2026; tipo de contenido: conferencias, revistas, "
              r"magazines y libros.")
for k, c in enumerate(ieee[:4]):
    partes += [rf"\textbf{{I{k + 1}: {EJES[k]}.}}", cadena(c)]

f1 = re.search(r"Fila 1 \(Abstract\):\s*(.+)", OTRAS).group(1)
f2 = re.search(r"Fila 2 \(Abstract\):\s*(.+)", OTRAS).group(1)
acm = re.findall(r"--- A\d: [^\n]+\n(.+)", OTRAS)
partes.append(r"\subsection*{ACM Digital Library (Advanced Search, campo \emph{Abstract})}")
partes.append(r"Las tres filas se combinan con AND. Filtro de fecha de publicación: 2017--2026.")
partes += [r"\textbf{Fila 1 (común):}", cadena(f1), r"\textbf{Fila 2 (común):}", cadena(f2)]
for k, c in enumerate(acm[:4]):
    partes += [rf"\textbf{{A{k + 1} --- Fila 3: {EJES[k]}.}}", cadena(c)]

open(os.path.join(BASE, "..", "RSL", "anexo_cadenas.tex"), "w", encoding="utf-8").write("\n\n".join(partes) + "\n")
print(f"Scopus {len(scopus)}, WoS {len(wos)}, IEEE {len(ieee)}, ACM {len(acm)} -> RSL/anexo_cadenas.tex")
