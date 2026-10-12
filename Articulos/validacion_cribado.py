"""Validación del cribado por un segundo revisor (sustituye a Rayyan).

Paso 1 — generar la planilla ciega:
    python Articulos/validacion_cribado.py generar
  Crea Articulos/validacion_cribado_revisor2.xlsx con todos los estudios incluidos y una muestra
  aleatoria del 20 % de los excluidos (semilla fija), en orden aleatorio y SIN la decisión del
  primer revisor. El segundo revisor llena las columnas "Decisión" y "Código" con las listas.

Paso 2 — calcular el acuerdo:
    python Articulos/validacion_cribado.py kappa
  Compara las decisiones con Articulos/cribado.csv, imprime el kappa de Cohen y la tabla de
  acuerdo, y guarda los desacuerdos en Articulos/desacuerdos_cribado.csv para resolverlos
  entre los autores.
"""
import csv
import os
import random
import re
import sys
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
PLANILLA = os.path.join(BASE, "validacion_cribado_revisor2.xlsx")
CRITERIOS = [
    ("CI1", "Estudio primario que clasifica texto de requerimientos en tipos (FR/NFR, subclases) o atributos de calidad"),
    ("CI2", "Usa ML, aprendizaje profundo, transformers o LLM"),
    ("CI3", "Reporta evaluación empírica cuantitativa (exactitud, precisión, recall, F1…)"),
    ("CE1", "Fuera del dominio de software (manufactura, medicina, redes…)"),
    ("CE2", "Otra tarea de software/RE (ambigüedad, trazabilidad, generación, bugs…) o clases que no son tipos de requerimiento"),
    ("CE3", "Sin evaluación empírica (visión, tutorial, dataset sin experimentos)"),
    ("CE4", "Estudio secundario (revisión, mapeo, survey)"),
    ("CE5", "Duplicado o versión resumida/extendida de otro registro"),
]


def leer_cribado():
    with open(os.path.join(BASE, "cribado.csv"), encoding="utf-8-sig") as fh:
        return {int(r["id"]): r for r in csv.DictReader(fh)}


def resumenes():
    out = {}
    for b in ["S1", "S2", "S3", "S4"]:
        with open(os.path.join(BASE, "SCUPUS", f"{b}.csv"), encoding="utf-8-sig") as fh:
            for x in csv.DictReader(fh):
                out.setdefault((x["DOI"] or x["Title"]).strip().lower(), re.sub(r"\s+", " ", x["Abstract"]))
    return out


def generar():
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.worksheet.datavalidation import DataValidation

    crib, abst = leer_cribado(), resumenes()
    incluidos = [i for i, r in crib.items() if r["decision"] == "I"]
    excluidos = [i for i, r in crib.items() if r["decision"] != "I"]
    rnd = random.Random(2026)
    muestra = incluidos + rnd.sample(excluidos, round(0.2 * len(excluidos)))
    rnd.shuffle(muestra)

    wb = Workbook()
    ws = wb.active
    ws.title = "Cribado"
    enc = ["ID", "Año", "Título", "Resumen", "Decisión (I/E)", "Código (CE1–CE5 si E)", "Comentario"]
    ws.append(enc)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="1F4E78")
    for i in muestra:
        r = crib[i]
        clave = (r["doi"] or r["titulo"]).strip().lower()
        ws.append([i, int(r["anio"]), r["titulo"], abst.get(clave, ""), None, None, None])
    for col, ancho in zip("ABCDEFG", [6, 7, 45, 90, 14, 20, 30]):
        ws.column_dimensions[col].width = ancho
    for fila in ws.iter_rows(min_row=2):
        for c in fila:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    fin = len(muestra) + 1
    dv1 = DataValidation(type="list", formula1='"I,E"', allow_blank=True)
    dv2 = DataValidation(type="list", formula1='"CE1,CE2,CE3,CE4,CE5"', allow_blank=True)
    ws.add_data_validation(dv1)
    ws.add_data_validation(dv2)
    dv1.add(f"E2:E{fin}")
    dv2.add(f"F2:F{fin}")
    for c in ws[f"E2:F{fin}"]:
        for x in c:
            x.fill = PatternFill("solid", fgColor="FFF2CC")
    ws.freeze_panes = "C2"

    inst = wb.create_sheet("Instrucciones")
    inst.append(["Cómo llenar la planilla"])
    inst["A1"].font = Font(bold=True, size=13)
    for t in ["1. Lee el título y el resumen de cada fila. No consultes las decisiones del otro revisor.",
              "2. En 'Decisión' elige I (incluir: cumple CI1, CI2 y CI3) o E (excluir).",
              "3. Si eliges E, indica en 'Código' el criterio de exclusión que aplica.",
              "4. Regla de duda: si el resumen no basta para decidir, marca I (pasa a texto completo).",
              "5. Al terminar, guarda el archivo con el mismo nombre y ejecuta: "
              "python Articulos/validacion_cribado.py kappa", ""]:
        inst.append([t])
    inst.append(["Código", "Criterio"])
    for c in inst[inst.max_row]:
        c.font = Font(bold=True)
    for cod, txt in CRITERIOS:
        inst.append([cod, txt])
    inst.column_dimensions["A"].width = 12
    inst.column_dimensions["B"].width = 110
    wb.move_sheet("Instrucciones", offset=-1)
    wb.save(PLANILLA)
    print(f"Planilla creada: {PLANILLA}")
    print(f"  {len(incluidos)} incluidos + {len(muestra) - len(incluidos)} excluidos (20 %) = {len(muestra)} filas")


def kappa():
    from openpyxl import load_workbook

    crib = leer_cribado()
    ws = load_workbook(PLANILLA)["Cribado"]
    pares, desacuerdos, vacios = [], [], 0
    for fila in ws.iter_rows(min_row=2, values_only=True):
        i, _, titulo, _, dec, cod, com = fila
        if dec not in ("I", "E"):
            vacios += 1
            continue
        r1 = "I" if crib[i]["decision"] == "I" else "E"
        pares.append((r1, dec))
        if r1 != dec:
            desacuerdos.append([i, titulo, crib[i]["decision"], dec, cod or "", com or ""])
    if vacios:
        print(f"Atención: {vacios} filas sin decisión (no se cuentan).")
    n = len(pares)
    if not n:
        sys.exit("La planilla no tiene decisiones todavía.")
    po = sum(a == b for a, b in pares) / n
    c1, c2 = Counter(a for a, _ in pares), Counter(b for _, b in pares)
    pe = sum(c1[k] * c2[k] for k in ("I", "E")) / n ** 2
    k = (po - pe) / (1 - pe) if pe < 1 else 1.0
    t = Counter(pares)
    print(f"Registros comparados: {n}")
    print(f"                 Revisor 2: I   E")
    print(f"  Revisor 1: I            {t[('I','I')]:4d} {t[('I','E')]:3d}")
    print(f"  Revisor 1: E            {t[('E','I')]:4d} {t[('E','E')]:3d}")
    print(f"Acuerdo observado: {po:.1%}   Kappa de Cohen: {k:.3f}")
    nivel = ("casi perfecto" if k > .8 else "sustancial" if k > .6 else "moderado" if k > .4
             else "aceptable" if k > .2 else "leve")
    print(f"Interpretación (Landis y Koch, 1977): acuerdo {nivel}")
    with open(os.path.join(BASE, "desacuerdos_cribado.csv"), "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "titulo", "revisor1", "revisor2", "codigo_r2", "comentario_r2"])
        w.writerows(desacuerdos)
    print(f"{len(desacuerdos)} desacuerdos guardados en Articulos/desacuerdos_cribado.csv")


if __name__ == "__main__":
    {"generar": generar, "kappa": kappa}.get(sys.argv[1] if len(sys.argv) > 1 else "", lambda: print(__doc__))()
