from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from listings.models import Meal
from cart.models import Cart
from .forms import CartAddMealForm, CartAddMealForm  # make sure the form import is correct
from decimal import Decimal

# Create your views here.

def get_cart(request):
    cart = request.session.get(settings.CART_ID)
    if not cart:
        cart = request.session[settings.CART_ID] = {}
    return cart


def cart_add(request, meal_id):
    cart = get_cart(request)
    meal = get_object_or_404(Meal, id=meal_id)
    meal_id = str(meal.id)
    form = CartAddMealForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data

        # Add meal to cart if not already in cart
        if meal_id not in cart:
            cart[meal_id] = {
                'quantity': 0,
                'price': str(meal.price)
            }

        # Overwrite quantity or add to existing
        if request.POST.get('overwrite_qty'):
            cart[meal_id]['quantity'] = cd['quantity']
        else:
            cart[meal_id]['quantity'] += cd['quantity']

        request.session.modified = True
        return redirect('cart:cart_detail')


def cart_remove(request, meal_id):
    cart = get_cart(request)
    meal_id = str(meal_id)

    if meal_id in cart:
        del cart[meal_id]
        request.session.modified = True

    return redirect('cart:cart_detail')


def cart_clear(request):
    del request.session[settings.CART_ID]
    request.session.modified = True
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = get_cart(request)
    meal_ids = cart.keys()
    meals = Meal.objects.filter(id__in=meal_ids)
    temp_cart = cart.copy()

    for meal in meals:
        cart_item = temp_cart[str(meal.id)]
        cart_item['meal'] = meal
        # calculate total price first
        cart_item['total_price'] = Decimal(cart_item['price']) * cart_item['quantity']
        # assign the form separately
        cart_item['update_quantity_form'] = CartAddMealForm(initial={
            'quantity': cart_item['quantity']
        })

    cart_total_price = sum(
        item['total_price']
        for item in temp_cart.values()
    )

    return render(
        request,
        'detail.html',
        {
            'cart': temp_cart.values(),
            'cart_total_price': cart_total_price
        }
    )
