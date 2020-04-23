# Generated by Django 2.2.11 on 2020-03-19 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rap', '0003_project_json'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(blank=True, default='', max_length=100, null=True)),
                ('name', models.CharField(blank=True, default='', max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Calais Entity',
                'verbose_name_plural': 'Entities',
            },
        ),
        migrations.CreateModel(
            name='SocialTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Calais Social Tag',
                'verbose_name_plural': 'Social Tags',
            },
        ),
        migrations.AlterField(
            model_name='heresearcharea',
            name='gtrs',
            field=models.ManyToManyField(blank=True, default=None, related_name='gtrs', to='rap.GTRCategory'),
        ),
        migrations.CreateModel(
            name='SocialTagInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('importance', models.IntegerField(blank=True, default=0, null=True)),
                ('socialtag', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rap.SocialTag')),
            ],
        ),
        migrations.CreateModel(
            name='EntityInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('relevance', models.FloatField(blank=True, default=0.0, null=True)),
                ('entity', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='rap.Entity')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='entities',
            field=models.ManyToManyField(to='rap.EntityInstance'),
        ),
        migrations.AddField(
            model_name='project',
            name='socialtags',
            field=models.ManyToManyField(to='rap.SocialTagInstance'),
        ),
    ]
