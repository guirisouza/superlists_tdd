from django.shortcuts import render, redirect
from .models import ItemModel
from django.http import HttpResponse

# Create your views here.

def home_page(request):
    if request.method == "POST":
        new_item_text = request.POST.get('item_text', '')
        ItemModel.objects.create(text=new_item_text)

        return redirect('/')


    items = ItemModel.objects.all()
    return render(request, 'home.html', {'items': items})
