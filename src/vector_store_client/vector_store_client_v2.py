# vector_store_client_v2.py
"""
Módulo para manejar la interacción con la vector database.

Incluye:
- Validación de metadatos y embeddings.
- Inserción de puntos en la base de datos con metadatos extendidos.
"""

import qdrant_client
from qdrant_client.http.models import PointStruct


def insert_embeddings_v2(client, index_name, embeddings, metadata_list, batch_size=100):
    """
    Inserta embeddings y metadatos en un índice de Qdrant.

    Args:
        client: Cliente de Qdrant.
        index_name: Nombre del índice.
        embeddings: Lista de embeddings generados.
        metadata_list: Lista de metadatos asociados a cada embedding.
        batch_size: Tamaño del lote para inserción.
    """
    points = []
    for i, (embedding, metadata) in enumerate(zip(embeddings, metadata_list)):
        if embedding is None:
            print(f"Advertencia: Embedding en posición {i} es None. Saltando.")
            continue

        points.append(PointStruct(
            id=i,
            vector=embedding,
            payload=metadata
        ))

    # Insertar los puntos en lotes
    for i in range(0, len(points), batch_size):
        batch = points[i:i + batch_size]
        client.upsert(
            collection_name=index_name,
            points=batch
        )
        print(f"Lote {i // batch_size + 1} insertado con éxito.")

    print("Embeddings y metadatos insertados correctamente.")


if __name__ == "__main__":
    # Ejemplo de prueba
    from qdrant_client import QdrantClient

    client = QdrantClient("http://localhost:6333")
    example_embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    example_metadata = [
        {"type": "narrative", "content": "Texto narrativo de prueba."},
        {"type": "table", "content": "Encabezado1\tEncabezado2\nDato1\tDato2"},
    ]

    insert_embeddings_v2(client, "test_index",
                         example_embeddings, example_metadata)
