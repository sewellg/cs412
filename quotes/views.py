from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

import time
import random
# Create your views here.

quotes = [
        "I have an idea so smart that my head would explode if I even began to know what I was talking about.",
        "Shut up Meg.",
        "I may be an idiot, but there's one thing I'm not sir, and that is an idiot.",
    ]

imgsrc = [
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTvOplh8cRMSKxCW4ViL_hJB6qhCTfA1siHn1T4gLfnL13Sr37Qczqvu0FDYreoxiBSS-0&usqp=CAU",
    "https://preview.redd.it/are-you-the-family-guy-because-youre-peter-griffin-or-are-v0-mxuao4bg49ec1.jpeg?auto=webp&s=40439ebd83c79abef4eeb1071c605c55ced68915",
    "https://static.wikia.nocookie.net/simpsons/images/4/4a/Profile_-_Peter_Griffin.png/revision/latest/thumbnail/width/360/height/450?cb=20250307004047",
    ]

def main(request):
    '''respond to url, delegates to 'quote' template'''
    template_name = 'quotes/quote.html'

    context = {
        "time": time.ctime(),
        
        "quotes": random.choice(quotes),

        "src": random.choice(imgsrc),
    }
    return render(request, template_name, context)

def quote(request):
    '''respond to url, delegates to 'quote' template'''
    template_name = 'quotes/quote.html'

    
    context = {
        "time": time.ctime(),
        
        "quotes": random.choice(quotes),

        "src": random.choice(imgsrc),
    }
    return render(request, template_name, context)

def show_all(request):
    template_name = 'quotes/show_all.html'

    context = {
        "time": time.ctime(),
        
        "quotes": quotes,

        "src": imgsrc,
    }

    return render(request, template_name, context)

def about(request):
    '''delegates to 'about' template'''
    template_name = 'quotes/about.html'

    context = {
        "time": time.ctime(),
        
    }
    return render(request, template_name, context)