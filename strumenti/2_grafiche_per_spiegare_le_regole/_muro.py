"""Scrive README.md = muro di miniature (GitHub lo mostra aprendo la cartella). Clic su una miniatura = grafica grande.
Le descrizioni restano in COSA_MOSTRA_OGNI_GRAFICA.md. Uso: python _muro.py"""
import glob, os
D = os.path.dirname(os.path.abspath(__file__))
N = "COSA_MOSTRA_OGNI_GRAFICA.md"
GRUPPI = [("regole_v10", "Regole finali del loop"), ("libreria_nuove", "Libreria: grafiche nuove"),
          ("libreria_dialetti", "Libreria: stile grafico"), ("libreria_testo", "Libreria: regole testo → testo"),
          ("libreria_concetti_ai", "Libreria: concetti delle regole AI")]
out = ["# Grafiche per spiegare le regole\n",
       "**Qui solo le grafiche; cosa mostra ognuna e a cosa serve: [%s](%s).**\n" % (N, N),
       "A cosa servono: chi deve spiegare una regola (un'AI in chat o una persona) mostra la grafica già fatta invece di disegnarne una nuova. "
       "Per trovare quella giusta cerca la regola in [%s](%s): una riga per grafica, con cosa si vede e a cosa serve. "
       "Clic su una miniatura per vederla grande.\n" % (N, N)]
tot = 0
alta = lambda f: "__TAVOLA" in f or "__SCHEMA" in f  # ponytail: le alte in fondo, se no bucano la griglia
for pre, titolo in GRUPPI + [("*", "Tavole riassuntive e schemi del loop")]:
    png = sorted(os.path.basename(f) for f in glob.glob(os.path.join(D, pre + "__*.png")))
    png = [f for f in png if alta(f) == (pre == "*")]
    tot += len(png)
    misura = 'width="190"'
    if pre == "*":  # tavole alte e schemi larghi: altezza fissa, ordinate per forma -> righe piene, niente buchi
        from PIL import Image
        forma = lambda f: (lambda s: s[1] / s[0])(Image.open(os.path.join(D, f)).size)
        png.sort(key=forma, reverse=True); misura = 'height="300"'
    out.append("\n## %s (%d)\n\n<p>\n%s\n</p>\n" % (titolo, len(png), "\n".join(
        '<a href="%s"><img src="%s" %s alt="%s"></a>' % (f.replace(" ", "%20"), f.replace(" ", "%20"), misura, f.split("__", 1)[1][:-4])
        for f in png)))
open(os.path.join(D, "README.md"), "w", encoding="utf-8").write("\n".join(out))
assert tot == len(glob.glob(os.path.join(D, "*__*.png"))), "png fuori dai gruppi"
print("README.md:", tot, "miniature")
