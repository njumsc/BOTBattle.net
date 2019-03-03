from django.urls import path
from goldennum import views

urlpatterns = [
    path('', views.index),
    path('admin/', views.admin),
    path('admin/startRoom/', views.startRoom),
    path('admin/stopRoom/', views.stopRoom),

    path('getAct/', views.getAct),
    path('submitResult/', views.submitResult),

    path('roomStatus/', views.roomStatus),

    path('userReg/', views.userReg),
    path('userOut/', views.userOut),
    path('userAct/', views.userAct),
    path('userStatus/', views.userStatus),
    # path('userScript/', views.userScript),

    path('getStatus/', views.getStatus),
]
