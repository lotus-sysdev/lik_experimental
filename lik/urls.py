from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('display_report/', display_report, name='display_report'),
    path('delete_selected_rows_report/', delete_selected_rows_report, name='delete_selected_rows_report'),
    path('add_report/', add_report, name='add_report'),
    path('report_detail/<int:id>/', report_detail, name='report_detail'),
    path('edit_report/<int:id>/', edit_report, name='edit_report'),
    path('delete_report/<int:id>/', delete_report, name='delete_report'),
    path('add_report_mobile/', add_report_mobile.as_view(), name='add_report_mobile'),
]

