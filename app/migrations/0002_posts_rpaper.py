# Generated by Django 4.1.2 on 2025-01-15 13:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='rPaper',
            field=models.ForeignKey(default=20, on_delete=django.db.models.deletion.CASCADE, related_name='posts', related_query_name='post', to='app.researchpapers'),
            preserve_default=False,
        ),
    ]
