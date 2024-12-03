from django.contrib import admin

# Register your models here.
from .models import Purchases, Postepowania

admin.site.register(Purchases)
admin.site.register(Postepowania)

from .models import LogPurchase

admin.site.register(LogPurchase)


from .models import EZZ

admin.site.register(EZZ)
