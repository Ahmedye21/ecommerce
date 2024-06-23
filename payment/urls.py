from django.urls import path
from . import views
app_name = 'payment'
urlpatterns = [
    path('add_pay_info/', views.add_pay_info, name='add_pay_info'),
    path('payment/', views.payment, name='payment'),
    path('payment_success/', views.payment_success, name='payment_success'),

]