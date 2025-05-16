def generar_html(resumenes, filename="resumen.html"):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("<html><body>")
        for resumen in resumenes:
            f.write(f"<h2>{resumen['title']}</h2>")
            f.write(f"<p>{resumen['resumen']}</p>")
        f.write("</body></html>")
    return filename
