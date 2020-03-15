from django.urls import path

from . import views
app_name = 'login'
urlpatterns = [
    path('', views.Index, name='index'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.Register, name='register'),
    path('makeLogin/', views.makeLogin, name='makeLogin'),
    path('postRegister/', views.postRegister, name='postRegister'),
]
