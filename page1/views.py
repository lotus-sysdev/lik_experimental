import json
import os
import csv
from PIL import Image
import pandas as pd
import requests
import datetime

from django.core.files.base import ContentFile
# from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import redirect, render, get_object_or_404
from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from django.urls import reverse

from .decorators import *
from .forms import *
from .models import *
import openpyxl
from openpyxl_image_loader import SheetImageLoader


# -------------------- Placeholder for homepage --------------------#
@login_required
def placeholder(request):
    return render(request, 'home.html')


# -------------------- Common Functions --------------------#
# Adding entity (Customer and Supplier)
@login_required
def add_entity_view(request, entity_form, template_name, redirect_template, initial = None):
    entity_form_instance = entity_form(request.POST or None)
    if request.method == 'POST':
        form = entity_form(request.POST)
        if form.is_valid():
            form.save()
            return redirect(redirect_template)
    else:
        print(initial)
        if (initial):
            form = (entity_form(initial=initial))
            entity_form_instance = form
        else: 
            form = entity_form()

    return render(request, template_name, {'entity_form': entity_form_instance})


# Common add_entity function for adding alamat and pic
@login_required
def add_entity(request, entity_id, entity_model, form_class, template_name, entity_field, entity_form_field, initial_data=None, redirect_url = None):
    entity = get_object_or_404(entity_model, **{entity_field: entity_id})

    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            setattr(form.instance, entity_form_field, entity)
            form.save()
            if redirect_url:
                return redirect(redirect_url)
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
@GA_required
def add_customer(request):
    return add_entity_view(request, CustomerForm, 'customer/add_cust.html', 'display_customer')

@login_required
@GA_required
def add_supplier(request):
    return add_entity_view(request, SupplierForm, 'supplier/add_supp.html', 'display_supplier')


# -------------------- Add Alamat and PIC -------------------- #
@login_required
@GA_required
def add_customer_pic(request, cust_id):
    redirect_url  = reverse('customer_detail', args=(cust_id,))
    return add_entity(request, cust_id, Customer, CustPICForms, 'pic/add_cust_pic.html', 'cust_id', 'customer_id', {'customer_id': cust_id}, redirect_url=redirect_url)

@login_required
@GA_required
def add_supplier_pic(request, supp_id):
    redirect_url  = reverse('supplier_detail', args=(supp_id,))
    return add_entity(request, supp_id, Supplier, SuppPICForms, 'pic/add_supp_pic.html', 'supp_id', 'supplier_id', {'supplier_id': supp_id}, redirect_url=redirect_url)

@login_required
@GA_required
def add_customer_alamat(request, cust_id):
    redirect_url  = reverse('customer_detail', args=(cust_id,))
    return add_entity(request, cust_id, Customer, CustAlamatForms, 'alamat/add_customer_alamat.html', 'cust_id', 'customer_id', {'customer_id': cust_id}, redirect_url=redirect_url)

@login_required
@GA_required
def add_supplier_alamat(request, supp_id):
    redirect_url  = reverse('supplier_detail', args=(supp_id,))
    return add_entity(request, supp_id, Supplier, SuppAlamattForms, 'alamat/add_supplier_alamat.html', 'supp_id', 'supplier_id', {'supplier_id': supp_id}, redirect_url=redirect_url)


# -------------------- Edit and Delete Alamat and PIC -------------------- #
@login_required
@GA_required
def edit_customer_pic(request, pic_id):
    pic = get_object_or_404(CustomerPIC, id=pic_id)
    form = CustPICForms(request.POST or None, instance=pic)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('customer_detail', cust_id=pic.customer_id.pk)
    return render(request, 'pic/edit_customer_pic.html', {'form': form, 'pic': pic})

@login_required
@GA_required
def delete_customer_pic(request, pic_id):
    return delete_entity(request, CustomerPIC, 'id', pic_id)

@login_required
@GA_required
def edit_customer_alamat(request, alamat_id):
    alamat = get_object_or_404(CustomerAlamat, id=alamat_id)
    form = CustAlamatForms(request.POST or None, instance=alamat)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('customer_detail', cust_id=alamat.customer_id.pk)
    return render(request, 'alamat/edit_customer_alamat.html', {'form': form, 'alamat': alamat})

@login_required
@GA_required
def delete_customer_alamat(request, alamat_id):
    return delete_entity(request, CustomerAlamat, 'id', alamat_id)

# Supplier
@login_required
@GA_required
def edit_supplier_pic(request, pic_id):
    pic = get_object_or_404(SupplierPIC, id=pic_id)
    form = SuppPICForms(request.POST or None, instance=pic)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('supplier_detail', supp_id=pic.supplier_id.pk)
    return render(request, 'pic/edit_supplier_pic.html', {'form': form, 'pic': pic})

@login_required
@GA_required
def delete_supplier_pic(request, pic_id):
    return delete_entity(request, SupplierPIC, 'id', pic_id)

@login_required
@GA_required
def edit_supplier_alamat(request, alamat_id):
    alamat = get_object_or_404(SupplierAlamat, id=alamat_id)
    form = SuppAlamattForms(request.POST or None, instance=alamat)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('customer_detail', cust_id=alamat.supplier_id.pk)
    return render(request, 'alamat/edit_supplier_alamat.html', {'form': form, 'alamat': alamat})

@login_required
@GA_required
def delete_supplier_alamat(request, alamat_id):
    return delete_entity(request, SupplierAlamat, 'id', alamat_id)


# -------------------- Add Item -------------------- #
@login_required
@GA_required
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
                regex_pattern = r'/'
                replacement_string = '.'
                nama_cleaned = re.sub(regex_pattern, replacement_string, item.nama)
                # Save the resized image
                # image_name = f"{item.nama}.{image.name.split('.')[-1]}"
                # image_path = os.path.join(settings.MEDIA_ROOT, image_name)
                resized_image_name = f"media_{nama_cleaned}_{item.Tanggal}.{image.name.split('.')[-1]}"  # Rename the file to avoid overwriting the original
                resized_image_path = os.path.join(settings.MEDIA_ROOT, resized_image_name)
                img.save(resized_image_path)
                

                # os.remove(image_path)

                item.gambar = resized_image_name
                print(item.gambar)
                item.save()
            return redirect('display_item')

    else:
        form = ItemForm()
    
    return render(request, 'item/add_item.html', {'item_form': form})


# -------------------- Display Tables -------------------- #
@login_required
@GA_required
def display_customer(request):
    return display_entities(request, Customer, 'customer/display_customer.html')

@login_required
@GA_required
def display_supplier(request):
    return display_entities(request, Supplier, 'supplier/display_supplier.html')

@login_required
@GA_required
def display_item(request):
    return display_entities(request, Items, 'item/display_item.html')


# -------------------- Customer Functions -------------------- #
@login_required
@GA_required
def customer_detail(request, cust_id):
    customer_pics = CustomerPIC.objects.filter(customer_id=cust_id)
    customer_alamat = CustomerAlamat.objects.filter(customer_id=cust_id)
    extra_context = {'customer_pics':customer_pics, 'customer_alamat':customer_alamat}
    return entity_detail(request, Customer, CustomerForm, 'cust_id', cust_id, 'customer/customer_detail.html', extra_context)

@login_required
@GA_required
def edit_customer(request, cust_id):
    return edit_entity(request, Customer, CustomerForm, 'cust_id', cust_id)

@login_required
@GA_required
def delete_customer(request, cust_id):
    return delete_entity(request, Customer, 'cust_id', cust_id)


# -------------------- Customer Functions -------------------- #
@login_required
@GA_required
def supplier_detail(request, supp_id):
    supplier_pics = SupplierPIC.objects.filter(supplier_id=supp_id)
    supplier_alamat = SupplierAlamat.objects.filter(supplier_id=supp_id)
    extra_context = {'supplier_pics':supplier_pics, 'supplier_alamat':supplier_alamat}
    return entity_detail(request, Supplier, SupplierForm, 'supp_id', supp_id, 'supplier/supplier_detail.html', extra_context)

@login_required
@GA_required
def edit_supplier(request, supp_id):
    return edit_entity(request, Supplier, SupplierForm, 'supp_id', supp_id)

@login_required
@GA_required
def delete_supplier(request, supp_id):
    return delete_entity(request, Supplier, 'supp_id', supp_id)


# -------------------- Item Functions -------------------- #
@login_required
@GA_required
def item_detail(request, SKU):
    entity = get_object_or_404(Items, SKU=SKU)
    item_sumber = ItemSumber.objects.filter(item=SKU)
    context = {'entity':entity, 'item_sumber':item_sumber, 'form':ItemForm(instance=entity)}
    return render(request, 'item/item_detail.html', context)

@login_required
@GA_required
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
                resized_image_name = f"{entity.SKU}_resized.{new_image.name.split('.')[-1]}"
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
@GA_required
def delete_item(request, SKU):
    entity = get_object_or_404(Items, SKU=SKU)
    image = entity.gambar
    image_str = str(image)
    image_path = os.path.join(settings.MEDIA_ROOT, image_str)
    print(image_path)
    os.remove(image_path)
    entity.delete()
    messages.success(request, 'Item deleted successfully')
    return redirect('/display_item')

@login_required
@GA_required
def approve_item(request, SKU):
    item = get_object_or_404(Items, SKU=SKU)
    item.is_approved = True
    item.save()
    # Redirect to the item list or any other appropriate view
    return redirect('display_item')

# -------------------- Item Sumber Functions -------------------- #
@login_required
@GA_required
def add_sumber(request, SKU):
    redirect_url  = reverse('item_detail', args=(SKU,))
    return add_entity(request, SKU, Items, SumberForm, 'item/add_sumber.html', 'SKU', 'item', redirect_url=redirect_url)

@login_required
@GA_required
def edit_sumber(request, sumber_id):
    sumber = get_object_or_404(ItemSumber, id=sumber_id)
    form = SumberForm(request.POST or None, instance=sumber)

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('item_detail', SKU=sumber.item.pk)
    return render(request, 'item/edit_sumber.html', {'form': form, 'sumber': sumber})

# def edit_customer_pic(request, pic_id):
#     pic = get_object_or_404(CustomerPIC, id=pic_id)
#     form = CustPICForms(request.POST or None, instance=pic)

#     if request.method == 'POST':
#         if form.is_valid():
#             form.save()
#             return redirect('customer_detail', cust_id=pic.customer_id.pk)
#     return render(request, 'pic/edit_customer_pic.html', {'form': form, 'pic': pic})
@login_required
@GA_required
def delete_sumber(request, sumber_id):
    return delete_entity(request, ItemSumber, 'id', sumber_id)


# -------------------- Order Functions -------------------- #
# Add Purchase Order and Work Order
@login_required
@GA_required
def add_PO(request):
    return add_entity_view(request, PurchaseForm, 'order/add_PO.html', 'display_purchase')

@login_required
@GA_required
def add_WO(request):
     return add_entity_view(request, WorkForm, 'order/add_WO.html', 'display_work')

# Display Purchase Order and Work Order
@login_required
@Messenger_Forbidden
def display_purchase(request):
    return display_entities(request, PurchaseOrder, 'order/display_purchase.html')

@login_required
@Messenger_Forbidden
def display_work(request):
    return display_entities(request, WorkOrder, 'order/display_work.html')

#  Detail of Purchase Order and Work Order
@login_required
@Messenger_Forbidden
def purchase_detail(request, id):
    entity = get_object_or_404(PurchaseOrder, id = id)

    if request.user.groups.filter(name='GA').exists() or request.user.groups.filter(name='Admin').exists():
            form = PurchaseForm(instance=entity)
    elif request.user.groups.filter(name='Accounting').exists():
        form = PurchaseFormNGA(instance=entity)
    context = {'entity': entity, 'form': form, 'entity_id': id}

    return render(request, 'order/purchase_detail.html', context)

@login_required
@Messenger_Forbidden
def work_detail(request, id):
    entity = get_object_or_404(WorkOrder, id = id)

    if request.user.groups.filter(name='GA').exists() or request.user.groups.filter(name='Admin').exists():
            form =WorkForm(instance=entity)
    elif request.user.groups.filter(name='Accounting').exists():
        form = WorkFormNGA(instance=entity)
    context = {'entity': entity, 'form': form, 'entity_id': id}

    return render(request, 'order/work_detail.html', context)

# Edit Purchase Order and Work Order
@login_required
@Messenger_Forbidden
def edit_purchase(request, id):
    entity = get_object_or_404(PurchaseOrder, id = id)

    if request.method == 'POST':
        if request.user.groups.filter(name='GA').exists() or request.user.groups.filter(name='Admin').exists():
            form = PurchaseForm(request.POST, instance=entity)
        elif request.user.groups.filter(name='Accounting').exists():
            form = PurchaseFormNGA(request.POST, instance=entity)
        
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    return render(request, 'order/purchase_detail.html', {'form': form})

@login_required
@Messenger_Forbidden
def edit_work(request, id):
    entity = get_object_or_404(WorkOrder, id = id)

    if request.method == 'POST':
        if request.user.groups.filter(name='GA').exists() or request.user.groups.filter(name='Admin').exists():
            form = WorkForm(request.POST, instance=entity)
        elif request.user.groups.filter(name='Accounting').exists():
            form = WorkFormNGA(request.POST, instance=entity)
        
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})

    return render(request, 'order/work_detail.html', {'form': form})

# Delete Purchase Order and Work Order
@login_required
@Messenger_Forbidden
def delete_purchase(request, id):
    return delete_entity(request, PurchaseOrder, 'id', id)

@login_required
@Messenger_Forbidden
def delete_work(request, id):
    return delete_entity(request, WorkOrder, 'id', id)
  

# -------------------- Login, Register, Logout Functions -------------------- #
# Login, Register, and Logout
def login_view(request):
    if request.method == 'POST':
        form = Login(request, request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
    else:
        form = Login()
    
    form.fields['email'].widget.attrs.update({'class':'form-control'})
    # form.fields['username'].widget.attrs.update({'class': 'form-control'})
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


# -------------------- User Action Logs -------------------- #
def user_action_logs(request):
    logs = UserActionLog.objects.all().order_by('-timestamp')[:100]  # Get the last 10 logs
    return render(request, 'logs.html', {'logs': logs})


# -------------------- Delivery Order -------------------- #
# Display calendar, and event addition/deletion functionality
@login_required
@Messenger_Only
def calendar(request):  
    all_events = Events.objects.all()
    messengers = Messenger.objects.all()
    request.session['num_forms'] = 1
    request.session.modified = True
    context = {
        "events":all_events,
        "messengers": messengers,
    }
    return render(request,'delivery/calendar.html',context)

@login_required
@Messenger_Only
def all_events(request):                                                                                                 
    all_events = Events.objects.all()                                                                                    
    out = []                                                                                                             

    for event in all_events: 
        event.start = event.start.astimezone(timezone.get_current_timezone())                                                                                            
        event.end = event.end.astimezone(timezone.get_current_timezone())                                                                                            
        out.append({     
            'title': event.title,                                                                                    
            'id': event.id,                                                                                              
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),                                                         
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),
            'messenger_id':event.messenger.id,      
            'messenger_color':event.messenger.color                                                       
        })                                                                                                               
                                                                                                                      
    return JsonResponse(out, safe=False) 
 
@login_required
@Messenger_Only
def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    event = Events(name=str(title), start=start, end=end)
    event.save()
    data = {}
    return JsonResponse(data)
 
@login_required
@Messenger_Only
def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.start = start
    event.end = end
    event.title = title
    event.save()
    data = {}
    return JsonResponse(data)
 
@login_required
@Messenger_Only
def remove(request):
    id = request.GET.get("id", None)
    event = Events.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)

# Forms for adding delivery order, messenger, and vehicle
# Delivery form functionality
@login_required
@Messenger_Only
def delivery_form(request):
    max_forms = 3  # Maximum number of forms allowed

    if request.method == 'POST':
        num_forms = int(request.POST.get('num_forms', 1))  # Get the submitted number of forms

        forms = [DeliveryForm(request.POST, prefix=str(i)) for i in range(1, num_forms + 1)]
        
        if all(form.is_valid() for form in forms):
            # All forms are valid, process the data as needed
            for form in forms:
                # Save or process each form's data
                instance = form.save(commit=False)
                # Do additional processing if needed
                instance.save()

            request.session['num_forms'] = 1
            request.session.modified = True
            return redirect('calendar')  # Redirect to a success page
    else:
        start_param = request.GET.get('start')
        end_param = request.GET.get('end')
        # Set initial data for the forms based on start and end parameters
        initial_data = {'start': start_param, 'end': end_param}

        num_forms = int(request.session.get('num_forms', 1))
        # print(num_forms)

        forms = [DeliveryForm(initial=initial_data, prefix=str(i)) for i in range(1, num_forms + 1)]

    context = {'forms': forms, 'max_forms': max_forms}
    return render(request, 'delivery/delivery_form.html', context)

@login_required
@Messenger_Only
def update_num_forms(request):
    if request.method == 'POST':
        num_forms = int(request.POST.get('num_forms', 1))
        request.session['num_forms'] = num_forms
        request.session.modified = True
        
        return JsonResponse({'status': 'success', 'num_forms':num_forms})

    return JsonResponse({'status': 'error'})

# Display, edit, and delete delivery
@login_required
@Messenger_Only
def delivery_detail(request, id):
    return entity_detail(request, Events, DeliveryForm, "id", id, 'delivery/delivery_detail.html')

@login_required
@Messenger_Only
def edit_delivery(request, id):
    return edit_entity(request, Events, DeliveryForm, 'id', id)

@login_required
@Messenger_Only
def delete_delivery(request, id):
    return delete_entity(request, Events, 'id', id)

# Adding messenger and vehicle
@login_required
def add_messenger(request):
    return add_entity_view(request, MessengerForm, 'delivery/add_messenger.html', 'calendar')

@login_required
def add_vehicle(request):
    return add_entity_view(request, VehicleForm, 'delivery/add_vehicle.html', 'calendar')


# -------------------- Error Pages -------------------- #
def forbidden(request):
    return render(request, 'forbidden.html')

def page_not_found(request, exception):
    return render(request, '404.html', status=404)


# -------------------- Upload CSV/Excel -------------------- #
def upload_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        csv_reader = csv.DictReader(decoded_file)

        success_count = 0
        error_messages = []

        for row_number, row in enumerate(csv_reader, start=1):
            try:
                # Get or create the Category instance based on the provided category name
                category_name = row['category']
                category_instance, _ = Category.objects.get_or_create(name=category_name)

                # Check if image URL is provided in the CSV row
                if 'gambar' in row and row['gambar']:
                    image_url = row['gambar']
                    # Download the image from the URL
                    response = requests.get(image_url)
                    if response.status_code == 200:
                        # Create a file-like object from the image content
                        image_content = response.content
                        # Use the image URL's filename as the uploaded file name
                        image_filename = image_url.split('/')[-1]
                        # Create a SimpleUploadedFile object with the image content
                        uploaded_image = SimpleUploadedFile(image_filename, image_content)

                # Create the Items object with the retrieved Category instance
                item_data = {
                    'nama': row['nama'],
                    'category': category_instance,
                    'quantity': row['quantity'],
                    'unit': row['unit'],
                    'price': row['price'],
                    'price_currency' : row['price_currency'],
                    'upload_type': 'bulk'
                }
                if 'gambar' in row and row['gambar']:
                    item_data['gambar'] = uploaded_image

                item = Items.objects.create(**item_data)
                # item.upload_type = "bulk"
                success_count += 1
            except Exception as e:
                error_messages.append(f"Error in row {row_number}: {str(e)}")

        if error_messages:
            return JsonResponse({'success': False, 'errors': error_messages,'message':f"{success_count} items imported successfully."})
        else:
            return JsonResponse({'success': True, 'message': f"{success_count} items imported successfully."})

    return render(request, 'item/upload_csv.html')

import re
def upload_excel(request):
    error_message = []
    processed_items = []
    categories = Category.objects.all()
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                excel_file = request.FILES['excel_file']
                wb = openpyxl.load_workbook(excel_file)
                worksheet = wb.active

                # Get column titles from the first row
                header_row = next(worksheet.iter_rows(values_only=True))
                column_titles = [str(cell).strip().lower() for cell in header_row]

                
                # Get column indices based on titles
                nama_index = column_titles.index('nama') if 'nama' in column_titles else None
                catatan_index = column_titles.index('catatan') if 'catatan' in column_titles else None
                category_index = column_titles.index('category') if 'category' in column_titles else None
                quantity_index = column_titles.index('quantity') if 'quantity' in column_titles else None
                unit_index = column_titles.index('unit') if 'unit' in column_titles else None
                price_index = column_titles.index('price') if 'price' in column_titles else None
                price_currency_index = column_titles.index('price_currency') if 'price_currency' in column_titles else None

                # Find the row containing the 'Gambar' column title
                gambar_row_index = None
                for row_index, row in enumerate(worksheet.iter_rows(values_only=True)):
                    if 'gambar' in [str(cell).strip().lower() for cell in row]:
                        gambar_row_index = row_index
                        break

                if gambar_row_index is not None:
                    # Load image from the 'Gambar' column for each row
                    image_loader = SheetImageLoader(worksheet)
                    for row_index, row in enumerate(worksheet.iter_rows(min_row=gambar_row_index + 2, values_only=True)):
                        try: 
                            # Extract category information
                            category_name = row[category_index] if category_index is not None else ''
                            category_instance, _ = Category.objects.get_or_create(name=category_name)

                            # Load image from specified cell
                            image_cell = chr(65 + column_titles.index('gambar')) + str(row_index + 2)
                            image = image_loader.get(image_cell)

                            image = image.resize((100, 100), Image.Resampling.LANCZOS)
                            regex_pattern = r'/'
                            replacement_string = '-'
                            
                            # Generate filename including item name, upload date, and row index
                            item_name = row[nama_index] if nama_index is not None else ''
                            item_name_cleaned = re.sub(regex_pattern, replacement_string, item_name)
                            upload_date = datetime.date.today().strftime('%Y-%m-%d')
                            filename = f"media_bulk_{item_name_cleaned}_{upload_date}_{row_index}.jpg"
                            
                            # Specify the full path including the media directory
                            image_path = os.path.join(settings.MEDIA_ROOT, filename)
                            
                            # Save the image to the media directory
                            image.save(image_path)

                            # Extract price currency or use default value 'IDR'
                            price_currency = row[price_currency_index] if price_currency_index is not None else 'IDR'

                            # Create and save instance with image path
                            instance = Items(
                                nama=row[nama_index] if nama_index is not None else '',
                                catatan=row[catatan_index] if catatan_index is not None else '',
                                category=category_instance,
                                quantity=row[quantity_index] if quantity_index is not None else 0,
                                unit=row[unit_index] if unit_index is not None else '',
                                price=row[price_index] if price_index is not None else 0,
                                price_currency=price_currency,
                                gambar=filename,
                                upload_type="bulk"
                            )
                            instance.save()
                            processed_items.append(instance)
                    
                        except Exception as e:
                            error_message.append(f"Error on cell {row_index + 1}: {str(e)}")
                            print(processed_items)
                            continue
                else:
                    # Handle case where 'Gambar' column title is not found
                    raise ValueError("'gambar' column title not found in the Excel file")
                
                return render(request, 'item/upload_excel.html', {'form': form, 'categories': categories, 'error_message': error_message, 'processed_items': processed_items})
                
            except openpyxl.utils.exceptions.InvalidFileException:
                error_message = "Invalid Excel file format. Please upload a valid Excel file."
            except ValueError as e:
                error_message = str(e)
        else:
            error_message = "Invalid form data. Please check your input and try again."

    else:
        form = ExcelUploadForm()
    
    # Render the upload form template
    return render(request, 'item/upload_excel.html', {'form': form, 'categories': categories, 'error_message': error_message})


# -------------------- Delete multiple items -------------------- #
def delete_selected_rows(request, model, key):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids[]')  # Assuming you're sending an array of selected IDs
        try:
            selected_items = model.objects.filter(**{f'{key}__in': selected_ids})

            # Additional logic for image deletion if applicable
            if hasattr(model, 'gambar'):
                for item in selected_items:
                    image_path = os.path.join(settings.MEDIA_ROOT, str(item.gambar))
                    if os.path.exists(image_path):
                        os.remove(image_path)
                    else:
                        print(f"Image file not found: {image_path}")

            selected_items.delete()  # Delete the selected rows from the database
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
def delete_selected_rows_item(request):
    return delete_selected_rows(request, Items, 'SKU')

def delete_selected_rows_cust(request):
    return delete_selected_rows(request, Customer, 'cust_id')

def delete_selected_rows_supp(request):
    return delete_selected_rows(request, Supplier, 'supp_id')

def delete_selected_rows_PO(request):
    return delete_selected_rows(request, PurchaseOrder, 'id')

def delete_selected_rows_WO(request):
    return delete_selected_rows(request, WorkOrder, 'id')
def add_additional_address(request):
    if request.method == 'POST':
        form = AdditionalAddressForm(request.POST)
        if form.is_valid():
            form.save()  # This saves the form data to the database
            return redirect('/calendar')
    else:
        form = AdditionalAddressForm()
    
    return render(request, 'delivery/add_delivery_address.html', {'form': form})


# -------------------- Log Book Basics -------------------- #
@login_required
@FO_Only
def add_log(request):
    start_param = request.GET.get('start')
    end_param = request.GET.get('end')
    initial_data = {'start': start_param, 'end': end_param}
    return add_entity_view(request, LogBookForm, 'log_book/add_log.html', 'log_book', initial=initial_data)

@login_required
@FO_Only
def log_book(request):  
    all_events = LogBook.objects.all()
    context = {
        "events":all_events,
    }
    return render(request,'log_book/log-book.html',context)

@login_required
@FO_Only
def lb_all_events(request):                                                                                                 
    all_events = LogBook.objects.all()                                                                                    
    out = []                                                                                                             

    for event in all_events: 
        event.start = event.start.astimezone(timezone.get_current_timezone())                                                                                            
        event.end = event.end.astimezone(timezone.get_current_timezone())                                                                                            
        out.append({     
            'nama': event.nama,                                                                                    
            'id': event.id,                                                                                              
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),                                                         
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),                                                       
        })                                                                                                               
                                                                                                                      
    return JsonResponse(out, safe=False) 
 
@login_required
@FO_Only
def lb_add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    nama = request.GET.get("nama", None)
    event = LogBook(name=str(nama), start=start, end=end)
    event.save()
    data = {}
    return JsonResponse(data)
 
@login_required
@FO_Only
def lb_update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    nama = request.GET.get("nama", None)
    id = request.GET.get("id", None)
    event = LogBook.objects.get(id=id)
    event.start = start
    event.end = end
    event.nama = nama
    event.save()
    data = {}
    return JsonResponse(data)
 
@login_required
@FO_Only
def lb_remove(request):
    id = request.GET.get("id", None)
    event = LogBook.objects.get(id=id)
    event.delete()
    data = {}
    return JsonResponse(data)

@login_required
@FO_Only
def log_detail(request, id):
    return entity_detail(request, LogBook, LogBookForm, "id", id, 'log_book/log_detail.html')

@login_required
@FO_Only
def edit_log(request, id):
    return edit_entity(request, LogBook, LogBookForm, 'id', id)

@login_required
@FO_Only
def delete_log(request, id):
    return delete_entity(request, LogBook, 'id', id)
