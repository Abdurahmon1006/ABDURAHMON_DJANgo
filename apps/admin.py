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

# O'yinlar uchun admin
@admin.register(game)
class gameAdmin(admin.ModelAdmin):
    list_display = ('nomi', 'kategoriya', 'yaratilgan_sana')
    list_filter = ('kategoriya', 'yaratilgan_sana')
    search_fields = ('nomi', 'tavsif')
    ordering = ('-yaratilgan_sana',)
    readonly_fields = ('yaratilgan_sana', 'yangilangan_sana')
