from django.db import models

class Estudiante(models.Model):
    persona_id = models.IntegerField(db_column='PersonaID', primary_key=True)
    nombre = models.CharField(db_column='Nombre', max_length=100)
    apellido = models.CharField(db_column='Apellido', max_length=100)
    identificacion = models.CharField(db_column='Identificacion', max_length=20)
    email = models.EmailField(db_column='Email', max_length=255, blank=True, null=True)
    telefono = models.CharField(db_column='Telefono', max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Programas.VW_Estudiantes'   
