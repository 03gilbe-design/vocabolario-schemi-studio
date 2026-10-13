"""INDICE.md -> foto (tabella con miniature, ~24 righe per foto) in _foto_indice\. Uso: python _indice_in_foto.py"""
import html, os, re, subprocess
D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(D, "_foto_indice"); os.makedirs(OUT, exist_ok=True)
CH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
e = html.escape
righe = [l for l in open(os.path.join(D, "INDICE.md"), encoding="utf-8") if l.startswith("| ![")]
css = ("body{margin:0;width:1500px;background:#F9F6EE;font-family:'Segoe UI';color:#5a4035}h1{background:#795447;color:#fff;margin:0;padding:14px 24px;font-size:28px}"
       "table{border-collapse:collapse;width:100%}td{border-bottom:1px solid #e6ddd3;padding:8px 10px;font-size:17px;vertical-align:top}"
       "td img{width:230px;border:1px solid #ddd;background:#fff}.f{font-family:Consolas;font-size:13px;color:#997E71;width:200px;word-break:break-all}.o{width:150px;font-size:14px;color:#997E71}")
N = 24
for k in range(0, len(righe), N):
    tr = ""
    for l in righe[k:k + N]:
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        img = re.search(r"\]\(([^)]*)\)", c[0]).group(1).replace("%20", " ")
        tr += '<tr><td><img src="file:///%s"></td><td class="f">%s</td><td>%s</td><td><b>%s</b></td><td class="o">%s</td></tr>' % (
            os.path.join(D, img).replace("\\", "/"), e(c[1].strip("`")), e(c[2]), e(c[3]), e(c[4] if len(c) > 4 else ""))
    h = os.path.join(OUT, "pag_%02d.html" % (k // N + 1))
    open(h, "w", encoding="utf-8").write('<html><head><meta charset="utf-8"><style>%s</style></head><body><h1>Grafiche delle regole · %d-%d di %d · cosa si vede / a cosa serve</h1><table>%s</table></body></html>' % (
        css, k + 1, min(k + N, len(righe)), len(righe), tr))
    png = h[:-5] + ".png"
    subprocess.run([CH, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files", "--window-size=1500,9000", "--screenshot=" + png, "file:///" + h.replace("\\", "/")], capture_output=True)
    from PIL import Image
    im = Image.open(png).convert("RGB"); px = im.load()
    fondo = next(y for y in range(im.height - 1, 0, -1) if any(px[x, y] != (249, 246, 238) for x in range(0, im.width, 9)))
    im.crop((0, 0, im.width, fondo + 10)).save(png); print(png, fondo)
