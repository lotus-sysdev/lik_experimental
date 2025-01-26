from django.urls import path
from .views import *

urlpatterns = [    
    path('dashboard/', dashboard, name='dashboard'),
    path('display_report/', display_report, name='display_report'),
    path('display_report_items/', display_report_items, name='display_report_items'),
    path('delete_selected_rows_report/', delete_selected_rows_report, name='delete_selected_rows_report'),
    path('add_report/', add_report, name='add_report'),
    path('report_detail/<int:id>/', report_detail, name='report_detail'),
    path('edit_report/<int:id>/', edit_report, name='edit_report'),
    path('delete_report/<int:id>/', delete_report, name='delete_report'),
    path('add_report_mobile/', add_report_mobile.as_view(), name='add_report_mobile'),
    path('register_user/', register_user, name="register_user"),
    path('login_user/', login_user, name="login_user"),
    path('logout_user/', logout_user, name="logout_user"),
    path('group/<int:group_id>/lokasi/', GroupLokasiListAPIView.as_view(), name='group_lokasi_list'),
    path('group/<int:group_id>/tujuan/', GroupTujuanListAPIView.as_view(), name='group_tujuan_list'),
    path('group/<int:group_id>/kayu/', GroupKayuListAPIView.as_view(), name='group_kayu_list'),
    path('check_token/<int:user_id>/', check_token, name='check_token'),
    path('display_group/', display_group, name='display_group'),
    path('save_group_changes/', save_group_changes, name='save_group_changes'),
    path('display_foto/<path:url>', display_foto, name="display_foto"),
    path('report-summary/<int:sender_id>/', ReportSummaryView.as_view(), name='report-summary'),
    path('report-summary/<int:sender_id>/<str:start_date>/<str:end_date>/', ReportSummaryView.as_view(), name='report-summary-date-range'),
]

