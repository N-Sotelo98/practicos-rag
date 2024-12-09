# embedding_v2.py
"""
Módulo para generación de embeddings adaptado al nuevo formato de chunks.

Incluye soporte para:
- Validación de chunks malformados.
- Manejo de errores en la generación de embeddings.
"""

from sentence_transformers import SentenceTransformer
from tqdm import tqdm

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
        list of list of float: Lista de embeddings generados para cada chunk.
    """
    if model is None:
        raise ValueError(
            "El modelo no está cargado. No se pueden generar embeddings.")

    embeddings = []
    try:
        print(f"Generando embeddings para {len(chunks)} chunks...")

        for chunk in tqdm(chunks, desc="Generando embeddings", unit="chunk"):
            content = chunk.get("content", "")
            if not content:
                print(f"Advertencia: Chunk sin contenido: {chunk}")
                embeddings.append(None)
                continue

            embedding = model.encode(content, convert_to_numpy=True)
            embeddings.append(embedding)

        print(f"Total de embeddings generados: {len(embeddings)}")
    except Exception as e:
        print(f"Error al generar embeddings: {e}")
    return embeddings


if __name__ == "__main__":
    # Ejemplo de prueba
    example_chunks = [
        {"type": "narrative", "content": "Este es un texto narrativo para prueba."},
        {"type": "table", "content": "Encabezado1\tEncabezado2\nDato1\tDato2"},
    ]

    embeddings = generate_embeddings_v2(example_chunks)
    print(f"Embeddings generados: {embeddings}")
