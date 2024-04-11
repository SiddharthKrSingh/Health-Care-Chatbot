# views.py
from django.shortcuts import render
from django.http import HttpResponse
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()  # Load environment variables

# Configure generative AI
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response


def chat_view(request):
    chat_history = request.session.get('chat_history', [])
    if request.method == 'POST':
        input_text = request.POST.get('input_text')
        if input_text:
            response = get_gemini_response(input_text)
            chat_history.append(("You", input_text))
            for chunk in response:
                chat_history.append(("Bot", chunk.text))
            request.session['chat_history'] = chat_history


    return render(request, 'chat.html', {'chat_history': chat_history})
