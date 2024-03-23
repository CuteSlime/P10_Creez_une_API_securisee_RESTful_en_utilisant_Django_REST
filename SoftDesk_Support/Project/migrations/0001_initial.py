# Generated by Django 5.0.3 on 2024-03-23 12:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, verbose_name='Nom du projet')),
                ('description', models.TextField(max_length=500, verbose_name='Description du projet')),
                ('type', models.CharField(choices=[('Back-end', 'Back-end'), ('Front-end', 'Front-end'), ('iOS', 'iOS'), ('Android', 'Android')], max_length=10, verbose_name='type de projet')),
                ('created_time', models.DateField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_author', to=settings.AUTH_USER_MODEL, verbose_name='Auteur du projet')),
                ('contributors', models.ManyToManyField(related_name='project_contributor', through='project.Contributor', to=settings.AUTH_USER_MODEL, verbose_name='Contributeurs')),
            ],
        ),
        migrations.AddField(
            model_name='contributor',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.project'),
        ),
    ]
