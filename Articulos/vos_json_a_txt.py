"""Convierte un mapa VOSviewer JSON en los archivos de mapa y red (formato VOSviewer)."""
import json
import sys

entrada, salida_map, salida_net = sys.argv[1:4]
d = json.load(open(entrada, encoding="utf-8-sig"))["network"]
pesos = sorted({k for it in d["items"] for k in it.get("weights", {})})
puntajes = sorted({k for it in d["items"] for k in it.get("scores", {})})
with open(salida_map, "w", encoding="utf-8") as fh:
    fh.write("\t".join(["id", "label", "x", "y", "cluster"] + [f"weight<{w}>" for w in pesos]
                       + [f"score<{s}>" for s in puntajes]) + "\n")
    for it in d["items"]:
        fila = [it["id"], it["label"], it["x"], it["y"], it["cluster"]]
        fila += [it["weights"].get(w, 0) for w in pesos] + [it.get("scores", {}).get(s, 0) for s in puntajes]
        fh.write("\t".join(str(v) for v in fila) + "\n")
with open(salida_net, "w", encoding="utf-8") as fh:
    for l in d["links"]:
        fh.write(f"{l['source_id']}\t{l['target_id']}\t{l.get('strength', 1)}\n")
print(len(d["items"]), "ítems,", len(d["links"]), "enlaces")
