# Generated by Django 3.2 on 2023-08-12 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Jobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('job_id', models.BigIntegerField()),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('job_link', models.URLField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=250, null=True)),
                ('source', models.CharField(blank=True, max_length=250, null=True)),
                ('company', models.CharField(blank=True, max_length=200, null=True)),
                ('last_updated', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]