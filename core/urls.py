from django.urls import path
from core import views

urlpatterns = [
    path('', views.index, name='index'),
    path('poseshennye', views.poseshennye, name='poseshennye'),
    path('clock/<str:name_clock>', views.clock, name='clock'),
]