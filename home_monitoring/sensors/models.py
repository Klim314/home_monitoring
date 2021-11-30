from django.db import models

# Create your models here.
class AirgradientSensorRecord(models.Model):
    event_datetime = models.DateTimeField()
    # UTC timestamp recording
    event_timestamp = models.IntegerField()
    sensor = models.CharField(max_length=30)
    co2 = models.IntegerField()
    pm2 = models.IntegerField()
    temp = models.DecimalField(decimal_places=2, max_digits=10)
    rhum = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        indexes = [
            models.Index(fields=["sensor", "event_datetime"]),
            models.Index(fields=["sensor", "event_timestamp"])
        ]
