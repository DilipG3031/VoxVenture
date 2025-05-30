# Generated by Django 5.1.4 on 2024-12-11 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SubjectMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('pdf', models.FileField(upload_to='pdfs/')),
                ('audio', models.FileField(blank=True, null=True, upload_to='audios/')),
            ],
        ),
    ]
