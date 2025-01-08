# Generated by Django 5.1.4 on 2025-01-02 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_alter_card_rarity'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cards',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('image', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
                ('group', models.CharField(max_length=255)),
                ('race', models.CharField(max_length=255)),
                ('nation', models.CharField(max_length=255)),
                ('grade', models.CharField(max_length=255)),
                ('power', models.CharField(max_length=255)),
                ('critical', models.CharField(max_length=255)),
                ('shield', models.CharField(max_length=255)),
                ('skill', models.CharField(max_length=255)),
                ('gift', models.CharField(max_length=255)),
                ('effect', models.TextField()),
                ('flavor', models.CharField(max_length=255)),
                ('regulation', models.CharField(max_length=255)),
                ('number', models.CharField(max_length=255)),
                ('rarity', models.CharField(max_length=255)),
                ('illustrator', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'cards',
            },
        ),
        migrations.DeleteModel(
            name='Card',
        ),
    ]
