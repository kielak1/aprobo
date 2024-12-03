from django.contrib import admin

# Register your models here.


from .models import Contracts, CBU, EZZC, LogContract

admin.site.register(Contracts)
admin.site.register(CBU)
admin.site.register(EZZC)
admin.site.register(LogContract)
