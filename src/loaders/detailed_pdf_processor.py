# loaders/detailed_pdf_processor.py

import os
import pdfplumber


def process_pdf_directly(pdf_paths):
    """
    Procesa una lista de archivos PDF para extraer estadísticas generales,
    incluyendo páginas, bloques de texto y tablas detectadas.
    """
    results = {}

    print(
        f"\n--- Iniciando procesamiento de {len(pdf_paths)} archivos PDF ---")

    for idx, pdf_path in enumerate(pdf_paths, start=1):
        print(f"\n[{idx}/{len(pdf_paths)}] Procesando archivo: {pdf_path}")
        try:
            with pdfplumber.open(pdf_path) as pdf:
                pdf_data = {
                    "total_paginas": len(pdf.pages),
                    "total_bloques": 0,
                    "total_tablas": 0,
                    "tablas_detectadas": []
                }

                for page_num, page in enumerate(pdf.pages, start=1):
                    # Extraer texto completo de la página
                    text = page.extract_text()
                    if text:
                        # Contar líneas como bloques
                        pdf_data["total_bloques"] += len(text.split("\n"))

                    # Extraer tablas
                    tables = page.extract_tables()
                    pdf_data["total_tablas"] += len(tables)
                    for table in tables:
                        if table:
                            pdf_data["tablas_detectadas"].append(
                                str(table[0])[:100]
                            )

                results[pdf_path] = pdf_data

                # Mostrar estadísticas por archivo
                print(
                    f"--- Estadísticas para {os.path.basename(pdf_path)} ---")
                print(
                    f"Páginas: {pdf_data['total_paginas']}, Bloques de texto: {pdf_data['total_bloques']}, Tablas: {pdf_data['total_tablas']}")
        except Exception as e:
            print(f"Error procesando {pdf_path}: {e}")

    print("\n--- Procesamiento completado ---")
    return results
