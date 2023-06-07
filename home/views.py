from django.shortcuts import render
from django.http import HttpResponse
from django.http import StreamingHttpResponse
from datetime import datetime
import time,json,random
from .aws_helper import *
from django_eventstream import send_event
# Create your views here.

def index(request):

    # Page from the theme 
    return render(request, 'pages/dashboard.html')




async def generate_random_data(request):
    """
    Generates random value between 0 and 100

    :return: String containing current timestamp (YYYY-mm-dd HH:MM:SS) and randomly generated data.
    """
    if request.META.get("HTTP_X_FORWARDED_FOR"):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        client_ip = x_forwarded_for.split(',')[0]
    elif request.META.get("REMOTE_ADDR"):
        client_ip = request.META.get('REMOTE_ADDR')
    else:
        client_ip = ""

    try:
        print("Client %s connected", client_ip)
        while True:
            json_data = json.dumps(
                client_data("client1")
            )
            yield json_data
            time.sleep(100)
    except GeneratorExit:
        print("Client %s disconnected", client_ip)

def chart_data(request):
    def event_stream():
        
        time.sleep(3)
        yield "\ndata: {}\n\n".format(next(generate_random_data(request)))
        print("hi")
    res=next(event_stream())
    return StreamingHttpResponse(res, content_type='text/event-stream')


def testing(request):
    return render(request, 'pages/dashboard.html')