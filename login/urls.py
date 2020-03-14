from django.urls import path

from . import views
app_name = 'login'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('makeLogin/', views.makeLogin, name='makeLogin'),
    path('postRegister/', views.postRegister, name='postRegister'),
]
