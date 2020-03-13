from django.urls import path

from . import views
app_name = 'PaoApp'
urlpatterns = [
<<<<<<< HEAD
    path( '', views.index, name= 'index'),
    path('login/', views.login, name = 'login'),
    path( 'testLogin/', views.testLogin, name = 'testLogin'),
    path( 'register/', views.register, name = 'register'),
    path( 'postRegister/', views.postRegister, name = 'postRegister'),
]
=======
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('testLogin/', views.testLogin, name='testLogin'),
    path('register/', views.register, name='register'),
    path('postRegister/', views.postRegister, name='postRegister'),
]
>>>>>>> c06dd248bbc65b9d2c50319399c98cbd5b3a5cef
