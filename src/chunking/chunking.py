from langchain.text_splitter import RecursiveCharacterTextSplitter


def split_text_into_chunks(text, chunk_size=1000, chunk_overlap=100):
    """
    Divide un texto en fragmentos (chunks) con un tamaño y solapamiento definidos.

    Args:
        text (str): El texto completo que se desea dividir.
        chunk_size (int): Longitud máxima de cada fragmento (en caracteres).
        chunk_overlap (int): Número de caracteres que se solaparán entre fragmentos.

    Returns:
        list: Lista de fragmentos de texto.
    """
    # Crear un divisor de texto
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    # Dividir el texto en fragmentos
    chunks = text_splitter.split_text(text)
    return chunks
