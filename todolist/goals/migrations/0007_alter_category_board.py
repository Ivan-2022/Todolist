# Generated by Django 4.0.1 on 2022-12-14 14:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goals', '0006_merge_0004_create_new_objects_0005_create_new_objects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='board',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='categories', to='goals.board', verbose_name='Доска'),
        ),
    ]
