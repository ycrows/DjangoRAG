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

def myfirst(request): 
  #template = loader.get_template('myfirst.html')
  #return HttpResponse(template.render({}, request))
  return render(request, 'myfirst.html')

@csrf_exempt
def chat(request):
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        response = chat_with_bot(user_message)
        return JsonResponse({'message': response})
    return render(request, 'chat.html')

def main(request):
   template = loader.get_template('main.html')
   return HttpResponse(template.render())

def testing(request):
  template = loader.get_template('template.html')
  context = {
    'fruits': ['Apple', 'Banana', 'Cherry'],
  }
  return HttpResponse(template.render(context, request))


