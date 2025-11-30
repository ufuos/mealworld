from django.shortcuts import render, get_object_or_404, redirect
from decimal import Decimal

# Celery task
from .tasks import order_created

# --- Stripe Added ---
from django.conf import settings
import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
# ---------------------

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint

from .models import OrderItem, Order
from .forms import OrderCreateForm
from listings.models import Meal
from cart.views import get_cart, cart_clear


def order_detail(request, order_id):
    order = Order.objects.get(pk=order_id)
    return render(
        request,
        'order_detail.html',
        {'order': order}
    )


def order_create(request):
    cart = get_cart(request)
    cart_qty = sum(item['quantity'] for item in cart.values())
    transport_cost = round((3.99 + (cart_qty // 10) * 1.5), 2)

    if request.method == 'POST':
        order_form = OrderCreateForm(request.POST)

        if order_form.is_valid():
            cf = order_form.cleaned_data
            transport = cf['transport']

            if transport == 'Recipient pickup':
                transport_cost = 0

            order = order_form.save(commit=False)

            if request.user.is_authenticated:
                order.user = request.user

            order.transport_cost = Decimal(transport_cost)
            order.save()

            # Create order items
            meal_ids = cart.keys()
            meals = Meal.objects.filter(id__in=meal_ids)

            for meal in meals:
                cart_item = cart[str(meal.id)]
                OrderItem.objects.create(
                    order=order,
                    meal=meal,
                    price=cart_item['price'],
                    quantity=cart_item['quantity']
                )

            # ----------------------
            # Stripe Payment Section
            # ----------------------
            customer = stripe.Customer.create(
                email=cf['email'],
                source=request.POST.get('stripeToken')
            )

            stripe.Charge.create(
                customer=customer,
                amount=int(order.get_total_cost() * 100),  # cents
                currency='usd',
                description=f"Order {order.id}"
            )
            # ----------------------

            cart_clear(request)

            order_created.delay(order.id)

            return render(
                request,
                'order_created.html',
                {'order': order}
            )

    else:
        # Prefill form if logged in
        if request.user.is_authenticated:
            initial_data = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'telephone': request.user.profile.phone_number,
                'address': request.user.profile.address,
                'postal_code': request.user.profile.postal_code,
                'city': request.user.profile.city,
                'country': request.user.profile.country,
            }
            order_form = OrderCreateForm(initial=initial_data)
        else:
            order_form = OrderCreateForm()

    return render(
        request,
        'order_create.html',
        {
            'cart': cart,
            'order_form': order_form,
            'transport_cost': transport_cost
        }
    )


# ----------------------------------------------------
# PDF Invoice View
# ----------------------------------------------------

def invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'

    html = render_to_string('pdf.html', {'order': order})
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + '/css/pdf.css')]

    weasyprint.HTML(string=html).write_pdf(
        response,
        stylesheets=stylesheets
    )

    return response
