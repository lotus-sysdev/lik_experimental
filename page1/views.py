import os
from PIL import Image

from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
from django.core.files import File
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseNotFound

from .decorators import *
from .forms import *
from .models import *



# -------------------- Placeholder for homepage --------------------#
@login_required
def placeholder(request):
    return render(request, 'home.html')


# -------------------- Common Functions --------------------#
# Adding entity (Customer and Supplier)
@login_required
def add_entity_view(request, entity_form, template_name, redirect_template):
    entity_form_instance = entity_form(request.POST or None)
    if request.method == 'POST':
        form = entity_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(redirect_template)
    else:
        form = entity_form()

    return render(request, template_name, {'entity_form': entity_form_instance})


# Common add_entity function for adding alamat and pic
@login_required
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
@login_required
def display_entities(request, entity_model, template_name):
    entities = entity_model.objects.all()
    return render(request, template_name, {'entities': entities})


# -------------------- Common Functions for Detail, Edit, and Delete -------------------- #
@login_required
def entity_detail(request, entity_model, entity_form, entity_id_field, entity_id, template_name, extra_context=None):
    entity = get_object_or_404(entity_model, **{entity_id_field: entity_id})
    form = entity_form(instance=entity)
    context = {'entity': entity, 'form': form, 'entity_id': entity_id}

    if extra_context:
        context.update(extra_context)

    return render(request, template_name, context)

@login_required
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

@login_required
def delete_entity(request, entity_model, entity_id_field, entity_id):
    entity = get_object_or_404(entity_model, **{entity_id_field: entity_id})

    if request.method == 'POST':
        entity.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})


# -------------------- Add Customer and Supplier Views -------------------- #
@login_required
def add_customer(request):
    return add_entity_view(request, CustomerForm, 'customer/add_cust.html', 'display_customer')

@login_required
def add_supplier(request):
    return add_entity_view(request, SupplierForm, 'supplier/add_supp.html', 'display_supplier')


# -------------------- Add Alamat and PIC -------------------- #
@login_required
def add_customer_pic(request, cust_id):
    return add_entity(request, cust_id, Customer, CustPICForms, 'pic/add_cust_pic.html', 'cust_id', 'customer_id', {'customer_id': cust_id})

@login_required
def add_supplier_pic(request, supp_id):
    return add_entity(request, supp_id, Supplier, SuppPICForms, 'pic/add_supp_pic.html', 'supp_id', 'supplier_id', {'supplier_id': supp_id})

@login_required
def add_customer_alamat(request, cust_id):
    return add_entity(request, cust_id, Customer, CustAlamatForms, 'alamat/add_customer_alamat.html', 'cust_id', 'customer_id', {'customer_id': cust_id})

@login_required
def add_supplier_alamat(request, supp_id):
    return add_entity(request, supp_id, Supplier, SuppAlamattForms, 'alamat/add_supplier_alamat.html', 'supp_id', 'supplier_id', {'supplier_id': supp_id})


# -------------------- Add Item -------------------- #
@login_required
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
            return redirect('display_item')

    else:
        form = ItemForm(disable_category=False)
    
    return render(request, 'item/add_item.html', {'item_form': form})


# -------------------- Display Tables -------------------- #
@login_required
def display_customer(request):
    return display_entities(request, Customer, 'customer/display_customer.html')

@login_required
def display_supplier(request):
    return display_entities(request, Supplier, 'supplier/display_supplier.html')

@login_required
def display_item(request):
    return display_entities(request, Items, 'item/display_item.html')


# -------------------- Customer Functions -------------------- #
@login_required
def customer_detail(request, cust_id):
    customer_pics = CustomerPIC.objects.filter(customer_id=cust_id)
    customer_alamat = CustomerAlamat.objects.filter(customer_id=cust_id)
    extra_context = {'customer_pics':customer_pics, 'customer_alamat':customer_alamat}
    return entity_detail(request, Customer, CustomerForm, 'cust_id', cust_id, 'customer/customer_detail.html', extra_context)

@login_required
def edit_customer(request, cust_id):
    return edit_entity(request, Customer, CustomerForm, 'cust_id', cust_id)

@login_required
def delete_customer(request, cust_id):
    return delete_entity(request, Customer, 'cust_id', cust_id)


# -------------------- Customer Functions -------------------- #
@login_required
def supplier_detail(request, supp_id):
    supplier_pics = SupplierPIC.objects.filter(supplier_id=supp_id)
    supplier_alamat = SupplierAlamat.objects.filter(supplier_id=supp_id)
    extra_context = {'supplier_pics':supplier_pics, 'supplier_alamat':supplier_alamat}
    return entity_detail(request, Supplier, SupplierForm, 'supp_id', supp_id, 'supplier/supplier_detail.html', extra_context)

@login_required
def edit_supplier(request, supp_id):
    return edit_entity(request, Supplier, SupplierForm, 'supp_id', supp_id)

@login_required
def delete_supplier(request, supp_id):
    return delete_entity(request, Supplier, 'supp_id', supp_id)


# -------------------- Item Functions -------------------- #
@login_required
def item_detail(request, SKU):
    entity = get_object_or_404(Items, SKU=SKU)
    item_sumber = ItemSumber.objects.filter(item=SKU)
    context = {'entity':entity, 'item_sumber':item_sumber, 'form':ItemForm(instance=entity, disable_category=True)}
    return render(request, 'item/item_detail.html', context)

@login_required
def edit_item(request, SKU):
    entity = get_object_or_404(Items,SKU=SKU)

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=entity)
        if form.is_valid():
            # Check if a new image file is provided
            new_image = request.FILES.get('gambar')
            
            if new_image:
                # Process the new image file (similar to the logic in your add_item view)
                img = Image.open(new_image)
                img = img.resize((100, 100))
                resized_image_name = f"{entity.nama}_resized.{new_image.name.split('.')[-1]}"
                resized_image_path = os.path.join(settings.MEDIA_ROOT, resized_image_name)
                img.save(resized_image_path)
                
                # Update the item's image field with the new image path
                form.instance.gambar = resized_image_name

            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ItemForm(instance=entity)

    return render(request, 'edit_item.html', {'form': form})

@login_required
def delete_item(request, SKU):
    return delete_entity(request, Items, 'SKU', SKU)


# -------------------- Item Sumber Functions -------------------- #
@login_required
def add_sumber(request, SKU):
    return add_entity(request, SKU, Items, SumberForm, 'item/add_sumber.html', 'SKU', 'item')


# -------------------- Order Functions -------------------- #
# Add Purchase Order and Work Order
def add_PO(request):
    return add_entity_view(request, PurchaseForm, 'order/add_PO.html', 'display_purchase')

@login_required
def add_WO(request):
    return add_entity_view(request, WorkForm, 'order/add_WO.html', 'display_work')

# Display Purchase Order and Work Order
def display_purchase(request):
    return display_entities(request, PurchaseOrder, 'order/display_purchase.html')

def display_work(request):
    return display_entities(request, WorkOrder, 'order/display_work.html')

#  Detail of Purchase Order and Work Order
def purchase_detail(request, id):
    return entity_detail(request, PurchaseOrder, PurchaseForm, 'id',id, 'order/purchase_detail.html')

def work_detail(request, id):
    return entity_detail(request, WorkOrder, WorkForm, 'id', id, 'order/work_detail.html')

# Edit Purchase Order and Work Order
def edit_purchase(request, id):
    return edit_entity(request, PurchaseOrder, PurchaseForm, 'id', id)

def edit_work(request, id):
    return edit_entity(request, WorkOrder, WorkForm, 'id', id)

# Delete Purchase Order and Work Order
def delete_purchase(request, id):
    return delete_entity(request, PurchaseOrder, 'id', id)

def delete_work(request, id):
    return delete_entity(request, WorkOrder, 'id', id)
  

# -------------------- Login, Register, Logout Functions -------------------- #
# Login, Register, and Logout
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = AuthenticationForm()

    form.fields['username'].widget.attrs.update({'class': 'form-control'})
    form.fields['password'].widget.attrs.update({'class': 'form-control'})

    return render(request, 'accounts/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = Register(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')
    else:
        form = Register()
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/login')


def user_action_logs(request):
    logs = UserActionLog.objects.all().order_by('-timestamp')[:100]  # Get the last 10 logs
    return render(request, 'logs.html', {'logs': logs})

