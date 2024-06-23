from django.urls import path
from . import views

app_name = 'item'

urlpatterns = [
    path('<int:pk>/', views.item_detail, name='item'),
    path('<int:pk>/delete/', views.item_delete, name='item_delete'),
    path('<int:pk>/mark-as-sold/', views.mark_as_sold, name='mark_as_sold'),
    path('add_item/', views.add_item, name='add_item'),
    path('search/', views.search_items, name='search'),
]

