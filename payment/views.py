from django.shortcuts import render, redirect, get_object_or_404
from .models import pay_info
from django.utils.timezone import now
def add_pay_info(request):
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
                'date': 'now()',
            })

        try:
            pay_info_obj = pay_info.objects.create(
                name=name,
                email=email,
                phone=phone,
                location=location,
                state=state,
                date=now(),
            )
        except Exception as e:
            return render(request, 'payment/add_pay_info.html', {
                'error': f'Error occurred: {str(e)}',
                'name': name,
                'email': email,
                'phone': phone,
                'location': location,
                'state': state,
                'date': 'now()',
            })

        return redirect('payment:card')

    return render(request, 'payment/add_pay_info.html')


def payment(request):
    return render(request, 'payment/card.html')

def payment_success(request):
    return render(request, 'payment/order-confirmation.html')
