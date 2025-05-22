from django.shortcuts import render
import time
import random

# Create your views here.

daily_special = [
    "The Can I Have Your Slaw-tograph Burger",
    "The Baby, I was Corn This Way Burger",
    "The Once Upon a Thyme Burger",
    "The Rib Long and Prosper Burger"
]

def main(request):

    template_name = 'restaurant/main.html'

    return render(request, template_name)

def restaurant_main(request):

    template_name = 'restaurant/main.html'

    return render(request, template_name)

def order(request):
    template_name = 'restaurant/order.html'

    context = {
    "botd": random.choice(daily_special),
    }

    return render(request, template_name, context)

def confirmation(request):
    template_name = 'restaurant/confirmation.html'
    print(request.POST)

    if request.POST:

        hamburger = request.POST['hamburger']
        cheeseburger = request.POST['cheeseburger']
        fries = request.POST['fries']
        drink = request.POST['drink']
        botd = request.POST['botd']

        context = {
            'order': [hamburger, cheeseburger, fries, drink, botd]
        }
