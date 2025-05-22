from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random

# Create your views here.
def home(request):
    '''func to respond to home request'''
    
    response_text = f'''
    <html>
    <h1>Hello, world!</h1>
    the current time is {time.ctime()}.
    </html
    '''

    return HttpResponse(response_text)

def home_page(request):
    '''respond to the url '', delegate work to a template'''

    template_name = 'hw/home.html'
    # create dict of context variables
    context = {
        "time": time.ctime(),
        "letter1": chr(random.randint(65,90)),
        "letter2": chr(random.randint(65,90)),
        "number": random.randint(1,10),

    }

    return render(request, template_name, context)

def about(request):
    '''respond to the url '', delegate work to a template'''

    template_name = 'hw/about.html'
    # create dict of context variables
    context = {
        "time": time.ctime(),
        "letter1": chr(random.randint(65,90)),
        "letter2": chr(random.randint(65,90)),
        "number": random.randint(1,10),

    }

    return render(request, template_name, context)
