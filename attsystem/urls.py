from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('holi/', views.holi, name='holi'),
    path('over/', views.over, name='over'),
    path('bustravel/', views.travel, name='travel'),
    path('test/', views.test, name='test'),
    path('hoiltest/', views.hoiltest, name='hoiltest'),
    path('empInfo/', views.empInfo, name='empInfo'),
]
