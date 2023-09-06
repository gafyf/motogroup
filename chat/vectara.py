from langchain.embeddings import FakeEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Vectara
from langchain.document_loaders import TextLoader
from django.shortcuts import render
# from openai import Completion
import tempfile
import urllib.request
import openai
from decouple import config


OPENAI_API_KEY = config('OPENAI_API_KEY')
VECTARA_CUSTOMER_ID = config('VECTARA_CUSTOMER_ID')
VECTARA_CORPUS_ID = config('VECTARA_CORPUS_ID')
VECTARA_API_KEY = config('VECTARA_API_KEY')



def chat(request):

    loader = TextLoader("C:/Users/39327/Downloads/402-Contratto%20Octo.pdf")
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    vectara = Vectara.from_documents(
        docs,
        embedding=FakeEmbeddings(size=768),
        doc_metadata={"speech": "state-of-the-union"},
    )

    query = "qualli sono ERVIZI OGGETTO DEL CONTRATTO?"
    found_docs = vectara.similarity_search(
        query, n_sentence_context=0, filter="doc.speech = 'state-of-the-union'"
    )

    print(found_docs[0].page_content)

    urls = [
        [
            "https://www.gilderlehrman.org/sites/default/files/inline-pdfs/king.dreamspeech.excerpts.pdf",
            "I-have-a-dream",
        ],
        [
            "https://www.parkwayschools.net/cms/lib/MO01931486/Centricity/Domain/1578/Churchill_Beaches_Speech.pdf",
            "we shall fight on the beaches",
        ],
    ]
    files_list = []
    for url, _ in urls:
        name = tempfile.NamedTemporaryFile().name
        urllib.request.urlretrieve(url, name)
        files_list.append(name)

    docsearch: Vectara = Vectara.from_files(
        files=files_list,
        embedding=FakeEmbeddings(size=768),
        metadatas=[{"url": url, "speech": title} for url, title in urls],
    )

    
        

    return render(request, 'chat/chat.html')
    
