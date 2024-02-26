from django.contrib import admin
from .models import *

admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Items)
admin.site.register(CustomerPIC)
admin.site.register(SupplierPIC)
admin.site.register(PurchaseOrder)
admin.site.register(WorkOrder)
admin.site.register(UserActionLog)
