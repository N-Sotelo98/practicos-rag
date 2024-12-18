# vector_store_search.py

"""
Módulo para manejar la búsqueda de embeddings en Qdrant.
"""


from qdrant_client.http.models import QueryRequest


def search_embeddings(client, index_name, query_embedding, limit=5):
    """
    Realiza una búsqueda en Qdrant usando QueryRequest.

    Args:
        client: Cliente de Qdrant.
        index_name: Nombre de la colección.
        query_embedding: Embedding de la consulta (vector plano).
        limit: Número máximo de resultados a devolver.

    Returns:
        Lista de resultados de la búsqueda.
    """
    try:
        # Verificar el formato del embedding
        if not isinstance(query_embedding, list) or len(query_embedding) != 384:
            raise ValueError(
                f"El embedding de la consulta no es válido. "
                f"Esperado: lista de 384 dimensiones, Recibido: {type(query_embedding)}, Tamaño: {len(query_embedding) if isinstance(query_embedding, list) else 'N/A'}"
            )

        print(
            f"query_embedding válido: {query_embedding[:5]}... [Total dimensiones: {len(query_embedding)}]")

        # Crear la solicitud de consulta con QueryRequest
        query_request = QueryRequest(
            vector={"default": query_embedding},  # Vector con nombre explícito
            limit=limit,
            with_payload=True
        )
        print(f"QueryRequest creado: {query_request}")

        # Verificar el estado de la colección antes de la consulta
        collection_info = client.http.collections_api.get_collection(
            index_name)
        if "default" not in collection_info.result.config.params.vectors:
            raise ValueError(
                f"La colección '{index_name}' no contiene un vector llamado 'default'. "
                f"Vectores disponibles: {list(collection_info.result.config.params.vectors.keys())}"
            )

        print(
            f"Estado de la colección '{index_name}': {collection_info.result.status}")

        # Realizar la consulta
        results = client.http.points_api.query_points(
            collection_name=index_name,
            query_request=query_request
        )

        print(
            f"Consulta realizada con éxito. Resultados obtenidos: {len(results.result)}")
        return results.result

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
