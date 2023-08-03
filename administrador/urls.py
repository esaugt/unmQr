from django.urls import path
from . import views
from .views import MyPasswordResetView, MyPasswordResetDoneView,  MyPasswordResetConfirmView, MyPasswordResetCompleteView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.signout, name='logout'),
    path('registro/', views.register, name='registro'),
    path('registro/confirmación', views.registro_cnfrm, name= 'registro_cnfrm'),
    path('reset_recuperar/', views.recuperar, name='recuperar'),
    path('administrador/', views.administrador, name='administrador'),
    path('ver_sitios/<int:bloque_id>/', views.ver_sitios, name='ver_sitios'),
    path('bloque/<int:bloque_id>/editar/', views.editar_bloque, name='editar_bloque'),
    path('editar_sitio/<int:sitio_id>/', views.editar_sitio, name='editar_sitio'),

     ##Reestablecer contraseña
    path('reset/password_reset', MyPasswordResetView.as_view(), name='password_reset'),
    path('reset/password_reset_done', MyPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', MyPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', MyPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

# urls.py
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
