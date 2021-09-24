from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('holi/', views.holi, name='holi'),
    path('backs/', views.backs, name='backs'),
    path('over/', views.over, name='over'),
    path('bustravel/', views.travel, name='travel'),
    path('hoiltest/', views.hoiltest, name='hoiltest'),
    path('overtest/', views.overtest, name='overtest'),
    path('updateEmp/', views.updateEmp, name='updateEmp'),
    path('checkdata/', views.checkdata, name='checkdata'),
    path('testcheckdata/', views.testcheckdata, name='testcheckdata'),
    path('daliy/', views.daliy, name='daliy'),
    path('monthliy/', views.monthliy, name='monthliy'),
    path('leaveinterface/', views.leaveinterface, name='leaveinterface'),
]
