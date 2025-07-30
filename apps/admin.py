from django.contrib import admin
from .models import *
from .forms import *

class ishAdmin(admin.ModelAdmin):
    form = ishForum


















admin.site.register(ish)

# Yutuqlar uchun admin
@admin.register(yutuq)
class yutuqAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'darajasi', 'sana')
    list_filter = ('darajasi', 'sana')
    search_fields = ('nomi', 'tavsif')
    ordering = ('-sana',)
