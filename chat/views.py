from langchain.vectorstores import Vectara
from django.shortcuts import render
from .models import Message
from account.models import Profile
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


vectara = Vectara(
    vectara_customer_id=settings.VECTARA_CUSTOMER_ID,
    vectara_corpus_id=settings.VECTARA_CORPUS_ID,
    vectara_api_key=settings.VECTARA_API_KEY
)

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
