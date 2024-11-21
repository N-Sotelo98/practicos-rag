import re
from nltk.tokenize import sent_tokenize
from typing import List, Dict, Any


def hybrid_chunking(text: str, max_chunk_size: int = 250) -> List[Dict[str, Any]]:
    """
    Divide el texto en chunks híbridos (narrativos y tablas).

    Args:
        text (str): Texto a chunkear.
        max_chunk_size (int): Tamaño máximo permitido para cada chunk.

    Returns:
        List[Dict[str, Any]]: Lista de chunks con el tipo y contenido.
    """
    chunks = []
    current_chunk = ""

    # Separar tablas explícitamente (se asume que están delimitadas por "\n")
    sections = re.split(
        r'\[TABLE START\](.*?)\[TABLE END\]', text, flags=re.DOTALL)

    for i, section in enumerate(sections):
        section = section.strip()

        if i % 2 == 1:  # Es una tabla (índices impares en el split)
            if current_chunk:
                # Guardar el chunk narrativo acumulado antes de la tabla
                chunks.append(
                    {"type": "narrative", "content": current_chunk.strip()})
                current_chunk = ""
            # Guardar la tabla como un chunk separado
            chunks.append({"type": "table", "content": section.strip()})
        else:  # Es texto narrativo
            sentences = sent_tokenize(section)  # Dividir el texto en oraciones
            for sentence in sentences:
                if len(current_chunk) + len(sentence) <= max_chunk_size:
                    current_chunk += sentence + " "
                else:
                    # Guardar el chunk cuando alcance el tamaño máximo
                    chunks.append(
                        {"type": "narrative", "content": current_chunk.strip()})
                    current_chunk = sentence + " "

    # Guardar cualquier chunk narrativo restante
    if current_chunk:
        chunks.append({"type": "narrative", "content": current_chunk.strip()})

    return chunks
