from django.urls import path

from . import views

app_name = 'robots'

urlpatterns = [
    path('add/', views.add, name='add')
] 