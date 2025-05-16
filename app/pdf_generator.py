from fpdf import FPDF
from fpdf.enums import Align
from datetime import datetime
import unicodedata

def limpiar_texto(texto: str) -> str:
    """Normaliza caracteres y reemplaza símbolos problemáticos"""
    reemplazos = {
        '’': "'", '“': '"', '”': '"', '–': '-', '—': '-', '…': '...',
        '_': ' ', '\u200b': '', '́': '', '`': "'", '‘': "'"
    }
    for orig, rep in reemplazos.items():
        texto = texto.replace(orig, rep)
    # Normalizar a formato NFC para compatibilidad con FPDF
    return unicodedata.normalize('NFC', texto)

class PDFResumen(FPDF):
    def __init__(self):
        super().__init__()
        self.set_margins(15, 15, 15)  # Márgenes: izquierdo, superior, derecho
        self.set_auto_page_break(True, 20)  # Margen inferior de 20mm

    def header(self):
        self.set_font("Helvetica", "B", 16)
        self.set_text_color(57, 86, 140)  # Azul corporativo
        self.cell(0, 10, "Resumen Diario de Noticias", new_x="LMARGIN", new_y="NEXT", align="C")
        self.set_font("Helvetica", "", 12)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, datetime.now().strftime("%d/%m/%Y %H:%M"), align="C")
        self.ln(12)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(8)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}} • Generado por NewsDigest", align="C")

def generar_pdf(resumenes: list, filename: str = "resumen.pdf") -> str:
    """
    Genera un PDF estilizado a partir de una lista de resúmenes.
    
    Args:
        resumenes: Lista de diccionarios con 'url' y 'resumen'
        filename: Nombre del archivo de salida
    
    Returns:
        str: Ruta del archivo generado
    """
    if not resumenes:
        raise ValueError("No hay contenido para generar el PDF")

    pdf = PDFResumen()
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)
    ancho_util = 180  # 210mm (A4) - 15*2 márgenes

    for fuente in resumenes:
        # Encabezado de fuente
        pdf.set_font("Helvetica", "B", 12)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(0, 8, f"Fuente: {limpiar_texto(fuente['url'])}", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        # Contenido del resumen
        pdf.set_font("Helvetica", size=11)
        pdf.set_text_color(60, 60, 60)
        
        contenido = limpiar_texto(fuente["resumen"]).split("\n")
        for linea in contenido:
            linea = linea.strip()
            if not linea:
                continue
            
            if linea.startswith("* "):
                pdf.set_x(20)  # Sangría para viñetas
                linea = linea[2:].strip()
                pdf.multi_cell(
                    w=ancho_util - 10,
                    h=6,
                    txt=f"• {linea}",
                    split_only=True,
                    align=Align.J
                )
            else:
                pdf.multi_cell(
                    w=ancho_util,
                    h=6,
                    txt=linea,
                    split_only=True,
                    align=Align.J
                )
            pdf.ln(3)

        pdf.ln(8)
        pdf.line(pdf.get_x(), pdf.get_y(), ancho_util + 15, pdf.get_y())
        pdf.ln(10)

    pdf.output(filename)
    return filename

# Ejemplo de uso
if __name__ == "__main__":
    datos_ejemplo = [
        {
            "url": "https://ejemplo.com/feed",
            "resumen": "* Noticia importante: Este es un texto de ejemplo con una palabramuylargaysin espaciospara probar la división automática.\n* Segunda noticia: Otro contenido relevante con diferentes características."
        }
    ]
    
    generar_pdf(datos_ejemplo, "ejemplo.pdf")