from celery import shared_task
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.conf import settings
from io import BytesIO
import weasyprint
from .models import Order


@shared_task
def order_created(order_id):
    # Get the order from the database
    order = Order.objects.get(id=order_id)

    # Email subject and message
    subject = f'Order nr. {order.id}'
    message = (
        f'Dear {order.first_name},\n\n'
        f'Your order was successfully created.\n'
        f'Your order ID is {order.id}.'
    )

    # EmailMessage object
    email = EmailMessage(
        subject,
        message,
        'eshop@mealworld.store',   # updated shop email
        [order.email]
    )

    # Generate PDF
    html = render_to_string('pdf.html', {'order': order})
    out = BytesIO()

    stylesheets = [
        weasyprint.CSS(f"{settings.STATIC_ROOT}/css/pdf.css")
    ]

    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # Attach PDF to email
    email.attach(
        f'order_{order.id}.pdf',
        out.getvalue(),
        'application/pdf'
    )

    # Send email
    email.send()


@shared_task
def status_change_notification(order_id):
    # Get the order from the database
    order = Order.objects.get(id=order_id)

    # Email subject and body
    subject = f'Order nr. {order.id}'
    message = (
        f'Dear {order.first_name},\n\n'
        f'The status of your order {order.id} '
        f'has been changed to {order.status}.'
    )

    # Send the email
    mail_sent = send_mail(
        subject,
        message,
        'eshop@mealworld.store',   # updated shop email
        [order.email]
    )
    return mail_sent
