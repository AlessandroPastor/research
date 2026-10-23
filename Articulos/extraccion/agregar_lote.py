"""Agrega un lote de extracciones (JSON) a extraccion_texto_completo.json.

Uso:  python Articulos/extraccion/agregar_lote.py <lote.json>
"""
import json
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
PRINCIPAL = os.path.join(BASE, "extraccion_texto_completo.json")
datos = json.load(open(PRINCIPAL, encoding="utf-8"))
lote = json.load(open(sys.argv[1], encoding="utf-8"))
datos["estudios"].update(lote)
json.dump(datos, open(PRINCIPAL, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"+{len(lote)} -> {len(datos['estudios'])} estudios extraídos")
