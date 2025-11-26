from django.urls import path
from . import views

urlpatterns = [
    path('', views.scraper_view, name='scraper'),
    path('enviar-resultados/', views.enviar_resultados_email, name='enviar_resultados'),
]