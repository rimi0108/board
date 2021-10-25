from django.urls import path

from postings.views import PostingView

urlpatterns = [ 
    path('', PostingView.as_view()),
    path('/<int:user_id>', PostingView.as_view())
] 