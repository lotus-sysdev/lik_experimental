from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.http import HttpResponse, JsonResponse
from .models import *
# Create your views here.
def placeholder(request):
    return render(request, 'home.html')

def add_customer(request):
    customer_form = CustomerForm(request.POST or None)
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('success_url')  # Replace 'success_url' with the URL you want to redirect to after successfully adding a customer
    else:
        form = CustomerForm()

    return render(request, 'add_cust.html', {'customer_form': customer_form})
def add_supplier(request):
    supplier_form = SupplierForm(request.POST or None)
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('success_url')  # Replace 'success_url' with the URL you want to redirect to after successfully adding a customer
    else:
        form = SupplierForm()

    return render(request, 'add_supp.html', {'supplier_form': supplier_form})

# def add_pic (request):
#     pic_form = PIC_Forms(request.POST or None)
#     if request.method == 'POST':
#         form = PIC_Forms(request.POST)
#         if form.is_valid():
#             form.save()
#             # return redirect('success_url')  # Replace 'success_url' with the URL you want to redirect to after successfully adding a customer
#     else:
#         form = PIC_Forms()

#     return render(request, 'add_pic.html', {'pic_form': pic_form})

def add_item(request):
    item_form = ItemForm(request.POST or None)
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('success_url')  # Replace 'success_url' with the URL you want to redirect to after successfully adding a customer
    else:
        form = ItemForm()

    return render(request, 'add_item.html', {'item_form': item_form})
def add_customer_pic(request, cust_id):
    cust_id = Customer.objects.get(cust_id=cust_id)
    if request.method == 'POST':
        form = Cust_PIC_Forms(request.POST)
        if form.is_valid():
            # Set the customer_id field of the form to the customer ID
            form.instance.customer_id = cust_id
            form.save()
    else:
        form = Cust_PIC_Forms(initial={'customer_id': cust_id})
    return render(request, 'add_cust_pic.html', {'form': form})
def goto_add_pic(request, cust_id):
    customer = get_object_or_404(Customer, cust_id=cust_id)
    return render(request, 'add_cust_pic.html',{'customer' : customer})

def add_supplier_pic(request, supp_id):
    supp_id = Supplier.objects.get(supp_id=supp_id)
    if request.method == 'POST':
        form = Supp_PIC_Forms(request.POST)
        if form.is_valid():
            # Set the customer_id field of the form to the customer ID
            form.instance.supplier_id = supp_id
            form.save()
    else:
        form = Supp_PIC_Forms(initial={'supplier_id': supp_id})
    return render(request, 'add_supp_pic.html', {'form': form})
def goto_add_pic2(request, supp_id):
    supplier = get_object_or_404(Supplier, supp_id=supp_id)
    return render(request, 'add_supp_pic.html',{'supplier' : supplier})
# Displaying Tables
def display_customer(request):
    customers = Customer.objects.all()
    return render(request, 'display_customer.html', {'customers': customers})

def display_supplier(request):
    suppliers = Supplier.objects.all()
    return render(request, 'display_supplier.html', {'suppliers': suppliers})

def display_item(request):
    items = Items.objects.all()
    return render(request, 'display_item.html', {'items': items})

# Customer Details, Edit, and Delete
def customer_detail(request, cust_id):
    customer = get_object_or_404(Customer, cust_id=cust_id)
    form = CustomerForm(instance=customer)
    return render(request, 'customer_detail.html', {'customer': customer, 'form': form})

def edit_customer(request, cust_id):
    customer = get_object_or_404(Customer, cust_id=cust_id)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = CustomerForm(instance=customer)

    return render(request, 'edit_customer.html', {'form': form})

def delete_customer(request, cust_id):
    customer = get_object_or_404(Customer, cust_id=cust_id)

    if request.method == 'POST':
        customer.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})

# Supplier Details, Edit, and Delete
def supplier_detail(request, supp_id):
    supplier = get_object_or_404(Supplier, supp_id=supp_id)
    form = SupplierForm(instance=supplier)
    return render(request, 'supplier_detail.html', {'supplier': supplier, 'form': form})

def edit_supplier(request, supp_id):
    supplier = get_object_or_404(Supplier, supp_id=supp_id)

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = SupplierForm(instance=supplier)

    return render(request, 'edit_supplier.html', {'form': form})

def delete_supplier(request, supp_id):
    supplier = get_object_or_404(Supplier, supp_id=supp_id)

    if request.method == 'POST':
        supplier.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
