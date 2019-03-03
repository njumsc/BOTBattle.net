from django.http import HttpResponse
from django.http import HttpResponseRedirect

def index(request):
    return HttpResponse("index")


def favicon(request):
    image_data = open('favicon.32px.ico', 'rb').read()
    return HttpResponse(image_data, content_type="image/png")

def static(request, file):
    static_data = open('static/' + file, 'rb').read()
    extend_name = file.split('.')[-1]
    if extend_name == 'css':
        return HttpResponse(static_data, content_type='text/css')
    elif extend_name == 'js':
        return HttpResponse(static_data, content_type='text/javascript')
    else:
        return HttpResponse(static_data)
