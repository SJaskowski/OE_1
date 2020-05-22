# Generated by Django 3.0.4 on 2020-05-22 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PojedynczaWartoscWyniku',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wartosc', models.FloatField()),
                ('x1', models.FloatField()),
                ('x2', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Wynik',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('czas', models.TimeField()),
                ('sredniWynik', models.FloatField()),
                ('odchylenieStandardowe', models.FloatField()),
                ('iteracja', models.IntegerField()),
                ('wyniki', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Main.PojedynczaWartoscWyniku')),
            ],
        ),
    ]