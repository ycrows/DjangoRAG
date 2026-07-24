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
from rag.rag_create_preset import rag_create_preset
from rag.rag_get_preset import rag_get_preset

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
    presets = rag_get_preset()
    
    if request.method == 'POST':
        user_message = request.POST.get('message', '')
        user_preset = request.POST.get('preset', '')
        hidden_message = anonymizer(user_message)
        response = chat_with_bot(hidden_message, user_preset)
        return JsonResponse({'message': response})
    return render(request, 'chat/chat.html', {"presets": presets})

def base(request):
   template = loader.get_template('base.html')
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

def main(request):
    return render(request, "main.html")

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

def preset(request):
    return render(request, "chat/preset.html")

import json
def save_preset(request):
   if request.method == "POST":
      try:
        # 1. Parse the JSON data from the frontend request body
        data = json.loads(request.body)
        print(data)

        # 2. Extract the variables (optional, but good for validation)
        title = data.get('title')
        model = data.get('model')
        temperature = int(data.get('temperature'))
        top_p = int(data.get('top_p'))
        frequency_penalty = int(data.get('frequency_penalty'))
        presence_penalty = int(data.get('presence_penalty'))
        max_tokens = int(data.get('max_tokens'))

        
        stop_raw = data.get('stop_sequence')
        stop = [
            item.replace("\\n", "\n")
            for item in stop_raw.split("|")
        ]

        
        # 3. Pass the data into your saving function
        # (Or you could create a Django Model instance directly right here)
        rag_create_preset(slug=title, model=model, temperature=temperature, top_p=top_p, frequency_penalty=frequency_penalty, presence_penalty=presence_penalty, max_tokens=max_tokens, stop=stop) 

        # 4. Return the success response the JavaScript is waiting for
        return JsonResponse({'success': True})

      except json.JSONDecodeError:
          # Handles the case where the JSON is malformed
          return JsonResponse({'success': False, 'error': 'Invalid JSON data provided.'}, status=400)
      except Exception as e:
          # Handles any other errors (like database errors in your save function)
          return JsonResponse({'success': False, 'error': str(e)}, status=500)