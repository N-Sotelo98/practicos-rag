from transformers import pipeline
from sentence_transformers import SentenceTransformer, util

# Cargar el modelo de embeddings para similitud semántica
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Cargar el modelo de generación de palabras clave (T5)
keyword_extractor = pipeline("text2text-generation", model="t5-small")


def generate_keywords_with_t5(query):
    """
    Genera palabras clave a partir de una consulta usando el modelo T5.

    Parámetros:
        - query: Consulta en texto.

    Salida:
        - Lista de palabras clave generadas automáticamente.
    """
    # Cambiar el prompt para que sea más claro
    prompt = f"Genera palabras clave relevantes para esta consulta: {query}"
    output = keyword_extractor(prompt, max_length=50, num_return_sequences=1)

    # Procesar la salida para convertirla en una lista
    keywords_text = output[0]["generated_text"]
    keywords = [kw.strip() for kw in keywords_text.split(",") if kw.strip()]

    return keywords


def expand_keywords_with_similarity(keywords, top_k=3):
    """
    Expande una lista de palabras clave utilizando similitud semántica.

    Parámetros:
        - keywords: Lista de palabras clave iniciales.
        - top_k: Número de términos relacionados por palabra clave.

    Retorna:
        - Lista de palabras clave expandidas.
    """
    expanded_keywords = set(keywords)

    # Generar embeddings para todas las palabras clave
    all_embeddings = embedding_model.encode(keywords, convert_to_tensor=True)

    for i, keyword in enumerate(keywords):
        try:
            # Calcular similitud con todas las demás palabras clave
            scores = util.pytorch_cos_sim(all_embeddings[i], all_embeddings)[0]

            # Obtener los índices de las palabras clave más similares
            similar_indices = scores.topk(
                k=min(top_k, len(keywords))).indices.tolist()

            # Asegurarse de que similar_indices sea una lista de enteros
            if isinstance(similar_indices[0], list):
                similar_indices = [
                    idx for sublist in similar_indices for idx in sublist]

            # Agregar las palabras clave más similares a la lista expandida
            # Evitar agregar la misma palabra
            similar_terms = [keywords[idx]
                             for idx in similar_indices if idx != i]
            expanded_keywords.update(similar_terms)
        except RuntimeError as e:
            print(f"Error al expandir la palabra clave '{keyword}': {e}")
    return list(expanded_keywords)
