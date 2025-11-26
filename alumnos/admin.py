from django.contrib import admin
from .models import Alumno

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'apellido', 'email', 'carrera', 'estado', 'usuario']
    list_filter = ['estado', 'carrera', 'fecha_creacion']
    search_fields = ['nombre', 'apellido', 'email']