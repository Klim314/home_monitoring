from django.shortcuts import render, HttpResponse
from django.views import View

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


def log_airgradient(request, sensor_id):
    """Logs data fron a
    """
    print(f"logging data for sensor={sensor_id}")
    print(request.POST)
    return HttpResponse("Hello, world. You're at the polls index.")


class DashboardView(View):
    def get(self, request):
        print("GETTING TO DASHBOARD")
        return HttpResponse("result")
