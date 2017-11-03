from django.contrib import admin
from .models import ProxyMessage
# Register your models here.
class ProxyMessageAdmin(admin.ModelAdmin):
    list_display = ("IP","Port","Area","Address","Type")
    search_fields = ('IP','Area')

admin.site.register(ProxyMessage,ProxyMessageAdmin)