# Generated by Django 4.2.6 on 2024-03-06 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_rename_markid_pdfmark_mark_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pdfmark',
            name='listOfSpans',
            field=models.TextField(),
        ),
    ]
