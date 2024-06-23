from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404 , redirect
from django.contrib.auth.models import User
from .models import Item  , Category


def item_detail(request, pk):
    item                        = get_object_or_404(Item, pk=pk)
    categories                  = Category.objects.all() 
    related_items               = Item.objects.filter(category=item.category).exclude(pk=item.pk)[:3]
    show_delete_button          = False
    show_sold_button            = False
    if request.user             == item.created_by:
        show_delete_button      = True
        if not item.is_sold:
            show_sold_button    = True

    user = request.user
    is_owner = item.created_by == user

    return render(request, 'item/item.html', {
        'item': item,
        'categories': categories,
        'is_owner': is_owner,
        'related_items': related_items,
        'show_delete_button': show_delete_button,
        'show_sold_button': show_sold_button,
    })




@login_required
def mark_as_sold(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.user == item.created_by and request.method == 'POST':
        item.mark_as_sold()
    return redirect('item:item', pk=pk)



@login_required
def add_item(request):
    if request.method   == 'POST':
        name            = request.POST['name']
        price           = request.POST['price']
        category_id     = request.POST['category']
        description     = request.POST['description']
        image           = request.FILES.get('image')



        if not name or not price or not category_id:
            return render(request, 'add_item.html', {
                'categories': Category.objects.all(),
                'error': 'All fields except image are required.'
            })

        try:
            price = float(price)
        except ValueError:
            return render(request, 'add_item.html', {
                'categories': Category.objects.all(),
                'error': 'Invalid price format.'
            })

        category = get_object_or_404(Category, pk=category_id)

        item        = Item.objects.create(
            name        =name,
            description = description,
            price       =price,
            category    =category,
            image       =image,
            created_by  =request.user
        )
        return redirect('item:item', pk=item.id)
    categories = Category.objects.all()
    return render(request, 'item/add_item.html', {'categories': categories})

@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.user == item.created_by:
        if request.method == 'POST':
            item.delete()
            return redirect('core:index')
    return redirect('item:item', pk=pk)
def search_items(request):
    query = request.GET.get('q')
    items = Item.objects.filter(name__icontains=query) if query else []
    categories = Category.objects.all()
    return render(request, 'item/search_results.html', {'items': items, 'query': query , 'categories': categories})