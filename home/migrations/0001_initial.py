# Generated by Django 5.1.1 on 2024-10-06 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=70)),
                ('text', models.TextField()),
            ],
            options={
                'verbose_name': 'contact us message',
                'verbose_name_plural': 'contact us messages',
            },
        ),
    ]
