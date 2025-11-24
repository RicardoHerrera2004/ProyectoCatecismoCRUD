from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_estudiantes, name='lista_estudiantes'),
    path('nuevo/', views.crear_estudiante, name='crear_estudiante'),
    path('<int:persona_id>/editar/', views.editar_estudiante, name='editar_estudiante'),
    path('<int:persona_id>/eliminar/', views.eliminar_estudiante, name='eliminar_estudiante'),
]
