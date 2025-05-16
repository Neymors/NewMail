from app import cliente, resumen, pdf_generator, html_generator, mail_sender

def ejecutar_pipeline(urls, output_format='pdf', send_mail=False):
    print("🔄 Leyendo feeds...")
    articulos = cliente.leer_feeds(urls)

    print("🧠 Generando resumen...")
    resumenes = resumen.resumir_noticias(articulos)

    print(f"📝 Generando archivo en formato {output_format.upper()}...")
    if output_format == 'pdf':
        archivo = pdf_generator.generar_pdf(resumenes)
    else:
        archivo = html_generator.generar_html(resumenes)

    if send_mail:
        print("📧 Enviando por correo...")
        mail_sender.enviar_correo(archivo)

    return f"✅ Proceso completado. Archivo generado: {archivo}" + (" y enviado por correo." if send_mail else ".")

