from django.contrib import admin

from .models import BS_tab

class BS_tab_admin(admin.ModelAdmin):
    list_display=['title','subtitle','authors','publishedDate','price','previewlink','itemid']

admin.site.register(BS_tab,BS_tab_admin)