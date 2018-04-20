from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('input/', views.input, name='input'),
    # path('input/', views.updating_input, name='input'),
    path('plot/', views.plot, name='plot'),

    path('actions/', views.actions, name='actions'),
    path('results/', views.results, name='results'),

    path('about/', views.about, name='about'),
    path('chart/', views.chart, name='chart'),
    path('ajax/load-gasoline-units/', views.load_gasoline_units, name='ajax_load_gasoline_units'),
]