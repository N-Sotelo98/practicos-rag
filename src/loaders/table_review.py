# src/loaders/table_review.py

import pdfplumber


def process_and_review_tables(pdf_path, max_tables=None):
    """
    Revisa y analiza detalladamente las tablas en el PDF proporcionado.

    Args:
        pdf_path (str): Ruta completa al archivo PDF.
        max_tables (int, optional): Número máximo de tablas a procesar. Si es None, procesa todas las tablas.

    Returns:
        list: Listado de tablas procesadas.
    """
    processed_tables = []  # Para almacenar las tablas procesadas

    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_tables = 0

            print(f"\nProcesando archivo: {pdf_path}")

            for page_num, page in enumerate(pdf.pages):
                tables = page.extract_tables()

                for table in tables:
                    if max_tables is not None and total_tables >= max_tables:
                        print(
                            f"\nLímite de {max_tables} tablas alcanzado para {pdf_path}")
                        return processed_tables

                    total_tables += 1
                    processed_tables.append(table)

                    print(
                        f"\nTabla {total_tables} detectada en la página {page_num + 1}:")
                    for row in table:
                        print("\t".join(str(cell) if cell else "" for cell in row))

            print(f"\n--- Total de tablas detectadas: {total_tables} ---")
    except Exception as e:
        print(f"Error al procesar tablas en {pdf_path}: {e}")

    return processed_tables
