from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('input/', views.input, name='input'),
    path('plot/', views.plot, name='plot'),
    path('results/', views.results, name='results'),
    path('about/', views.about, name='about'),
    path('chart/', views.chart, name='chart')
]