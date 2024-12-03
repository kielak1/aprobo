import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'test1.settings')
django.setup()


from contracts.models import  LogContract



import datetime

# Konfiguracja środowiska Django





def copy_dates_to_temp():
    for log in LogContract.objects.all():
        log.data_tmp = datetime.datetime.combine(log.data, datetime.time.min)
        log.save(update_fields=['data_tmp'])

if __name__ == "__main__":
    copy_dates_to_temp()
    print("Data copied to temp fields successfully.")
