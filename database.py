import sys
import array
import time
import os
from dotenv import load_dotenv

import oracledb
from langchain_community.vectorstores import oraclevs
from langchain_community.vectorstores.oraclevs import OracleVS

from langchain_community.vectorstores.utils import DistanceStrategy
from langchain_core.documents import BaseDocumentTransformer, Document

from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import (
    Language,
    RecursiveCharacterTextSplitter,
)
from langchain_upstage import UpstageEmbeddings
import warnings
from langchain_upstage import UpstageLayoutAnalysisLoader

class Database:
    def __init__(self):
        warnings.filterwarnings("ignore")
        load_dotenv()
        
        username=os.environ["DB_USER"]
        password=os.environ["DB_PASSWORD"]
        dsn=os.environ["DSN"]

        self.con = oracledb.connect(user=username, password=password, dsn=dsn)
        self.embeddings = UpstageEmbeddings(model="solar-embedding-1-large")
        print("Connection successful!")
    
    def make_docs_from_pdf(self):
        file_path = "./oracle-database-23ai-new-features-guide.pdf"
        layzer = UpstageLayoutAnalysisLoader(file_path, split="page")
        docs = layzer.load()
        text_splitter = RecursiveCharacterTextSplitter.from_language(
            chunk_size=1500, chunk_overlap=200, language=Language.HTML
        )
        return text_splitter.split_documents(docs)

    def load_embedding(self, docs = "", table_name = "text_embeddings"):
        self.knowledge_base = OracleVS.from_documents(docs, self.embeddings, client=self.con, 
                                                table_name=table_name, 
                                                distance_strategy=DistanceStrategy.DOT_PRODUCT)
    
    def set_vector_store(self, table_name = "text_embeddings"):
        self.vector_store = OracleVS(client=self.con, 
                        embedding_function=self.embeddings, 
                        table_name=table_name, 
                        distance_strategy=DistanceStrategy.DOT_PRODUCT)
    
    def get_chunks(self, question):
        vector_store = self.vector_store
        result_chunks=vector_store.similarity_search(query = question, k = 10)
        return result_chunks

    def get_retriever(self):
        vector_store = self.vector_store
        retriever = vector_store.as_retriever()
        return retriever
    
    def create_index(self, idx_name = "ivf_idx1", idx_type = "IVF"):
        oraclevs.create_index(
            client=self.con,
            vector_store=self.vector_store,
            params={
                "idx_name": idx_name,
                "idx_type": idx_type,
            },
        )
    

if __name__ == "__main__":
    database = Database()
    # docs = database.make_docs_from_pdf()
    # database.load_embedding(docs)

    database.set_vector_store()

    question = "강릉"
    result_chunks = database.get_chunks(question)
    database.create_index()
    print(result_chunks)

