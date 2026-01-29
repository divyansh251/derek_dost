
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from .models import ChatSession
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENROUTER_API_KEY
)

def home(request):
    chats = ChatSession.objects.order_by("-created_at")[:10]
    return render(request, "assistant/index.html", {"chats": chats})


def ask_ai(request):
    question = request.GET.get("q")

    if not question:
        return JsonResponse({"error": "Empty query"}, status=400)
    #print("Question Recieved", question)

    history = ChatSession.objects.order_by("-created_at")[:5]

    messages = [
        {
            "role": "system",
            "content": "You are a professional software engineer AI that writes clean production-ready code and explains clearly."
        }
    ]

    for chat in reversed(history):
        messages.append({"role": "user", "content": chat.user_query})
        messages.append({"role": "assistant", "content": chat.ai_response})

    messages.append({"role": "user", "content": question})

    completion = client.chat.completions.create(
        model="tngtech/deepseek-r1t2-chimera:free",
        messages=messages,
        extra_headers={
            "HTTP-Referer": "http://localhost",
            "X-Title": "Django AI Assistant"
        }
    )

    answer = completion.choices[0].message.content

    ChatSession.objects.create(
        user_query=question,
        ai_response=answer
    )
    
    #print("Answer got",answer)

    return JsonResponse({"answer": answer})
# Create your views here.
