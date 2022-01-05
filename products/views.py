from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.urls import reverse
import random 
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.views.generic import (FormView)
from django.views.generic.detail import SingleObjectMixin



# create random number of 15 digits for each bill
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)



def add_bill(request):
    form = CreateOrderForm(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            client = form.save()
            # print(client , type(client))
            new_bill =  Order.objects.create(
                client=client,
                transaction_id = random_with_N_digits(15)
                )
            return redirect("products:create-line", pk=new_bill.id)
    return render(request, 'pages/add_bill.html',{
        'form':form,
    })
    
    
def create_line(request,pk):
    order = Order.objects.get(pk = pk)
    lines = order.orderitem_set.all()
    form = LineForm(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            line=  form.save(commit=False)
            line.order = order
            line.save()
            return redirect("products:detail-line", pk=line.id)
        else:
            return render(request, 'partials/line_form.html',{'form':form,})    
        
    return render(request, 'partials/create_line.html',{
        'order':order,
        'lines':lines,
        'form':form,
  
    })
    
    
def create_line_form(request):
    context = {
        "form": LineForm()
    }
    return render(request, 'partials/line_form.html', context)


def update_line_form(request,pk):
    line = OrderItem.objects.get(pk = pk)
    form = LineForm(request.POST or None , instance=line)
    if request.method=="POST":
        if form.is_valid():
            line.save()
            return redirect("products:detail-line", pk=line.id)
        context = {
            "form": form,
            "line": line,
        }
    return render(request, 'partials/line_form.html', context)


def detail_line(request,pk):
    line = OrderItem.objects.get(pk = pk)
    context = {
        "line": line,
    }
    return render(request, 'partials/line_detail.html', context)


def delete_line(request,pk):
    line = OrderItem.objects.get(pk = pk)
    line.delete()
    return HttpResponse('')