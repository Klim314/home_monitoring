# Generated by Django 3.2.8 on 2021-10-13 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AirgradientSensorRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_datetime', models.DateTimeField()),
                ('event_timestamp', models.IntegerField()),
                ('sensor', models.CharField(max_length=30)),
                ('co2', models.IntegerField()),
                ('pm2', models.IntegerField()),
                ('temp', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rhum', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.AddIndex(
            model_name='airgradientsensorrecord',
            index=models.Index(fields=['sensor', 'event_datetime'], name='sensors_air_sensor_75cf10_idx'),
        ),
        migrations.AddIndex(
            model_name='airgradientsensorrecord',
            index=models.Index(fields=['sensor', 'event_timestamp'], name='sensors_air_sensor_5c3dde_idx'),
        ),
    ]
