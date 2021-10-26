from django.urls import path

from postings.views import UserPostView, PostView, PostModifyView
urlpatterns = [ 
    path('post', UserPostView.as_view()),
    path('post/<int:user_id>', UserPostView.as_view()),
    path('posts', PostView.as_view()),
    path('update/<int:post_id>', PostModifyView.as_view()),
    path('delete/<int:post_id>', PostModifyView.as_view())
] 