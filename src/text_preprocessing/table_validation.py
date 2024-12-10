"""
Módulo para validar la detección de tablas en documentos PDF.

Incluye:
- Funciones para verificar la detección de tablas.
- Herramientas para inspección manual.
"""

import pdfplumber
from text_preprocessing.text_processing_v2 import preprocess_text_v2


def validate_tables_in_pdf(pdf_path, pages_with_tables, pages_without_tables):
    """
    Valida la detección de tablas en un documento PDF.

    Args:
        pdf_path (str): Ruta al archivo PDF.
        pages_with_tables (list): Páginas que deben contener tablas.
        pages_without_tables (list): Páginas que no deben contener tablas.
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number in pages_with_tables + pages_without_tables:
                raw_text = pdf.pages[page_number - 1].extract_text()
                processed_text = preprocess_text_v2(raw_text)

                # Validar si contiene tablas
                contains_table = "[TABLE START]" in processed_text and "[TABLE END]" in processed_text

                if page_number in pages_with_tables:
                    status = "Correcto" if contains_table else "Error - No se detectaron tablas"
                else:
                    status = "Correcto" if not contains_table else "Error - Se detectaron tablas"

                print(
                    f"Página {page_number} (con tablas: {page_number in pages_with_tables}): {status}"
                )
    except Exception as e:
        print(f"Error al procesar el archivo {pdf_path}: {e}")


def inspect_tables_in_pdf(pdf_path, pages):
    """
    Inspecciona las tablas en un documento PDF.

    Args:
        pdf_path (str): Ruta al archivo PDF.
        pages (list): Páginas a inspeccionar.
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number in pages:
                raw_text = pdf.pages[page_number - 1].extract_text()
                processed_text = preprocess_text_v2(raw_text)

                print(f"\nPágina {page_number} (Texto Crudo):")
                print(raw_text[:1000])  # Truncar para visualización
                print("\nTexto Preprocesado:")
                print(processed_text[:1000])  # Truncar para visualización

                # Verificar tablas
                if "[TABLE START]" in processed_text:
                    print("\nSe detectaron tablas.")
                else:
                    print("\nNo se detectaron tablas.")
    except Exception as e:
        print(f"Error al procesar el archivo {pdf_path}: {e}")
