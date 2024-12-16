# src/chunking/hierarchical_chunker.py

def chunk_documents_hierarchically(processed_data, chunk_size=3000):
    """
    Realiza un chunking jerárquico de los documentos procesados, respetando la estructura de capítulos y artículos.
    Los chunks tienen un tamaño aproximado y se enriquecen con metadatos adicionales.
    Args:
        processed_data (dict): Datos procesados y enriquecidos.
        chunk_size (int): Tamaño máximo de cada chunk en caracteres.
    Returns:
        list: Lista de chunks generados con sus metadatos.
    """
    chunks = []

    for archivo, archivo_data in processed_data.items():
        current_chunk_text = ""
        current_chunk_tables = []
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

                # Detectar cambio de capítulo y guardar el chunk anterior
                if current_capitulo and capitulo != current_capitulo:
                    if current_chunk_text or current_chunk_tables:
                        chunks.append({
                            "capitulo": current_capitulo,
                            "texto": current_chunk_text.strip(),
                            "tablas": current_chunk_tables,
                            "metadatos": {
                                "archivo": archivo.split("/")[-1],
                                "paginas_inicial": paginas_inicial,
                                "paginas_final": paginas_final,
                                "total_caracteres": len(current_chunk_text),
                                "total_tablas": len(current_chunk_tables)
                            }
                        })
                    current_chunk_text = ""
                    current_chunk_tables = []
                    current_chunk_size = 0
                    paginas_inicial = None

                current_capitulo = capitulo
                if paginas_inicial is None:
                    paginas_inicial = pagina_numero
                paginas_final = pagina_numero

                if tipo == "texto":
                    if current_chunk_size + len(texto) > chunk_size:
                        chunks.append({
                            "capitulo": current_capitulo,
                            "texto": current_chunk_text.strip(),
                            "tablas": current_chunk_tables,
                            "metadatos": {
                                "archivo": archivo.split("/")[-1],
                                "paginas_inicial": paginas_inicial,
                                "paginas_final": paginas_final,
                                "total_caracteres": len(current_chunk_text),
                                "total_tablas": len(current_chunk_tables)
                            }
                        })
                        current_chunk_text = texto + "\n"
                        current_chunk_tables = []
                        current_chunk_size = len(texto)
                        paginas_inicial = pagina_numero
                    else:
                        current_chunk_text += texto + "\n"
                        current_chunk_size += len(texto)

                elif tipo == "tabla" and tabla:
                    current_chunk_tables.append(tabla)

        if current_chunk_text or current_chunk_tables:
            chunks.append({
                "capitulo": current_capitulo,
                "texto": current_chunk_text.strip(),
                "tablas": current_chunk_tables,
                "metadatos": {
                    "archivo": archivo.split("/")[-1],
                    "paginas_inicial": paginas_inicial,
                    "paginas_final": paginas_final,
                    "total_caracteres": len(current_chunk_text),
                    "total_tablas": len(current_chunk_tables)
                }
            })

    return chunks
