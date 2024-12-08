# Generated by Django 5.0.3 on 2024-12-08 14:39

import datetime
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CBU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sygnatura', models.CharField(max_length=40, verbose_name='Sygnatura')),
                ('data_zawarcia', models.DateField(default=datetime.date(1990, 1, 1), verbose_name='Data zawarcia')),
                ('data_zakonczenia', models.DateField(default=datetime.date(1990, 1, 1), verbose_name='Data zakończenia')),
                ('status', models.CharField(max_length=20, verbose_name='Status')),
                ('nazwa_kontrahenta', models.CharField(max_length=400, verbose_name='Nazwa kontrahenta')),
                ('osoba_prowadzaca', models.CharField(max_length=50, verbose_name='Osoba prowadząca')),
                ('wartosc_wydatkowa', models.FloatField(verbose_name='Wartość wydatkowa')),
                ('wartosc_wplywowa', models.FloatField(verbose_name='Wartość wpływowa')),
                ('wartosc_odbiorow_wydatkowych', models.FloatField(verbose_name='Wartość odbiorów wydatkowych')),
                ('wartosc_odbiorow_wplywowych', models.FloatField(verbose_name='Wartość odbiorów wpływowych')),
                ('temat', models.CharField(max_length=700, verbose_name='Temat')),
                ('idemand', models.CharField(max_length=20, verbose_name='IDemand')),
                ('mandant', models.CharField(default=None, max_length=20, verbose_name='Mandant')),
            ],
            options={
                'verbose_name': 'CBU',
                'verbose_name_plural': 'CBU',
            },
        ),
        migrations.CreateModel(
            name='EZZC',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sygnatura', models.CharField(max_length=40, verbose_name='Sygnatura')),
                ('sygnatura_nadrzedna', models.CharField(max_length=41, null=True, verbose_name='Sygnatura nadrzędna')),
                ('przedmiot', models.CharField(max_length=377, verbose_name='Przedmiot')),
                ('numer_SRM', models.CharField(max_length=21, null=True, verbose_name='Numer SRM')),
                ('numer_ZZZT', models.CharField(max_length=22, null=True, verbose_name='Numer ZZZT')),
                ('wartosc', models.FloatField(verbose_name='Wartość')),
                ('typ_umowy', models.CharField(max_length=38, verbose_name='Typ umowy')),
                ('komorka', models.CharField(max_length=7, verbose_name='Komórka')),
                ('podstawa_prawna', models.CharField(max_length=24, verbose_name='Podstawa prawna')),
                ('waluta', models.CharField(max_length=6, null=True, verbose_name='Waluta')),
                ('wlasciciel_merytoryczny', models.CharField(max_length=25, verbose_name='Właściciel merytoryczny')),
                ('opiekun_BZ', models.CharField(max_length=26, null=True, verbose_name='Opiekun BZ')),
                ('dostawca', models.CharField(max_length=98, verbose_name='Dostawca')),
                ('koordynatorzy', models.CharField(max_length=52, verbose_name='Koordynatorzy')),
                ('typ_zakresu', models.CharField(max_length=41, verbose_name='Typ zakresu')),
                ('status', models.CharField(max_length=15, verbose_name='Status')),
                ('od_kiedy', models.DateField(default=datetime.date(1990, 1, 1), verbose_name='Od kiedy')),
                ('do_kiedy', models.DateField(default=datetime.date(1990, 1, 1), verbose_name='Do kiedy')),
            ],
            options={
                'verbose_name': 'EZZC',
                'verbose_name_plural': 'EZZC',
            },
        ),
        migrations.CreateModel(
            name='ImportedEZZ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('EZZ_number', models.CharField(max_length=20, verbose_name='Numer EZZ')),
                ('ordering_person', models.CharField(max_length=40, verbose_name='Osoba zamawiająca')),
                ('creation_date', models.DateField(default=datetime.date(1990, 1, 1), verbose_name='Data utworzenia')),
                ('subject', models.CharField(max_length=5000, verbose_name='Temat')),
                ('status', models.CharField(max_length=40, verbose_name='Status')),
                ('suplier', models.CharField(max_length=300, null=True, verbose_name='Dostawca')),
                ('source_of_financing', models.CharField(max_length=20, verbose_name='Źródło finansowania')),
                ('final_receiver', models.CharField(max_length=30, verbose_name='Odbiorca końcowy')),
                ('current_acceptor', models.CharField(default='', max_length=199, null=True, verbose_name='Aktualny akceptor')),
                ('date_of_last_acceptance', models.DateField(default=datetime.date(1990, 1, 1), null=True, verbose_name='Data ostatniej akceptacji')),
            ],
            options={
                'verbose_name': 'Zaimportowane EZZ',
                'verbose_name_plural': 'Zaimportowane EZZ',
            },
        ),
        migrations.CreateModel(
            name='LogContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('akcja', models.CharField(default=None, max_length=303, null=True, verbose_name='Akcja')),
                ('data', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Data')),
            ],
            options={
                'verbose_name': 'Log umowy',
                'verbose_name_plural': 'Logi umów',
            },
        ),
        migrations.CreateModel(
            name='Contracts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=700, verbose_name='Temat')),
                ('kontrahent', models.CharField(default='', max_length=400, null=True, verbose_name='Kontrahent')),
                ('numer_umowy', models.CharField(max_length=41, null=True, verbose_name='Numer umowy')),
                ('data_zawarcia', models.DateField(default=datetime.date(1990, 1, 1), verbose_name='Data zawarcia')),
                ('obslugiwana', models.BooleanField(default=None, null=True, verbose_name='Obsługiwana')),
                ('zakres', models.CharField(max_length=700, null=True, verbose_name='Zakres')),
                ('czy_wymagana_kontynuacja', models.BooleanField(null=True, verbose_name='Czy wymagana kontynuacja')),
                ('wymagana_data_zawarcia_kolejnej_umowy', models.DateField(default=None, null=True, verbose_name='Wymagana data zawarcia kolejnej umowy')),
                ('przedmiot_kolejnej_umowy', models.CharField(max_length=700, null=True, verbose_name='Przedmiot kolejnej umowy')),
                ('wartosc', models.FloatField(default=0, max_length=19, null=True, verbose_name='Wartość')),
                ('waluta', models.CharField(default='PLN', max_length=5, null=True, verbose_name='Waluta')),
                ('osoba_prowadzaca', models.CharField(default=None, max_length=42, null=True, verbose_name='Osoba prowadząca')),
                ('komentarz', models.CharField(blank=True, default=None, max_length=303, null=True, verbose_name='Komentarz')),
                ('nr_ezz', models.CharField(default=None, max_length=30, null=True, verbose_name='Numer EZZ')),
                ('liczba_aneksow', models.IntegerField(default=0, verbose_name='Liczba aneksów')),
                ('cbu', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cbu', to='contracts.cbu', verbose_name='CBU')),
            ],
            options={
                'verbose_name': 'Umowa',
                'verbose_name_plural': 'Umowy',
            },
        ),
    ]
