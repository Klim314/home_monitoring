from django.shortcuts import render, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_protect, csrf_exempt

import json
from datetime import datetime, timezone, timedelta
import pytz
import pandas as pd
import plotly
import dash
from plotly import express as px

from .models import AirgradientSensorRecord

from . import plotly_app


# we're not using the ORM For now just for speed of development
import sqlite3
conn = sqlite3.connect("temp.sqlite3")
cur = conn.cursor()




# Create your views here.
def log_generic(request):
    """Testing view used to just print to logs and figure out what the payload looks like
    """
    print(request.POST)
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def log_airgradient(request, sensor_id):
    """Logs data fron an airgradient sensor
    """

    print(f"logging data for sensor={sensor_id}")
    data = json.loads(request.body.decode("utf-8"))
    dt = datetime.now(timezone.utc).astimezone()

    print(f"received data at dt={dt}: {data}")


    AirgradientSensorRecord.objects.create(
        event_datetime=dt,
        event_timestamp=dt.timestamp(),
        sensor=sensor_id,
        co2=data["rco2"],
        pm2=data["pm02"],
        temp=data["atmp"],
        rhum=data["rhum"]
    )
    return HttpResponse(f"Log: {sensor_id} successful")


class DashboardView(View):
    def get(self, request):
        data = AirgradientSensorRecord.objects.filter(event_datetime__gte=datetime.now(timezone.utc).astimezone() - timedelta(hours=6) )
        dt = datetime.now(timezone.utc).astimezone()
        target_dt = dt - timedelta(days=1)
        data = AirgradientSensorRecord.objects.filter(event_datetime__gt=target_dt)
        df = pd.DataFrame(data.values())
        # print(df)
        agg = df.groupby(pd.Grouper(key="event_datetime", freq='min')).mean().reset_index()
        agg["event_datetime"] = agg["event_datetime"].dt.tz_convert("singapore")
        print(agg)
        fig_co2 = px.scatter(agg, x='event_datetime', y='co2')
        fig_co2.data[0].update(mode='markers+lines')
        context = {"fig_co2": fig_co2.to_html(full_html=False)}

        return render(request, "sensors/dashboard.html", context=context)

def dashboard_dash(request):
    return render(request, "sensors/dashboard_dash.html")

