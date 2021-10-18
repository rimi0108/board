from django.http import HttpResponse

def index(request):
    return HttpResponse("글 작성하셈")