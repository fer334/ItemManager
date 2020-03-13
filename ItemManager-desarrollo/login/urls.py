from django.urls import path

from . import views
app_name = 'PaoApp'
urlpatterns = [
    path( '', views.index, name= 'index'),
    path('login/', views.login, name = 'login'),
    path( 'testLogin/', views.testLogin, name = 'testLogin'),
    path( 'register/', views.register, name = 'register'),
    path( 'postRegister/', views.postRegister, name = 'postRegister'),
]