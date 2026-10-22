"""Exporta con VOSviewer (línea de comandos) los mapas de palabras clave y les da formato final.

Requiere: VOSviewer.jar en C:\\VOSviewer, y Articulos/vosviewer/palabras.json guardado desde VOSviewer.
Genera en recursos/:
  - vos_palabras_red.png    vista de red (clústeres)
  - vos_palabras_anios.png  vista superpuesta por año promedio de publicación, con barra de colores

Uso:  python Articulos/vos_figuras.py
"""
import csv
import os
import subprocess

import matplotlib
matplotlib.use("Agg")
from matplotlib import cm
from PIL import Image, ImageChops, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
VOS = os.path.join(BASE, "vosviewer")
REC = os.path.abspath(os.path.join(BASE, "..", "recursos"))
JAR = r"C:\VOSviewer\VOSviewer.jar"
ANIO_MIN, ANIO_MAX = 2022, 2025

# 1. Mapa y red a partir del JSON guardado en VOSviewer
subprocess.run(["python", os.path.join(BASE, "vos_json_a_txt.py"), os.path.join(VOS, "palabras.json"),
                os.path.join(VOS, "palabras_map.txt"), os.path.join(VOS, "palabras_network.txt")], check=True)

# 2. Mapa para la vista por año: solo el puntaje de año, acotado a [ANIO_MIN, ANIO_MAX]
with open(os.path.join(VOS, "palabras_map.txt"), encoding="utf-8") as fh:
    filas = list(csv.reader(fh, delimiter="\t"))
cab = filas[0]
quitar = {i for i, c in enumerate(cab) if c in ("score<Avg. citations>", "score<Avg. norm. citations>")}
i_anio = cab.index("score<Avg. pub. year>")
with open(os.path.join(VOS, "palabras_map_anio.txt"), "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, delimiter="\t")
    for n, f in enumerate(filas):
        if n:
            f[i_anio] = str(min(max(float(f[i_anio]), ANIO_MIN), ANIO_MAX))
        w.writerow([v for i, v in enumerate(f) if i not in quitar])


# Colores de la vista por año: Viridis estándar, la misma paleta que se usa en la barra.
COLORES = os.path.join(VOS, "overlay_viridis.txt")
with open(COLORES, "w", encoding="utf-8") as fh:
    fh.write("color value\tred\tgreen\tblue\n")
    for i in range(11):
        r, g, b, _ = cm.viridis(i / 10)
        fh.write(f"{i / 10:.1f}\t{int(r * 255)}\t{int(g * 255)}\t{int(b * 255)}\n")


def vos(mapa, vista, salida, extra=()):
    # Si el archivo existe, VOSviewer pregunta si lo sobrescribe y se queda esperando.
    if os.path.exists(salida):
        os.remove(salida)
    subprocess.run(["java", "-jar", JAR, "-map", os.path.join(VOS, mapa), "-network",
                    os.path.join(VOS, "palabras_network.txt"), vista, *extra, "-skip_clustering",
                    "-save_screenshot_png", salida], check=True, cwd=os.path.dirname(JAR), timeout=120)


def recortar(img, margen=40):
    fondo = Image.new(img.mode, img.size, (255, 255, 255))
    caja = ImageChops.difference(img.convert("RGB"), fondo.convert("RGB")).getbbox()
    x0, y0, x1, y1 = caja
    return img.crop((max(0, x0 - margen), max(0, y0 - margen), min(img.width, x1 + margen),
                     min(img.height, y1 + margen)))


red = os.path.join(REC, "vos_palabras_red.png")
anios = os.path.join(REC, "vos_palabras_anios.png")
vos("palabras_map.txt", "-network_visualization", red)
vos("palabras_map_anio.txt", "-overlay_visualization", anios, ["-overlay_colors", COLORES])

recortar(Image.open(red).convert("RGB")).save(red, dpi=(300, 300))

# 3. Barra de colores (paleta por defecto de VOSviewer para la vista superpuesta: viridis)
img = recortar(Image.open(anios).convert("RGB"))
ancho, alto = 520, 34
barra = Image.new("RGB", (ancho, alto))
for x in range(ancho):
    r, g, b, _ = cm.viridis(x / (ancho - 1))
    for y in range(alto):
        barra.putpixel((x, y), (int(r * 255), int(g * 255), int(b * 255)))
try:
    fuente = ImageFont.truetype("arial.ttf", 30)
except OSError:
    fuente = ImageFont.load_default()
lienzo = Image.new("RGB", (img.width, img.height + 110), "white")
lienzo.paste(img, (0, 0))
d = ImageDraw.Draw(lienzo)
x0, y0 = img.width - ancho - 60, img.height + 20
lienzo.paste(barra, (x0, y0))
d.rectangle([x0, y0, x0 + ancho - 1, y0 + alto - 1], outline=(120, 120, 120))
for anio in range(ANIO_MIN, ANIO_MAX + 1):
    x = x0 + (anio - ANIO_MIN) / (ANIO_MAX - ANIO_MIN) * (ancho - 1)
    t = str(anio)
    tw = d.textlength(t, font=fuente)
    d.text((x - tw / 2, y0 + alto + 6), t, fill=(40, 40, 40), font=fuente)
lienzo.save(anios, dpi=(300, 300))
print("listo:", red, anios)
