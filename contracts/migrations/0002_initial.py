# Generated by Django 5.0.3 on 2024-12-01 21:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contracts', '0001_initial'),
        ('general', '0001_initial'),
        ('ideas', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='contracts',
            name='ideas',
            field=models.ManyToManyField(blank=True, default=None, to='ideas.ideas', verbose_name='Pomysły'),
        ),
        migrations.AddField(
            model_name='contracts',
            name='koordynator',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Koordynator'),
        ),
        migrations.AddField(
            model_name='contracts',
            name='section',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='general.sections', verbose_name='Sekcja'),
        ),
        migrations.AddField(
            model_name='contracts',
            name='ezzc',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ezzc', to='contracts.ezzc', verbose_name='EZZC'),
        ),
        migrations.AddField(
            model_name='logcontract',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Użytkownik'),
        ),
        migrations.AddField(
            model_name='contracts',
            name='log',
            field=models.ManyToManyField(blank=True, default=None, to='contracts.logcontract', verbose_name='Logi'),
        ),
    ]
