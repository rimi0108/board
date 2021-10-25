import json
from json.decoder import JSONDecodeError

from django.http.response import JsonResponse 
from django.views         import View

from utils           import log_in_confirm
from users.models    import User
from postings.models import Posting

class PostingView(View):
    @log_in_confirm
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            user = request.user
            
            content = data['content']
            
            if not content:
                return JsonResponse({'message':'EMPTY_CONTENT'}, status=400)
            
            Posting.objects.create(
                content   = content,
                image_url = data['image_url'],
                user_id   = user
            )
            
            return JsonResponse({'message':'POSTING_SUCCESS'}, status=201)
        
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)