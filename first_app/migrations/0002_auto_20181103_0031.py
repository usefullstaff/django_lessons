# Generated by Django 2.1.2 on 2018-11-02 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='user_pic',
            new_name='user',
        ),
        migrations.AddField(
            model_name='person',
            name='user_pick',
            field=models.ImageField(blank=True, default='place_icons/default.png', upload_to='place_icons/', verbose_name='Аватарка '),
        ),
        migrations.AlterField(
            model_name='person',
            name='home_loc',
            field=models.CharField(db_index=True, max_length=1000, verbose_name='Домашний адрес'),
        ),
    ]
