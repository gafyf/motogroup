from langchain.vectorstores import Vectara
from django.shortcuts import render, redirect
from decouple import config
from .models import Message
from account.models import Profile
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse , HttpResponse
from django.views.decorators.csrf import csrf_exempt

# from langchain.document_loaders import PyPDFLoader, TextLoader
# from langchain.llms import OpenAI
# from langchain.text_splitter import CharacterTextSplitter
# from langchain.chains import RetrievalQA
# from langchain.embeddings import FakeEmbeddings


OPENAI_API_KEY = config('OPENAI_API_KEY')
VECTARA_CUSTOMER_ID = config('VECTARA_CUSTOMER_ID')
VECTARA_CORPUS_ID = config('VECTARA_CORPUS_ID')
VECTARA_API_KEY = config('VECTARA_API_KEY')

vectara = Vectara(
    vectara_customer_id=VECTARA_CUSTOMER_ID,
    vectara_corpus_id=VECTARA_CORPUS_ID,
    vectara_api_key=VECTARA_API_KEY
)

# query = "on a sportster xl1200t, how to disassembly and assembly the bulb rear turn signal ?"
# found_docs = vectara.similarity_search(query)
# print('found_docs', found_docs)

# # Access the content of the first document
# document = found_docs[0].page_content
# print('document', document)
# for document in found_docs:
#     document_content = document.page_content

# # Do something with the document content
#     print('document_content', document_content)



@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = {'Message': message}
        found_docs = vectara.similarity_search(message)
        document = found_docs[0].page_content
        for document in found_docs:
            document_content = document.page_content
        print(document_content)
        profile = Profile.objects.get(user=request.user)
        messages = Message.objects.filter(profile=profile)
        date = []
        for m in messages:
            date_time = m.date.strftime("%H:%M:%S")
            date.append({'id':m.id,'message':m.message,'answer':m.answer, 'date':date_time,'user':m.profile})
        context = {
            'date': date,
        }
        response.update({'r':str(document_content)})
        return JsonResponse(response)


@login_required
def chat(request):
    template = 'chat/chat.html'
    response = render(request, template)
    return response

# def send(request):
#     message = request.POST['message']
#     answer = request.POST['answer']
#     username = request.user.profile

#     new_message = Message.objects.create(message=message, answer=answer, profile=username)
#     new_message.save()
#     return HttpResponse('Message sent successfully')



# Create your views here.

# url = "https://www.gilderlehrman.org/sites/default/files/inline-pdfs/king.dreamspeech.excerpts.pdf"

# response = requests.get(url)
# response.raise_for_status()  # Check if the request was successful

# files = {
#     "file": (
#         "king.dreamspeech.excerpts.pdf",
#         response.content,
#         "application/pdf"
#     )
# }
# print('files', files)

# loader = PyPDFLoader("C:/Users/39327/Downloads/402-Contratto_Octo.pdf")
# documents = loader.load()
# text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
# docs = text_splitter.split_documents(documents)

# files = {"file": ("Contratto_Octo.pdf", open("C:/Users/39327/Downloads/402-Contratto_Octo.pdf", "rb"), "application/pdf")}
# print('files', files)
# url = "https://api.vectara.io/v1/upload"

# headers = {
#   'Content-Type': 'multipart/form-data',
#   'Accept': 'application/json',
#   'x-api-key': VECTARA_API_KEY
# }

# response = requests.request("POST", url, headers=headers, files=files)

# print(response.text)

# def chat(request):

#     loader = PyPDFLoader("C:/Users/39327/Downloads/402-Contratto_Octo.pdf")
#     pages = loader.load_and_split()
#     print('pages', pages)

#     vectara = Vectara.from_documents(
#         pages,
#         embedding=FakeEmbeddings(size=768),
#         doc_metadata={"contratto": "contratto-abbonamento"},
#         vectara_customer_id=VECTARA_CUSTOMER_ID,
#         vectara_corpus_id=VECTARA_CORPUS_ID,
#         vectara_api_key=VECTARA_API_KEY,
#     )
#     query = "qualle sono le condizioni di abbonamento?"

    
#     found_docs = vectara.similarity_search(
#         query, n_sentence_context=0, filter="doc.contratto = 'contratto-abbonamento'"
#     )
#     print('found_docs', found_docs)

#     return render(request, 'chat/chat.html', {'query': query, 'found_docs': found_docs, 'pages': pages})
    
