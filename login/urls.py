from django.urls import path

from . import views
app_name = 'login'
urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('login/', views.LoginPage.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.Register.as_view(), name='register'),
    path('makeLogin/', views.makeLogin, name='makeLogin'),
    path('postRegister/', views.postRegister, name='postRegister'),
]
