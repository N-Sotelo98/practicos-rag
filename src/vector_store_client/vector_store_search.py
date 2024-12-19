# vector_store_search.py

"""
Módulo para manejar la búsqueda de embeddings en Qdrant.
"""


from qdrant_client.http.models import QueryRequest


def search_embeddings(client, index_name, query_embedding, limit=5):
    """
    Realiza una búsqueda en Qdrant usando el vector nombrado 'default'.

    Args:
        client: Cliente de Qdrant.
        index_name: Nombre de la colección.
        query_embedding: Embedding de la consulta (vector plano).
        limit: Número máximo de resultados a devolver.

    Returns:
        Lista de resultados de la búsqueda.
    """
    try:
        # Validar que el embedding sea correcto
        if not isinstance(query_embedding, list) or len(query_embedding) != 384:
            raise ValueError(
                f"El vector de consulta debe ser una lista de 384 dimensiones. "
                f"Recibido: {type(query_embedding)} con tamaño {len(query_embedding)}"
            )

        # Debug para el embedding enviado
        print(
            f"query_embedding enviado: {query_embedding[:5]}... [{len(query_embedding) - 10} dimensiones omitidas] ...{query_embedding[-5:]}")

        # Realizar la consulta con el parámetro 'using="default"'
        results = client.query_points(
            collection_name=index_name,
            query=query_embedding,  # Vector de consulta
            limit=limit,
            using="default",  # Nombre explícito del vector
            with_payload=True,   # Incluir los payloads
            with_vectors=True    # Solicitar la inclusión de vectores
        )

        print(
            f"Consulta realizada con éxito. Resultados obtenidos: {len(results.points)}")
        return results.points

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
