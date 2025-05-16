from flask import Flask, render_template, request, send_file
from app.pipeline import ejecutar_pipeline
import os
import re
from datetime import datetime

app = Flask(__name__)
OUTPUT_DIR = os.path.abspath(os.path.dirname(__file__))

DEFAULT_FEEDS = [
    "https://news.google.com/rss",
    "https://www.cronista.com/rss/novedades.xml",
    "https://www.msn.com/es-us/money/rss",
    "https://www.msn.com/es-ar/feed",
    "https://news.google.com/rss/publications/CAAqIggKIhxDQklTRHdnTWFnc0tDWFJ1TG1OdmJTNWhjaWdBUAE",
    "https://news.google.com/rss/topics/CAAqLAgKIiZDQkFTRmdvSUwyMHZNRGx1YlY4U0JtVnpMVFF4T1JvQ1FWSW9BQVAB",
    "https://news.google.com/rss/topics/CAAqLQgKIidDQkFTRndnTWFoTUtFWEYxWldScFoybDBZV3d1WTI5dExtRnlLQUFQAQ",
    "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZ4ZERBU0JtVnpMVFF4T1NnQVAB",
    "https://news.google.com/rss/topics/CAAqKAgKIiJDQkFTRXdvSkwyMHZNREUxY0dwa0VnWmxjeTAwTVRrb0FBUAE",
    "https://news.google.com/rss/topics/CAAqBwgKMKeAiQswpI2IAw",
    "https://www.infobae.com/rss/politica.xml",
    "https://www.lanacion.com.ar/economia/",
    "https://www.economist.com/",
    "https://www.nytimes.com/international/section/world",
    "https://www.wsj.com/business?mod=nav_top_section",
    "https://www.bbc.com/news/war-in-ukraine",
    "https://www.radaraustral.com/articulos/categoria/global/",
    "https://www.infobae.com/tag/geopolitica/",
    "https://www.ft.com/middle-east-war"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    download_link = None

    if request.method == 'POST':
        raw_input = request.form.get('urls', '')
        urls = re.findall(r'https?://[^\s]+', raw_input.strip())

        if not urls:
            urls = DEFAULT_FEEDS

        output = request.form.get('output', 'pdf')
        accion = request.form.get('accion')
        correo_usuario = request.form.get('email')

        if correo_usuario:
            os.environ['MAIL_DESTINATARIO'] = correo_usuario

        enviar = (accion == 'enviar')
        archivo = ejecutar_pipeline(urls, output_format=output, send_mail=enviar)
        download_link = os.path.basename(archivo)

    return render_template('index.html', resultado=resultado, download_link=download_link)

@app.route('/auto')
def resumen_automatico():
    output = 'pdf'
    enviar = True

    try:
        archivo = ejecutar_pipeline(DEFAULT_FEEDS, output_format=output, send_mail=enviar)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"[{timestamp}] ✅ Resumen generado y enviado.<br>Archivo: {archivo}"
    except Exception as e:
        return f"❌ Error al generar resumen: {e}", 500

@app.route('/download/<filename>')
def download(filename):
    full_path = os.path.join(OUTPUT_DIR, filename)
    return send_file(full_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
