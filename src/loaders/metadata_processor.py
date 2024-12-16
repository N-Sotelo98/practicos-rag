# loaders/metadata_processor.py

import pdfplumber
import re
import uuid


def process_pdfs_with_validated_metadata(pdf_paths, verbose=False):
    """
    Procesa múltiples archivos PDF con validación de metadatos (capítulos y artículos).
    Args:
        pdf_paths (list): Lista de rutas de archivos PDF a procesar.
        verbose (bool): Si es True, imprime detalles durante el procesamiento.
    Returns:
        dict: Datos enriquecidos de los PDFs procesados.
    """
    processed_data = {}
    total_global_chapters = 0
    total_global_articles = 0
    total_global_warnings = 0

    for pdf_path in pdf_paths:
        warnings = 0
        unique_articles = set()
        duplicate_articles_count = 0
        total_chapters = 0

        try:
            with pdfplumber.open(pdf_path) as pdf:
                archivo_data = {"archivo": pdf_path, "paginas": []}
                chapter_title = None
                current_article = None
                detected_articles = set()

                for page_num, page in enumerate(pdf.pages, start=1):
                    pagina_data = {"numero": page_num, "contenido": []}
                    text = page.extract_text()

                    if not text:
                        if verbose:
                            print(
                                f"Página {page_num}: No se pudo extraer texto.")
                        continue

                    # Detectar capítulo
                    chapter_match = re.search(
                        r"^\s*(CAPÍTULO\s+[IVXLCDM0-9]+)", text, re.IGNORECASE | re.MULTILINE)
                    if chapter_match:
                        chapter_title = chapter_match.group(1).upper()
                        total_chapters += 1
                        detected_articles.clear()  # Reiniciar artículos
                        if verbose:
                            print(f"Capítulo detectado: {chapter_title}")

                    # Procesar líneas de texto
                    missing_metadata = 0
                    for line in text.split("\n"):
                        article_match = re.match(r"Artículo\s+(\d+)", line)
                        if article_match:
                            article_number = int(article_match.group(1))
                            detected_article = f"Artículo {article_number}"

                            if detected_article not in detected_articles:
                                detected_articles.add(detected_article)
                                unique_articles.add(detected_article)
                                current_article = detected_article
                                if verbose:
                                    print(
                                        f"Artículo detectado: {current_article}")
                            else:
                                duplicate_articles_count += 1

                        # Agregar bloque con metadatos
                        if line.strip():
                            bloque = {
                                "id": str(uuid.uuid4()),
                                "tipo": "texto",
                                "texto": line.strip(),
                                "longitud": len(line.strip()),
                                "capitulo": chapter_title or "No identificado",
                                "articulo": current_article or "No identificado",
                                "pagina": page_num
                            }
                            if not chapter_title or not current_article:
                                missing_metadata += 1
                            pagina_data["contenido"].append(bloque)

                    if missing_metadata > 0 and verbose:
                        print(
                            f"Advertencia: {missing_metadata} bloques sin metadatos en la página {page_num}.")
                        warnings += 1

                    # Procesar tablas
                    tables = page.extract_tables()
                    for table_index, table in enumerate(tables):
                        if table:
                            contexto_tabla = f"Capítulo: {chapter_title or 'Desconocido'}, Artículo: {current_article or 'Desconocido'}, Página: {page_num}"
                            pagina_data["contenido"].append({
                                "id": str(uuid.uuid4()),
                                "tipo": "tabla",
                                "tabla": table,
                                "contexto": contexto_tabla,
                                "longitud": len(table),  # Número de filas
                                "capitulo": chapter_title or "Desconocido",
                                "articulo": current_article or "Desconocido",
                                "pagina": page_num
                            })
                            if verbose:
                                print(
                                    f"Tabla {table_index + 1} detectada en la página {page_num}: {contexto_tabla}")

                    archivo_data["paginas"].append(pagina_data)

                total_global_chapters += total_chapters
                total_global_articles += len(unique_articles)
                total_global_warnings += warnings

            processed_data[pdf_path] = archivo_data
            if verbose:
                print(f"\nResumen de {pdf_path}:")
                print(f"Total capítulos detectados: {total_chapters}")
                print(f"Total artículos únicos: {len(unique_articles)}")
                print(
                    f"Artículos duplicados ignorados: {duplicate_articles_count}")
                print(f"Advertencias de metadatos faltantes: {warnings}")
        except Exception as e:
            print(f"Error procesando {pdf_path}: {e}")

    # Resumen global
    if verbose:
        print("\n=== Resumen Global ===")
        print(
            f"Total capítulos detectados en todos los archivos: {total_global_chapters}")
        print(
            f"Total artículos únicos en todos los archivos: {total_global_articles}")
        print(
            f"Total advertencias globales de metadatos faltantes: {total_global_warnings}")

    return processed_data
