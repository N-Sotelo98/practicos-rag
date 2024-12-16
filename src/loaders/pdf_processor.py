# src/loaders/pdf_processor.py

from loaders.config_loader import setup_project_paths
from loaders.pdf_page_counter import count_pdf_pages
from loaders.pdf_inspector import inspect_pdf_content
from loaders.detailed_pdf_processor import process_pdf_directly
from loaders.table_review import process_and_review_tables


def process_pdfs():
    """
    Orquesta la configuración, conteo, inspección y análisis avanzado de los PDFs.
    """
    # Configuración de rutas
    paths = setup_project_paths()
    CAPITULOS_DIR = paths["CAPITULOS_DIR"]

    # Obtener lista de todos los PDFs en la carpeta
    pdf_paths = [
        os.path.join(CAPITULOS_DIR, file)
        for file in os.listdir(CAPITULOS_DIR)
        if file.endswith(".pdf")
    ]

    # Verificación inicial: Conteo e inspección básica
    print("\n--- Verificando y contando páginas en los PDFs ---")
    pdf_page_counts = count_pdf_pages(CAPITULOS_DIR)
    for pdf in pdf_page_counts:
        print(f"{pdf['file_name']}: {pdf['page_count']} páginas")

    print("\n--- Inspeccionando los 3 archivos más cortos ---")
    short_pdfs = [pdf["file_name"] for pdf in pdf_page_counts[:3]]
    inspect_pdf_content(CAPITULOS_DIR, short_pdfs)

    # Análisis avanzado: Procesamiento detallado
    print("\n--- Procesando TODOS los PDFs directamente ---")
    results = process_pdf_directly(pdf_paths)

    # Análisis de tablas en profundidad
    print("\n--- Revisando tablas en TODOS los PDFs ---")
    for pdf_file in pdf_paths:
        process_and_review_tables(pdf_file)
        print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    process_pdfs()
