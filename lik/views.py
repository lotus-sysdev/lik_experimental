from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import generics, status

from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate

from .serializers import *
from .models import *
from .forms import *
# Create your views here.
def delete_selected_rows(request, model, key):
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids[]')  # Assuming you're sending an array of selected IDs
        try:
            selected_items = model.objects.filter(**{f'{key}__in': selected_ids})

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

def display_report(request):
    entities = Report.objects.all()
    return render(request, 'Report/display_report.html', {'entities': entities})

def delete_selected_rows_report(request):
    return delete_selected_rows(request, Report, 'id')

def add_report(request, initial=None):
    entity_form_instance = ReportForm(request.POST or None)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect(redirect_template)
    else:
        print(initial)
        if (initial):
            form = (ReportForm(initial=initial))
            entity_form_instance = form
        else: 
            form = ReportForm()

    return render(request, 'Report/add_report.html', {'entity_form': entity_form_instance})

def report_detail(request, id):
    return entity_detail(request, Report, ReportForm, 'id', id, 'Report/report_detail.html')

def delete_report(request, id):
    return delete_entity(request, Report, 'id', id)

def edit_report(request, id):
    return edit_entity(request, Report, ReportForm, 'id', id)

class add_report_mobile(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

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
        # Get user's groups
        groups = list(user.groups.values_list('id', flat=True))
        # Include groups in response data
        return Response({'token': token.key, 'groups': groups}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_200_OK)

@permission_classes([IsAuthenticated])
def tujuan_options_list(request):
    # Sample dictionary data
    options = [
        {'label': 'Sumatra Prima Fiberboard', 'value': 'spf'},
        {'label': 'Cipta Mandala', 'value': 'cipta-mandala'},
    ]
    return JsonResponse(options, safe=False)

@permission_classes([IsAuthenticated])
def lokasi_options_list(request):
    # Sample dictionary data
    lokasi_options = [
        {'label': 'Muara Enim', 'value': 'muara-enim'},
        {'label': 'Perkebunan Rakyat', 'value': 'perkebunan-rakyat'},
        {'label': 'Gunung Rajo', 'value': 'gunung-rajo'},
    ]
    return JsonResponse(lokasi_options, safe=False)

class GroupLokasiListAPIView(generics.ListAPIView):
    serializer_class = LokasiSerializer

    def get_queryset(self):
        group_id = self.kwargs['group_id']
        lokasi_ids = Group_Lokasi.objects.filter(group_id=group_id).values_list('lokasi_id', flat=True)
        return Lokasi.objects.filter(id__in=lokasi_ids)