"""Genera RSL/anexo_cadenas.tex con las cadenas de búsqueda de Scopus, tomadas del archivo de fórmulas.

Uso:  python Articulos/anexo_cadenas.py
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SCOPUS = open(os.path.join(BASE, "FORMULAS_BUSQUEDA_SCOPUS.txt"), encoding="utf-8").read()
EJES = ["aumentación y desbalance", "BERT y transformers", "LLM como clasificador",
        "GitHub y auto-etiquetado"]


def cadena(texto):
    return r"\begin{flushleft}\ttfamily\scriptsize\detokenize{" + texto.strip() + r"}\end{flushleft}"


partes = [r"\section*{Anexo A. Cadenas de búsqueda completas}",
          r"\addcontentsline{toc}{section}{Anexo A. Cadenas de búsqueda completas}",
          r"Las cuatro cadenas se ejecutaron en Scopus (\emph{Advanced document search}) en octubre de 2026. "
          r"Los registros de las cuatro se unieron y se eliminaron los duplicados entre cadenas."]

scopus = [l for l in SCOPUS.splitlines() if l.startswith("TITLE-ABS-KEY")]
for k, c in enumerate(scopus[:4]):
    partes += [rf"\textbf{{S{k + 1}: {EJES[k]}.}}", cadena(c)]

open(os.path.join(BASE, "..", "RSL", "anexo_cadenas.tex"), "w", encoding="utf-8").write("\n\n".join(partes) + "\n")
print(f"Scopus {len(scopus)} cadenas -> RSL/anexo_cadenas.tex")
