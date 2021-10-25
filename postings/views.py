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
    
    @log_in_confirm
    def get(self, request):
        user = request.user
        
        if not Posting.objects.filter(user_id=user.id).exists():
            return JsonResponse({'message':'POST_DOES_NOT_EXISTS'}, status=400)
        
        posts = Posting.objects.filter(user_id=user.id)
        
        results = [{
            'id'        : post.id,
            'content'   : post.content,
            'image_url' : post.image_url,
            'user_name' : user.name
        } for post in posts]
        
        return JsonResponse({'MY_POST_LIST' : results}, status=200)
        