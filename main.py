import argparse
from app import pipeline

#load_dotenv(dotenv_path=r"C:\Users\s\Downloads\Gaston\Programacion\NewMail\.env")

def main():
    parser = argparse.ArgumentParser(description="Generador de resúmenes de noticias")
    parser.add_argument('--output', choices=['pdf', 'html'], default='pdf', help='Formato de salida')
    parser.add_argument('--send', action='store_true', help='Enviar el resumen por correo')
    args = parser.parse_args()

    urls = [
        "https://www.cronista.com/rss/novedades.xml",
        "https://www.msn.com/es-us/money/rss",
        "https://www.msn.com/es-ar/feed",
        "https://news.google.com/rss/publications/CAAqIggKIhxDQklTRHdnTWFnc0tDWFJ1TG1OdmJTNWhjaWdBUAE",
        "https://news.google.com/rss/topics/CAAqLAgKIiZDQkFTRmdvSUwyMHZNRGx1YlY4U0JtVnpMVFF4T1JvQ1FWSW9BQVAB",
    ]

    resultado = pipeline.ejecutar_pipeline(urls, output_format=args.output, send_mail=args.send)
    print(resultado)

if __name__ == '__main__':
    main()
