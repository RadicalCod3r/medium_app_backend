# Generated by Django 4.1.3 on 2022-11-18 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_post_body'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'Categories'},
        ),
    ]