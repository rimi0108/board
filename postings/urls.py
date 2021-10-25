from django.urls import path

from postings.views import UserPostView, PostView

urlpatterns = [ 
    path('/<int:user_id>', UserPostView.as_view()),
    path('', PostView.as_view())
] 