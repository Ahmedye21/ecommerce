from django.shortcuts import render, redirect , HttpResponse , get_object_or_404
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.contrib.auth.decorators import login_required
from item.models import Item , Category , Purchase

def index(request):
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)
    context = {
        'categories': categories,
        'items': items,
    }
    return render(request, 'core/index.html', context)

def Category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    items = Item.objects.filter(category=category , is_sold=False )
    context = {
        'category': category,
        'items': items,
    }
    return render(request, 'core/category.html', context)



def signup(request):
    if request.method == "POST":
        uname   = request.POST.get('username')
        email   = request.POST.get('email')
        pass1   = request.POST.get('password1')
        pass2   = request.POST.get('password2')
        if pass1!=pass2:
            return HttpResponse("Your password and confrom password are not Same!!")
        else:

            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('core:login')
    return render(request, 'core/signup.html')
def my_login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request,username=username,password=pass1)
        if user is not None:
            login(request,user)
            return redirect('core:index')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'core/login.html')
@login_required
def profile(request):
    user                            = request.user
    items                           = Item.objects.filter(created_by=user)
    sold_items                      = items.filter(is_sold=True)
    unsold_items                    = items.filter(is_sold=False)
    money_gained                    = sold_items.aggregate(total=Sum('price'))['total'] or 0.0
    money_spent_on_purchases        = Purchase.objects.filter(buyer=user).aggregate(total=Sum('price'))['total'] or 0.0
    money_u_have                    = money_gained - money_spent_on_purchases
    


    
    context = {
        'user': user,
        'items': unsold_items,
        'sold_items': sold_items,
        'money_gained': money_gained,
        'total_items_listed': items.count(),
        'total_items_sold': sold_items.count(),
        'money_u_have': money_u_have,
    }
    
    return render(request, 'core/profile.html', context)

@login_required
def user_logout(request):
    logout(request)
    return redirect("core:login")
