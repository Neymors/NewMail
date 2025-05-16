from fpdf import FPDF
from datetime import datetime
import unicodedata

class PDFResumen(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Resumen Diario de Noticias', border=False, ln=True, align='C')
        self.set_font('Arial', '', 10)
        self.cell(0, 5, datetime.now().strftime('%d/%m/%Y'), border=False, ln=True, align='R')
        self.ln(3)
        self.set_draw_color(50, 50, 50)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.3)
        self.line(10, self.get_y(), 200, self.get_y())
        self.set_font('Arial', 'I', 8)
        page = f'Página {self.page_no()}/{{nb}}'
        self.cell(0, 10, page, align='C')

def limpiar_texto(texto: str) -> str:
    # Normaliza y elimina caracteres conflictivos
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('ascii')
    reemplazos = {
        '*': '', '–': '-', '—': '-', '…': '...', '“': '"', '”': '"', '’': "'"
    }
    for orig, rep in reemplazos.items():
        texto = texto.replace(orig, rep)
    return texto.strip()

def cortar_palabras_largas(texto, max_len=100):
    palabras = texto.split()
    resultado = []
    for palabra in palabras:
        if len(palabra) > max_len:
            palabra = ' '.join(palabra[i:i+max_len] for i in range(0, len(palabra), max_len))
        resultado.append(palabra)
    return ' '.join(resultado)

def generar_pdf(resumenes: list, filename: str = "resumen.pdf") -> str:
    if not resumenes or not isinstance(resumenes, list):
        raise ValueError("El texto proporcionado para el PDF está vacío o no es válido.")

    pdf = PDFResumen(orientation='P', unit='mm', format='A4')
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for fuente in resumenes:
        texto = limpiar_texto(fuente.get('resumen', '')).strip()
        if not texto:
            continue

        for linea in texto.split("\n"):
            linea = cortar_palabras_largas(linea)
            pdf.multi_cell(0, 8, linea)
        pdf.ln(6)

    pdf.output(filename)
    return filename
