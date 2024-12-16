# loaders/pdf_inspector.py

import os
import pdfplumber


def inspect_pdf_content(capitulos_dir, pdf_files, num_pages_limit=None, char_limit=None):
    """
    Inspecciona contenido de archivos PDF seleccionados.

    Args:
        capitulos_dir (str): Directorio que contiene los PDFs.
        pdf_files (list): Lista de nombres de archivos PDF a inspeccionar.
        num_pages_limit (int, optional): Filtra PDFs con un número de páginas menor al límite.
        char_limit (int, optional): Límite de caracteres a mostrar por página. Si es None, muestra todo el texto.
    """
    filtered_pdfs = []
    if num_pages_limit:
        for pdf_file in pdf_files:
            pdf_path = os.path.join(capitulos_dir, pdf_file)
            with pdfplumber.open(pdf_path) as pdf:
                if len(pdf.pages) <= num_pages_limit:
                    filtered_pdfs.append(pdf_file)
        pdf_files = filtered_pdfs

    for pdf_file in pdf_files:
        pdf_path = os.path.join(capitulos_dir, pdf_file)
        print(f"\n--- Inspeccionando: {pdf_file} ---\n")

        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_number, page in enumerate(pdf.pages, start=1):
                    text = page.extract_text()
                    if text:
                        # Aplica el límite de caracteres, si está definido
                        display_text = text[:char_limit] if char_limit else text
                        print(f"--- Página {page_number} ---")
                        print(display_text)
                        print("\n" + "-" * 80)  # Separador para cada página
                    else:
                        print(f"--- Página {page_number} ---")
                        print(
                            "[Advertencia: No se pudo extraer texto de esta página]\n")
                        print("-" * 80)
        except Exception as e:
            print(f"Error al procesar el archivo {pdf_file}: {e}")
