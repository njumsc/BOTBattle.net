from django.urls import path
from goldennum import views

urlpatterns = [
    path('', views.index),

    path('getAct/', views.getAct),
    path('submitResult/', views.submitResult),

    path('startRoom/', views.startRoom),
    path('stopRoom/', views.stopRoom),
    path('roomStatus/', views.roomStatus),

    path('userReg/', views.userReg),
    path('userOut/', views.userOut),
    path('userAct/', views.userAct),
    path('userStatus/', views.userStatus),
    # path('userScript/', views.userScript),

    path('getStatus/', views.getStatus),
]
