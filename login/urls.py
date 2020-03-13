from django.urls import path

from . import views
app_name = 'login'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('makeLogin/', views.register, name='makeLogin'),
    path('postRegister/', views.postRegister, name='postRegister'),
]
