from django.contrib import admin

# Register your models here.
from .models import StatusIdei, Ideas, LogIdea

admin.site.register(StatusIdei)
admin.site.register(Ideas)
admin.site.register(LogIdea)
