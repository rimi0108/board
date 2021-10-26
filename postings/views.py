import json
from json.decoder import JSONDecodeError

from django.http.response import JsonResponse 
from django.views         import View
from django.core.paginator import Paginator, EmptyPage

from utils           import log_in_confirm
from users.models    import User
from postings.models import Posting

class UserPostView(View):
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
    
    def get(self, request, user_id):
        
        if not Posting.objects.filter(user_id=user_id).exists():
            return JsonResponse({'message':'POST_DOES_NOT_EXISTS'}, status=400)
        
        user = User.objects.get(id=user_id)
        
        all_posts = Posting.objects.filter(user_id=user_id)
        
        paginator = Paginator(all_posts, 4)
    
        page_number = request.GET.get('page', 1)
        
        try:
            posts = paginator.page(page_number)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
        
        results = [{
            'id'        : post.id,
            'content'   : post.content,
            'image_url' : post.image_url,
            'user_name' : user.name
        } for post in posts]
        
        return JsonResponse({'MY_POST_LIST' : results, 'page':page_number}, status=200)    
    
class PostView(View):
    def get(self, request):
        all_posts = Posting.objects.all().order_by('id')

        paginator = Paginator(all_posts, 4)
        
        page_number = request.GET.get('page', 1)
        
        try:
            posts = paginator.page(page_number)
        except EmptyPage:
                posts = paginator.page(paginator.num_pages)

        results = [{
            'id'        : post.id,
            'content'   : post.content,
            'image_url' : post.image_url,
            'user_name' : post.user_id.name
        } for post in posts]

        return JsonResponse({'POST_LIST' : results,'page': page_number}, status=200)
    
class PostModifyView(View):
    @log_in_confirm
    def get(self, request, post_id):     
        
        if not Posting.objects.filter(id=post_id, user_id=request.user).exists():
            return JsonResponse({'message':'NO_PERMISSION_TO_UPDATE'}, status=400)
        
        post = Posting.objects.get(id=post_id, user_id=request.user)
        
        content = request.GET.get('content', '')
        post.content = content
        image_url = request.GET.get('image_url', '')
        post.image_url = image_url
        post.save()
        
        return JsonResponse({'message':'UPDATE_SUCCESS'}, status=201)
  
    @log_in_confirm
    def delete(self, request, post_id):
        
        if not Posting.objects.filter(id=post_id, user_id=request.user).exists():
             return JsonResponse({'message':'NO_PERMISSION_TO_DELETE'}, status=400)
        
        Posting.objects.get(id=post_id, user_id=request.user).delete()
        
        return JsonResponse({'message':'DELETE_SUCCESS'}, status=200)
        