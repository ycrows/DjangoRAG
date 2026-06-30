from django.http import HttpResponse
from django.template import loader
from .models import Member

#tut
from rag.rag_chat_with_bot import chat_with_bot
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect


def members(request):
  mymembers = Member.objects.all().values()
  template = loader.get_template('all_members.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))

def details(request, id):
  mymember = Member.objects.get(id=id)
  template = loader.get_template('details.html')
  context = {
    'mymember': mymember,
  }
  return HttpResponse(template.render(context, request))

# this runs when there's no subpage
def home(request): 
  mymembers = Member.objects.all().values()
  template = loader.get_template('myfirst.html')
  context = {
    'mymembers': mymembers,
  }
  return HttpResponse(template.render(context, request))

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        response = chat_with_bot(user_message)
        return JsonResponse({'message': response})
    return render(request, 'chat.html')