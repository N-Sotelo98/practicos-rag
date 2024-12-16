# src/chunking/chunk_review.py

def revisar_chunks(chunked_data, num_ejemplos=3, incluir_tablas=False):
    """
    Revisa los chunks generados, mostrando ejemplos de texto narrativo y/o tablas según se indique.
    Args:
        chunked_data (list): Lista de chunks generados.
        num_ejemplos (int): Número máximo de ejemplos a mostrar.
        incluir_tablas (bool): Si es True, revisa solo chunks que incluyan tablas.
    """
    print("\n--- Ejemplo de revisión de chunks ---\n")
    ejemplos_mostrados = 0

    for idx, chunk in enumerate(chunked_data):
        if incluir_tablas and chunk["tablas"]:
            print(f"--- Chunk {idx + 1} (Con Tablas) ---")
            print(f"Capítulo: {chunk['capitulo']}")
            print(f"Texto (tamaño): {len(chunk['texto'])} caracteres")
            print(f"Metadatos: {chunk['metadatos']}")
            print("\nTexto del Chunk:")
            print(chunk["texto"][:500])
            print("\nTablas del Chunk:")
            for i, tabla in enumerate(chunk["tablas"]):
                print(f"- Tabla {i + 1}: {len(tabla)} filas")
                print(f"Primera fila: {tabla[0]}")
            ejemplos_mostrados += 1

        elif not incluir_tablas and not chunk["tablas"]:
            print(f"--- Chunk {idx + 1} (Narrativo) ---")
            print(f"Capítulo: {chunk['capitulo']}")
            print(f"Texto (tamaño): {len(chunk['texto'])} caracteres")
            print(f"Metadatos: {chunk['metadatos']}")
            print("\nTexto del Chunk:")
            print(chunk["texto"][:500])
            ejemplos_mostrados += 1

        if ejemplos_mostrados >= num_ejemplos:
            break
