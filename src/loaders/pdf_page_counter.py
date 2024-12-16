import os
import pdfplumber


def count_pdf_pages(pdf_directory):
    """
    Cuenta el número de páginas en cada archivo PDF dentro de un directorio.
    """
    pdf_page_counts = []
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith(".pdf")]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_directory, pdf_file)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                num_pages = len(pdf.pages)
                pdf_page_counts.append(
                    {"file_name": pdf_file, "page_count": num_pages})
        except Exception as e:
            print(f"Error al procesar {pdf_file}: {e}")

    return sorted(pdf_page_counts, key=lambda x: x["page_count"])
