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
    currenttime = time.time()
    expectedtime = currenttime + (random.randint(30,60) * 60)

    order = []
    total = 0

    if request.POST:

        if 'hamburger' in request.POST:
            order += ['Hamburger']
            total += 4.99
        if 'cheeseburger' in request.POST:
            order += ['Cheeseburger']
            total += 5.99
        if 'fries' in request.POST:
            order += ['Fries']
            total += 3.99
        if 'cheese_fries' in request.POST:
            if 'Fries' in order:
                order.remove('Fries')
                total -= 3.99
            order += ['Cheese Fries']
            total += 4.99
        if 'chili_cheese_fries' in request.POST:
            if 'Fries' in order:
                order.remove('Fries')
                total -= 3.99
            order += ['Chili Cheese Fries']
            total += 5.99
        if 'drink' in request.POST:
            order += ['Soft Drink']
            total += 1.99
        if 'botd' in request.POST:
            order += ['Burger of the Day']
            total += 7.99

        special = request.POST['special']
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']


        context = {
            'order': order,
            'total': total,
            'special': special,
            'name': name,
            'phone': phone,
            'email': email,
            'expectedtime': time.ctime(expectedtime),
        }

    return render(request, template_name, context)