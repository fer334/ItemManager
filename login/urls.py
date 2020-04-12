from django.urls import path
from django.views.generic import TemplateView

from . import views
app_name = 'login'
urlpatterns = [
    path('inicio/', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.user_register, name='register'),

    path('admin/', views.admin, name='admin'),
    path('admin/access/', views.users_access, name='administrarAccesos'),
    path('<str:name>/update/', views.user_update, name='userUpdate'),
    path(
        'accesoDenegado/',
        TemplateView.as_view(template_name='login/accesoDenegado.html'),
        name='AccesoDenegado',
    ),
]
