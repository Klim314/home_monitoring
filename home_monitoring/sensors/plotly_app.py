# Dash stuff
import dash
from dash import dcc
from dash import html
from django_plotly_dash import DjangoDash

# Python imports
import pandas as pd
import re
from datetime import datetime, timedelta, timezone
from plotly import express as px

# Django models
from .models import AirgradientSensorRecord




app = DjangoDash('SensorDashboard')   # replaces dash.Dash

def calculate_default_window(freq, points=300, min_days=1):
    print(f"calculating window for {freq}")
    unit_map = {"min": timedelta(minutes=1), "H": timedelta(hours=1), }
    num, unit = re.findall(r"(\d+)(\w+)", freq)[0]
    num, unit = int(num), unit_map[unit]
    interval = num * unit
    return max(timedelta(days=1), interval * 300)

def generate_aggregates(freq=None):
    if freq is None:
        freq = "1min"
    dt = datetime.now(timezone.utc).astimezone()
    interval = calculate_default_window(freq)
    target_dt = dt - interval
    data = AirgradientSensorRecord.objects.filter(event_datetime__gt=target_dt)
    df = pd.DataFrame(data.values())
    # print(df)
    agg = df.groupby(["sensor", pd.Grouper(key="event_datetime", freq=freq)]).mean().reset_index()
    return agg

def generate_fig_co2(agg, sensor_id="de2ba8", freq=None):
    fig_co2 = px.scatter(agg.loc[agg.sensor == sensor_id], x='event_datetime', y='co2', title=f"CO2 trend for sensor={sensor_id}")
    fig_co2.data[0].update(mode='markers+lines')
    fig_co2.update_layout(yaxis_title=f"CO₂ Levels (PPM)")
    if freq:
        fig_co2.update_layout(xaxis_title=f"Time ({freq} intervals)")

    return fig_co2


def serve_layout(freq="1min"):
    agg = generate_aggregates(freq=freq)
    fig_co2 = generate_fig_co2(agg, sensor_id=agg.sensor.iloc[0])
    unique_sensors = sorted({ sensor_id for sensor_id in agg.sensor})
    dropdown_sensors_options = [{"label": sensor_id, "value": sensor_id} for sensor_id in unique_sensors]
    if unique_sensors:
        dropdown_sensors = dcc.Dropdown(id="dropdown_sensor", options=dropdown_sensors_options, style={"min-width": "320px"}, value=unique_sensors[0])
    else:
        dropdown_sensors = dcc.Dropdown(id="dropdown_sensor", options=[], style={"min-width": "320px"}, placeholder="ERROR: NO SENSORS DETECTED")


    _ =  html.Div([
        html.Div([
            dropdown_sensors,
            dcc.Dropdown(id="dropdown_freqs", options=[
                {"label": "1min", "value": "1min"},
                {"label": "15min", "value": "15min"},
                {"label": "30min", "value": "30min"},
                {"label": "1h", "value": "1H"},
                {"label": "6h", "value": "6H"},
            ], style={"min-width": "320px"}, value="1min")
        ], style={"display":'flex', "justify-content": "space-between"}),
        html.Div([
            dcc.Graph(
                id='fig_co2',
                figure=fig_co2
            )
        ])
    ])
    return _


app.layout = serve_layout


@app.callback(
    dash.dependencies.Output('fig_co2', 'figure'),
    [
        dash.dependencies.Input('dropdown_freqs', 'value'),
        dash.dependencies.Input('dropdown_sensor', 'value'),
    ])
def callback_update_unit(freq_value, sensor_value):
    print(f"Updating sensor_id={sensor_value}, freq={freq_value}")
    agg = generate_aggregates(freq=freq_value)
    return generate_fig_co2(agg, sensor_id=sensor_value)


