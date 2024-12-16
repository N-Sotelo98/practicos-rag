import pdfplumber
# Asegurando importación válida
from text_preprocessing.text_processing_v2 import preprocess_text_v2


def validate_tables_in_pdf(pdf_path: str, pages_with_tables: list, pages_without_tables: list):
    """
    Valida la detección de tablas en un archivo PDF específico.

    Args:
        pdf_path (str): Ruta absoluta del archivo PDF.
        pages_with_tables (list): Lista de páginas donde se esperan tablas.
        pages_without_tables (list): Lista de páginas donde no se esperan tablas.

    Returns:
        None
    """
    print(f"\nValidando archivo: {pdf_path}")
    if not os.path.isabs(pdf_path):
        raise ValueError("La ruta proporcionada debe ser absoluta.")

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"El archivo PDF no existe: {pdf_path}")

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number in pages_with_tables:
                page = pdf.pages[page_number - 1]
                raw_text = page.extract_text()
                preprocessed_text = preprocess_text_v2(raw_text)

                if "[TABLE START]" in preprocessed_text and "[TABLE END]" in preprocessed_text:
                    print(f"Página {page_number} (con tablas: True): Correcto")
                else:
                    print(
                        f"Página {page_number} (con tablas: True): Error - No se detectaron tablas")

            for page_number in pages_without_tables:
                page = pdf.pages[page_number - 1]
                raw_text = page.extract_text()
                preprocessed_text = preprocess_text_v2(raw_text)

                if "[TABLE START]" not in preprocessed_text and "[TABLE END]" not in preprocessed_text:
                    print(
                        f"Página {page_number} (con tablas: False): Correcto")
                else:
                    print(
                        f"Página {page_number} (con tablas: False): Error - Se detectaron tablas")
    except Exception as e:
        print(f"Error al validar tablas en el PDF: {e}")


def inspect_tables_in_pdf(pdf_path: str, pages: list):
    """
    Inspecciona las tablas detectadas en un archivo PDF específico.

    Args:
        pdf_path (str): Ruta absoluta del archivo PDF.
        pages (list): Lista de páginas a inspeccionar.

    Returns:
        None
    """
    print(f"\nInspeccionando archivo: {pdf_path}")
    if not os.path.isabs(pdf_path):
        raise ValueError("La ruta proporcionada debe ser absoluta.")

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"El archivo PDF no existe: {pdf_path}")

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page_number in pages:
                page = pdf.pages[page_number - 1]
                raw_text = page.extract_text()
                preprocessed_text = preprocess_text_v2(raw_text)

                print(f"\nPágina {page_number} (Texto Preprocesado):")
                # Mostrar primeros 1000 caracteres
                print(preprocessed_text[:1000])
    except Exception as e:
        print(f"Error al inspeccionar tablas en el PDF: {e}")
