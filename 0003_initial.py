# Generated by Django 5.1.4 on 2024-12-13 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Voiceclone', '0002_delete_subjectmaterial'),
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
