def process_pdf_to_json(pdf_path: str, output_json_path: str = None) -> dict:
    """
    Procesa un archivo PDF y extrae su contenido en formato JSON.
    Opcionalmente, guarda el JSON en un archivo si se proporciona 'output_json_path'.
    """
    try:
        from PyPDF2 import PdfReader

        reader = PdfReader(pdf_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text()

        pdf_data = {
            "capitulos": [
                {
                    "numero": "1",
                    "titulo": "Ejemplo de Título",
                    "articulos": [
                        {
                            "numero": "1.1",
                            "contenido": text
                        }
                    ]
                }
            ]
        }

        # Si se proporciona una ruta para guardar el JSON, guárdalo
        if output_json_path:
            print(f"Guardando JSON en: {output_json_path}")
            with open(output_json_path, "w", encoding="utf-8") as f:
                json.dump(pdf_data, f, ensure_ascii=False, indent=4)

        return pdf_data

    except Exception as e:
        print(f"Error al procesar el PDF {pdf_path}: {e}")
        raise
