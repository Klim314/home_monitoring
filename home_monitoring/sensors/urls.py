from django.urls import path

from . import views

urlpatterns = [
    path('airgradient/log', views.log_generic, name='log_generic'),
    path('airgradient/log/<str:sensor_id>', views.log_airgradient, name='log_sensor'),
    path("dashboard", views.DashboardView.as_view(), name='dashboard'),
    path("dashboard_dash", views.dashboard_dash, name='dashboard_dash'),

]
