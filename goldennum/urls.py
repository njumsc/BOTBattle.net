from django.urls import path
from goldennum import views

urlpatterns = [
    path('getAct/', views.getAct),
    path('submitResult/', views.submitResult),

    path('startRoom/', views.startRoom),
    path('stopRoom/', views.stopRoom),

    path('userReg/', views.userReg),
    path('userOut/', views.userOut),
    path('userAct/', views.userAct),
]
