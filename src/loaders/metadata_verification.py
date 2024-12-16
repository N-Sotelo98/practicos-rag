# src/loaders/metadata_verification.py

def verificar_metadatos_guardados(processed_data, max_files=5, max_pages=3, max_blocks=5):
    """
    Verifica los metadatos almacenados en `processed_data` con opciones para limitar la salida.

    Args:
        processed_data (dict): Datos procesados de los PDFs.
        max_files (int): Número máximo de archivos a mostrar.
        max_pages (int): Número máximo de páginas por archivo a mostrar.
        max_blocks (int): Número máximo de bloques por página a mostrar.
    """
    print("\n=== Verificación de Metadatos Guardados ===")
    for idx, (archivo, archivo_data) in enumerate(processed_data.items(), start=1):
        if idx > max_files:
            print(
                "\n... (Se han procesado más archivos, pero se limitan los resultados mostrados)")
            break

        print(f"\nArchivo {idx}: {archivo}")
        paginas = archivo_data.get("paginas", [])
        print(f"Total de páginas procesadas: {len(paginas)}")

        for page_idx, pagina in enumerate(paginas[:max_pages], start=1):
            print(f"\n--- Página {pagina.get('numero', 'Desconocida')} ---")

            for block_idx, bloque in enumerate(pagina.get("contenido", [])[:max_blocks], start=1):
                tipo = bloque.get("tipo", "Desconocido")
                if tipo == "texto":
                    capitulo = bloque.get("capitulo", "Desconocido")
                    articulo = bloque.get("articulo", "Desconocido")
                    longitud = bloque.get("longitud", "Desconocido")
                    texto_preview = bloque.get("texto", "Desconocido")[
                        :50]  # Muestra un preview del texto
                    print(
                        f"[Texto {block_idx}] Capítulo: {capitulo}, Artículo: {articulo}, Longitud: {longitud}, Contenido: {texto_preview}...")
                elif tipo == "tabla":
                    capitulo = bloque.get("capitulo", "Desconocido")
                    articulo = bloque.get("articulo", "Desconocido")
                    dimensiones = bloque.get("longitud", "Desconocido")
                    print(
                        f"[Tabla {block_idx}] Capítulo: {capitulo}, Artículo: {articulo}, Dimensiones: {dimensiones} filas")

                # Advertencias de metadatos incompletos
                if capitulo == "Desconocido" or articulo == "Desconocido":
                    print(
                        "Advertencia: Metadatos incompletos detectados en este bloque.")
