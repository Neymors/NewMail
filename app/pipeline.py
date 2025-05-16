from app import cliente, resumen, pdf_generator, html_generator, mail_sender
from datetime import datetime

def ejecutar_pipeline(urls, output_format='pdf', send_mail=False):
    print("🔄 Leyendo feeds...")
    articulos = cliente.leer_feeds(urls)

    print("🧠 Generando resumen...")
    resumenes = resumen.resumir_noticias(articulos)

    fecha = datetime.now().strftime("%Y-%m-%d")
    if output_format == 'pdf':
        archivo = f"resumen-{fecha}.pdf"
        pdf_generator.generar_pdf(resumenes, filename=archivo)
    else:
        archivo = f"resumen-{fecha}.html"
        html_generator.generar_html(resumenes, filename=archivo)

    if send_mail:
        print("📧 Enviando por correo...")
        mail_sender.enviar_correo(archivo)

    return archivo
