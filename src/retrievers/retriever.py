from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.chains import MapReduceDocumentsChain, ReduceDocumentsChain
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
import os
import logging

logger = logging.getLogger(__name__)


class Retriever:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo")

    def process_query(self, list_documents: str, enhanced=True, **kwargs) -> str:
        """
        Process the query using the defined retriever mechanims naive and advanced using summarization for the context.
        """
        context = """You are a food safety officer seeking detailed information about food safety regulations. You can only use the  {context} to answer 
                     answer the following question {question} Reply with N/A if the context is not relevant to the question.
                     Always answer in spanish"""
        if enhanced:
            content_summarization = self.summarization(list_documents)
            template_sumarrization = """You are a food safety officer seeking detailed information about food safety regulations.
            Taking into account the summaries of the documents {content}, please answer the following question: {question} if Reply with N/A if the context is not relevant to the question.
            For the summaries provided don't forget to include the reference to the document that supports each theme.
            Answer should always be in spanish.
            """
            prompt_summarization = ChatPromptTemplate.from_template(
                template_sumarrization
            )
            prompt_summarization = prompt_summarization.invoke(
                input={"content": content_summarization, "question": kwargs["question"]}
            )
            summary_method_answer = self.llm.invoke(prompt_summarization).content

        # Process documents  extract

        prompt = ChatPromptTemplate.from_template(context)
        prompt = prompt.invoke(
            input={"context": kwargs["context"], "question": kwargs["question"]}
        )

        content_naive = self.llm.invoke(prompt).content
        return (content_naive, summary_method_answer)

    def summarization(self, retrieved_queries: str) -> str:
        """
        Summarize the text using the LLM
        """
        map_template = """The following is a set of documents
                            {docs}
                        Based on this list of docs, please identify the main themes
                        inclue all the content of the documents in your answer
                        Taking into account the metadata of each document don't forget to include the reference to the document that supports each theme.
                        Helpful Answer:"""
        map_prompt = ChatPromptTemplate.from_template(map_template)
        map_chain = LLMChain(llm=self.llm, prompt=map_prompt)

        # reduce_template = """Here is a collection of summaries:
        #                     {docs}
        #                     Please analyze these and create a final, consolidated summary that captures all the main themes and details across the provided documents. Ensure the final summary incorporates all relevant information from the documents, explicitly referencing which document supports each theme or detail. It is critical to include all the content of the relevant documents in your answer.
        #                     Provide a helpful answer."""

        # reduce_prompt = ChatPromptTemplate.from_template(reduce_template)
        # reduce_chain = LLMChain(llm=self.llm, prompt=reduce_prompt)

        # commbine_documents_chain = StuffDocumentsChain(
        #     llm_chain=reduce_chain, document_variable_name="docs"
        # )

        # reduce_documents_chain = ReduceDocumentsChain(
        #     combine_documents_chain=commbine_documents_chain,
        #     collapse_documents_chain=commbine_documents_chain,
        # )

        # map_reduce_chain = MapReduceDocumentsChain(
        #     llm_chain=map_chain,
        #     reduce_documents_chain=reduce_documents_chain,
        #     document_variable_name="docs",
        #     return_intermediate_steps=False,
        # )

        answer = map_chain.invoke(retrieved_queries)
        return answer
