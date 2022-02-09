from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from django.urls import reverse
import random 
from django.db.models import Q
from django.http import JsonResponse


def home(request):
    # ps = Product.objects.all()
    # for p in ps:
    #     p.available_in_ventory = 10
    #     p.save()
    return render(request, 'pages/home.html')
    

def about(request):
    about = About.objects.first()
    return render(request, 'pages/about.html', {"about": about})
    
def about_details(request):
    about = About.objects.first()
    return render(request, 'partials/about_details.html', {"about": about})
    
def edit_about(request):
    about = About.objects.first()
    form = AboutForm(request.POST or None, instance=about)
    if request.method=="POST":
        if form.is_valid():
            form.save()
            return redirect("products:about_details");
    return render(request, 'partials/about_form.html', {"form": form})
    



def clients(request):
    search_qs = request.GET.get('search_clients', '')
    if search_qs:
        clients = Client.objects.filter(Q(name__icontains=search_qs)|
                                        Q(id__icontains=search_qs))
    else:
        clients = Client.objects.all()
    
    return render(request, 'pages/clients.html',{
        "clients": clients,
    })
    
    
def client_details(request, pk):
    client = Client.objects.get(pk = pk)
    client_bills = Order.objects.filter(client = client).order_by('-date_ordered')
    return render(request, 'pages/client_details.html',{
        'client':client,
        'client_bills':client_bills,
    })
    


def reports(request):
    products = Product.objects.all()
    inventory_products_count = 0
    for product in products:
        inventory_products_count += product.available_in_ventory
    return render(request, 'pages/reports.html',{
        'products_count':products.count(),
        "inventory_products_count":inventory_products_count,

    })
    
def all_products(request):
    
    search_qs = request.GET.get('searchname', '')
    if search_qs:
        products = Product.objects.filter(Q(name__icontains=search_qs)|
                                          Q(code__icontains=search_qs))
    else:
        products = Product.objects.all()
    return render(request, 'pages/products.html',{
        'products':products,

    })
    
def product_details(request, slug):
    product = Product.objects.get(PROslug = slug)
    return render(request, 'pages/product_details.html',{
        'product':product,
    })
    
def add_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST)
        if form.is_valid():
            myform = form.save(commit=False)
            myform.code = random_with_N_digits(6)
            myform.save()
            return redirect(reverse('products:all_products'))
    else:
        form = AddProductForm()
    return render(request, 'pages/add_product.html',{
        'form':form,
    })
    
def edit_product(request, slug):
    product = Product.objects.get(PROslug = slug)
    if request.method == "POST":
        form = AddProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect(reverse('products:product_details', kwargs={'slug':product.PROslug}))
    else:
        form = AddProductForm(instance=product)
    return render(request, 'pages/edit_product.html',{
        'form':form,
    })

def complete_bill(request,pk):
    bill = Order.objects.get(pk=pk)
    # if bill.complete !=True:
    #     items = bill.orderitem_set.all()
    #     for item in items:
    #         product = Product.objects.get(pk =item.product.id )
    #         if product.available_in_ventory >= item.qty:
    #             product.available_in_ventory -= item.qty
    #             product.save()
    bill.complete = True
    bill.save()
    return HttpResponse('')


def bills(request):
    search_qs = request.GET.get('search_bills', '')
    if search_qs:
        bills = Order.objects.filter(Q(client__name__icontains=search_qs)|
                                        Q(transaction_id__icontains=search_qs))
    else:
        bills = Order.objects.all()
    
    return render(request, 'pages/bills.html',{'bills': bills})


def bill_details(request, pk):
    bill = Order.objects.get(pk = pk)
    items = bill.orderline_set.all()
    return render(request, 'pages/bill_details.html',{
        'bill':bill,
        'items':items,
    })



# create random number of 15 digits for each bill
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)



def add_bill(request):
    form = BillUserForm(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            client = form.save()
            new_bill =  Order.objects.create(
                client=client,
                transaction_id = random_with_N_digits(15),
                remaining_atthattime = client.remaining_money,
                paid = 0,
                
                )
            return redirect("products:create-line", pk=new_bill.id)
    return render(request, 'pages/add_bill.html',{
        'form':form,
    })
    
    
def create_line(request,pk):
    order = Order.objects.get(pk = pk)
    lines = order.orderline_set.all()
    form = LineForm(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            line=  form.save(commit=False)
            founded = OrderLine.objects.filter(product = line.product,order = order).exists()
            if founded:
                return redirect("products:message")
            else:
                if order.complete == True:
                    order.complete = False
                    order.save()
                    order.client.remaining_money = order.remaining_atthattime
                    order.client.save()
                product = Product.objects.get(pk =line.product.id)
                if product.available_in_ventory >= line.qty:
                        product.available_in_ventory -= line.qty
                        product.save()
                else:
                    return render(request, 'partials/not_enough_smg.html',{'product_qty_available':line.product.available_in_ventory,}) 
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
    line = OrderLine.objects.get(pk = pk)
    bill = line.order
    old_qty = line.qty
    product = Product.objects.get(pk =line.product.id )
    form = LineForm(request.POST or None , instance=line)
    if request.method=="POST":
        if form.is_valid():
            if bill.complete == True:
                bill.complete = False
                bill.save()
                bill.client.remaining_money = bill.remaining_atthattime
                bill.client.save()
                
            myform = form.save(commit=False)
            new_qty = myform.qty
            update_value = old_qty - new_qty
            # reduce
            if update_value > 0:
                product.available_in_ventory += update_value
                product.save()
                myform.save()
            # add more
            elif update_value < 0:
                if product.available_in_ventory >= abs(update_value):
                    product.available_in_ventory -= abs(update_value)
                    product.save()
                    myform.save()
                else:
                    return render(request, 'partials/line_form.html',{'form':form,'line': line,'product_qty_available':line.product.available_in_ventory,}) 
            return redirect("products:detail-line", pk=line.id)
            
    context = {
        "form": form,
        "line": line,
    }
    return render(request, 'partials/line_form.html', context)


def detail_line(request,pk):
    line = OrderLine.objects.get(pk = pk)
    context = {
        "line": line,
    }
    return render(request, 'partials/line_detail.html', context)



def delete_line(request):
    line_id = request.GET.get("line_id")
    line = OrderLine.objects.get(id = line_id)
    order = line.order
    if order.complete == True:
        order.complete = False
        order.save()
        order.client.remaining_money = order.remaining_atthattime
        order.client.save()
    line.product.available_in_ventory += line.qty
    line.product.save()
    line.delete()
    line_founded = OrderLine.objects.filter(id = line_id).exists()
    data = {
        "line_founded":line_founded,
        "order_total":order.get_bill_total,
        
        # sum of bill total and client remaining
        "total2":float(order.get_bill_total + order.client.remaining_money) ,
        "still":float(order.get_bill_total + order.client.remaining_money) - float(order.paid) ,
        "bill_state":order.complete,
    }
    return JsonResponse(data)


def detail_client(request,pk):
    client = Client.objects.get(pk = pk)
    context = {
        "client": client,
    }
    return render(request, 'partials/client_detail.html', context)



def edit_bill_user_information(request,pk):
    bill = Order.objects.get(pk = pk)
    client = Client.objects.get(pk=bill.client.id)
    form = BillUserForm(request.POST or None, instance=client)
    if request.method=="POST":
        if form.is_valid():
            form.save()
            return redirect("products:detail-client", pk=client.id)
    return render(request, 'partials/user_bill_form.html',{
        'form':form,
        'bill':bill,
        'client':client,
        
    })
    
    
def payment(request):
    bill_id = request.GET.get("order_id")
    paid_value = request.GET.get("paid_value")
    bill = Order.objects.get(pk = bill_id)
    if bill.complete == True:
        bill.complete = False
        bill.save()
        bill.client.remaining_money = bill.remaining_atthattime
        bill.client.save()

    total2 = bill.get_bill_total + bill.client.remaining_money
    bill.paid = float(paid_value)
    bill.save()
    data = {
        "bill_paid":bill.paid,
        "bill_state":bill.complete,
        "still":float(total2) - float(bill.paid),
    }
    return JsonResponse(data)

   

def another_bill_for_client(request,pk):
    client = Client.objects.get(pk=pk)
    new_bill =  Order.objects.create(
                client=client,
                transaction_id = random_with_N_digits(15),
                 remaining_atthattime = client.remaining_money,
                 paid = 0,
                )
    return redirect("products:create-line", pk=new_bill.id)


def delete_bill(request,pk):
    bill = Order.objects.get(pk=pk)
    if bill.complete == True:
        bill.delete()
    else:
        lines = bill.orderline_set.all()
        for line in lines:
            line.product.available_in_ventory += line.qty
            line.product.save()
        bill.delete() 
    return redirect("products:bills")

def delete_bills_list(request):
    bill_id = request.GET.get("id")
    bill = Order.objects.get(id=bill_id)
    if bill.complete == True:
        bill.delete()
    else:
        lines = bill.orderline_set.all()
        for line in lines:
            line.product.available_in_ventory += line.qty
            line.product.save()
        bill.delete()
    data = {} 
    return JsonResponse(data)

def delete_product(request,pk):
    p = Product.objects.get(pk=pk)
    p.delete()
    return redirect("products:all_products")

def delete_products_list(request):
    product_id = request.GET.get("id")
    p = Product.objects.get(id=product_id)
    p.delete()
    data = {} 
    return JsonResponse(data)


def delete_client(request,pk):
    c = Client.objects.get(pk=pk)
    c.delete()
    return redirect("products:clients")


def delete_clients_list(request):
    client_id = request.GET.get("id")
    c = Client.objects.get(id=client_id)
    c.delete()
    data = {} 
    return JsonResponse(data)


def line_message(request):
    return render(request, 'partials/message.html')

def line_not_enough_message(request):
    return render(request, 'partials/not_enough_smg.html')


def autoSearch_products(request):
    q_original = request.GET.get('term')
    qs = Product.objects.filter(Q(name__icontains = q_original) | 
                                Q(code__startswith = q_original))
    if qs:
        names = []
        names+=[x.name for x in qs]
    else:
        names = ['لا توجد نتائج']
    return JsonResponse(names, safe=False)

def autosearch_bills(request):
    q_original = request.GET.get('term')
    qs = Order.objects.filter(Q(client__name__icontains=q_original)|
                                        Q(transaction_id__startswith=q_original))
    if qs:
        clients = []
        clients+=[x.transaction_id for x in qs]
    else:
        clients = ['لا توجد نتائج']
    return JsonResponse(clients, safe=False)

def autosearch_incombills(request):
    q_original = request.GET.get('term')
    qs = IncomingOrder.objects.filter(Q(seller__icontains=q_original)|
                                        Q(transaction_id__startswith=q_original))
    if qs:
        names = []
        names+=[x.transaction_id for x in qs]
    else:
        names = ['لا توجد نتائج']
    return JsonResponse(names, safe=False)



def autosearch_clients(request):
    q_original = request.GET.get('term')
    qs = Client.objects.filter(Q(name__icontains=q_original)|
                                        Q(id__icontains=q_original))
    
    
    if qs:
        name = []
        name+=[x.name for x in qs]
    else:
        name = ['لا توجد نتائج']
    return JsonResponse(name, safe=False)


 
def generate_bill(request,id):
    about = About.objects.first()
    bill = Order.objects.get(id=id)
    lines = bill.orderline_set.all() 
    return render(request, 'pages/end_bill.html', {
        'about':about,
        'bill':bill,
        'lines':lines,
    })
 

    
    
def end_bill(request):
    bill_id = request.GET.get("id")
    bill = Order.objects.get(id=bill_id)
    total2 = bill.get_bill_total + bill.remaining_atthattime
    data={
            "bill_total":total2,
            "still":bill.client.remaining_money,
        }
    if not bill.complete:
        bill.client.remaining_money = float(total2) - float(bill.paid)
        bill.client.save()
        bill.complete = True
        bill.save()
        data={
            "bill_total":total2,
            "still":bill.client.remaining_money,
        }
    return JsonResponse(data)



def live_bill_user_update(request):
    bill_id = request.GET.get("bill_id")
    bill = Order.objects.get(id = bill_id)
    data = {
        "bill_total":bill.get_bill_total,
        "bill_paid":bill.paid,
        "client_remaining":bill.remaining_atthattime,
        "bill_state":bill.complete,
        
    }
    return JsonResponse(data)






#  ************* Quiq bill functions *****************

    
def create_quiqline(request,pk):
    quiqorder = QuiqOrder.objects.get(pk = pk)
    lines = quiqorder.quiqorderline_set.all()
    form = QuiqLineForm(request.POST or None)

    if request.method=="POST":
        if quiqorder.complete == True:
            quiqorder.complete = False
            quiqorder.save()
        if form.is_valid():
            line=  form.save(commit=False)
            founded = QuiqOrderLine.objects.filter(product = line.product,quiqorder = quiqorder).exists()
            if founded:
                return redirect("products:message")
            else:
                product = Product.objects.get(pk =line.product.id)
                if product.available_in_ventory >= line.qty:
                        product.available_in_ventory -= line.qty
                        product.save()
                else:
                    return render(request, 'partials/not_enough_smg.html',{'product_qty_available':line.product.available_in_ventory,}) 
                line.quiqorder = quiqorder
                line.save()
                return redirect("products:detail_quiqline", pk=line.id)
        else:
            return render(request, 'partials/quiqline_form.html',{'form':form,})    
        
    return render(request, 'partials/create_quiqline.html',{
        'quiqorder':quiqorder,
        'lines':lines,
        'form':form,
  
    })
    
    
def detail_quiqline(request,pk):
    quiqline = QuiqOrderLine.objects.get(pk = pk)
    context = {
        "quiqline": quiqline,
    }
    return render(request, 'partials/quiqline_detail.html', context)


def create_quiqline_form(request):
    context = {
        "form": QuiqLineForm()
    }
    return render(request, 'partials/quiqline_form.html', context)


def update_quiqline(request,pk):
    line = QuiqOrderLine.objects.get(pk = pk)
    old_qty = line.qty
    product = Product.objects.get(pk =line.product.id )
    form = QuiqLineForm(request.POST or None , instance=line)

    if request.method=="POST":
        if line.quiqorder.complete == True:
            line.quiqorder.complete = False
            line.quiqorder.save()
        if form.is_valid():
            myform = form.save(commit=False)
            new_qty = myform.qty
            update_value = old_qty - new_qty
            # reduce
            if update_value > 0:
                product.available_in_ventory += update_value
                product.save()
                myform.save()
            elif update_value < 0:
                if product.available_in_ventory >= abs(update_value):
                    product.available_in_ventory -= abs(update_value)
                    product.save()
                    myform.save()
                else:
                    return render(request, 'partials/quiqline_form.html',{'form':form,'line': line,'product_qty_available':line.product.available_in_ventory,}) 
            return redirect("products:detail_quiqline", pk=line.id)
    context = {
        "form": form,
        "line": line,
    }
    return render(request, 'partials/quiqline_form.html', context)


def delete_quiqline(request):
    quiqline_id = request.GET.get("quiqline_id")
    quiqline = QuiqOrderLine.objects.get(id = quiqline_id)
    quiq_order = quiqline.quiqorder
    if quiq_order.complete == True:
        quiq_order.complete = False
        quiq_order.save()
    quiqline.product.available_in_ventory += quiqline.qty
    quiqline.product.save()
    quiqline.delete()
    quiqline_founded = OrderLine.objects.filter(id = quiqline_id).exists()
    data = {
        "quiqline_founded":quiqline_founded,
        "quiqorder_total":quiq_order.get_bill_total,
        
       
    }
    return JsonResponse(data)


def quiq_bills(request):
    search_qs = request.GET.get('search_quiqbills', '')
    if search_qs:
        quiqbills = QuiqOrder.objects.filter(transaction_id__startswith=search_qs)
    else:
        quiqbills = QuiqOrder.objects.all()
    
    return render(request, 'pages/quiqbills.html',{'quiqbills': quiqbills})


def quiqbill_details(request, pk):
    quiqbill = QuiqOrder.objects.get(pk = pk)
    items = quiqbill.quiqorderline_set.all()
    return render(request, 'pages/quiqbill_details.html',{
        'quiqbill':quiqbill,
        'items':items,
    })

    
def quiqbill_payment(request):
    quiqbill_id = request.GET.get("quiqorder_id")
    paid_value = request.GET.get("paid_value")
    quiqbill = QuiqOrder.objects.get(pk = quiqbill_id)
    if quiqbill.complete == True:
        quiqbill.complete = False
        quiqbill.save()

    quiqbill.paid = float(paid_value)
    quiqbill.save()
    data = {
        "quiqbill_paid":quiqbill.paid,
        "quiqbill_state":quiqbill.complete,
    }
    return JsonResponse(data)


def delete_quiqbill(request,pk):
    quiqbill = QuiqOrder.objects.get(pk=pk)
    if quiqbill.complete == True:
        quiqbill.delete()
    else:
        quiqlines = quiqbill.quiqorderline_set.all()
        for quiqline in quiqlines:
            quiqline.product.available_in_ventory += quiqline.qty
            quiqline.product.save() 
        quiqbill.delete()
    return redirect("products:quiqbills")

def delete_quiqbills_list(request):
    quiqbill_id = request.GET.get("id")
    quiqbill = QuiqOrder.objects.get(id=quiqbill_id)
    if quiqbill.complete == True:
        quiqbill.delete()
    else:
        quiqlines = quiqbill.quiqorderline_set.all()
        for quiqline in quiqlines:
            quiqline.product.available_in_ventory += quiqline.qty
            quiqline.product.save() 
        quiqbill.delete()
    data = {}
    return JsonResponse(data)


def add_quiqbill(request):
    quiqbill = QuiqOrder.objects.create(
        transaction_id = random_with_N_digits(15),
        paid = 0,
    )
    return redirect("products:create_quiqline", pk = quiqbill.id )


def live_quiqbill(request):
    quiqbill_id = request.GET.get("quiqbill_id")
    quiqbill = QuiqOrder.objects.get(id = quiqbill_id)
    data = {
        "quiqbill_total":quiqbill.get_bill_total,
        "quiqbill_state":quiqbill.complete,
    }
    return JsonResponse(data)


def print_quiqbill(request,pk):
    about = About.objects.first()
    quiqbill = QuiqOrder.objects.get(pk=pk)
    quiqlines = quiqbill.quiqorderline_set.all() 
    return render(request, 'pages/print_quiqbill.html', {
        'about':about,
        'quiqbill':quiqbill,
        'quiqlines':quiqlines,
    })


def end_quiqbill(request):
    quiqbill_id = request.GET.get('id')
    quiqbill = QuiqOrder.objects.get(id=quiqbill_id)
    if quiqbill.complete==False:
        quiqbill.complete= True
        quiqbill.save()
    data={}
    return JsonResponse(data)

 
    
def autosearch_quiqbills(request):
    q_original = request.GET.get('term')
    qs = QuiqOrder.objects.filter(transaction_id__startswith=q_original)
    if qs:
        quiqbills = []
        quiqbills+=[x.transaction_id for x in qs]
    else:
        quiqbills = ['لا توجد نتائج']
    return JsonResponse(quiqbills, safe=False)
    
    
def ended_products(request):
    products = Product.objects.filter(available_in_ventory=0)
    
    return render(request, 'pages/ended_products.html',{"products": products})



# ******** incoming bills *********************                 

def add_incombill(request):
    new_bill = IncomingOrder.objects.create(
        transaction_id = random_with_N_digits(15),
    )
    return redirect('products:create_incomline', pk=new_bill.id)
    
def create_incomline(request,pk):
    incomorder = IncomingOrder.objects.get(pk = pk)
    lines = incomorder.incomingorderline_set.all()
    form = IncomingLineForm(request.POST or None)

    if request.method=="POST":
        if form.is_valid():
            line=  form.save(commit=False)
            founded = IncomingOrderLine.objects.filter(product = line.product,incomingorder = incomorder).exists()
            if founded:
                return redirect("products:message")
            else:
                line.incomingorder = incomorder
                line.save()
                return redirect("products:detail_incomline", pk=line.id)
        else:
            return render(request, 'partials/incomline_form.html',{'form':form,})    
        
    return render(request, 'partials/create_incomline.html',{
        'incomorder':incomorder,
        'lines':lines,
        'form':form,
  
    })
    
    

    
def detail_incomline(request,pk):
    incomline = IncomingOrderLine.objects.get(pk = pk)
    context = {
        "incomline": incomline,
    }
    return render(request, 'partials/incomline_detail.html', context)


def incomline_form(request):
    context = {
        "form": IncomingLineForm()
    }
    return render(request, 'partials/incomline_form.html', context)


def incom_bills(request):
    search_qs = request.GET.get('search_incombills', '')
    if search_qs:
        incombills = IncomingOrder.objects.filter(transaction_id__startswith=search_qs)
    else:
        incombills = IncomingOrder.objects.all()
    
    return render(request, 'pages/incombills.html',{'incombills': incombills})


def incom_bills_detail(request,pk):

    incombill = IncomingOrder.objects.get(pk=pk)
    
    return render(request, 'pages/incombill_detail.html',{'incombill': incombill})



def update_incomline(request,pk):
    line = IncomingOrderLine.objects.get(pk = pk)
    form = IncomingLineForm(request.POST or None , instance=line)
    if request.method=="POST":
        if form.is_valid():
            form.save()
            return redirect("products:detail_incomline", pk=line.id)
    context = {
        "form": form,
        "line": line,
    }
    return render(request, 'partials/incomline_form.html', context)


def delete_incomline(request,pk):
    incomline = IncomingOrderLine.objects.get(pk = pk)
    incomline.delete()
    return HttpResponse('')



def update_incombill_info(request,pk):
    incombill = IncomingOrder.objects.get(pk = pk)
    form = IncomInfoForm(request.POST or None,instance=incombill)
    if request.method=="POST":
        if form.is_valid():
            form.save()
            return redirect('products:incombill_info_details', pk=incombill.id)
    return render(request,'partials/incombill_info_form.html',{"form":form,"incombill":incombill})



def incombill_info_details(request,pk):
    incombill = IncomingOrder.objects.get(pk = pk)
    return render(request,'partials/incombill_info_details.html',{"incombill":incombill})

def empty_the_bill(request):
    incombill_id = request.GET.get("id")
    incombill = IncomingOrder.objects.get(id = incombill_id)
    
    if not incombill.empty_done:
        lines = incombill.incomingorderline_set.all()
        for line in lines:
            line.product.available_in_ventory += line.qty
            line.product.save()
        incombill.empty_done = True
        incombill.save()
        data={
            "empty_done":incombill.empty_done,
        }
    return JsonResponse(data)


def delete_incombill(request,pk):
    incombill = IncomingOrder.objects.get(pk = pk)
    incombill.delete()
    return redirect("products:incom_bills")


def delete_incombill_list(request):
    incombill_id = request.GET.get("id")
    incombill = IncomingOrder.objects.get(id = incombill_id)
    incombill.delete()
    data = {}
    return JsonResponse(data)
