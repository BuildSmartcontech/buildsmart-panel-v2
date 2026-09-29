# utils/pdf_generator.py - Generador de PDF para planes (CON SOPORTE UNICODE)
import os
import datetime
import re
from fpdf import FPDF

class PDFPlan(FPDF):
    def __init__(self):
        super().__init__()
        # Agregar fuente UTF-8
        self.core_fonts_encoding = 'utf-8'
    
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'SAMU IA - Plan de Marketing', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Generado: {datetime.datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 0, 'C')

def limpiar_texto(texto: str) -> str:
    """Limpia caracteres problemáticos para PDF"""
    # Reemplazar caracteres especiales
    reemplazos = {
        '\u2011': '-',  # Guion no rompible
        '\u2013': '-',  # Guion largo
        '\u2014': '-',  # Guion muy largo
        '\u2018': "'",  # Comilla simple izquierda
        '\u2019': "'",  # Comilla simple derecha
        '\u201c': '"',  # Comilla doble izquierda
        '\u201d': '"',  # Comilla doble derecha
        '\u2022': '*',  # Viñeta
        '\u2026': '...',  # Puntos suspensivos
    }
    
    for old, new in reemplazos.items():
        texto = texto.replace(old, new)
    
    # Eliminar otros caracteres no ASCII
    texto = texto.encode('ascii', 'ignore').decode('ascii')
    return texto

def generar_pdf_plan(contenido: str, titulo: str = "Plan de Marketing", nombre_archivo: str = None) -> str:
    """
    Genera un PDF a partir del contenido del plan
    
    Args:
        contenido: Texto del plan
        titulo: Título del documento
        nombre_archivo: Nombre del archivo (opcional)
    
    Returns:
        str: Ruta del archivo PDF generado
    """
    # Crear carpeta si no existe
    os.makedirs("pdfs", exist_ok=True)
    
    # Limpiar contenido
    contenido = limpiar_texto(contenido)
    titulo = limpiar_texto(titulo)
    
    # Generar nombre de archivo
    if nombre_archivo is None:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"plan_marketing_{timestamp}.pdf"
    
    ruta = os.path.join("pdfs", nombre_archivo)
    
    try:
        # Crear PDF
        pdf = PDFPlan()
        pdf.add_page()
        
        # Título
        pdf.set_font('Arial', 'B', 16)
        pdf.cell(0, 10, titulo, 0, 1, 'C')
        pdf.ln(5)
        
        # Fecha
        pdf.set_font('Arial', 'I', 10)
        pdf.cell(0, 10, f"Fecha de generacion: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M')}", 0, 1)
        pdf.ln(5)
        
        # Contenido
        pdf.set_font('Arial', '', 11)
        
        # Dividir el contenido en líneas (máximo 190 caracteres por línea)
        lineas = contenido.split('\n')
        for linea in lineas:
            if linea.strip() == '':
                pdf.ln(3)
                continue
            
            # Limpiar línea
            linea = limpiar_texto(linea)
            
            if len(linea) > 190:
                # Dividir líneas largas
                partes = [linea[i:i+190] for i in range(0, len(linea), 190)]
                for parte in partes:
                    pdf.cell(0, 6, parte, 0, 1)
            else:
                pdf.cell(0, 6, linea, 0, 1)
        
        # Guardar
        pdf.output(ruta)
        return ruta
        
    except Exception as e:
        print(f"❌ Error generando PDF: {e}")
        return None

if __name__ == "__main__":
    # Prueba
    test_contenido = """Plan de Marketing - Prueba
    
Objetivos:
1. Incrementar ventas en 20%
2. Mejorar presencia digital

Estrategias:
- SEO local
- Marketing de contenido
- Redes sociales

Nota: Este es un plan de prueba con caracteres especiales como ñ, á, é, í, ó, ú.
"""
    ruta = generar_pdf_plan(test_contenido, "Plan de Prueba")
    print(f"✅ PDF generado: {ruta}")