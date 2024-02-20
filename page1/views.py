import os
from PIL import Image
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.core.files import File
from django.http import HttpResponse, JsonResponse
from .forms import *
from .models import *

# -------------------- Placeholder for homepage --------------------#
def placeholder(request):
    return render(request, 'home.html')


# -------------------- Common Functions --------------------#
# Adding entity (Customer and Supplier)
def add_entity_view(request, entity_form, template_name):
    entity_form_instance = entity_form(request.POST or None)
    if request.method == 'POST':
        form = entity_form(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = entity_form()

    return render(request, template_name, {'entity_form': entity_form_instance})


# Common add_entity function for adding alamat and pic
def add_entity(request, entity_id, entity_model, form_class, template_name, entity_field, entity_form_field, initial_data=None):
    entity = get_object_or_404(entity_model, **{entity_field: entity_id})

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            setattr(form.instance, entity_form_field, entity)
            form.save()
    else:
        form = form_class(initial=initial_data)

    return render(request, template_name, {'entity': entity, 'form': form, 'entity_id': entity_id})


# Display entities for displaying tables
def display_entities(request, entity_model, template_name):
    entities = entity_model.objects.all()
    return render(request, template_name, {'entities': entities})


# -------------------- Common Functions for Detail, Edit, and Delete -------------------- #
def entity_detail(request, entity_model, entity_form, entity_id_field, entity_id, template_name):
    entity = get_object_or_404(entity_model, **{entity_id_field: entity_id})
    form = entity_form(instance=entity)
    context = {'entity': entity, 'form': form, 'entity_id': entity_id}
    return render(request, template_name, context)

def edit_entity(request, entity_model, entity_form, entity_id_field, entity_id):
    entity = get_object_or_404(entity_model, **{entity_id_field: entity_id})

    if request.method == 'POST':
        form = entity_form(request.POST, instance=entity)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = entity_form(instance=entity)

    return render(request, 'edit_entity.html', {'form': form})

def delete_entity(request, entity_model, entity_id_field, entity_id):
    entity = get_object_or_404(entity_model, **{entity_id_field: entity_id})

    if request.method == 'POST':
        entity.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


# -------------------- Add Customer and Supplier Views -------------------- #
def add_customer(request):
    return add_entity_view(request, CustomerForm, 'add_cust.html')

def add_supplier(request):
    return add_entity_view(request, SupplierForm, 'add_supp.html')


# -------------------- Add Alamat and PIC -------------------- #
def add_customer_pic(request, cust_id):
    return add_entity(request, cust_id, Customer, Cust_PIC_Forms, 'add_cust_pic.html', 'cust_id', 'customer_id', {'customer_id': cust_id})

def add_supplier_pic(request, supp_id):
    return add_entity(request, supp_id, Supplier, Supp_PIC_Forms, 'add_supp_pic.html', 'supp_id', 'supplier_id', {'supplier_id': supp_id})

def add_customer_alamat(request, cust_id):
    return add_entity(request, cust_id, Customer, Cust_Alamat_Forms, 'add_customer_alamat.html', 'cust_id', 'customer_id', {'customer_id': cust_id})

def add_supplier_alamat(request, supp_id):
    return add_entity(request, supp_id, Supplier, Supp_Alamat_Forms, 'add_supplier_alamat.html', 'supp_id', 'supplier_id', {'supplier_id': supp_id})


# -------------------- PIC Listing for Customer and Supplier -------------------- #
def cust_pic_list(request, cust_id):
    customer = get_object_or_404(Customer, cust_id=cust_id)
    customer_pics = CustomerPIC.objects.filter(customer_id=cust_id)
    return render(request, 'cust_pic_list.html', {'customer': customer, 'customer_pics': customer_pics})

def supp_pic_list(request, supp_id):
    supplier = get_object_or_404(Supplier, supp_id=supp_id)
    supplier_pics = SupplierPIC.objects.filter(supplier_id=supp_id)
    return render(request, 'supp_pic_list.html', {'supplier': supplier, 'supplier_pics': supplier_pics})


# -------------------- Add Item -------------------- #
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
                # image_name = f"{item.nama}.{image.name.split('.')[-1]}"
                # image_path = os.path.join(settings.MEDIA_ROOT, image_name)
                resized_image_name = f"{item.nama}_resized.{image.name.split('.')[-1]}"  # Rename the file to avoid overwriting the original
                resized_image_path = os.path.join(settings.MEDIA_ROOT, resized_image_name)
                img.save(resized_image_path)

                # os.remove(image_path)

                item.gambar = resized_image_name
                print(item.gambar)
                item.save()

    else:
        form = ItemForm()
    
    return render(request, 'add_item.html', {'item_form': form})


# -------------------- Display Tables -------------------- #
def display_customer(request):
    return display_entities(request, Customer, 'display_customer.html')

def display_supplier(request):
    return display_entities(request, Supplier, 'display_supplier.html')

def display_item(request):
    return display_entities(request, Items, 'display_item.html')


# -------------------- Customer Functions -------------------- #
def customer_detail(request, cust_id):
    return entity_detail(request, Customer, CustomerForm, 'cust_id', cust_id, 'customer_detail.html')

def edit_customer(request, cust_id):
    return edit_entity(request, Customer, CustomerForm, 'cust_id', cust_id)

def delete_customer(request, cust_id):
    return delete_entity(request, Customer, 'cust_id', cust_id)


# -------------------- Customer Functions -------------------- #
def supplier_detail(request, supp_id):
    return entity_detail(request, Supplier, SupplierForm, 'supp_id', supp_id, 'supplier_detail.html')

def edit_supplier(request, supp_id):
    return edit_entity(request, Supplier, SupplierForm, 'supp_id', supp_id)

def delete_supplier(request, supp_id):
    return delete_entity(request, Supplier, 'supp_id', supp_id)


# -------------------- Item Functions -------------------- #
def item_detail(request, SKU):
    return entity_detail(request, Items, ItemForm, 'SKU', SKU, 'item_detail.html')

def edit_item(request, SKU):
    return edit_entity(request, Items, ItemForm, 'SKU', SKU)

def delete_item(request, SKU):
    return delete_entity(request, Items, 'SKU', SKU)