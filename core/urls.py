from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<int:category_id>/', views.Category_detail, name='category_detail'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.my_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]
