# chunking_optimized.py
"""
Módulo para realizar chunking optimizado de textos con metadatos.

Actualizaciones:
- Consolidación de tablas completas en un solo chunk.
- Filtrado directo de chunks vacíos o menores a un tamaño mínimo.
- Lógica revisada para garantizar chunks narrativos significativos.
- Mejora en la detección de encabezados y tablas.
"""

import re
from nltk.tokenize import sent_tokenize
from typing import List, Dict, Any


def extract_headers(text: str) -> List[str]:
    """
    Extrae encabezados flexibles (como títulos de capítulos y secciones) del texto.

    Args:
        text (str): Texto del documento.

    Returns:
        List[str]: Lista de encabezados detectados en el texto.
    """
    # Buscar patrones genéricos de encabezados (opcional ajustar según los textos)
    headers = re.findall(
        r'(CAPÍTULO \w+|Sección [\w\d.]+|Artículo \d+)', text, flags=re.IGNORECASE)
    return headers


def is_valid_narrative(text: str, threshold: float = 0.7) -> bool:
    """
    Evalúa si un texto es una narrativa válida basada en la proporción de palabras significativas.

    Args:
        text (str): Texto a evaluar.
        threshold (float): Proporción mínima de palabras significativas.

    Returns:
        bool: True si es una narrativa válida, False de lo contrario.
    """
    words = text.split()
    meaningful_words = [word for word in words if len(word) > 3]
    return len(meaningful_words) / len(words) >= threshold if words else False


def chunk_narratives(
    text: str,
    file_name: str,
    chapter: str,
    section: str,
    max_chunk_size: int = 250,
    overlap: int = 50,
    min_chunk_size: int = 20
) -> List[Dict[str, Any]]:
    """
    Divide narrativas en chunks con superposición y agrega metadatos.

    Args:
        text (str): Texto narrativo a dividir.
        file_name (str): Nombre del archivo de origen.
        chapter (str): Capítulo al que pertenece el chunk.
        section (str): Sección o artículo del chunk.
        max_chunk_size (int): Tamaño máximo de cada chunk.
        overlap (int): Superposición entre chunks.
        min_chunk_size (int): Tamaño mínimo para un chunk válido.

    Returns:
        List[Dict[str, Any]]: Lista de chunks narrativos con metadatos.
    """
    tokens = sent_tokenize(text)
    chunks = []
    current_chunk = ""

    for token in tokens:
        if len(current_chunk) + len(token) <= max_chunk_size:
            current_chunk += token + " "
        else:
            if len(current_chunk.strip()) >= min_chunk_size and is_valid_narrative(current_chunk):
                chunks.append({
                    "type": "narrative",
                    "content": current_chunk.strip(),
                    "file_name": file_name,
                    "chapter": chapter,
                    "section": section
                })
            # Agregar superposición
            current_chunk = current_chunk[-overlap:].strip() + token + " "

    if len(current_chunk.strip()) >= min_chunk_size and is_valid_narrative(current_chunk):  # Último chunk
        chunks.append({
            "type": "narrative",
            "content": current_chunk.strip(),
            "file_name": file_name,
            "chapter": chapter,
            "section": section
        })

    return chunks


def process_tables(
    tables: List[str],
    file_name: str,
    chapter: str,
    section: str,
    min_chunk_size: int = 20
) -> List[Dict[str, Any]]:
    """
    Procesa tablas completas y agrega metadatos.

    Args:
        tables (List[str]): Lista de tablas extraídas del texto.
        file_name (str): Nombre del archivo de origen.
        chapter (str): Capítulo al que pertenece el chunk.
        section (str): Sección o artículo del chunk.
        min_chunk_size (int): Tamaño mínimo para un chunk válido.

    Returns:
        List[Dict[str, Any]]: Lista de tablas estructuradas con metadatos.
    """
    processed_tables = []
    for table in tables:
        rows = table.split("\n")
        # Estructura tabular simple
        structured_table = " | ".join(row.strip()
                                      for row in rows if row.strip())
        if len(structured_table) >= min_chunk_size:
            processed_tables.append({
                "type": "table",
                "content": structured_table,
                "file_name": file_name,
                "chapter": chapter,
                "section": section
            })
    return processed_tables


def optimized_chunking(
    text: str,
    file_name: str,
    max_chunk_size: int = 250,
    overlap: int = 50,
    min_chunk_size: int = 20
) -> List[Dict[str, Any]]:
    """
    Realiza chunking optimizado del texto, separando narrativas y tablas, e incluye metadatos.

    Args:
        text (str): Texto a chunkear.
        file_name (str): Nombre del archivo de origen.
        max_chunk_size (int): Tamaño máximo de cada chunk.
        overlap (int): Superposición entre chunks narrativos para conservar contexto.
        min_chunk_size (int): Tamaño mínimo para un chunk válido.

    Returns:
        List[Dict[str, Any]]: Lista de chunks con tipo (narrativa o tabla) y contenido.
    """
    chunks = []
    headers = extract_headers(text)
    chapter = headers[0] if headers else "Unknown"
    section = headers[1] if len(headers) > 1 else "Unknown"

    # Separar texto en secciones delimitadas por tablas
    sections = re.split(
        r'\[TABLE START\](.*?)\[TABLE END\]', text, flags=re.DOTALL)

    for i, section_content in enumerate(sections):
        section_content = section_content.strip()

        if i % 2 == 1:  # Es una tabla
            tables = [section_content]
            chunks.extend(process_tables(tables, file_name,
                          chapter, section, min_chunk_size))
        else:  # Es narrativa
            narrative_chunks = chunk_narratives(
                section_content, file_name, chapter, section, max_chunk_size, overlap, min_chunk_size
            )
            chunks.extend(narrative_chunks)

    return chunks


if __name__ == "__main__":
    # Ejemplo de prueba
    example_text = """
    ### Capítulo 1 ###
    Este es un texto narrativo que explica los puntos principales.
    Este texto es lo suficientemente largo para ser dividido en múltiples chunks.

    [TABLE START]
    Encabezado1\tEncabezado2\tEncabezado3
    Dato1\tDato2\tDato3
    Dato4\tDato5\tDato6
    [TABLE END]

    ### Sección 1.1 ###
    Este es otro texto narrativo que debe ser dividido.
    """

    chunks = optimized_chunking(
        example_text, file_name="example.pdf", max_chunk_size=100, overlap=20, min_chunk_size=20
    )
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i + 1}: {chunk}")
