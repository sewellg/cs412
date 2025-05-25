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
    '''responds to url and delegates to main template'''
    template_name = 'restaurant/main.html'

    context = {
        'time': time.ctime(),
    }

    return render(request, template_name, context)

def restaurant_main(request):
    '''responds to url and delegates to main template'''

    template_name = 'restaurant/main.html'

    context = {
        'time': time.ctime(),
    }

    return render(request, template_name, context)

def order(request):
    '''responds to url and delegates to order template'''


    template_name = 'restaurant/order.html'

    context = {
    "botd": random.choice(daily_special),
    'time': time.ctime(),
    }

    return render(request, template_name, context)

def confirmation(request):
    '''responds to url and delegates to confirmation template'''


    template_name = 'restaurant/confirmation.html'
    print(request.POST)
    currenttime = time.time()
    expectedtime = currenttime + (random.randint(30,60) * 60)
    # calculates time by adding a random number of minutes from 30-60.
    # multiply by 60 to get seconds in order to work with time func
    order = []
    total = 0

    if request.POST:
        # function of this if loop is to see if each given element was selected 
        # by the user or not to determine their order

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
                # dont want duplicate fry orders
            order += ['Cheese Fries']
            total += 4.99

        if 'chili_cheese_fries' in request.POST:
            if 'Fries' in order:
                order.remove('Fries')
                total -= 3.99
                # dont want duplicate fry orders
            order += ['Chili Cheese Fries']
            total += 5.99

        if 'drink' in request.POST:
            order += ['Soft Drink']
            total += 1.99

        if 'botd' in request.POST:
            order += ['Burger of the Day']
            total += 7.99

        special = request.POST['special'] # did customer order a burger of the day?
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
            'time': time.ctime(),
        }

    return render(request, template_name, context)