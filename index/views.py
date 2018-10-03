from django.http import HttpResponse
from django.http import HttpResponseRedirect


def index(request):
    return HttpResponse("index")


def favicon(request):
    image_data = open('favicon.32px.ico', 'rb').read()
    return HttpResponse(image_data, content_type="image/png")
