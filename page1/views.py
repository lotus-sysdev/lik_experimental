from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomerForm,PIC_Forms
from django.http import HttpResponse, JsonResponse  
from .models import *
# Create your views here.
def placeholder(request):
    return HttpResponse("Hello World")
def my_view(request):
    customer_form = CustomerForm(request.POST or None)
    pic_form = PIC_Forms(request.POST or None)
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('success_url')  # Replace 'success_url' with the URL you want to redirect to after successfully adding a customer
    else:
        form = CustomerForm()

    return render(request, 'page1.html', {'customer_form': customer_form})

def display_customer(request):
    customers = Customer.objects.all()
    return render(request, 'display_customer.html', {'customers': customers})

def display_supplier(request):
    suppliers = Supplier.objects.all()
    return render(request, 'display_supplier.html', {'suppliers': suppliers})

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

    return render(request, 'yourapp/edit_customer.html', {'form': form})

# yourapp/views.py
def delete_customer(request, cust_id):
    customer = get_object_or_404(Customer, cust_id=cust_id)

    if request.method == 'POST':
        customer.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def supplier_detail(request, cust_id):
    customer = get_object_or_404(Supplier, cust_id=cust_id)
    form = SupplierForm(instance=customer)
    return render(request, 'customer_detail.html', {'customer': customer, 'form': form})

def edit_supplier(request, cust_id):
    customer = get_object_or_404(Supplier, cust_id=cust_id)

    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = SupplierForm(instance=customer)

    return render(request, 'yourapp/edit_customer.html', {'form': form})

# yourapp/views.py
def delete_supplier(request, cust_id):
    customer = get_object_or_404(Supplier, cust_id=cust_id)

    if request.method == 'POST':
        customer.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})