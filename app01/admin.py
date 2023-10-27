from django.contrib import admin
from app01.models import Articles, Tags, Cover

# Register your models here.

admin.site.register(Articles)
admin.site.register(Tags)
admin.site.register(Cover)
