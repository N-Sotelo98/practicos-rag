def preprocess_text_v2(text: str) -> str:
    """
    Procesa texto para limpiar y detectar tablas con delimitadores [TABLE START] y [TABLE END].

    Args:
        text (str): Texto extraído del PDF.

    Returns:
        str: Texto procesado con tablas delimitadas.
    """
    # Limpieza básica del texto
    text = text.strip()
    text = text.replace("\r", "").replace("\n\n", "\n").replace("..", ".")

    # Dividir el texto por líneas
    lines = text.splitlines()
    processed_lines = []
    in_table = False

    for i, line in enumerate(lines):
        # Detectar si una línea es parte de una tabla
        if detect_table_line(line):
            if not in_table:
                processed_lines.append("[TABLE START]")
                in_table = True
            processed_lines.append(line)
        else:
            if in_table:
                processed_lines.append("[TABLE END]")
                in_table = False
            processed_lines.append(line)

    # Finalizar tabla si quedó abierta
    if in_table:
        processed_lines.append("[TABLE END]")

    # Ensamblar texto procesado
    processed_text = "\n".join(processed_lines)

    # Validar consistencia en delimitadores
    if "[TABLE START]" in processed_text and "[TABLE END]" not in processed_text:
        processed_text += "\n[TABLE END]"
    if "[TABLE END]" in processed_text and "[TABLE START]" not in processed_text:
        processed_text = "[TABLE START]\n" + processed_text

    return processed_text


def detect_table_line(line: str) -> bool:
    """
    Detecta si una línea pertenece a una tabla basándose en patrones comunes.

    Args:
        line (str): Línea de texto.

    Returns:
        bool: True si la línea parece ser parte de una tabla, False en caso contrario.
    """
    # Detectar patrones comunes de tablas: múltiples espacios, tabulaciones o alineaciones numéricas
    return (
        bool(re.search(r" {2,}", line)) or  # Múltiples espacios
        bool(re.search(r"\t", line)) or    # Tabulaciones
        # Alineación numérica
        bool(re.match(r"^\d+(\.\d+)?(\s{2,}|\t)\d+", line))
    )
