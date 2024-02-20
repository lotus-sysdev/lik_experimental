import os
from PIL import Image
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files import File
from django.http import HttpResponse, JsonResponse
from .forms import *
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

def cust_pic_list(request, cust_id):
    customer = get_object_or_404(Customer, cust_id=cust_id)
    customer_pics = CustomerPIC.objects.filter(customer_id=cust_id)
    return render(request, 'cust_pic_list.html', {'customer': customer, 'customer_pics': customer_pics})

def supp_pic_list(request, supp_id):
    supplier = get_object_or_404(Supplier, supp_id=supp_id)
    supplier_pics = SupplierPIC.objects.filter(supplier_id=supp_id)
    return render(request, 'supp_pic_list.html', {'supplier': supplier, 'supplier_pics': supplier_pics})

def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            image = item.gambar
            if image:
                # Open the image
                img = Image.open(image)
                
                # Resize the image
                img = img.resize((100, 100))  # Change the dimensions as needed
                
                # Save the resized image
                resized_image_name = f"{item.nama}_resized.jpg"  # Rename the file to avoid overwriting the original
                resized_image_path = os.path.join(settings.MEDIA_ROOT, 'resized_images', resized_image_name)
                img.save(resized_image_path)

                item.gambar = os.path.join('resized_images', resized_image_name)
                print(item.gambar)
                item.save()
    else:
        form = ItemForm()
    
    return render(request, 'add_item.html', {'item_form': form})
def add_customer_pic(request, cust_id):
    customer = get_object_or_404(Customer, cust_id=cust_id)
    if request.method == 'POST':
        form = Cust_PIC_Forms(request.POST)
        if form.is_valid():
            # Set the customer_id field of the form to the customer ID
            form.instance.customer_id = cust_id
            form.save()
    else:
        form = Cust_PIC_Forms(initial={'customer_id': cust_id})
    return render(request, 'add_cust_pic.html', {'customer':customer,'form': form, 'cust_id':cust_id})

def add_supplier_pic(request, supp_id):
    supplier = get_object_or_404(Supplier, supp_id=supp_id)
    if request.method == 'POST':
        form = Supp_PIC_Forms(request.POST)
        if form.is_valid():
            # Set the customer_id field of the form to the customer ID
            form.instance.supplier_id = supp_id
            form.save()
    else:
        form = Supp_PIC_Forms(initial={'supplier_id': supp_id})
    return render(request, 'add_supp_pic.html', {'supplier':supplier,'form': form,'supp_id':supp_id})

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
    context = {'customer': customer, 'form': form, 'cust_id': cust_id}
    return render(request, 'customer_detail.html', context)

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
    
# Item Details, Edit, and Delete
def item_detail(request, SKU):
    item = get_object_or_404(Items, SKU=SKU)
    form = ItemForm(instance=item)
    return render(request, 'item_detail.html', {'item': item, 'form': form})    

def edit_item(request, SKU):
    item = get_object_or_404(Items, SKU=SKU)

    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ItemForm(instance=item)

    return render(request, 'edit_item.html', {'form': form})

def delete_item(request, SKU):
    item = get_object_or_404(Items, SKU=SKU)

    if request.method == 'POST':
        item.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
def add_customer_alamat(request, cust_id):
    customer = get_object_or_404(Customer, cust_id=cust_id)
    if request.method == 'POST':
        form = Cust_Alamat_Forms(request.POST)
        if form.is_valid():
            # Set the customer_id field of the form to the customer ID
            form.instance.customer_id = customer
            form.save()
    else:
        form = Cust_Alamat_Forms(initial={'customer_id': cust_id})
    return render(request, 'add_customer_alamat.html', {'customer':customer,'form': form, 'cust_id':cust_id})

def add_supplier_alamat(request, supp_id):
    supplier = get_object_or_404(Supplier, supp_id=supp_id)
    if request.method == 'POST':
        form = Supp_Alamat_Forms(request.POST)
        if form.is_valid():
            # Set the customer_id field of the form to the customer ID
            form.instance.supplier_id = supplier
            form.save()
    else:
        form = Supp_Alamat_Forms(initial={'supplier_id': supp_id})
    return render(request, 'add_supplier_alamat.html', {'supplier':supplier,'form': form,'supp_id':supp_id})