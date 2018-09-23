from django.http import HttpResponse
from django.http import HttpResponseRedirect
def index(request):
    return HttpResponse("index")

def favicon(request):
    image_data = open('5ba7145ad390f.32px.ico', 'rb').read()
    return HttpResponse(image_data, content_type="image/png")