"""Scrive README.md = muro di miniature (GitHub lo mostra aprendo la cartella). Clic su una miniatura = grafica grande.
Le descrizioni restano in INDICE.md. Uso: python _muro.py"""
import glob, os
D = os.path.dirname(os.path.abspath(__file__))
GRUPPI = [("regole_v10", "Regole finali del loop (13/10)"), ("libreria_nuove", "Libreria: grafiche nuove"),
          ("libreria_dialetti", "Libreria: stile grafico"), ("libreria_testo", "Libreria: regole testo → testo"),
          ("libreria_concetti_ai", "Libreria: concetti delle regole AI")]
out = ["# Grafiche delle regole\n", "Tutte le grafiche mai generate, in una cartella sola. Clic su una miniatura per vederla grande; "
       "cosa si vede e a cosa serve ciascuna: [INDICE.md](INDICE.md).\n"]
tot = 0
alta = lambda f: "__TAVOLA" in f or "__SCHEMA" in f  # ponytail: le alte in fondo, se no bucano la griglia
for pre, titolo in GRUPPI + [("*", "Tavole riassuntive e schemi del loop")]:
    png = sorted(os.path.basename(f) for f in glob.glob(os.path.join(D, pre + "__*.png")))
    png = [f for f in png if alta(f) == (pre == "*")]
    tot += len(png)
    out.append("\n## %s (%d)\n\n<p>\n%s\n</p>\n" % (titolo, len(png), "\n".join(
        '<a href="%s"><img src="%s" width="190" alt="%s"></a>' % (f.replace(" ", "%20"), f.replace(" ", "%20"), f.split("__", 1)[1][:-4])
        for f in png)))
open(os.path.join(D, "README.md"), "w", encoding="utf-8").write("\n".join(out))
assert tot == len(glob.glob(os.path.join(D, "*__*.png"))), "png fuori dai gruppi"
print("README.md:", tot, "miniature")
