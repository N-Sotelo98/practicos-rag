# chunking/separated_chunker.py

def chunk_documents_separately(processed_data, chunk_size=3000):
    """
    Realiza un chunking separado para texto narrativo y tablas.
    Los chunks narrativos respetan la jerarquía de capítulos.
    Las tablas generan chunks independientes con su contexto.

    Args:
        processed_data (dict): Datos enriquecidos procesados de los PDFs.
        chunk_size (int): Tamaño máximo de caracteres por chunk narrativo.

    Returns:
        tuple: (chunks_narrativos, chunks_tablas)
    """
    chunks_narrativos = []
    chunks_tablas = []

    for archivo, archivo_data in processed_data.items():
        current_chunk_text = ""
        current_chunk_size = 0
        current_capitulo = None
        paginas_inicial = None
        paginas_final = None

        for pagina in archivo_data.get("paginas", []):
            pagina_numero = pagina.get("numero", "Desconocida")
            for item in pagina.get("contenido", []):
                capitulo = item.get("capitulo", "No identificado")
                tipo = item.get("tipo", "No especificado")
                texto = item.get("texto", "").strip()
                tabla = item.get("tabla", None)

                # Procesar texto narrativo
                if tipo == "texto":
                    if current_capitulo and capitulo != current_capitulo:
                        # Guardar el chunk narrativo actual al cambiar de capítulo
                        chunks_narrativos.append({
                            "capitulo": current_capitulo,
                            "texto": current_chunk_text.strip(),
                            "metadatos": {
                                "archivo": archivo.split("/")[-1],
                                "paginas_inicial": paginas_inicial,
                                "paginas_final": paginas_final,
                                "total_caracteres": len(current_chunk_text),
                            }
                        })
                        # Reiniciar para el nuevo capítulo
                        current_chunk_text = ""
                        current_chunk_size = 0
                        paginas_inicial = None

                    current_capitulo = capitulo
                    if paginas_inicial is None:
                        paginas_inicial = pagina_numero
                    paginas_final = pagina_numero

                    if current_chunk_size + len(texto) > chunk_size:
                        # Guardar el chunk actual y empezar uno nuevo
                        chunks_narrativos.append({
                            "capitulo": current_capitulo,
                            "texto": current_chunk_text.strip(),
                            "metadatos": {
                                "archivo": archivo.split("/")[-1],
                                "paginas_inicial": paginas_inicial,
                                "paginas_final": paginas_final,
                                "total_caracteres": len(current_chunk_text),
                            }
                        })
                        current_chunk_text = texto + "\n"
                        current_chunk_size = len(texto)
                        paginas_inicial = pagina_numero
                    else:
                        current_chunk_text += texto + "\n"
                        current_chunk_size += len(texto)

                # Procesar tablas
                elif tipo == "tabla" and tabla:
                    chunks_tablas.append({
                        "tabla": tabla,
                        "metadatos": {
                            "archivo": archivo.split("/")[-1],
                            "capitulo": capitulo,
                            "pagina": pagina_numero,
                            "filas": len(tabla),
                            "columnas": len(tabla[0]) if tabla else 0
                        }
                    })

        # Guardar el último chunk narrativo
        if current_chunk_text:
            chunks_narrativos.append({
                "capitulo": current_capitulo,
                "texto": current_chunk_text.strip(),
                "metadatos": {
                    "archivo": archivo.split("/")[-1],
                    "paginas_inicial": paginas_inicial,
                    "paginas_final": paginas_final,
                    "total_caracteres": len(current_chunk_text),
                }
            })

    return chunks_narrativos, chunks_tablas