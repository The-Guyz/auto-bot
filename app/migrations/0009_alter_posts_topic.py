# Generated by Django 4.1.2 on 2024-12-28 23:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_posts_researchpapers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='topic',
            field=models.CharField(max_length=1000),
        ),
    ]
