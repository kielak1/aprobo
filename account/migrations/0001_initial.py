# Generated by Django 5.0.3 on 2024-12-08 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('groups', models.ManyToManyField(related_name='baskets', to='auth.group')),
            ],
            options={
                'verbose_name': 'Koszyk uprawnień',
                'verbose_name_plural': 'Koszyki uprawnień',
            },
        ),
    ]
