# chunking/chunk_verifier.py

def verificar_chunks_narrativos_completos(chunks_narrativos, num_chunks=3):
    """
    Verifica y muestra contenido completo de chunks narrativos.

    Args:
        chunks_narrativos (list): Lista de chunks narrativos.
        num_chunks (int): Número de chunks narrativos a verificar.
    """
    print("\n--- Verificando Chunks Narrativos Completos ---\n")
    for idx, chunk in enumerate(chunks_narrativos[:num_chunks]):
        print(f"--- Chunk Narrativo Completo {idx + 1} ---")
        print(f"Capítulo: {chunk['capitulo']}")
        print(f"Metadatos: {chunk['metadatos']}\n")
        print("Contenido Completo:")
        print(chunk["texto"])
        print("\n" + "=" * 80)


def verificar_chunks_tablas_completos(chunks_tablas, num_chunks=3):
    """
    Verifica y muestra contenido completo de chunks de tablas.

    Args:
        chunks_tablas (list): Lista de chunks de tablas.
        num_chunks (int): Número de chunks de tablas a verificar.
    """
    print("\n--- Verificando Chunks de Tablas Completos ---\n")
    for idx, chunk in enumerate(chunks_tablas[:num_chunks]):
        print(f"--- Chunk de Tabla Completo {idx + 1} ---")
        print(f"Metadatos: {chunk['metadatos']}\n")
        print("Contenido Completo de la Tabla:")
        for fila in chunk["tabla"]:
            print(fila)
        print("\n" + "=" * 80)
