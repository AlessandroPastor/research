"""Genera RSL/resultados_auto.tex: cifras del PRISMA, tablas del mapeo y de la síntesis del texto completo.

Entradas:
  Articulos/SCUPUS/S1..S4.csv                       registros identificados
  Articulos/cribado.csv                             decisión de cribado de cada registro único
  Articulos/incluidos.csv                           etiquetas (por resumen) de los 145 incluidos
  Articulos/extraccion/extraccion_texto_completo.json   extracción y calidad del texto completo

Cada vez que se agrega un lote de extracción, se vuelve a ejecutar y se recompila RSL/rsl.tex.

Uso:  python Articulos/resultados_rsl.py
"""
import csv
import json
import os
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(BASE, "..", "RSL", "resultados_auto.tex")


def leer(ruta):
    with open(ruta, encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


identificados = {s: len(leer(os.path.join(BASE, "SCUPUS", s + ".csv"))) for s in ("S1", "S2", "S3", "S4")}
cribado = leer(os.path.join(BASE, "cribado.csv"))
decision = Counter(f["decision"] for f in cribado)
incluidos = {f["id"]: f for f in leer(os.path.join(BASE, "incluidos.csv"))}
estudios = json.load(open(os.path.join(BASE, "extraccion", "extraccion_texto_completo.json"),
                          encoding="utf-8"))["estudios"]

excl_tc = sorted((i for i, v in estudios.items() if v.get("Elegible tras texto completo") == "No"), key=int)
sintesis = sorted((i for i in estudios if i not in excl_tc), key=int)
mapeo = [i for i in incluidos if i not in excl_tc]

# Descripción breve de cada estudio de la síntesis: clave bib, tarea, datos, desbalance, clasificador, F1 macro.
# Se redacta a partir de los campos del formulario de extracción.
CORTO = {
    "2": ("Deocadez2017-Automatically", "Bin.", "300 reseñas", "Ninguna (muestra balanceada)", "Semisupervisado (NB, SVM)", "--"),
    "13": ("Toth2018-Study", "MC 11", "PROMISE", "Elimina PO", "12 clasificadores ML", "0.76$^a$"),
    "19": ("Younas2019-Automated", "MC 12", "PROMISE", "Ninguna", "Similitud Word2Vec", "--"),
    "33": ("Hey2020-NoRBERT", "Bin./NFR", "PROMISE", "ROS/RUS (entren.)", "BERT", "--"),
    "70": ("Li2022-Automatic", "Bin./4 NFR", "PROMISE reetiq.", "Omite clases raras", "BERT + GAT", "--"),
    "98": ("Binkhonain2023-Machine", "MC 12", "PROMISE\\_exp", "Descomposición (entren.)", "SVM jerárquico", "0.51"),
    "138": ("Alhoshan2023-ZeroShot", "Bin./NFR", "PROMISE, SecReq", "Ninguna", "Zero-shot (SBERT)", "--"),
    "172": ("Metu2024-Hybrid", "NFR", "PROMISE\\_exp", "Sobremuestreo previo$^b$", "Bi-LSTM + SVM", "--"),
    "174": ("Fazelnia2024-Lessons", "MC 12", "PROMISE", "ROS/RUS (entren.)", "NLI, ChatGPT", "--"),
    "177": ("Saleem2024-Mlr", "Multiet.", "PROMISE, EHR", "Ninguna", "BM25 + RL", "+13\\,\\%"),
    "226": ("Saleem2025-Analyzing", "MC", "Kaggle (976)", "Ninguna", "Few-shot (redes prot.)", "--"),
    "228": ("Binkhonain2025-Prompts", "Bin./NFR", "PROMISE, SecReq", "Ninguna", "5 LLM few-shot", "0.92--0.94"),
    "9": ("Li2018-Automatically", "MC", "Solicitudes OSS (3,000)", "Palabras clave, aprendizaje activo", "SVM, k-NN, NB", "--"),
    "71": ("Li2022-Automatically", "NFR", "PROMISE ampliado", "Conjunto balanceado nuevo", "BERT + Bi-LSTM", "--"),
    "72": ("Kaur2022-Bert", "4 NFR", "PROMISE", "Omite clases raras", "BERT-CNN", "--"),
    "118": ("Kaur2023-Improving", "Bin./NFR", "PROMISE", "Agrupa raras en 'otras'", "BERT-BiLSTM-CNN", "--"),
    "245": ("Casillo2025-Beyond", "Seg. bin.", "SecReq", "Ninguna", "ML, BERT con CWE/CVE", "--"),
    "253": ("Ali2025-Cloud", "Bin./NFR", "PROMISE (1,521)", "SMOTE previo$^b$", "SVM, RF, CNN, BERT", "--"),
    "285": ("Alsanoosy2025-Large", "Bin.", "9 fuentes (4,732)", "Ninguna (balanceado)", "Ensamble de 7 codif.", "--"),
    "349": ("Petrillo2026-Explainable", "Seg. bin.", "SecReq", "Ninguna", "RoBERTa, LoRA", "--"),
    "380": ("NguyenVan2026-Evaluating", "Jerárq.", "4 fuentes, sin dup.", "Focal Loss", "Transformer jerárquico", "0.90/0.72/0.55"),
    "400": ("Kaur2026-Hybrid", "Jerárq.", "PROMISE\\_exp, PURE, SRS", "Aumentación BERT previa$^b$", "LSTM-BERT-LSTM", "--"),
    "419": ("Rahman2026-RequiBERT", "Bin./NFR", "PROMISE", "Elimina PO", "BERT de dominio", "0.85"),
    "89": ("Vijayvargiya2022-Software", "Bin.", "PROMISE", "SMOTE previo$^b$", "8 modelos DL", "--"),
    "97": ("Yahya2023-Novel", "NFR 5", "Reseñas en árabe", "EDA (TextAttack)", "RNN + LSTM", "--"),
    "112": ("Yucalar2023-Developing", "Bin.", "Turco (4,600)", "Ninguna", "BERTurk y 19 más", "--"),
    "127": ("Khan2023-Non", "MC 12", "PROMISE", "Muestras añadidas a mano", "XLNet, BERT", "--"),
    "156": ("Bagies2024-Classifying", "Seg. CIA", "1,135 req. seguridad", "Ninguna", "SVM + SBERT", "--"),
    "164": ("Abbas2024-Enscl", "Bin.", "PROMISE\\_exp", "SMOTE-Tomek previo$^b$", "Ensamble + CatBoost", "--"),
    "231": ("Alhaizaey2025-AgilePLM", "MC 8", "10,006 historias", "Focal Loss", "BERT, XLNet", "--"),
    "241": ("Eltahier2025-Bert", "Bin.", "PROMISE, FR\\_NFR", "Ninguna", "BERT", "--"),
    "261": ("Subahi2025-Enhancing", "Seg. bin./7", "803 NFR", "Paráfrasis T5", "BERT, ANN, SVM", "--"),
    "267": ("Petrillo2025-Explainable", "Seg. bin.", "SecReq", "3 aumentaciones (entren.)", "BERT, RoBERTa, XLNet", "--"),
    "275": ("Karlsson2025-Reliable", "FR/NFR", "PROMISE", "Ninguna", "GPT-4o, LLaMA 3.3", "--"),
    "299": ("Shafikuzzaman2025-Effectiveness", "Bin./NFR", "PROMISE, SecReq", "Omite clases raras", "GPT-4o, Llama 3, SBERT", "0.66--0.80"),
    "336": ("Bhar2026-Knowledge", "NFR 5", "PROMISE + clínicos", "Ninguna", "BERT, SVM", "--"),
    "344": ("Aldhafer2026-Adaptive", "Bin./4/10", "PROMISE, EHR", "Aumentación adaptativa (entren.)", "BiGRU", "+6.7 pts"),
    "348": ("Said2026-Intelligent", "MC 12", "PROMISE(\\_exp)", "Aumentación (entren.)", "BERT + RoBERTa", "0.84/0.90"),
    "363": ("Almohammady2026-Context", "4 NFR", "PROMISE, PURE", "Focal Loss", "Codificador de dominio", "0.80$^d$"),
    "381": ("Aloufi2026-Evireqrag", "Bin./NFR", "PROMISE(\\_exp), SecReq", "Ninguna", "RAG + LLM", "0.89"),
    "403": ("Limaylla2025-Spanish", "NFR 11", "PROMISE\\_exp (español)", "Generación ChatGPT + RUS", "RL, NB, SVM", "en tablas"),
    "414": ("Bishop2026-demand", "NFR 9", "Sintético (O3DG)", "Generación con LLM", "ML y DL", "--"),
    "425": ("Alhoshan2026-SeqFAL", "Seg. bin.", "SecReq + PROMISE", "Ninguna", "Aprendizaje activo federado", "--"),
    "430": ("Bagies2026-Transformer", "Seg. bin.", "Reseñas", "Ninguna", "SBERT, Paraphrase", "--"),
    "252": ("Groen2025-Classification", "Calidad ISO", "1,000 reseñas", "Ninguna", "Patrones, crowd, ChatGPT", "--"),
    "391": ("Kamal2026-GitReq", "MC 8", "GitReq (6,302 issues)", "Ninguna", "4 LLM zero-shot", "0.64"),
    "432": ("Wellhausen2026-UserReviews", "Usab. bin.", "300 reseñas", "Ninguna", "GPT-4.1", "--"),
    "250": ("BenAmmar2025-TAOS", "MC 12", "PROMISE deriv.", "TAOS (entren.)", "BERT", "0.89$^c$"),
    "269": ("Chaudhary2025-Exploring", "FR/NFR", "1,880 reseñas", "Ninguna", "GPT-4o mini", "--"),
    "272": ("Pham2025-Generating", "NFR 11", "PROMISE, PURE", "Generación GPT-4o (entren.)", "SVM, NB, BERT", "--"),
    "273": ("Saleem2025-Generative", "FR/NFR", "PROMISE", "Ninguna", "ChatGPT, Gemini", "--"),
    "277": ("Alsaleh2025-Hybrid", "Usab. 3", "Reseñas", "Ninguna", "BERT-BiLSTM-CNN", "--"),
    "280": ("Shreda2025-Identifying", "NFR 5", "PURE", "SMOTE + RUS", "ML, CNN, BERT", "--"),
    "295": ("Aryan2025-Multi", "Jerárq.", "PROMISE(\\_exp)", "Ninguna", "BERT, RoBERTa", "0.34--0.55"),
    "323": ("Tang2025-FewShot", "Bin./NFR", "PROMISE, PURE", "Ejemplos estratificados", "7 LLM few-shot", "0.60--0.80"),
    "330": ("Kiani2026-DeepLearning", "FR 6", "PROMISE, propio", "Sobremuestreo", "Ensamble BERT", "--"),
    "370": ("Khayashi2026-Deep", "Bin.", "PURE (4,661)", "Ninguna", "CNN, LSTM, GRU", "--"),
    "395": ("Nagaraju2026-Hierarchical", "Jerárq.", "PROMISE\\_exp", "Pesos, Focal Loss", "ML, DL, BERT", "0.66"),
}
faltan = [i for i in sintesis if i not in CORTO]
if faltan:
    raise SystemExit(f"Agregue a CORTO la descripción breve de: {faltan}")

lineas = ["% Archivo generado por Articulos/resultados_rsl.py. No editar a mano.", ""]


def macro(nombre, valor):
    lineas.append(rf"\newcommand{{\{nombre}}}{{{valor}}}")


# --- Cifras del PRISMA -----------------------------------------------------
macro("nS", " / ".join(str(identificados[s]) for s in ("S1", "S2", "S3", "S4")))
macro("nIdent", sum(identificados.values()))
macro("nDup", sum(identificados.values()) - len(cribado))
macro("nCrib", len(cribado))
macro("nExclCrib", sum(decision[c] for c in ("CE1", "CE2", "CE3", "CE5")))
macro("nCEuno", decision["CE1"])
macro("nCEdos", decision["CE2"])
macro("nCEtres", decision["CE3"])
macro("nCEcinco", decision["CE5"])
macro("nSec", decision["CE4"])
macro("nBuscados", decision["I"])
macro("nRecuperados", len(estudios))
macro("nSinAcceso", decision["I"] - len(estudios))
macro("nExclTC", len(excl_tc))
macro("nSintesis", len(sintesis))
macro("nMapeo", len(mapeo))


# --- Indicadores de la síntesis ------------------------------------------
def cuenta(campo, pred):
    return sum(1 for i in sintesis if pred(estudios[i].get(campo, "")))


tecnica = cuenta("Técnica contra el desbalance", lambda s: not s.startswith("Ninguna"))
macro("nTecnica", tecnica)
macro("nSoloEnt", cuenta("¿Aumenta solo el entrenamiento?", lambda s: s == "Sí"))
macro("nNoEnt", cuenta("¿Aumenta solo el entrenamiento?", lambda s: s == "No"))
macro("nEntNoIndica", cuenta("¿Aumenta solo el entrenamiento?", lambda s: s == "No se indica"))
macro("nMacro", cuenta("F1 macro", lambda s: s.strip() != ""))
macro("nDupSi", cuenta("¿Controla duplicados entre entrenamiento y prueba?", lambda s: s == "Sí"))
macro("nDupNo", cuenta("¿Controla duplicados entre entrenamiento y prueba?", lambda s: s == "No"))
macro("nDupNoIndica", cuenta("¿Controla duplicados entre entrenamiento y prueba?", lambda s: s == "No se indica"))
macro("nEstad", cuenta("¿Prueba estadística?", lambda s: s == "Sí"))
macro("nCodigo", cuenta("¿Código o datos disponibles?", lambda s: s == "Sí"))
macro("nLLMclas", cuenta("Uso del LLM", lambda s: s.startswith("Clasificador")))
macro("nLLMgen", cuenta("Uso del LLM", lambda s: s.startswith("Generador")))
totales = {i: sum(estudios[i]["calidad"].values()) for i in sintesis}
macro("qMedia", f"{sum(totales.values()) / len(totales):.1f}")
macro("qMin", f"{min(totales.values()):g}")
macro("qMax", f"{max(totales.values()):g}")
macro("nCalidadAlta", sum(1 for t in totales.values() if t >= 6))
macro("nCalidadBaja", sum(1 for t in totales.values() if t < 4))
lineas.append("")

# --- Tabla: mapeo por enfoque y periodo ------------------------------------
PERIODOS = [("2017--2020", range(2017, 2021)), ("2021--2023", range(2021, 2024)), ("2024--2026", range(2024, 2027))]
ENFOQUES = [("ML clásico", "ML clásico"), ("Aprendizaje profundo", "Aprendizaje profundo"),
            ("Transformer", "Transformers (BERT y variantes)"), ("LLM", "LLM")]
lineas += [r"\newcommand{\tablaMapeo}{%", r"\begin{table}[!t]",
           r"\caption{Estudios del mapeo por enfoque principal y periodo ($n=\nMapeo$)}", r"\label{tab:mapeo}",
           r"\centering\footnotesize", r"\begin{tabularx}{\columnwidth}{@{}Y rrr r@{}}", r"\toprule",
           r"\textbf{Enfoque} & " + " & ".join(rf"\textbf{{{p}}}" for p, _ in PERIODOS) + r" & \textbf{Total} \\",
           r"\midrule"]
for clave, nombre in ENFOQUES:
    fila = [sum(1 for i in mapeo if incluidos[i]["enfoque"] == clave and int(incluidos[i]["anio"]) in r)
            for _, r in PERIODOS]
    lineas.append(f"{nombre} & " + " & ".join(map(str, fila)) + f" & {sum(fila)} \\\\")
lineas.append(r"\midrule")
fila = [sum(1 for i in mapeo if int(incluidos[i]["anio"]) in r) for _, r in PERIODOS]
lineas.append(r"\textbf{Total} & " + " & ".join(map(str, fila)) + f" & {sum(fila)} \\\\")
fila = [sum(1 for i in mapeo if incluidos[i]["desbalance"] == "True" and int(incluidos[i]["anio"]) in r)
        for _, r in PERIODOS]
lineas.append(r"Mencionan el desbalance & " + " & ".join(map(str, fila)) + f" & {sum(fila)} \\\\")
lineas += [r"\bottomrule", r"\end{tabularx}", r"\end{table}}", ""]

# --- Tabla: técnicas y fuentes de datos en el mapeo -----------------------
aum = Counter(incluidos[i]["aumento"] for i in mapeo if incluidos[i]["aumento"])
fuentes = Counter(incluidos[i]["fuente_datos"] for i in mapeo)
macro("nMapeoTecnica", sum(aum.values()))
macro("nMapeoDesbalance", sum(1 for i in mapeo if incluidos[i]["desbalance"] == "True"))
macro("nMapeoPROMISE", fuentes["SRS / PROMISE"])
macro("nMapeoResenas", fuentes["Reseñas / feedback"])
macro("nMapeoIssues", fuentes["Issues / GitHub"])
macro("nMapeoHistorias", fuentes["Historias de usuario"])
macro("nMapeoBinaria", sum(1 for i in mapeo if incluidos[i]["binaria"] == "True"))
macro("nMapeoMultiet", sum(1 for i in mapeo if incluidos[i]["multietiqueta"] == "True"))
lineas += [r"\newcommand{\tablaTecnicas}{%", r"\begin{table}[!t]",
           r"\caption{Técnicas contra el desbalance identificadas en los resúmenes del mapeo}",
           r"\label{tab:tecnicas}", r"\centering\footnotesize", r"\begin{tabularx}{\columnwidth}{@{}Y r@{}}",
           r"\toprule", r"\textbf{Técnica} & \textbf{Estudios} \\", r"\midrule"]
for t, n in aum.most_common():
    lineas.append(f"{t} & {n} \\\\")
lineas += [r"\midrule", rf"\textbf{{Total}} & {sum(aum.values())} \\", r"\bottomrule", r"\end{tabularx}",
           r"\end{table}}", ""]

# --- Tabla: síntesis del texto completo -----------------------------------
# Se divide en partes de hasta FILAS_POR_TABLA filas para que cada una quepa en una página.
FILAS_POR_TABLA = 30
SIMB = {"Sí": r"\checkmark", "No": "--", "No aplica": "n/a", "No se indica": "?", "Parcial": "p"}
CABECERA = [r"\centering\scriptsize",
            r"\begin{tabularx}{\textwidth}{@{}L{2.3cm} L{1.3cm} L{2.0cm} L{3.4cm} Y L{1.4cm} c c c c@{}}",
            r"\toprule",
            r"\textbf{Estudio} & \textbf{Tarea} & \textbf{Datos} & \textbf{Tratamiento del desbalance} & "
            r"\textbf{Clasificador} & \textbf{F1 macro} & \textbf{Dup.} & \textbf{Est.} & \textbf{Cód.} & \textbf{QA} \\",
            r"\midrule"]
NOTA = (r"\\[2pt]\parbox{\textwidth}{\scriptsize Bin.: binaria FR/NFR; MC: multiclase con FR y NFR (número de "
        r"clases); Multiet.: multietiqueta; Jerárq.: jerárquica; Seg.: seguridad; ROS/RUS: sobremuestreo y "
        r"submuestreo aleatorios; (entren.): aplicado solo al entrenamiento. Dup.: controla duplicados entre "
        r"entrenamiento y prueba; Est.: prueba estadística; Cód.: código o datos disponibles; \checkmark{} sí, -- no, "
        r"? no se indica, n/a no aplica, p parcial. QA: puntuación de calidad sobre 8. "
        r"$^a$F1 calculado con la precisión y la exhaustividad promedio por clase. "
        r"$^b$El remuestreo o la aumentación se aplican antes de partir el conjunto. "
        r"$^c$Con fuga entre entrenamiento y prueba (Sección~\ref{sec:pr5}). "
        r"$^d$En proyectos no vistos; 0.97 con validación cruzada por oración.}")


def fila_sintesis(i):
    v = estudios[i]
    clave, tarea, datos, desb, clas, f1 = CORTO[i]
    return (rf"\cite{{{clave}}} ({incluidos[i]['anio']}) & {tarea} & {datos} & {desb} & {clas} & {f1} & "
            f"{SIMB.get(v['¿Controla duplicados entre entrenamiento y prueba?'], '?')} & "
            f"{SIMB.get(v['¿Prueba estadística?'], '?')} & {SIMB.get(v['¿Código o datos disponibles?'], '?')} & "
            f"{totales[i]:g} \\\\")


partes = [sintesis[k:k + FILAS_POR_TABLA] for k in range(0, len(sintesis), FILAS_POR_TABLA)]
lineas.append(r"\newcommand{\tablaSintesis}{%")
for n, parte in enumerate(partes, 1):
    sufijo = "" if len(partes) == 1 else f" (parte {n} de {len(partes)})"
    lineas += [r"\begin{table*}[!t]",
               rf"\caption{{Estudios analizados con el texto completo ($n=\nSintesis$){sufijo}}}"]
    if n == 1:
        lineas.append(r"\label{tab:sintesis}")
    lineas += CABECERA + [fila_sintesis(i) for i in parte] + [r"\bottomrule", r"\end{tabularx}"]
    if n == len(partes):
        lineas.append(NOTA)
    lineas.append(r"\end{table*}")
lineas += ["}", ""]

# --- Tabla: calidad por criterio ------------------------------------------
lineas += [r"\newcommand{\tablaCalidad}{%", r"\begin{table}[!t]",
           r"\caption{Resultado de la evaluación de calidad ($n=\nSintesis$)}", r"\label{tab:calidadres}",
           r"\centering\footnotesize", r"\begin{tabularx}{\columnwidth}{@{}Y rrr r@{}}", r"\toprule",
           r"\textbf{Criterio} & \textbf{Sí} & \textbf{Parcial} & \textbf{No} & \textbf{Media} \\", r"\midrule"]
NOMBRES = {"QA1": "QA1 Objetivos", "QA2": "QA2 Datos descritos", "QA3": "QA3 Protocolo sin fuga",
           "QA4": "QA4 Métricas para desbalance", "QA5": "QA5 Línea base", "QA6": "QA6 Variabilidad o pruebas",
           "QA7": "QA7 Reproducibilidad", "QA8": "QA8 Limitaciones"}
for q, nombre in NOMBRES.items():
    vals = [estudios[i]["calidad"][q] for i in sintesis]
    lineas.append(f"{nombre} & {vals.count(1)} & {vals.count(0.5)} & {vals.count(0)} & "
                  f"{sum(vals) / len(vals):.2f} \\\\")
lineas += [r"\bottomrule", r"\end{tabularx}", r"\end{table}}", ""]

open(SALIDA, "w", encoding="utf-8").write("\n".join(lineas) + "\n")
print(f"identificados {sum(identificados.values())}, únicos {len(cribado)}, incluidos {decision['I']}, "
      f"texto completo {len(estudios)} (excluidos {len(excl_tc)}), síntesis {len(sintesis)}, mapeo {len(mapeo)}")
print("->", os.path.normpath(SALIDA))
