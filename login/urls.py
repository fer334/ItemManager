from django.urls import path

from . import views
app_name = 'login'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.user_register, name='register'),
]
