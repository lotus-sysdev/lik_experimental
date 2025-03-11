# Standard library imports
import os
import json
import uuid
import pytz
import logging

# Third-party imports
from itertools import groupby
from operator import itemgetter
from PIL import Image, ImageFile
from collections import defaultdict
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, permission_classes

# Local application imports
from .forms import *
from .models import *
from .serializers import *
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import traceback


# Set up logger
logger = logging.getLogger(__name__)
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from django.http import JsonResponse
from django.db.models import Count, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models.functions import ExtractDay, ExtractMonth, ExtractYear, Upper


# -------------------- Dashboard --------------------#
def dashboard(request):
    form = ReportFilterForm(request.GET)

    if form.is_valid():
        kayu = form.cleaned_data.get('kayu')
        sender = form.cleaned_data.get('sender')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')

        reports = Report.objects.all()
        if kayu:
            reports = reports.filter(kayu=kayu)
        if sender:
            reports = reports.filter(sender__username=sender)
        if start_date and end_date:
            reports = reports.filter(tanggal__range=[start_date, end_date])


        sender_name = "All Senders" 
        if sender:
            sender = User.objects.get(username=sender)
            sender_name = sender.first_name  

        kayu_counts = reports.values('kayu').annotate(count=Count('id'))
        sender_counts = reports.values('sender__first_name').annotate(count=Count('id'))

        plat_data = reports.annotate(
            upper_plat=Upper('plat')
        ).values(
            'upper_plat', 'tanggal', 'sender__first_name', 'driver', 'tujuan'
        ).annotate(count=Count('id')).order_by('upper_plat', 'tanggal')

        grouped_plat_data = []
        for key, group in groupby(plat_data, key=itemgetter('upper_plat')):
            group_list = list(group)
            earliest_date = group_list[0]['tanggal']

            tujuan_counter = defaultdict(int)

            for item in group_list:
                tujuan_counter[item['tujuan']] += item['count']

            grouped_plat_data.append({
                'upper_plat': key,
                'senders': list(set(item['sender__first_name'] for item in group_list)),
                'drivers': list(set(item['driver'] for item in group_list)),
                'count': sum(item['count'] for item in group_list),
                'tujuan': list(tujuan_counter.keys()),
                'tujuan_count': dict(tujuan_counter),
                'earliest_date': earliest_date.isoformat(),            })

        grouped_plat_data = sorted(grouped_plat_data, key=lambda x: x['earliest_date'])
        tonase_counts = reports.values(
            'kayu',
            day=ExtractDay('tanggal'),
            month=ExtractMonth('tanggal'),
            year=ExtractYear('tanggal')
        ).annotate(berat=Sum('berat'))
        unique_vehicle_counts = reports.values(
            upper_plat=Upper('plat'),
            day=ExtractDay('tanggal'),
            month=ExtractMonth('tanggal'),
            year=ExtractYear('tanggal')
        ).values('day', 'month', 'year', 'tujuan').annotate(count=Count('id', distinct=True))
        vehicle_kayu_counts = reports.values(
            'kayu',
            upper_plat=Upper('plat'),
            day=ExtractDay('tanggal'),
            month=ExtractMonth('tanggal'),
            year=ExtractYear('tanggal')
        ).annotate(count=Count('upper_plat', distinct=True))
        data_AllTujuan_counts = reports.values(
            day=ExtractDay('tanggal'),
            month=ExtractMonth('tanggal'),
            year=ExtractYear('tanggal')
        ).values('day', 'month', 'year', 'tujuan')\
        .annotate(count=Count('id'))\
        .order_by('year', 'month', 'day') 

        # Serialize the counts data
        kayu_counts_serialized = json.dumps(list(kayu_counts))
        sender_counts_serialized = json.dumps(list(sender_counts))
        plat_counts_serialized = json.dumps(grouped_plat_data)
        tonase_counts_serialized = json.dumps(list(tonase_counts))
        unique_vehicle_serialized = json.dumps(list(unique_vehicle_counts))
        vehicle_kayu_serialized = json.dumps(list(vehicle_kayu_counts))
        data_dmy_tujuan = json.dumps(list(data_AllTujuan_counts))

        total_reports = reports.count()
        total_revised_reports = reports.filter(tiketId__icontains="R").count()
        total_tonase = reports.aggregate(total=Sum('berat'))['total'] or 0
        total_rejects = reports.aggregate(total=Sum('reject'))['total'] or 0
        total_unique_vehicles = reports.annotate(upper_plat=Upper('plat')).values('plat').distinct().count()
        # tonase_counts = reports.annotate(
        #     day=ExtractDay('tanggal'),
        #     month=ExtractMonth('tanggal'),
        #     year=ExtractYear('tanggal')
        # ).values('day', 'month', 'year').annotate(
        #     total_berat=Sum('berat')
        # ).order_by('year', 'month', 'day')

        # tonase_counts_serialized = json.dumps(list(tonase_counts))
        

    else: 
        reports = Report.objects.all()
        kayu_counts = Report.objects.values('kayu').annotate(count=Count('id'))
        sender_counts = Report.objects.values('sender__first_name').annotate(count=Count('id'))

        sender_name = "All Senders"  
        if sender:
            sender = User.objects.get(username=sender)
            sender_name = sender.first_name 

        plat_data = reports.annotate(
            upper_plat=Upper('plat')
        ).values(
            'upper_plat', 'tanggal', 'sender__first_name', 'driver', 'tujuan'
        ).annotate(count=Count('id')).order_by('upper_plat')

        grouped_plat_data = []
        for key, group in groupby(plat_data, key=itemgetter('upper_plat', 'tanggal')):
            group_list = list(group)
            earliest_date = group_list[0]['tanggal']  

            tujuan_counter = defaultdict(int)

            for item in group_list:
                tujuan_counter[item['tujuan']] += item['count']

            grouped_plat_data.append({
                'upper_plat': key,
                'senders': list(set(item['sender__first_name'] for item in group_list)),
                'drivers': list(set(item['driver'] for item in group_list)),
                'count': sum(item['count'] for item in group_list),
                'tujuan': list(tujuan_counter.keys()),
                'tujuan_count': dict(tujuan_counter),
                'earliest_date': earliest_date.isoformat(),
                
            })

        grouped_plat_data = sorted(grouped_plat_data, key=lambda x: x['earliest_date'])
        tonase_counts = Report.objects.annotate(
            'kayu',
            day=ExtractDay('tanggal'),
            month=ExtractMonth('tanggal'),
            year=ExtractYear('tanggal')
        ).annotate(berat=Sum('berat'))
        unique_vehicle_counts = Report.objects.annotate(
            upper_plat=Upper('plat'),
            day=ExtractDay('tanggal'),
            month=ExtractMonth('tanggal'),
            year=ExtractYear('tanggal')
        ).values('day', 'month', 'year', 'tujuan').annotate(count=Count('upper_plat', distinct=True))
        vehicle_kayu_counts = Report.objects.annotate(
            'kayu',
            upper_plat=Upper('plat'),
            day=ExtractDay('tanggal'),
            month=ExtractMonth('tanggal'),
            year=ExtractYear('tanggal')
        ).annotate(count=Count('upper_plat', distinct=True))
        data_AllTujuan_counts = reports.values(
            day=ExtractDay('tanggal'),
            month=ExtractMonth('tanggal'),
            year=ExtractYear('tanggal')
        ).values('day', 'month', 'year', 'tujuan').annotate(count=Count('id'))


        kayu_counts_serialized = json.dumps(list(kayu_counts))
        sender_counts_serialized = json.dumps(list(sender_counts))
        plat_counts_serialized = json.dumps(grouped_plat_data)
        tonase_counts_serialized = json.dumps(list(tonase_counts))
        unique_vehicle_serialized = json.dumps(list(unique_vehicle_counts))
        vehicle_kayu_serialized = json.dumps(list(vehicle_kayu_counts))
        data_dmy_tujuan = json.dumps(list(data_AllTujuan_counts))
        # tonase_counts = reports.annotate(
        #     day=ExtractDay('tanggal'),
        #     month=ExtractMonth('tanggal'),
        #     year=ExtractYear('tanggal')
        # ).values('day', 'month', 'year').annotate(
        #     total_berat=Sum('berat')
        # ).order_by('year', 'month', 'day')

       
        # tonase_counts_serialized = json.dumps(list(tonase_counts))
        
        total_reports = Report.objects.count()
        total_revised_reports = reports.filter(tiketId__icontains="R").count()
        total_tonase = Report.objects.aggregate(total=Sum('berat'))['total'] or 0
        total_rejects = Report.objects.aggregate(total=Sum('reject'))['total'] or 0
        total_unique_vehicles = Report.objects.values('plat').distinct().count()

        print(grouped_plat_data)

    

    # Serialize the tonase data to JSON for frontend

    context = {
        'form' : form,
        'reports' : reports,
        'kayu_counts': kayu_counts_serialized,
        'sender_name': sender_name,
        'sender_counts': sender_counts_serialized,
        'plat_counts': grouped_plat_data,
        'tonase_counts': tonase_counts_serialized,
        'unique_vehicle_counts': unique_vehicle_serialized,
        'data_AllTujuan_counts' : data_dmy_tujuan,
        'vehicle_kayu_counts': vehicle_kayu_serialized,
        'total_revised_reports': total_revised_reports,
        'total_reports': total_reports,
        'total_tonase': total_tonase,
        'total_rejects': total_rejects,
        'total_unique_vehicles': total_unique_vehicles,
    }

    return render(request, 'dashboard.html', context)


# -------------------- Common Functions --------------------#
def delete_selected_rows(request, model, key):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids[]')  # Assuming you're sending an array of selected IDs
        try:
            selected_items = model.objects.filter(**{f'{key}__in': selected_ids})

            # Additional logic for image deletion if applicable
            if hasattr(model, 'foto') and hasattr(model, 'og_foto'):
                for item in selected_items:
                    image_path = os.path.join(settings.MEDIA_ROOT, str(item.foto))
                    og_image_path = os.path.join(settings.MEDIA_ROOT, str(item.og_foto))
                    if os.path.exists(image_path) and os.path.exists(og_image_path):
                        os.remove(image_path)
                        os.remove(og_image_path)
                    else:
                        print(f"Image file not found:\nResized Image: {image_path}\nOriginal Image: {og_image_path}")
                    

            selected_items.delete()  # Delete the selected rows from the database
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

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

def entity_detail(request, entity_model, entity_form, entity_id_field, entity_id, template_name, extra_context=None):
    entity = get_object_or_404(entity_model, **{entity_id_field: entity_id})
    form = entity_form(instance=entity)
    context = {'entity': entity, 'form': form, 'entity_id': entity_id}

    if extra_context:
        context.update(extra_context)

    return render(request, template_name, context)

def delete_entity(request, entity_model, entity_id_field, entity_id):
    entity = get_object_or_404(entity_model, **{entity_id_field: entity_id})

    if request.method == 'POST':
        entity.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
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

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_completed_status(request):
    if request.method == 'POST':
        ids = request.POST.getlist('ids[]')  # Get list of IDs
        status = request.POST.get('status')  # This will be True or False

        if not ids or status is None:
            return JsonResponse({"error": "Invalid data"}, status=400)

        # Convert status to a boolean (it might come as a string)
        status = True if status == 'true' else False

        # Update the 'completed' status for selected reports
        updated_count = Report.objects.filter(id__in=ids).update(completed=status)

        return JsonResponse({"success": True, "updated_count": updated_count})
    return JsonResponse({"error": "Invalid method"}, status=405)


def approve_transfer(request):
    try:
        if request.user.groups.filter(name__in=['Accounting', 'GA']).exists():
            # Get selected report IDs and transfer date with time
            selected_ids = request.POST.getlist('ids[]')
            transfer_date_str = request.POST.get('transfer_date')

            if not selected_ids:
                return JsonResponse({"status": "error", "message": "No reports selected."})

            if not transfer_date_str:
                return JsonResponse({"status": "error", "message": "No transfer date provided."})

            # Attempt to parse the combined date and time
            jakarta_timezone = pytz.timezone('Asia/Jakarta')

            try:
                transfer_date = datetime.fromisoformat(transfer_date_str)  # Parse ISO datetime string (YYYY-MM-DDTHH:MM)
            except ValueError as e:
                logger.error(f"Invalid transfer date format: {e}")
                return JsonResponse({"status": "error", "message": "Invalid date format."})

            # Ensure the parsed datetime is timezone-aware
            if transfer_date.tzinfo is None:
                transfer_date = jakarta_timezone.localize(transfer_date)  # Localize to Asia/Jakarta timezone

            # Set the exact time (including the time zone) if it's already aware
            for report_id in selected_ids:
                report = Report.objects.get(id=report_id)
                report.tanda_transaksi = transfer_date  # Store the timezone-aware datetime object
                report.save()

            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "message": "You don't have permission to approve transfers."})

    except Exception as e:
        logger.error(f"Error in approve_transfer view: {e}")
        return JsonResponse({"status": "error", "message": "An unexpected error occurred."})


# -------------------- Report Functions --------------------#
@login_required
def display_report_items(request):
    # Dapatkan parameter untuk pencarian
    search_date = request.GET.get('search_date')
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Ambil data dari model Report
    queryset = Report.objects.all()

    # Pencarian berdasarkan tanggal (search_date)
    if search_date:
        try:
            # Mengubah string tanggal menjadi objek datetime
            search_date = datetime.strptime(search_date, '%Y-%m-%d').date()

            # Membuat waktu mulai dan berakhir untuk hari tersebut
            start_of_day = datetime.combine(search_date, datetime.min.time())  # 00:00:00
            end_of_day = start_of_day + timedelta(days=1) - timedelta(seconds=1)  # 23:59:59

            # Pastikan waktu berada di zona waktu Asia/Jakarta
            jakarta_timezone = pytz.timezone('Asia/Jakarta')

            # Konversi start_of_day dan end_of_day ke waktu lokal Jakarta
            start_of_day = jakarta_timezone.localize(start_of_day)  
            end_of_day = jakarta_timezone.localize(end_of_day)  

            # Gunakan `date_time__date` untuk memfilter berdasarkan tanggal tanpa memperhatikan waktu
            queryset = queryset.filter(date_time__date=search_date)

        except ValueError:
            pass  # Tangani error jika format tanggal salah

    # Pencarian berdasarkan rentang tanggal start_date_str dan end_date_str
    if start_date_str and end_date_str:
        try:
            # Mengubah string tanggal menjadi objek datetime
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')

            # Filter rentang tanggal
            queryset = queryset.filter(tanggal__range=[start_date, end_date])

        except ValueError:
            pass  # Tangani error jika format tanggal salah

    # Filtering berdasarkan kolom pencarian lainnya
    search_column = request.GET.get('search_column')
    search_value = request.GET.get('search_value')

    if search_column and search_value:
        column_fields = [
            'date_time', 'id', 'sender__first_name', 'tiketId', 'plat', 'driver', 
            'PO', 'DO', 'no_tiket', 'kayu', 'berat', 'reject', 'lokasi', 'tujuan', 
            'tanggal', 'completed', 'foto', 'og_foto', 'tanda_transaksi'
        ]
        
        if 0 <= int(search_column) < len(column_fields):
            column_field = column_fields[int(search_column)]
            if column_field == 'completed':
                if search_value == 'Yes':
                    queryset = queryset.filter(completed=True)
                elif search_value == 'No':
                    queryset = queryset.filter(completed=False)
            else:
                queryset = queryset.filter(**{f"{column_field}__icontains": search_value})

    # Penerapan sorting berdasarkan kolom
    order_column_index = int(request.GET.get('order[0][column]', 0))
    order_direction = request.GET.get('order[0][dir]', 'desc')

    column_fields = [
        'date_time', 'id', 'sender__first_name', 'tiketId', 'plat', 'driver', 
        'PO', 'DO', 'no_tiket', 'kayu', 'berat', 'reject', 'lokasi', 'tujuan', 
        'tanggal', 'completed', 'foto', 'og_foto', 'tanda_transaksi'
    ]
    order_field = column_fields[order_column_index]

    if order_direction == 'asc':
        queryset = queryset.order_by(order_field)
    else:
        queryset = queryset.order_by(f'-{order_field}')

    # Kalkulasi total
    total_berat = queryset.aggregate(Sum('berat'))['berat__sum'] or 0
    total_reject = queryset.aggregate(Sum('reject'))['reject__sum'] or 0
    unique_plat_count = queryset.values('plat').count()

    # Pagination
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 25))

    paginator = Paginator(queryset, length)
    page_number = (start // length) + 1

    try:
        entities_page = paginator.page(page_number)
    except PageNotAnInteger:
        entities_page = paginator.page(1)
    except EmptyPage:
        entities_page = paginator.page(paginator.num_pages)

    data = list(entities_page.object_list.values(
        'date_time', 'id', 'sender__first_name', 'tiketId', 'plat', 'driver', 
        'PO', 'DO', 'no_tiket', 'kayu', 'berat', 'reject', 'lokasi', 'tujuan', 
        'tanggal', 'completed', 'foto', 'og_foto', 'tanda_transaksi'
    ))

    for item in data:
        item['completed'] = item['completed']

    response = {
        'draw': draw,
        'recordsTotal': paginator.count,
        'recordsFiltered': paginator.count,
        'data': data,
        'total_berat': total_berat,
        'total_reject': total_reject,
        'unique_plat_count': unique_plat_count,
    }

    return JsonResponse(response)

def display_report(request):
    user_is_admin = request.user.groups.filter(name__in=['Accounting', 'GA']).exists() if request.user.is_authenticated else False
    return render(request, 'Report/display_report.html', {'user_is_admin': user_is_admin})



@login_required
def delete_selected_rows_report(request):
    return delete_selected_rows(request, Report, 'id')

@login_required
def add_report(request, initial=None):
    entity_form_instance = ReportForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save(commit=False)
            foto = request.FILES.get('foto')
            og_foto = request.FILES.get('og_foto')

            if foto:
                resized_foto_path = process_image(foto, False)
                form.instance.foto = resized_foto_path
                report.save()
            if og_foto:
                resized_og_foto_path = process_image(og_foto, True)
                form.instance.og_foto = resized_og_foto_path
                report.save()

            report.save()
            return redirect('display_report')
    else:
        print(initial)
        if (initial):
            form = (ReportForm(initial=initial))
            entity_form_instance = form
        else: 
            form = ReportForm()

    return render(request, 'Report/add_report.html', {'entity_form': entity_form_instance})

@login_required
def report_detail(request, id):
    return entity_detail(request, Report, ReportForm, 'id', id, 'Report/report_detail.html')

@login_required
def delete_report(request, id):
    return delete_entity(request, Report, 'id', id)

@login_required
def edit_report(request, id):
    entity = get_object_or_404(Report,id = id)
    
    # Fetch the latest tiketId for the given report object
    latest_tiketId = entity.tiketId
    
    # Check if the latest tiketId already contains an index
    if 'R' in latest_tiketId:
        # Extract the index from the latest tiketId
        base_tiketId, current_index = latest_tiketId.rsplit('R', 1)
        try:
            index = int(current_index)
            index += 1
        except ValueError:
            # If the index is not an integer, start from 1
            index = 1
        new_tiketId = f"{base_tiketId}R{index}"
    else:
        new_tiketId = f"{latest_tiketId}R1"
    
    if request.method == 'POST':
        form = ReportForm(request.POST, request.FILES, instance=entity)
        
        if form.is_valid():
            # Set the new tiketId before saving the form
            form.instance.tiketId = new_tiketId
            # Check if a new image file is provided
            foto = request.FILES.get('foto')
            og_foto = request.FILES.get('og_foto')

            if foto:
                resized_foto_path = process_image(foto, False)
                form.instance.foto = resized_foto_path
            if og_foto:
                resized_og_foto_path = process_image(og_foto, True)
                form.instance.og_foto = resized_og_foto_path

            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ReportForm(instance=entity)
    
    return render(request, "/api/edit_report.html", {'form': form})

def process_image(image, is_original):
    upload_date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    img = Image.open(image)

    # Generate a unique identifier
    unique_id = str(uuid.uuid4())[:8]  # Use the first 8 characters of a UUID
    
    # Strip file extension from the image filename
    image_name_without_extension, extension = os.path.splitext(image.name)
    
    # Resize the image
    if is_original:
        resized_img = img.resize((500, 500))
    else:
        resized_img = img.resize((100, 100))
    
    # Construct the resized image name
    if is_original:
        resized_image_name = f"original-{upload_date}-{unique_id}-{extension}"
    else:
        resized_image_name = f"resized-{upload_date}-{unique_id}-{extension}"
    
    # Save the resized image
    resized_image_path = os.path.join(settings.MEDIA_ROOT, 'report_photos', resized_image_name)
    resized_img.save(resized_image_path)

    relative_path = os.path.relpath(resized_image_path, settings.MEDIA_ROOT )
    
    return relative_path
            

# -------------------- Functions for mobile app --------------------#
# Set maximum image quality
ImageFile.MAXBLOCK = 2**20
class add_report_mobile(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        try:
            # Get image from request
            image_data = self.request.FILES.get('foto')

            if not image_data:
                raise ValueError("No image provided")

            print("Received Image:", image_data.name)

            # Open image using PIL
            image = Image.open(image_data)
            upload_date = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

            # Generate new file names
            og_image_name = f'original-{upload_date}-{image_data.name}'
            resized_image_name = f'resized-{upload_date}-{image_data.name}'

            # Paths for saving images
            og_image_path = os.path.join('report_photos', og_image_name)
            resized_image_path = os.path.join('report_photos', resized_image_name)

            # Resize and save original image
            og_image = image.resize((500, 500), Image.Resampling.LANCZOS)
            og_image_io = ContentFile(b"")
            og_image.save(og_image_io, format='JPEG', optimize=True, quality=95)
            og_image_file = default_storage.save(og_image_path, og_image_io)

            # Resize and save resized image
            resized_image = image.resize((100, 100))
            resized_image_io = ContentFile(b"")
            resized_image.save(resized_image_io, format='JPEG')
            resized_image_file = default_storage.save(resized_image_path, resized_image_io)

            # Assign file paths to serializer
            serializer.validated_data['og_foto'] = og_image_file
            serializer.validated_data['foto'] = resized_image_file

            # Save to DB
            serializer.save()

        except Exception as e:
            print("Error processing image:", str(e))
            traceback.print_exc()  # Print full error traceback
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password') 
    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        groups = list(user.groups.values_list('id', flat=True))
        serializedUser = UserSerializer(user)
        print(groups)
        return Response({'token': token.key, 'groups': groups, 'user' : serializedUser.data}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)  

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)

# @permission_classes([IsAuthenticated])
class GroupLokasiListAPIView(generics.ListAPIView):
    serializer_class = LokasiSerializer

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        group_lokasis = Group_Lokasi.objects.filter(group_id=group_id)
        lokasi_ids = [lokasi.id for group_lokasi in group_lokasis for lokasi in group_lokasi.lokasi.all()]
        return Lokasi.objects.filter(id__in=lokasi_ids)
    
# @permission_classes([IsAuthenticated])
class GroupTujuanListAPIView(generics.ListAPIView):
    serializer_class = TujuanSerializer

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        group_tujuans = Group_Tujuan.objects.filter(group_id=group_id)
        tujuan_ids = [tujuan.id for group_tujuan in group_tujuans for tujuan in group_tujuan.tujuan.all()]
        return Tujuan.objects.filter(id__in=tujuan_ids)

# @permission_classes([IsAuthenticated])
class GroupKayuListAPIView(generics.ListAPIView):
    serializer_class = KayuSerializer

# @permission_classes([IsAuthenticated])
class GroupKayuListAPIView(generics.ListAPIView):
    serializer_class = KayuSerializer
    def get_queryset(self):
        group_id = self.kwargs['group_id']
        group_kayus = Group_Kayu.objects.filter(group_id=group_id)
        kayu_ids = [kayu.id for group_kayu in group_kayus for kayu in group_kayu.kayu.all()]
        return Kayu.objects.filter(id__in=kayu_ids)

@api_view(['GET'])
def check_token(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        try:
            user_token = Token.objects.get(user=user)
            return Response({"token": user_token.key}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"token": ""}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    

# -------------------- Admin Change Groups --------------------#
@login_required
def display_group(request):
    group_lokasi = Group_Lokasi.objects.all()
    group_tujuan = Group_Tujuan.objects.all()
    group_kayu = Group_Kayu.objects.all()

    group_data = {}

    for gl in group_lokasi:
        group_id = gl.group.id
        group_data.setdefault(group_id, {'group': gl.group, 'lokasi': set(), 'tujuan': set(), 'kayu': set()})
        group_data[group_id]['lokasi'] |= set(gl.lokasi.all())

    for gt in group_tujuan:
        group_id = gt.group.id
        group_data.setdefault(group_id, {'group': gt.group, 'lokasi': set(), 'tujuan': set(), 'kayu': set()})
        group_data[group_id]['tujuan'] |= set(gt.tujuan.all())

    for gk in group_kayu:
        group_id = gk.group.id
        group_data.setdefault(group_id, {'group': gk.group, 'lokasi': set(), 'tujuan': set(), 'kayu': set()})
        group_data[group_id]['kayu'] |= set(gk.kayu.all())

    group_data_list = list(group_data.values())

    # Retrieve all Kayu, Lokasi, and Tujuan objects
    all_kayu = Kayu.objects.all()
    all_lokasi = Lokasi.objects.all()
    all_tujuan = Tujuan.objects.all()

    return render(request, 'Group/display_groups.html', {'group_data': group_data_list, 'all_kayu': all_kayu, 'all_lokasi': all_lokasi, 'all_tujuan': all_tujuan})

@login_required
@transaction.atomic
def save_group_changes(request):
    if request.method == 'POST':
        group_id = request.POST.get('group_id')
        kayu_ids = request.POST.getlist('kayu_ids[]')
        lokasi_ids = request.POST.getlist('lokasi_ids[]')
        tujuan_ids = request.POST.getlist('tujuan_ids[]')

        try:
            # Retrieve the group object using name
            group = Group.objects.get(name=group_id)

            # Delete existing object
            Group_Kayu.objects.filter(group=group).delete()
            Group_Tujuan.objects.filter(group=group).delete()
            Group_Lokasi.objects.filter(group=group).delete()

            # Create a single Group_Kayu instance and add all kayu_ids to it
            group_kayu_instance = Group_Kayu.objects.create(group=group)
            group_kayu_instance.kayu.add(*kayu_ids)

            # Similar process for Group_Lokasi and Group_Tujuan
            group_lokasi_instance = Group_Lokasi.objects.create(group=group)
            group_lokasi_instance.lokasi.add(*lokasi_ids)

            group_tujuan_instance = Group_Tujuan.objects.create(group=group)
            group_tujuan_instance.tujuan.add(*tujuan_ids)
            
            return JsonResponse({'success': True})
        except Group.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Group not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
        
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
  
@login_required
def display_foto(request, url):
    # Get the URL parameter 'url' from the request

    # Render the display_image.html template with the image_url context variable
    return render(request, 'Report/display_foto.html', {'url': url})


class ReportSummaryView(generics.GenericAPIView):
    serializer_class = ReportSummarySerializer

    def get(self, request, sender_id):
        # Get start and end date from request parameters
        start_date_str = request.GET.get('start_date')
        end_date_str = request.GET.get('end_date')

        # Set default values to the first and last day of the current month if not provided
        if not start_date_str:
            start_date = datetime.now().replace(day=1).date()
        else:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()

        if not end_date_str:
            next_month = datetime.now().replace(day=28) + timedelta(days=4)
            end_date = (next_month - timedelta(days=next_month.day)).date()
        else:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

        reports = Report.objects.filter(sender_id=sender_id, tanggal__range=(start_date, end_date))
        summary = reports.values('kayu').annotate(
            total_plat=Count('plat', distinct=True),
        )

        return Response(summary)