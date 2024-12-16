import pdfplumber
import json
from text_preprocessing.text_processing_v2 import preprocess_text_v2
import re


def process_pdf_to_json(pdf_path: str, output_json_path: str = None) -> dict:
    """
    Procesa un archivo PDF y extrae su contenido en formato JSON.
    Aplica preprocesamiento para detectar encabezados y tablas.
    Opcionalmente, guarda el JSON en un archivo si se proporciona 'output_json_path'.

    Args:
        pdf_path (str): Ruta del archivo PDF.
        output_json_path (str, opcional): Ruta para guardar el archivo JSON.

    Returns:
        dict: Datos del PDF en formato JSON.
    """
    try:
        # Abrir el PDF usando pdfplumber
        with pdfplumber.open(pdf_path) as pdf:
            pdf_data = {
                "capitulos": []
            }

            for page_number, page in enumerate(pdf.pages, start=1):
                # Extraer texto crudo de la página
                raw_text = page.extract_text()
                if not raw_text:
                    print(
                        f"Advertencia: No se pudo extraer texto de la página {page_number}")
                    continue

                # Dividir texto en líneas para procesar tablas
                lines = raw_text.split("\n")
                preprocessed_lines = []

                # Detectar tablas en el texto crudo
                in_table = False
                for line in lines:
                    if detect_table_line(line):
                        if not in_table:
                            preprocessed_lines.append("[TABLE START]")
                            in_table = True
                        preprocessed_lines.append(line)
                    else:
                        if in_table:
                            preprocessed_lines.append("[TABLE END]")
                            in_table = False
                        preprocessed_lines.append(line)

                # Finalizar tabla si quedó abierta
                if in_table:
                    preprocessed_lines.append("[TABLE END]")

                # Unir líneas preprocesadas
                preprocessed_text = preprocess_text_v2(
                    "\n".join(preprocessed_lines))

                # Agregar los datos procesados al JSON
                pdf_data["capitulos"].append({
                    "numero": str(page_number),
                    "titulo": f"Página {page_number}",
                    "articulos": [
                        {
                            "numero": f"{page_number}.1",
                            "contenido": preprocessed_text
                        }
                    ]
                })

        # Si se proporciona una ruta para guardar el JSON, guárdalo
        if output_json_path:
            print(f"Guardando JSON en: {output_json_path}")
            with open(output_json_path, "w", encoding="utf-8") as f:
                json.dump(pdf_data, f, ensure_ascii=False, indent=4)

        return pdf_data

    except Exception as e:
        print(f"Error al procesar el PDF {pdf_path}: {e}")
        raise


def detect_table_line(line: str) -> bool:
    """
    Detecta si una línea pertenece a una tabla basada en patrones comunes.

    Args:
        line (str): Línea de texto a analizar.

    Returns:
        bool: True si la línea parece ser parte de una tabla, False en caso contrario.
    """
    # Detectar columnas separadas por espacios múltiples o tabulaciones
    return bool(re.search(r" {2,}", line)) or bool(re.search(r"\t", line))
