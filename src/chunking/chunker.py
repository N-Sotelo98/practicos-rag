from typing import List, Dict, Any
import logging
import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from collections import namedtuple
import json


"""
  Class in charge of enforcing chunking strategies to the data
 """
logger = logging.getLogger(__name__)


class Chunker:
    def __init__(self, data, max_chunk_size=3000, output_path="./data/staging/"):
        load_dotenv()
        os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini"
        )  
        self.data = data
        self.chunk_size = max_chunk_size
        self.output_path = output_path

    def summarize_table(self, tables: List[str]) -> str:
        """
        Summarize the content of the table using the LLM
        """
        table_summaries = []
        context="""Eres un analista que trabaja en el sector alimentario tu trabajo es resumir la información presente en la siguiente tabla: {table} 
                                                en caso de que no contenga informacion relevante para tu rubro laboral tu respuesta debe ser N/A """
        template = ChatPromptTemplate.from_template(context)
        for table in tables:
            prompt = template.invoke(input={"table": table})
            content_table = self.llm.invoke(prompt).content
            if content_table != "N/A":
                table_summaries.append(content_table)

        return table_summaries

    # To do: generate blocks of text based on keywords: ARTICULO, Resolucion ANexo
    def process_text(self, text: str) -> List[str]:
        """
        Processes the text into a list of sentence chunks. A new chunk is created if:
        - The sentence starts with 'Resolución' or 'Artículo'.
        - The chunk exceeds a predefined size limit (`self.chunk_size`).

        Args:
        - text: A string containing the text to be processed.

        Returns:
        - A list of sentence chunks.
        """
        chunk_sentences = []
        sentences = text.split("\n")
        text_block = []

        for sentence in sentences:
            if (
                sentence.startswith("Artículo")
                or sentence.startswith("Resolución")
                or sentence.startswith("RESOLUCION")
                or len(text_block) >= self.chunk_size
            ):
                if text_block:
                    chunk_sentences.append(" ".join(text_block))
                text_block = [sentence]
            else:
                text_block.append(sentence)

        if text_block:
            chunk_sentences.append(" ".join(text_block))

        return chunk_sentences

    def chunking_hybrid(self) -> Dict[str, Any]:
        """
        Function which performs hybrid chunking on the data. It processes the text and tables in the data and returns a list of chunks.

        Returns:
            Dict[str, Any]: A dictionary containing the chunks.
        """
        chunks: tuple = []
        name_file=''
        Chunk: tuple = namedtuple("Chunk", ["contenido", "metadata"])
        for chapter in self.data:
            name_file=chapter["file_name"]
            sentences = self.process_text(chapter["text"])
            table_summaries = self.summarize_table(chapter["tables"])

            for sentence in sentences:
                chunk_sentece=Chunk(contenido=sentence,metadata=chapter["file_name"])
                chunks.append(chunk_sentece)

            for table_summary in table_summaries:
                chunk_table=Chunk(contenido=table_summary,metadata=chapter["file_name"])
                chunks.append(chunk_table)

        chunks_dict = [chunk._asdict() for chunk in chunks]
        with open(f"{self.output_path}+_{name_file}__chunked.json", "w",encoding='utf-8') as f:
            json.dump(chunks_dict, f)

        return chunks
