import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def hybrid_reranking(results, query_embedding, query_keywords):
    """
    Rerankea resultados de retrieval usando similitud semántica y palabras clave.

    Parámetros:
        - results: Resultados recuperados inicialmente.
        - query_embedding: Embedding de la consulta del usuario (tensor).
        - query_keywords: Lista de palabras clave generadas y expandidas.

    Retorna:
        - Resultados rerankeados por relevancia.
    """
    # Convertir el embedding de la consulta al CPU si está en un dispositivo (GPU/MPS)
    if query_embedding.is_cuda or query_embedding.device.type == 'mps':
        query_embedding = query_embedding.cpu()

    query_embedding = query_embedding.numpy()  # Convertir a NumPy

    # Filtrar vectores válidos (sin NaN) y asociarlos a sus resultados
    valid_results = []
    valid_embeddings = []
    for result in results:
        if result.vector is not None:
            vector = np.asarray(result.vector)
            if not np.isnan(vector).any():
                valid_results.append(result)
                valid_embeddings.append(vector)

    # Verificar si hay resultados válidos
    if not valid_results:
        raise ValueError(
            "No se encontraron vectores válidos en los resultados.")

    # Calcular similitud coseno entre el embedding de la consulta y los resultados válidos
    similarities = cosine_similarity([query_embedding], valid_embeddings)[0]

    for i, result in enumerate(valid_results):
        # Sumar puntuación basada en similitud coseno
        result.score += similarities[i]

        # Incrementar puntuación si el contenido incluye palabras clave
        content = result.payload['content']['content'].lower()
        for keyword in query_keywords:
            if keyword in content:
                result.score += 0.1  # Incremento basado en coincidencias

    # Ordenar resultados por puntuación final
    return sorted(valid_results, key=lambda x: x.score, reverse=True)
