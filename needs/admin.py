from django.contrib import admin

# Register your models here.
from .models import StatusNeed, Needs, LogNeed

admin.site.register(StatusNeed)
admin.site.register(Needs)
admin.site.register(LogNeed)
