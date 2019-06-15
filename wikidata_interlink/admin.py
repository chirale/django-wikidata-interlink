from django.contrib import admin

# Register your models here.
from .models import *

AUTO_MODELS = [Wikipedia, Label]

for curmodel in AUTO_MODELS:
    admin.site.register(curmodel)


@admin.register(Wikidata)
class WikidataAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'q')
    search_fields = ('q',)
