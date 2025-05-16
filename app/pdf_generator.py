# app/pdf_generator.py
from fpdf import FPDF
from datetime import datetime

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
    # Elimina asteriscos y caracteres problemáticos
    reemplazos = {
        '*': '',
        '’': "'",
        '“': '"',
        '”': '"',
        '–': '-',
        '—': '-',
        '…': '...',
    }
    for orig, rep in reemplazos.items():
        texto = texto.replace(orig, rep)
    return texto.strip()


def generar_pdf(resumenes: list, filename: str = "resumen.pdf") -> str:
    if not resumenes or not isinstance(resumenes, list):
        raise ValueError("El texto proporcionado para el PDF está vacío o no es válido.")
    
    pdf = PDFResumen(orientation='P', unit='mm', format='A4')
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    for fuente in resumenes:
        # Obtener solo el texto resumido, sin mostrar ni filtrar por URL
        texto = limpiar_texto(fuente.get('resumen', ''))
        if not texto:
            continue
        
        # Cuerpo del resumen
        for linea in texto.split("\n"):
            pdf.multi_cell(0, 8, linea)
        pdf.ln(6)
    
    pdf.output(filename)
    return filename
