# vector_store_client_v2.py
"""
Módulo para manejar la interacción con la vector database.

Incluye:
- Validación exhaustiva de puntos.
- Inserción robusta en lotes pequeños para evitar errores globales.
"""

from qdrant_client.http.models import PointStruct


def insert_embeddings_v2(client, index_name, embeddings, metadata_list, batch_size=100):
    """
    Inserta embeddings y metadatos en Qdrant con validaciones adicionales y tolerancia a errores.

    Args:
        client: Cliente de Qdrant.
        index_name: Nombre de la colección.
        embeddings: Lista de embeddings generados.
        metadata_list: Lista de metadatos asociados a cada embedding.
        batch_size: Tamaño del lote para inserción.
    """
    valid_points = []
    vector_key = "default"  # Clave esperada en la colección

    # Validar y construir puntos
    for i, (embedding, metadata) in enumerate(zip(embeddings, metadata_list)):
        try:
            # Validar estructura del embedding
            if not isinstance(embedding, list) or len(embedding) != 384:
                raise ValueError(
                    f"Embedding inválido en índice {i}: {embedding}")

            # Validar estructura del metadata
            if not isinstance(metadata, dict):
                raise ValueError(f"Payload inválido en índice {i}: {metadata}")

            # Crear punto
            point = PointStruct(
                id=i,
                # Asegurarse de usar la clave 'default'
                vector={vector_key: embedding},
                payload=metadata
            )
            valid_points.append(point)
        except Exception as e:
            print(f"Error al procesar el punto {i}: {e}")

    # Insertar puntos en lotes pequeños para detectar errores específicos
    for i in range(0, len(valid_points), batch_size):
        batch = valid_points[i:i + batch_size]
        print(
            f"Intentando insertar lote {i // batch_size + 1} con {len(batch)} puntos...")

        try:
            response = client.upsert(
                collection_name=index_name,
                points=batch
            )
            print(f"Lote {i // batch_size + 1} insertado con éxito: {response}")
        except Exception as e:
            print(f"Error al insertar lote {i // batch_size + 1}: {e}")
            for point in batch:  # Intentar insertar punto por punto en caso de error
                try:
                    single_response = client.upsert(
                        collection_name=index_name,
                        points=[point]
                    )
                    print(
                        f"Punto {point.id} insertado con éxito: {single_response}")
                except Exception as single_error:
                    print(
                        f"Error al insertar el punto {point.id}: {single_error}")

    print("Proceso de inserción finalizado.")
