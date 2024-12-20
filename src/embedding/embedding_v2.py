# embedding_v2.py

"""
Módulo para generación de embeddings adaptado al nuevo formato de chunks.

Incluye soporte para:
- Validación de chunks malformados.
- Manejo de errores en la generación de embeddings.
- Adaptación a la estructura esperada para inserción en Qdrant.
"""

import os
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import numpy as np
import openai
from openai import OpenAI


# Cargar el modelo preentrenado
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Modelo 'all-MiniLM-L6-v2' cargado correctamente.")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    model = None


def generate_embeddings_v2(chunks):
    """
    Genera embeddings para una lista de chunks en formato extendido.

    Args:
        chunks (list of dict): Lista de chunks con formato {"type": "...", "content": "..."}.

    Returns:
        list of dict: Lista con embeddings y metadatos para cada chunk válido.
    """
    if model is None:
        raise ValueError(
            "El modelo no está cargado. No se pueden generar embeddings.")

    embeddings_with_metadata = []
    try:
        print(f"Generando embeddings para {len(chunks)} chunks...")

        for idx, chunk in enumerate(tqdm(chunks, desc="Generando embeddings", unit="chunk")):
            content = chunk.get("content", "")
            chunk_type = chunk.get("type", "unknown")

            if not content:
                print(f"Advertencia: Chunk sin contenido (ID: {idx}): {chunk}")
                continue

            # Generar el embedding para el contenido
            embedding = model.encode(content, convert_to_numpy=True)
            if not isinstance(embedding, np.ndarray):
                print(f"Error: Embedding no válido para chunk ID {idx}")
                continue

            # Estructura del resultado adaptada a Qdrant (clave 'default' para el vector)
            embeddings_with_metadata.append({
                "id": idx,
                # Clave 'default' requerida por Qdrant
                "vector": {"default": embedding.tolist()},
                "payload": {
                    "type": chunk_type,
                    "content": content,
                    "content_length": len(content)
                }
            })

        print(
            f"Total de embeddings generados: {len(embeddings_with_metadata)}")
    except Exception as e:
        print(f"Error al generar embeddings: {e}")

    return embeddings_with_metadata


def generate_query_embedding(query):
    """
    Genera el embedding para una consulta de búsqueda en Qdrant.

    Args:
        query (str): Texto de la consulta.

    Returns:
        list: Embedding plano como lista de floats.
    """
    query_chunk = [{"type": "narrative", "content": query}
                   ]  # Formatear como chunk
    try:
        embedding_result = generate_embeddings_v2(query_chunk)[0]
        if "vector" in embedding_result and "default" in embedding_result["vector"]:
            # Devuelve el vector plano
            return embedding_result["vector"]["default"]
        else:
            raise ValueError(
                "El embedding generado no contiene el formato esperado ('vector' -> 'default').")
    except IndexError:
        raise ValueError(
            "No se generó un embedding para la consulta. Verifica `generate_embeddings_v2`.")
    except Exception as e:
        raise ValueError(
            f"Error inesperado al generar el embedding de la consulta: {e}")


if __name__ == "__main__":
    # Ejemplo de prueba
    example_chunks = [
        {"type": "narrative", "content": "Este es un texto narrativo para prueba."},
        {"type": "table", "content": "Encabezado1\tEncabezado2\nDato1\tDato2"},
        {"type": "empty", "content": ""},
    ]

    # Generar embeddings y metadatos
    embeddings_with_metadata = generate_embeddings_v2(example_chunks)

    # Imprimir resultados generados
    print("Embeddings generados y listos para inserción en Qdrant:")
    for item in embeddings_with_metadata:
        print(item)


# Crear una instancia del cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_embeddings_v2_openai(chunks):
    """
    Genera embeddings para una lista de chunks utilizando OpenAI.

    Args:
        chunks (list of dict): Lista de chunks con formato {"type": "...", "content": "..."}.

    Returns:
        list of dict: Lista con embeddings y metadatos para cada chunk válido.
    """
    embeddings_with_metadata = []
    try:
        print(f"Generando embeddings con OpenAI para {len(chunks)} chunks...")

        for idx, chunk in enumerate(tqdm(chunks, desc="Generando embeddings", unit="chunk")):
            content = chunk.get("content", "")
            chunk_type = chunk.get("type", "unknown")

            if not content:
                print(f"Advertencia: Chunk sin contenido (ID: {idx}): {chunk}")
                continue

            # Generar el embedding para el contenido utilizando OpenAI
            try:
                response = client.embeddings.create(
                    model="text-embedding-ada-002",
                    input=content
                )
                embedding = response.data[0].embedding
            except Exception as e:
                print(f"Error al generar embedding para chunk ID {idx}: {e}")
                continue

            # Estructura del resultado adaptada a Qdrant
            embeddings_with_metadata.append({
                "id": idx,
                "vector": {"default": embedding},
                "payload": {
                    "type": chunk_type,
                    "content": content,
                    "content_length": len(content)
                }
            })

        print(
            f"Total de embeddings generados con OpenAI: {len(embeddings_with_metadata)}")
    except Exception as e:
        print(f"Error al generar embeddings con OpenAI: {e}")

    return embeddings_with_metadata


def generate_query_embedding_openai(query):
    """
    Genera el embedding para una consulta de búsqueda usando OpenAI.

    Args:
        query (str): Texto de la consulta.

    Returns:
        list: Embedding plano como lista de floats.
    """
    query_chunk = [{"type": "narrative", "content": query}]
    try:
        embedding_result = generate_embeddings_v2_openai(query_chunk)[0]
        if "vector" in embedding_result and "default" in embedding_result["vector"]:
            # Devuelve el vector plano
            return embedding_result["vector"]["default"]
        else:
            raise ValueError(
                "El embedding generado no contiene el formato esperado ('vector' -> 'default').")
    except IndexError:
        raise ValueError(
            "No se generó un embedding para la consulta. Verifica `generate_embeddings_v2_openai`.")
    except Exception as e:
        raise ValueError(
            f"Error inesperado al generar el embedding de la consulta con OpenAI: {e}")
