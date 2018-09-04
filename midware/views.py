from django.http import HttpResponse

def index(request):
    return HttpResponse("index")

def favicon(request):
    return HttpResponse("")