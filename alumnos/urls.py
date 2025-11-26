from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('crear/', views.crear_alumno, name='crear_alumno'),
    path('enviar-pdf/<int:alumno_id>/', views.enviar_pdf_email, name='enviar_pdf'),
]