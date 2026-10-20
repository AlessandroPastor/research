"""Prepara los archivos de entrada para VOSviewer (van Eck y Waltman, 2010).

Genera en Articulos/vosviewer/:
  - incluidos_scopus.csv        los 145 estudios incluidos, con las columnas originales de Scopus
                                 (VOSviewer lo lee con "Read data from bibliographic database files" -> Scopus)
  - tesauro_palabras_clave.txt   une sinónimos y descarta términos genéricos de indexación

Uso:  python Articulos/preparar_vosviewer.py
"""
import csv
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(BASE, "vosviewer")
os.makedirs(SALIDA, exist_ok=True)

# --- 1. CSV con los estudios incluidos, en formato Scopus -----------------------
with open(os.path.join(BASE, "cribado.csv"), encoding="utf-8-sig") as fh:
    incluidos = {(r["doi"] or r["titulo"]).strip().lower() for r in csv.DictReader(fh) if r["decision"] == "I"}

filas, vistos, columnas = [], set(), None
for b in ["S1", "S2", "S3", "S4"]:
    with open(os.path.join(BASE, "SCUPUS", f"{b}.csv"), encoding="utf-8-sig", newline="") as fh:
        lector = csv.DictReader(fh)
        columnas = columnas or lector.fieldnames
        for x in lector:
            clave = (x["DOI"] or x["Title"]).strip().lower()
            if clave in incluidos and clave not in vistos:
                vistos.add(clave)
                filas.append(x)

with open(os.path.join(SALIDA, "incluidos_scopus.csv"), "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=columnas, quoting=csv.QUOTE_ALL, extrasaction="ignore")
    w.writeheader()
    w.writerows(filas)

# --- 2. Tesauro (formato VOSviewer: "label<TAB>replace by"; vacío = descartar) ---
UNIR = {
    "requirements engineering": ["requirement engineering", "requirements engineering (re)"],
    "non-functional requirements": ["non-functional requirement", "nonfunctional requirements", "nonfunctional requirement",
                                    "non functional requirements", "nfr", "nfrs", "non-functional", "quality requirements",
                                    "quality requirement"],
    "requirements classification": ["requirements classifications", "requirement classification", "software requirement classification",
                                    "software requirements classification", "requirements classification (rc)",
                                    "non-functional requirements classification", "nfr classification"],
    "software requirements": ["software requirement", "requirements", "software requirements specifications",
                              "software requirements specification", "specifications", "srs"],
    "functional requirements": ["functional requirement", "functionals"],
    "machine learning": ["machine-learning", "learning systems", "learning algorithms", "supervised learning",
                         "supervised machine learning", "learning approach"],
    "natural language processing": ["natural language processing systems", "nlp", "language processing",
                                    "natural languages", "computational linguistics", "text processing"],
    "deep learning": ["deep neural networks", "neural networks", "deep learning models"],
    "large language models": ["large language model", "llm", "llms", "language model", "language models",
                              "generative ai", "generative artificial intelligence"],
    "bert": ["bert model", "bidirectional encoder representations from transformers"],
    "transformers": ["transformer", "transformer modeling", "transformer models", "transformer model"],
    "zero-shot learning": ["zero-shot", "zero shot learning"],
    "few-shot learning": ["few-shot", "few shot learning"],
    "data augmentation": ["text augmentation", "data augmentations"],
    "class imbalance": ["imbalanced data", "imbalanced datasets", "data imbalance", "class imbalance problem"],
    "multi-label classification": ["multi-label classifications", "multi-labels", "multilabel classification"],
    "multi-class classification": ["multiclass classification"],
    "convolutional neural network": ["convolutional neural networks", "cnn"],
    "long short-term memory": ["lstm", "bilstm"],
    "support vector machine": ["support vector machines", "svm"],
    "prompt engineering": ["prompting", "prompt"],
    "user feedback": ["user reviews", "app reviews", "online user feedback"],
    "promise dataset": ["promise", "promise nfr"],
}
DESCARTAR = ["classification (of information)", "classification", "computer software selection and evaluation",
             "application programs", "computer software", "macros", "search engines", "open systems",
             "information systems", "information retrieval systems", "engineering education", "f1 scores",
             "performance", "semantics", "automation", "benchmarking", "classification tasks", "large datasets",
             "labeled data", "decision making", "decision trees", "nearest neighbor search", "functional programming",
             "learning", "state of the art", "data mining", "software design", "artificial intelligence",
             "computer aided software engineering", "requirement analysis"]

with open(os.path.join(SALIDA, "tesauro_palabras_clave.txt"), "w", encoding="utf-8") as fh:
    fh.write("label\treplace by\n")
    for destino, sinonimos in UNIR.items():
        for s in sinonimos:
            fh.write(f"{s}\t{destino}\n")
    for d in DESCARTAR:
        fh.write(f"{d}\t\n")

print(f"{len(filas)} estudios -> Articulos/vosviewer/incluidos_scopus.csv")
print("tesauro -> Articulos/vosviewer/tesauro_palabras_clave.txt")
