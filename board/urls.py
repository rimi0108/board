from django.urls import path, include

urlpatterns = [
    path('users', include('users.urls')),
    path('post', include('postings.urls')),
    path('posts', include('postings.urls'))
]
