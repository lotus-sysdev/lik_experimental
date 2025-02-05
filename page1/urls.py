from django.urls import path, include 
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home ,name='index'),
    path('success/', success ,name='success'),
    path('', home ,name='home'),

    # form add urls
    path('add_customer/', add_customer, name='add_customer'),
    path('add_supplier/', add_supplier, name='add_supplier'),
    path('add_item/',add_item, name='add_item'),
    path('add_PO/', add_PO, name='add_PO'),
    path('add_WO/', add_WO, name='add_WO'),

    # display customer, supplier, and item tables
    path('display_customer/',display_customer, name='display_customer'),
    path('display_supplier/',display_supplier, name='display_supplier'),
    path('display_item/', display_item, name="display_item"),
    path('item_list/',item_list, name='item_list'),

    # display purchase and work
    path('display_purchase/',display_purchase, name='display_purchase'),
    path('display_work/',display_work, name='display_work'),

    # purchase and work detail, edit, and delete
    path('purchase_detail/<int:id>/', purchase_detail, name='purchase_detail'),
    path('work_detail/<int:id>/', work_detail, name='work_detail'),
    path('edit_purchase/<int:id>/', edit_purchase, name='edit_purchase'),
    path('edit_work/<int:id>/', edit_work, name='edit_work'),
    path('delete_purchase/<int:id>/', delete_purchase, name='delete_purchase'),
    path('delete_work/<int:id>/', delete_work, name='delete_work'),

    # customer detail, edit, and delete
    path('customer_detail/<int:cust_id>/', customer_detail, name='customer_detail'),
    path('edit_customer/<int:cust_id>/', edit_customer, name='edit_customer'),
    path('delete_customer/<int:cust_id>/', delete_customer, name='delete_customer'),

    # supplier detail, edit, and delete
    path('supplier_detail/<int:supp_id>/', supplier_detail, name='supplier_detail'),
    path('edit_supplier/<int:supp_id>/', edit_supplier, name='edit_supplier'),
    path('delete_supplier/<int:supp_id>/', delete_supplier, name='delete_supplier'),
    
    # item detail, edit, and delete
    path('item_detail/<str:SKU>/', item_detail, name='item_detail'),
    path('edit_item/<str:SKU>/', edit_item, name='edit_item'),
    path('delete_item/<str:SKU>/', delete_item, name='delete_item'),
    # path('upload_csv/', upload_csv, name='upload_csv'),
    path('upload_excel/', upload_excel, name='upload_excel'),
    
    # Deletion of multiple rows
    path('delete_selected_rows_item/', delete_selected_rows_item, name='delete_selected_rows_item'),
    path('delete_selected_rows_cust/', delete_selected_rows_cust, name='delete_selected_rows_cust'),
    path('delete_selected_rows_supp/', delete_selected_rows_supp, name='delete_selected_rows_supp'),
    path('delete_selected_rows_PO/', delete_selected_rows_PO, name='delete_selected_rows_PO'),
    path('delete_selected_rows_WO/', delete_selected_rows_WO, name='delete_selected_rows_WO'),
    path('delete_selected_rows_delivery/', delete_selected_rows_delivery, name='delete_selected_rows_delivery'),
    path('delete_selected_rows_logbook/', delete_selected_rows_logbook, name='delete_selected_rows_logbook'),
    path('delete_selected_rows_prospect/', delete_selected_rows_prospect, name='delete_selected_rows_prospect'),

    # Item approval
    path('approve_item/<str:SKU>', approve_item, name='approve_item'),
    path('approve_selected_rows/', approve_selected_rows, name='approve_selected_rows'),
    
    # Sumber url
    path('add_sumber/<str:SKU>',add_sumber, name='add_sumber'),
    path('edit_sumber/<int:sumber_id>/', edit_sumber, name='edit_sumber'),
    path('delete_sumber/<int:sumber_id>/', delete_sumber, name='delete_sumber'),
    
    # PIC urls
    path('add_pic_cust/<int:cust_id>',add_customer_pic,name='add_pic_cust'),
    path('edit_customer_pic/<int:pic_id>/', edit_customer_pic, name='edit_customer_pic'),
    path('delete_customer_pic/<int:pic_id>/', delete_customer_pic, name='delete_customer_pic'),

    path('add_pic_supp/<int:supp_id>',add_supplier_pic,name='add_pic_supp'),
    path('edit_supplier_pic/<int:pic_id>/', edit_supplier_pic, name='edit_supplier_pic'),
    path('delete_supplier_pic/<int:pic_id>/', delete_supplier_pic, name='delete_supplier_pic'),

    path('add_pic_prospect/<int:prospect_id>',add_prospect_pic,name='add_pic_prospect'),
    path('edit_prospect_pic/<int:pic_id>/', edit_prospect_pic, name='edit_prospect_pic'),
    path('delete_prospect_pic/<int:pic_id>/', delete_prospect_pic, name='delete_prospect_pic'),

    # Alamat urls
    path('add_customer_alamat/<int:cust_id>/', add_customer_alamat, name='add_customer_alamat'),
    path('edit_customer_alamat/<int:alamat_id>/', edit_customer_alamat, name='edit_customer_alamat'),
    path('delete_customer_alamat/<int:alamat_id>/', delete_customer_alamat, name='delete_customer_alamat'),

    path('add_supplier_alamat/<int:supp_id>/', add_supplier_alamat, name='add_supplier_alamat'),
    path('edit_supplier_alamat/<int:alamat_id>/', edit_supplier_alamat, name='edit_supplier_alamat'),
    path('delete_supplier_alamat/<int:alamat_id>/', delete_supplier_alamat, name='delete_supplier_alamat'),
    
    # Login, Register, Logout
    path('login/',login_view, name="login"),
    path('register/',register_view, name="register"),
    path('logout/', logout_view, name='logout'),
    
    
    #Forgot Password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
    
    # User Action Log
    path('user_action_logs/', user_action_logs, name='user_action_logs'),

    # Delivery Order 
    path('calendar/', calendar, name='calendar'),
    path('all_events/', all_events, name='all_events'), 
    path('add_event/', add_event, name='add_event'), 
    path('update/', update, name='update'),
    path('remove/', remove, name='remove'),
    path('delivery_form/', delivery_form, name='delivery_form'),
    path('update_num_forms/', update_num_forms, name='update_num_forms'),
    path('display_delivery/',display_delivery, name='display_delivery'),

    path('delivery_detail/<int:id>', delivery_detail, name='delivery_detail'),
    path('edit_delivery/<int:id>/', edit_delivery, name='edit_delivery'),
    path('delete_delivery/<int:id>/', delete_delivery, name='delete_delivery'),

    path('add_messenger/', add_messenger, name='add_messenger'),
    path('add_vehicle/', add_vehicle, name='add_vehicle'),
    path('get_messenger/', get_messenger, name='get_messenger'),

    path('forbidden/', forbidden, name='forbidden'),

    path('add_additional_address/', add_additional_address, name='add_additional_address'),
    path('get_location_data/', get_location_data, name="get_location_data" ),

    # Log Book
    path('log_book/', log_book, name="log_book"),
    path('lb_all_events/', lb_all_events, name='lb_all_events'), 
    path('lb_add_event/', lb_add_event, name='lb_add_event'), 
    path('lb_update/', lb_update, name='lb_update'),
    path('lb_remove/', lb_remove, name='lb_remove'),
    path('add_log/', add_log, name="add_log"),
    path('log_detail/<int:id>', log_detail, name='log_detail'),
    path('edit_log/<int:id>/', edit_log, name='edit_log'),
    path('delete_log/<int:id>/', delete_log, name='delete_log'),
    path('display_log/',display_log, name='display_log'),

    # Dependable Addresses
    path('get_kota/', get_kota, name='get_kota'),
    path('get_kecamatan/', get_kecamatan, name='get_kecamatan'),
    path('get_kelurahan/', get_kelurahan, name='get_kelurahan'),
    path('get_region_details/', get_region_details, name='get_region_details'),
    path('get_kode_pos/', get_kode_pos, name='get_kode_pos'),

    # Prospect
    path('display_prospect/', display_prospect, name='display_prospect'),
    path('add_prospect/', add_prospect, name='add_prospect'),
    path('prospect_detail/<int:prospect_id>', prospect_detail, name='prospect_detail'),
    path('edit_prospect/<int:prospect_id>/', edit_prospect, name='edit_prospect'),
    path('delete_prospect/<int:prospect_id>/', delete_prospect, name='delete_prospect'),
    path('add_prospect_alamat/<int:prospect_id>/', add_prospect_alamat, name='add_prospect_alamat'),
    path('edit_prospect_alamat/<int:alamat_id>/', edit_prospect_alamat, name='edit_prospect_alamat'),
    path('delete_prospect_alamat/<int:alamat_id>/', delete_prospect_alamat, name='delete_prospect_alamat'),
    
    path('prospect_ticket/<int:prospect_id>/', prospect_ticket, name='prospect_ticket'),
    path('add_prospect_ticket/<int:prospect_id>/', add_prospect_ticket, name='add_prospect_ticket'),
    path('edit_prospect_ticket/<int:log_id>/', edit_prospect_ticket, name='edit_prospect_ticket'),
    path('delete_prospect_ticket/<int:log_id>/', delete_prospect_ticket, name='delete_prospect_ticket'),
    path('convert/<int:prospect_id>/', convert_to_customer, name='convert_to_customer'),

    path('add_ticket_log/<int:prospect_id>', add_ticket_log, name='add_ticket_log'),
    path('edit_ticket_log/<int:log_id>/', edit_ticket_log, name='edit_ticket_log'),
    path('delete_ticket_log/<int:log_id>/', delete_ticket_log, name='delete_ticket_log'),

    # Get PICs
    path('get_customer_pics/', get_customer_pics, name='get_customer_pics'),
    path('get_customer_by_pic/', get_customer_by_pic, name='get_customer_by_pic'),
    
    # Get Items
    path('get_customer_item/', get_customer_item, name='get_customer_item'),
    path('get_item_details/', get_item_details, name='get_item_details'),   
]

