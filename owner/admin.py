from django.contrib import admin
from .models import AdminUser,Status,optional,compulsary,Totalleave,forgot
# Register your models here.

admin.site.register(AdminUser)
admin.site.register(Status)
admin.site.register(optional)
admin.site.register(compulsary)
admin.site.register(Totalleave)
admin.site.register(forgot)

