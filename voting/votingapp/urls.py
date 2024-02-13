from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name='index'),
    path('detail/<str:slug>', views.detail, name='detail'),
    path('result/<str:slug>', views.result, name='result'),
    path('overallresult/', views.overallresult, name='overallresult'),
    path('manifesto/<int:id>', views.Manifesto, name='manifesto'),
]