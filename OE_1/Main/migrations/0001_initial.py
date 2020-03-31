# Generated by Django 3.0.4 on 2020-03-30 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chromosom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Gen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('allel', models.FloatField()),
                ('locus', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Individual',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('solution', models.FloatField()),
                ('epoch', models.IntegerField()),
                ('individual', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Main.Chromosom')),
            ],
        ),
        migrations.CreateModel(
            name='Population',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('population', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.Individual')),
            ],
        ),
        migrations.AddField(
            model_name='chromosom',
            name='gen',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.Gen'),
        ),
    ]
