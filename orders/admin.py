from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html
from .models import Order, OrderItem, Meal
from .tasks import status_change_notification
import xlsxwriter
import datetime


class OrderItemInline(admin.TabularInline):
    model = OrderItem


# ---------------------------- EXPORT XLSX ----------------------------

def export_to_xlsx(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    date_time_obj = datetime.datetime.now()
    timestamp = date_time_obj.strftime("%d-%b-%Y")
    content_disposition = f'attachment; filename=orders_{timestamp}.xlsx'

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = content_disposition

    workbook = xlsxwriter.Workbook(response, {'in_memory': True})
    worksheet = workbook.add_worksheet()

    fields = [field for field in opts.get_fields() if not field.one_to_many]
    header_list = [field.name for field in fields]

    meals = Meal.objects.all()
    for meal in meals:
        header_list.append(f'{meal.name} qty')
        header_list.append(f'{meal.name} price')

    header_list.append('order_price_total')

    # Header row
    for column, item in enumerate(header_list):
        worksheet.write(0, column, item)

    # Data rows
    for row, obj in enumerate(queryset):
        meal_tracker = {meal.name: {'qty': 0, 'price': 0} for meal in meals}

        order_items = obj.items.all()
        for item in order_items:
            meal_tracker[item.meal.name]['qty'] = item.quantity
            meal_tracker[item.meal.name]['price'] = item.price

        data_row = []
        order_price_total = 0

        for field in fields:
            value = getattr(obj, field.name)

            if field.name == 'transport_cost':
                order_price_total += value

            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')

            data_row.append(value)

        for meal in meal_tracker:
            data_row.append(meal_tracker[meal]['qty'])
            data_row.append(meal_tracker[meal]['price'])
            order_price_total += (
                meal_tracker[meal]['qty'] * meal_tracker[meal]['price']
            )

        data_row.append(order_price_total)

        for column, item in enumerate(data_row):
            worksheet.write(row + 1, column, item)

    workbook.close()
    return response


export_to_xlsx.short_description = 'Export selected orders to XLSX'


# ---------------------------- PDF LINK ----------------------------

def order_pdf(obj):
    url = reverse('orders:invoice_pdf', args=[obj.id])
    return format_html('<a href="{}" target="_blank">PDF</a>', url)


order_pdf.short_description = 'Invoice'


# ---------------------------- STATUS ACTIONS ----------------------------

def status_change(queryset, status):
    for order in queryset:
        order.status = status
        order.save()
        status_change_notification.delay(order.id)


def status_processing(modeladmin, request, queryset):
    queryset.update(status="processing")


status_processing.short_description = "Mark selected orders as Processing"


def status_ready_for_pickup(modeladmin, request, queryset):
    queryset.update(status="ready_for_pickup")


status_ready_for_pickup.short_description = "Mark selected orders as Ready for Pickup"


def status_shipped(modeladmin, request, queryset):
    queryset.update(status="shipped")


status_shipped.short_description = "Mark selected orders as Shipped"


def status_completed(modeladmin, request, queryset):
    status_change(queryset, 'Completed')


status_completed.short_description = "Mark selected orders as Completed"


# ---------------------------- ORDER ADMIN ----------------------------

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'first_name', 'last_name', 'email',
        'address', 'postal_code', 'city',
        'transport', 'created', 'status', order_pdf,
    ]

    list_filter = ['created', 'updated']
    inlines = [OrderItemInline]

    actions = [
        export_to_xlsx,
        status_processing,
        status_ready_for_pickup,
        status_shipped,
        status_completed,
    ]
