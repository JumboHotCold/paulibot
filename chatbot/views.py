import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .logic import PauliBotLogic

bot = PauliBotLogic()

def index(request):
    """Renders the main chat interface."""
    return render(request, 'chatbot/index.html')

@require_POST
def chat_api(request):
    """
    API endpoint that receives JSON { "message": "..." }
    and returns JSON { "response": "..." }
    """
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        if not user_message:
            return JsonResponse({'response': "Could you please clarify your question?"})

        # Process with Bot Logic
        bot_response = bot.process_query(user_message)
        
        return JsonResponse({'response': bot_response})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
