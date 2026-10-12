"""Análisis bibliométrico y cribado de las búsquedas de Scopus S1–S4 (Articulos/SCUPUS/S*.csv).

Genera lo que usa EstadoArte/EstadoArte_NFR.tex:
  - Articulos/cribado.csv               decisión (I/S/CE1–CE5) de cada uno de los registros únicos
  - Articulos/incluidos.csv             estudios incluidos con sus etiquetas (enfoque, fuente, tarea…)
  - Articulos/estadisticas_scopus.txt   todos los conteos que aparecen en el estado del arte
  - recursos/mapa_literatura.{png,pdf}  mapa de co-citación de los estudios incluidos

Las decisiones del cribado por título/resumen están en cribado_decisiones.py y los criterios en
criterios_inclusion_exclusion.md. Las etiquetas temáticas se asignan por palabras clave en el título,
el resumen y las palabras clave de autor, y se corrigen a mano (ENFOQUE_MANUAL, AUMENTO_MANUAL en
cribado_decisiones.py). Sirven para describir el panorama, no para incluir/excluir.

Uso:  python Articulos/analisis_scopus.py
"""
import csv
import os
import re
import sys
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

sys.stdout.reconfigure(encoding="utf-8")
BASE = os.path.dirname(os.path.abspath(__file__))
RECURSOS = os.path.join(BASE, "..", "recursos")
BUSQUEDAS = ["S1", "S2", "S3", "S4"]

# --- 1. Carga, conteo por búsqueda y deduplicación ----------------------------
por_busqueda, unicos = {}, {}
for b in BUSQUEDAS:
    with open(os.path.join(BASE, "SCUPUS", f"{b}.csv"), encoding="utf-8-sig") as fh:
        filas = list(csv.DictReader(fh))
    por_busqueda[b] = len(filas)
    for x in filas:
        clave = (x["DOI"] or x["Title"]).strip().lower()
        unicos.setdefault(clave, {**x, "busquedas": set()})["busquedas"].add(b)
registros = sum(por_busqueda.values())
lista = sorted(unicos.values(), key=lambda x: (x["Year"], x["Title"]))  # el ID es la posición + 1

# --- 2. Cribado por título y resumen ------------------------------------------
dec = {}
exec(open(os.path.join(BASE, "cribado_decisiones.py"), encoding="utf-8").read(), dec)
CODIGO = {**{i: "I" for i in dec["I"]}, **{i: "CE4" for i in dec["S"]}, **{i: "CE2" for i in dec["E2"]},
          **{i: "CE3" for i in dec["E3"]}, **{i: "CE5" for i in dec["E5"]}}
MOTIVO = {"I": "Incluido para texto completo", "CE1": "Fuera del dominio de software",
          "CE2": "Otra tarea de software/RE o clases que no son tipos de requerimiento",
          "CE3": "Sin evaluación empírica", "CE4": "Estudio secundario (contexto)",
          "CE5": "Duplicado o versión resumida de otro registro"}
for i, x in enumerate(lista, 1):
    x["id"], x["decision"] = i, CODIGO.get(i, "CE1")
incl = [x for x in lista if x["decision"] == "I"]

# --- 3. Etiquetas temáticas de los incluidos ----------------------------------
def texto(x):
    return " ".join([x["Title"], x["Abstract"], x["Author Keywords"]]).lower()


ENFOQUE = [  # orden de prioridad para el enfoque principal
    ("LLM", r"large language model|\bllms?\b|\bgpt|chatgpt|llama|gemma|mistral|zero-?shot|few-?shot|prompt"),
    ("Transformer", r"\bbert\b|roberta|xlnet|distilbert|transformer|pre-?trained (language )?model"),
    ("Aprendizaje profundo", r"deep learning|\bcnn\b|lstm|\bgru\b|neural network|convolutional|attention"),
    ("ML clásico", r"."),
]
AUMENTO = {
    "SMOTE / remuestreo": r"smote|tomek|oversampl|over-sampl|undersampl|resampl|random over",
    "EDA / léxica": r"easy data augmentation|\beda\b|synonym|random insertion|random swap",
    "Retrotraducción": r"back.?translat",
    "TextAttack / TAOS": r"textattack|\btaos\b",
    "Generación con LLM": r"(generat\w*|synthetic)\W+(\w+\W+){0,6}(data|requirements|samples|nfrs)\b.*?(llm|gpt|large language|chatgpt|generative)|(llm|gpt|large language|chatgpt|generative ai)\W+(\w+\W+){0,8}(generat\w*|synthetic)",
    "GAN": r"\bgan\b|generative adversarial",
    "Pérdida / pesos": r"focal loss|class weight|cost-sensitive|weighted loss",
}
DESBALANCE = r"imbalanc|augment|oversampl|smote|synthetic|minority class|long-tail|data scarcity|scarce"
FUENTE = [
    ("Reseñas / feedback", r"app review|user review|app store|user feedback|online feedback|crowd|user request"),
    ("Issues / GitHub", r"github|issue|bug report|defect report|open.?source"),
    ("Historias de usuario", r"user stor"),
    ("SRS / PROMISE", r"."),
]
DATASETS = {"PROMISE": r"promise(?!_exp| exp)", "PROMISE_exp": r"promise.?exp", "PURE": r"\bpure\b",
            "SecReq": r"secreq", "Dronology": r"dronology", "Mendeley FR_NFR": r"mendeley"}
for x in incl:
    t = texto(x)
    x["enfoque"] = next(k for k, p in ENFOQUE if re.search(p, t))
    x["aumento"] = [k for k, p in AUMENTO.items() if re.search(p, t)]
    x["desbalance"] = bool(re.search(DESBALANCE, t))
    x["fuente"] = next(k for k, p in FUENTE if re.search(p, t))
    x["datasets"] = [k for k, p in DATASETS.items() if re.search(p, t)]
    x["multietiqueta"] = bool(re.search(r"multi-?label", t))
    x["binaria"] = bool(re.search(r"functional and non-?functional|fr(s)? (and|vs\.?|/) nfr|binary", t))
    x["enfoque"] = dec["ENFOQUE_MANUAL"].get(x["id"], x["enfoque"])
    x["aumento"] = dec["AUMENTO_MANUAL"].get(x["id"], x["aumento"])
    x["desbalance"] = x["desbalance"] or bool(x["aumento"])

# --- 4. Co-citación dentro de los incluidos -----------------------------------
FUNDACIONALES = {
    "BERT (Devlin 2019)": r"bert: pre-training of deep bidirectional",
    "NoRBERT (Hey 2020)": r"norbert",
    "Kurtanović y Maalej 2017": r"automatically classifying functional and non-functional",
    "Cleland-Huang et al. 2007": r"automated classification of non-functional requirements",
    "PURE (Ferrari 2017)": r"pure: a dataset of public requirements",
    "GPT-3 (Brown 2020)": r"language models are few-shot learners",
    "Dalpiaz et al. 2019": r"requirements classification with interpretable machine learning",
    "Alhoshan et al. 2023": r"zero-shot learning for requirements classification",
    "PRCBERT (Luo 2022)": r"prcbert",
    "Lima et al. 2019 (PROMISE_exp)": r"software engineering repositories: expanding the promise",
    "SMOTE (Chawla 2002)": r"smote: synthetic minority",
    "EDA (Wei y Zou 2019)": r"eda: easy data augmentation",
    "TextAttack (Morris 2020)": r"textattack: a framework",
}
cocit = Counter()
for x in incl:
    refs = x["References"].lower()
    x["cita"] = {k for k, p in FUNDACIONALES.items() if re.search(p, refs)}
    cocit.update(x["cita"])

# --- 5. Mapa de la literatura (estudios incluidos) ----------------------------
# Mapa bipartito: los trabajos base quedan fijos en un círculo interior y cada estudio incluido se
# ubica según los trabajos base que cita (una arista = el estudio cita ese trabajo).
import math
SEMILLAS = {
    "10.48084/etasr.14313": "TAOS (Ben Ammar 2025)",
    "10.1007/s00766-025-00451-8": "Binkhonain y Alfayez 2025",
    "10.1109/access.2025.3570359": "Alhaizaey y Al-Mashari 2025",
}
NUCLEO = ["NoRBERT (Hey 2020)", "PRCBERT (Luo 2022)", "Alhoshan et al. 2023", "GPT-3 (Brown 2020)",
          "PURE (Ferrari 2017)", "Lima et al. 2019 (PROMISE_exp)", "SMOTE (Chawla 2002)",
          "EDA (Wei y Zou 2019)", "Cleland-Huang et al. 2007", "Kurtanović y Maalej 2017",
          "Dalpiaz et al. 2019"]
G = nx.Graph()
fijo = {}
for k, n in enumerate(NUCLEO):
    G.add_node(n, tipo="base")
    ang = 2 * math.pi * k / len(NUCLEO)
    fijo[n] = (math.cos(ang), math.sin(ang))
for x in incl:
    d = x["DOI"].lower() or x["Title"].lower()
    citas = [k for k in NUCLEO if k in x["cita"]]
    if not citas:
        continue
    G.add_node(d, tipo="semilla" if d in SEMILLAS else "corpus", enfoque=x["enfoque"])
    for k in citas:
        G.add_edge(d, k)
aislados = [x for x in incl if not (x["cita"] & set(NUCLEO))]
import random
random.seed(7)
pos = dict(fijo)
for n in G:  # cada estudio va al centroide de los trabajos base que cita, con un pequeño desplazamiento
    if n not in fijo:
        vec = [fijo[k] for k in G[n]]
        cx, cy = sum(v[0] for v in vec) / len(vec), sum(v[1] for v in vec) / len(vec)
        f = 0.55 if len(vec) == 1 else 0.85
        pos[n] = (cx * f + random.uniform(-0.09, 0.09), cy * f + random.uniform(-0.09, 0.09))
COLOR = {"LLM": "#d97706", "Transformer": "#059669", "Aprendizaje profundo": "#2563eb", "ML clásico": "#9ca3af"}

fig, ax = plt.subplots(figsize=(7.2, 6.4))
nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#cbd5e1", width=0.4, alpha=0.8)
corpus = [n for n in G if G.nodes[n]["tipo"] == "corpus"]
nx.draw_networkx_nodes(G, pos, nodelist=corpus, ax=ax, node_size=26,
                       node_color=[COLOR[G.nodes[n]["enfoque"]] for n in corpus], alpha=0.9, linewidths=0)
nx.draw_networkx_nodes(G, pos, nodelist=NUCLEO, ax=ax, node_shape="s", node_color="#334155",
                       node_size=[30 + 3 * G.degree(n) for n in NUCLEO])
sem = [n for n in G if G.nodes[n]["tipo"] == "semilla"]
nx.draw_networkx_nodes(G, pos, nodelist=sem, ax=ax, node_shape="*", node_color="#dc2626",
                       node_size=380, edgecolors="black", linewidths=0.6)
for n in NUCLEO:  # etiqueta pegada al cuadrado, hacia afuera del círculo
    x, y = pos[n]
    ax.annotate(f"{n} [{G.degree(n)}]", (x, y), xytext=(14 * x, 10 * y), textcoords="offset points",
                ha="left" if x > 0.2 else "right" if x < -0.2 else "center", va="center", fontsize=6.6,
                color="#0f172a", zorder=6, bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9))
for n in sem:
    x, y = pos[n]
    ax.annotate(SEMILLAS[n], (x, y), xytext=(0, 9), textcoords="offset points", ha="center", va="bottom",
                fontsize=6.6, fontweight="bold", color="#991b1b", zorder=7,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.9))
ley = [plt.Line2D([], [], marker="*", ls="", color="#dc2626", ms=11, mec="k", label="Artículo semilla"),
       plt.Line2D([], [], marker="s", ls="", color="#334155", ms=6, label="Trabajo base [n.º de estudios que lo citan]")]
ley += [plt.Line2D([], [], marker="o", ls="", color=c, ms=5, label=f"Incluido: {k}") for k, c in COLOR.items()]
ax.legend(handles=ley, loc="upper center", bbox_to_anchor=(0.5, 0.02), ncol=3, fontsize=6.3, frameon=False)
ax.set_xlim(-1.9, 1.9)
ax.set_ylim(-1.25, 1.2)
ax.axis("off")
fig.tight_layout()
for ext in ("png", "pdf"):
    fig.savefig(os.path.join(RECURSOS, f"mapa_literatura.{ext}"), dpi=300)

# --- 6. Salidas ----------------------------------------------------------------
with open(os.path.join(BASE, "cribado.csv"), "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.writer(fh)
    w.writerow(["id", "decision", "motivo", "anio", "tipo", "titulo", "fuente", "doi", "busquedas"])
    for x in lista:
        w.writerow([x["id"], x["decision"], MOTIVO[x["decision"]], x["Year"], x["Document Type"], x["Title"],
                    x["Source title"], x["DOI"], " ".join(sorted(x["busquedas"]))])
with open(os.path.join(BASE, "incluidos.csv"), "w", newline="", encoding="utf-8-sig") as fh:
    w = csv.writer(fh)
    w.writerow(["id", "anio", "tipo", "titulo", "fuente_pub", "doi", "citas", "enfoque", "aumento",
                "desbalance", "fuente_datos", "datasets", "multietiqueta", "binaria"])
    for x in incl:
        w.writerow([x["id"], x["Year"], x["Document Type"], x["Title"], x["Source title"], x["DOI"],
                    x["Cited by"] or 0, x["enfoque"], "; ".join(x["aumento"]), x["desbalance"], x["fuente"],
                    "; ".join(x["datasets"]), x["multietiqueta"], x["binaria"]])

with open(os.path.join(BASE, "estadisticas_scopus.txt"), "w", encoding="utf-8") as fh:
    def p(*a):
        print(*a)
        print(*a, file=fh)
    p("registros por búsqueda:", por_busqueda)
    p("registros identificados:", registros, "| duplicados:", registros - len(unicos), "| únicos:", len(unicos))
    p("decisiones:", sorted(Counter(x["decision"] for x in lista).items()))
    p("S5 (S1 y (S2 o S3)) entre incluidos:",
      sum(1 for x in incl if "S1" in x["busquedas"] and x["busquedas"] & {"S2", "S3"}))
    p("incluidos por tipo:", Counter(x["Document Type"] for x in incl).most_common())
    p("incluidos por año:", sorted(Counter(x["Year"] for x in incl).items()))
    tabla = Counter((x["Year"], x["enfoque"]) for x in incl)
    for e in COLOR:
        p(f"  {e:22s}", [tabla[(str(a), e)] for a in range(2017, 2027)])
    p("enfoque principal:", Counter(x["enfoque"] for x in incl).most_common())
    p("tratan desbalance/aumentación:", sum(x["desbalance"] for x in incl))
    p("métodos de aumentación:", Counter(m for x in incl for m in x["aumento"]).most_common())
    p("fuente de datos:", Counter(x["fuente"] for x in incl).most_common())
    p("datasets:", Counter(d for x in incl for d in x["datasets"]).most_common())
    p("multietiqueta:", sum(x["multietiqueta"] for x in incl), "| binaria FR/NFR:", sum(x["binaria"] for x in incl))
    p("desbalance x enfoque:", Counter(x["enfoque"] for x in incl if x["desbalance"]).most_common())
    p("LLM y aumentación:", [x["id"] for x in incl if x["enfoque"] == "LLM" and x["aumento"]])
    p("Transformer y aumentación:", [x["id"] for x in incl if x["enfoque"] == "Transformer" and x["aumento"]])
    p("co-citación (de", len(incl), "incluidos):", cocit.most_common())
    p("mapa: nodos", G.number_of_nodes(), "aristas", G.number_of_edges(), "aislados", len(aislados))
    p("grado de las semillas:", {SEMILLAS[n].split(chr(10))[0]: G.degree(n) for n in sem})
