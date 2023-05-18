from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone

import constants


def convert_scientificts_to_documents(list_data):
    result_list = []
    for data in list_data:
        tmp_data = data.copy()
        del tmp_data['page_content']
        doc = Document(page_content=data['page_content'],
                       metadata={**tmp_data})
        result_list.append(doc)
    return result_list


def populate(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=2000,
                                                   chunk_overlap=0)
    documents_splitted = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings(openai_api_key=constants.OPENAI_API_KEY)

    pinecone.init(
        api_key=constants.PINECONE_API_KEY,
        environment=constants.PINECONE_API_ENV,
    )

    index = pinecone.Index(constants.INDEX_NAME)
    index.delete(delete_all=True)
    Pinecone.from_documents(documents_splitted,
                            embeddings,
                            index_name=constants.INDEX_NAME)
