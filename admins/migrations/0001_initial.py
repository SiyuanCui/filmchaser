# Generated by Django 3.2.5 on 2023-03-21 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admins',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=50, verbose_name='username')),
                ('password', models.CharField(default='', max_length=128, verbose_name='password')),
            ],
            options={
                'verbose_name': 'admin',
                'verbose_name_plural': 'admin',
                'db_table': 'admins',
            },
        ),
    ]