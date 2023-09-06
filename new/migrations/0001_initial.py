# Generated by Django 4.0.4 on 2023-07-31 09:40

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='New',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=200)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('text', models.TextField(blank=True, max_length=50000)),
                ('image', models.ImageField(blank=True, upload_to='news')),
                ('link', models.URLField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'new',
                'verbose_name_plural': 'news',
                'ordering': ['-created_at'],
            },
        ),
    ]
