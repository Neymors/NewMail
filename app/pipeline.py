from app import cliente, resumen, pdf_generator, mail_sender
from datetime import datetime
import traceback

def ejecutar_pipeline(urls, output_format='pdf', send_mail=False):
    try:
        print("🔄 Leyendo feeds...")
        articulos = cliente.leer_feeds(urls or [])  # Usa lista vacía si urls es None

        print("🧠 Generando resumen...")
        resumenes = resumen.resumir_noticias(articulos)

        fecha = datetime.now().strftime("%Y-%m-%d")
        archivo = f"/tmp/resumen-{fecha}.{output_format}"  # Usa /tmp en GitHub Actions

        if output_format == 'pdf':
            pdf_generator.generar_pdf(resumenes, filename=archivo)
        else:
            html_generator.generar_html(resumenes, filename=archivo)

        if send_mail:
            print("📧 Enviando por correo...")
            mail_sender.enviar_correo(archivo)

        return archivo

    except Exception as e:
        print(f"❌ Error en el pipeline: {str(e)}")
        print(traceback.format_exc())  # Detalles del error
        raise  # Para que aparezca en GitHub Actions