from typing import List, Dict,Any
import glob
import re
from PyPDF2 import PdfReader
import json
import logging 

logger=logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (e.g., DEBUG, INFO, WARNING)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Format for log messages
    handlers=[
        logging.StreamHandler()  # Also log to the console
    ]
)
class Processing:
    '''
    Clase encargada del procesamiento de los datos para los distintos formatos de entrada 
    formatos soportados:
    - PDF
    Pipeline_workflow:
    - convertimos a json los pdfd
    - aplicamos expresiones regulares para limpiar los datos
    Retorna los datos listos para la segmentacion por chunks
    '''
    def __init__(self,ruta:str='./data/reglamentacion/',output:str='./data/staging/'):
        self.ruta=ruta
        self.output=output

    def load_pdfs(self):
        '''
        Cargamos los pdfs de la ruta especificada
        '''
        pdfs=glob.glob(self.ruta+"/*.pdf")
        pdfs = [path.replace("\\", "/") for path in pdfs] ## Compatibiliza con Windows
        logger.info(f"Se encontraron {len(pdfs)} pdfs en la ruta {self.ruta}")
        return pdfs
        
    def pdf_to_json(self):
        '''
        Convertimos todos los pdfs a json son almacenados en disco debido a la cantidad de datos
        '''
        try:
            pdfs=self.load_pdfs()
            for pdf in pdfs:
                with open(pdf,"rb") as file:
                    reader=PdfReader(file)
                    pdf_json={
                            "filename":pdf.split("/")[-1],
                            "contenido":''
                        }
                    for page in reader.pages:
                        content=page.extract_text()
                        pdf_json["contenido"]+=content
                logger.info(f"Procesando el PDF {pdf}")
                with open(self.output+pdf.split("/")[-1].replace(".pdf",".json"),"w",encoding='utf-8') as file:
                        json.dump(pdf_json,file,ensure_ascii=False)

        except Exception as e:
            logging.error(f"Error al procesar el PDF {pdf}: {e}")

    def clean_data(self):
        '''
        Utilizamos expresiones regulares para limpiar los datos
        '''
        jsons=glob.glob(self.output+"/*.json")
        logger.info(f"Se encontraron {len(jsons)} jsons en la ruta {self.output}")
        logger.info("Iniciando limpieza de datos")
        for json_file in jsons:
            with open(json_file,"r",encoding="utf-8") as file:
                data=json.load(file)
                # TO DO: algun patron para encadenar las expresiones regulares ??
                data["contenido"]=re.sub(r'\n+', ' ',data["contenido"])
                data["contenido"]=re.sub(r'^\s+|\s+$', '', data["contenido"],flags=re.MULTILINE)
                data["contenido"]=re.sub(r'[^\w\s.,;:()\-/%]', '',data["contenido"])
                data["contenido"]=re.sub(r'(\w)-\n(\w)', r'\1\2', data["contenido"])
                data["contenido"]=re.sub(r'(?<![.!?])\n(?![A-Z])', ' ', data["contenido"])
                data['contenido']=re.sub(r'(?i)(cap[ií]tulo \d+|secci[oó]n \d+)', r'\n### \1 ###\n', data['contenido'])
                data['contenido']=re.sub(r'(\S+)\s{2,}(\S+)', r'[TABLE START]\n\1\t\2\n[TABLE END]', data['contenido'])
            with open(json_file,"w",encoding="utf-8") as file:
                json.dump(data,file,ensure_ascii=False)
        logger.info("Finalizada la limpieza de datos")