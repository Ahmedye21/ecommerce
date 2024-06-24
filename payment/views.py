from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from .models import pay_info
from item.models import Item
from decimal import Decimal
from django.contrib.auth.decorators import login_required
@login_required
@transaction.atomic
def add_pay_info(request):
    item_id = request.GET.get('item_id')
    if not item_id:
        return render(request, 'payment/add_pay_info.html', {
            'error': 'No item selected. Please select an item.'
        })
    
    try:
        item = get_object_or_404(Item, id=item_id)
    except Item.DoesNotExist:
        return render(request, 'payment/add_pay_info.html', {
            'error': 'No item matches the given query.'
        })
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        location = request.POST.get('location')
        state = request.POST.get('state')

        if not (name and email and phone and location and state):
            return render(request, 'payment/add_pay_info.html', {
                'error': 'All fields are required.',
                'name': name,
                'email': email,
                'phone': phone,
                'location': location,
                'state': state,
                'item': item,
            })

        try:
            with transaction.atomic():
                pay_info_obj = pay_info.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    location=location,
                    state=state,
                    date=now(),
                )

                item.is_sold = True
                item.save()

                user = request.user
                item_price = Decimal(item.price) 
                user.profile.balance -= item_price
                user.profile.save()

        except Exception as e:
            return render(request, 'payment/add_pay_info.html', {
                'error': f'Error occurred: {str(e)}',
                'name': name,
                'email': email,
                'phone': phone,
                'location': location,
                'state': state,
                'item': item,
            })

        order_details = {
            'item': item,
            'name': name,
            'email': email,
            'phone': phone,
            'location': location,
            'state': state,
        }
        return render(request, 'payment/order-confirmation.html', order_details)

    return render(request, 'payment/add_pay_info.html', {'item': item})

def payment_success(request):
    return render(request, 'payment/order-confirmation.html')
