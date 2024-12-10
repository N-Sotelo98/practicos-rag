import pdfplumber
import json
from text_preprocessing.text_processing_v2 import preprocess_text_v2


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

                # Preprocesar el texto
                preprocessed_text = preprocess_text_v2(raw_text)

                # Agregar los datos procesados al JSON
                pdf_data["capitulos"].append({
                    # Puede reemplazarse con lógica para detectar capítulos
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
