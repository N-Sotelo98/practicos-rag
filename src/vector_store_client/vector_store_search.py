"""
Módulo para manejar la búsqueda de embeddings en Qdrant.
"""


def search_embeddings(client, index_name, query_embedding, limit=5):
    """
    Realiza una búsqueda en Qdrant para encontrar puntos similares a un embedding dado.

    Args:
        client: Cliente de Qdrant.
        index_name: Nombre de la colección.
        query_embedding: Embedding de la consulta (vector plano).
        limit: Número máximo de resultados a devolver.

    Returns:
        Lista de resultados de la búsqueda.
    """
    try:
        # Qdrant espera el vector como una lista, no como un diccionario
        results = client.search(
            collection_name=index_name,
            query_vector=query_embedding,  # Vector plano
            limit=limit,
            with_payload=True,
            with_vectors=True
        )
        return results
    except Exception as e:
        print(f"Error al realizar la búsqueda: {e}")
        return []


def format_search_results(query, results):
    """
    Formatea y muestra los resultados de una búsqueda de embeddings.

    Args:
        query: Texto de la consulta.
        results: Lista de resultados devueltos por Qdrant.

    Returns:
        None
    """
    print(f"\nResultados de la búsqueda para la consulta: '{query}'")
    if not results:
        print("No se encontraron resultados.")
        return

    print(f"Total de resultados: {len(results)}")
    print("-" * 80)

    for idx, result in enumerate(results, start=1):
        print(f"Resultado {idx}:")
        print(f"ID: {result.id}")
        print(f"Score: {result.score}")
        payload = result.payload
        print("Contenido del payload:")
        if payload and isinstance(payload, dict):
            for key, value in payload.items():
                print(
                    f"  {key}: {value[:100] if isinstance(value, str) else value}")
        print("-" * 80)
