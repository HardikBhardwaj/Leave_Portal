# Generated by Django 3.1.1 on 2021-02-11 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('reason', models.CharField(max_length=300)),
                ('from1', models.DateTimeField()),
                ('to', models.DateTimeField()),
                ('status1', models.CharField(max_length=200)),
                ('noofdays', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='compulsary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compulsaryleave', models.DateTimeField(max_length=200)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='forgot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('otp', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='optional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('optionalleave', models.DateTimeField(max_length=200)),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('sickleave', models.IntegerField(blank=True, null=True)),
                ('casualleave', models.IntegerField(blank=True, null=True)),
                ('optionalleave', models.IntegerField(blank=True, null=True)),
                ('overday', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Totalleave',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('leaves', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]