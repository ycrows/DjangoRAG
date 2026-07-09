from django.http import HttpResponse
from django.template import loader
from .models import Member

#w3s tut
from rag.rag_chat_with_bot import chat_with_bot
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect

#auth tutorial (realpython.com)
from django.contrib.auth import login
#from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.urls import reverse
from .forms import CustomUserCreationForm

from rag.anonymizer import anonymizer

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
        hidden_message = anonymizer(user_message)
        response = chat_with_bot(hidden_message)
        return JsonResponse({'message': response})
    return render(request, 'chat.html')

def main(request):
   template = loader.get_template('main.html')
   return HttpResponse(template.render())

def testing(request):
  template = loader.get_template('template.html')
  mymembers = Member.objects.all().values()
  context = {
    'fruits': ['Apple', 'Banana', 'Cherry'],
    'firstname': 'Linus',
    'mymembers' : mymembers,
    'greeting': 10,
  }
  return HttpResponse(template.render(context, request))

def dashboard(request):
    return render(request, "users/dashboard.html")

def sign_up(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/sign_up.html", {"form": form})