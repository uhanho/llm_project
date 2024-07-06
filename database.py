import sys
import array
import time
import os
import json
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
    
    def make_docs_from_pdf(self, file_path = "./sample_docs.txt"):
        layzer = UpstageLayoutAnalysisLoader(file_path)
        docs = layzer.load()
        text_splitter = RecursiveCharacterTextSplitter.from_documents(
            docs,
            self.embeddings,
            client=self.con, 
            table_name="sample_docs2", 
            distance_strategy=DistanceStrategy.DOT_PRODUCT
        )
        return text_splitter
    
    def make_docs_from_path(self, file_path = "./sample_docs.txt"):
        with open (file_path, 'rt') as myfile:
            contents = myfile.read()
        docs = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=200).create_documents([contents])
        return docs
    
    def make_docs_from_list(self, contents):
        docs = RecursiveCharacterTextSplitter(chunk_size=400, chunk_overlap=200).create_documents(contents)
        return docs

    def make_docs(self, file_path):
        with open (file_path, 'rt') as file:
            contents = json.load(file)

        # print(contents)
        descriptions = [d['description'] for d in contents if d is not None and d['description'] is not None]
        docs = " ".join(descriptions)

        return RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=300).create_documents(docs)

    def load_embedding(self, docs = "", table_name = "sample_docs2"):
        self.knowledge_base = OracleVS.from_documents(docs, self.embeddings, client=self.con, 
                                                table_name=table_name, 
                                                distance_strategy=DistanceStrategy.DOT_PRODUCT)
    
    def set_vector_store(self, table_name = "sample_docs2"):
        self.vector_store = OracleVS(client=self.con, 
                        embedding_function=self.embeddings, 
                        table_name=table_name, 
                        distance_strategy=DistanceStrategy.DOT_PRODUCT)
    
    def get_chunks(self, question):
        vector_store = self.vector_store
        result_chunks=vector_store.similarity_search(query = question, k = 3)
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
    table_name = "blog"
    docs = database.make_docs("./jeonju_blog.json")
    # docs = database.make_docs_from_path("./sample_docs.txt")
    database.load_embedding(docs, table_name)

#     database.set_vector_store(table_name)

#     question = "부산일까 서울일까?"
#     result_chunks = database.get_chunks(question)
    
#     print(result_chunks)

