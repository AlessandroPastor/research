"""Decisiones del cribado por título y resumen (revisor: Claude, 2026-10-09).
Los IDs son la posición en la lista ordenada por (año, título) que genera analisis_scopus.py.
Códigos: I = incluido para texto completo; S = estudio secundario (contexto);
E1..E5 = criterios de exclusión (ver criterios_inclusion_exclusion.md)."""
I = [1, 2, 9, 11, 13, 19, 20, 33, 37, 38, 39, 41, 43, 54, 57, 59, 61, 62, 70, 71, 72, 76, 83, 84,
     87, 88, 89, 94, 97, 98, 100, 110, 112, 118, 119, 122, 127, 131, 136, 138, 139, 156, 158, 163,
     164, 166, 170, 172, 174, 177, 181, 182, 193, 199, 206, 213, 215, 223, 225, 226, 228, 229,
     231, 233, 237, 239, 240, 241, 242, 243, 245, 248, 250, 251, 252, 253, 255, 261, 262, 265, 267,
     268, 269, 271, 272, 273, 274, 275, 277, 280, 283, 284, 285, 286, 288, 290, 295, 296, 298, 299,
     300, 312, 313, 315, 317, 319, 320, 322, 323, 330, 332, 336, 344, 345, 348, 349, 351, 352,
     354, 356, 363, 366, 370, 375, 380, 381, 386, 391, 393, 395, 400, 402, 403, 407, 408, 411, 414,
     415, 416, 419, 420, 422, 425, 430, 432]
S = [179, 201, 259, 287, 291, 292, 334, 335, 350, 353, 389, 427]
E3 = [125, 191, 217, 221]                      # sin evaluación empírica
E5 = [216, 310]                           # duplicado / resumen extendido de otro registro
E2 = [321, 3, 5, 6, 7, 8, 15, 17, 23, 24, 26, 27, 29, 36, 40, 42, 44, 46, 47, 52, 58, 60, 66, 67, 68, 78,
      82, 85, 93, 104, 106, 109, 113, 114, 124, 130, 132, 134, 137, 143, 146, 148, 151, 152, 153, 154,
      155, 160, 162, 165, 171, 175, 180, 183, 185, 190, 194, 195, 196, 198, 200, 202, 204, 211, 212,
      214, 222, 224, 227, 234, 235, 236, 244, 246, 247, 256, 258, 260, 263, 264, 266, 270, 276, 278,
      279, 281, 289, 294, 301, 304, 306, 307, 308, 309, 311, 316, 324, 325, 327, 329, 331, 338, 339,
      342, 343, 346, 347, 355, 357, 360, 368, 376, 379, 382, 383, 385, 387, 388, 390, 394, 397, 398,
      409, 412, 413, 417, 428, 433, 434]
# E1 (fuera del dominio de software) = todos los demás

# Codificación manual que corrige las etiquetas automáticas (revisado leyendo el resumen).
ENFOQUE_MANUAL = {83: "Transformer", 110: "Transformer", 139: "Transformer", 193: "Transformer",
                  226: "Aprendizaje profundo", 237: "Aprendizaje profundo", 242: "Transformer",
                  267: "Transformer", 312: "Transformer", 322: "Transformer", 332: "Transformer",
                  403: "ML clásico", 407: "Transformer", 430: "Transformer"}
AUMENTO_MANUAL = {182: [], 250: ["TextAttack / TAOS"], 273: [], 296: [], 381: [], 386: [], 411: [],
                  422: [], 432: [], 344: ["Generación con LLM"], 242: ["Otra / no especificada"],
                  267: ["Otra / no especificada"], 400: ["Otra / no especificada"],
                  408: ["Otra / no especificada"]}
