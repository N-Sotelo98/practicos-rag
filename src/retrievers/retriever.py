from langchain.retrievers import SelfQueryRetriever
from langchain_community.chat_models import ChatOpenAI
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
import os
import logging

logger=logging.getLogger(__name__)

class Retriever:
    def __init__(self):
        load_dotenv()
        self.api_key =os.getenv('OPENAI_API_KEY')
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo")
        
        
    def process_query(self,**kwargs)->str:
        context = """You are a food safety officer seeking detailed information about food safety regulations. Based on the provided {context},
                     answer the following question thoroughly and accurately: {question} use only the context provided to answer the question.""" 
        prompt = ChatPromptTemplate.from_template(context)
        
        prompt=prompt.invoke(input={"context":kwargs['context'],"question":kwargs['question']})
        contenido=self.llm.invoke(prompt).content
        return contenido