from django.urls import path
from user import views

urlpatterns = [
    path('login/', views.LoginLogout.as_view()),
    path('logout/', views.LoginLogout.as_view()),
    path('', views.UserView.as_view()),

]