from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection
from .models import Estudiante
from .forms import EstudianteForm

def lista_estudiantes(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT PersonaID, Nombre, Apellido, Identificacion, Email, Telefono
            FROM Programas.VW_Estudiantes
        """)
        rows = cursor.fetchall()

    estudiantes = [
        {
            'persona_id': r[0],
            'nombre': r[1],
            'apellido': r[2],
            'identificacion': r[3],
            'email': r[4],
            'telefono': r[5],
        }
        for r in rows
    ]

    return render(request, 'catecismo/lista_estudiantes.html', {
        'estudiantes': estudiantes,
        'titulo': 'Registro de catequizados',
    })


def crear_estudiante(request):
    if request.method == 'POST':
        form = EstudianteForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    EXEC Programas.SP_InsertarEstudiante
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    """,
                    [
                        cd['nombre'],
                        cd['apellido'],
                        cd['tipo_doc'],
                        cd['nro_doc'],
                        cd['fecha_nac'],
                        cd['telefono'],
                        cd['email'],
                        cd['fecha_bautismo'],
                        cd['lugar_bautismo'],
                        cd['observacion'],
                    ]
                )
                resultado = cursor.fetchone()

            return redirect('lista_estudiantes')
    else:
        form = EstudianteForm()

    return render(request, 'catecismo/form_estudiante.html', {
        'form': form,
        'titulo': 'Nuevo catequizado',
    })


def editar_estudiante(request, persona_id: int):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT PersonaID, Nombre, Apellido, Identificacion, Email, Telefono
            FROM Programas.VW_Estudiantes
            WHERE PersonaID = %s
        """, [persona_id])
        row = cursor.fetchone()

    if not row:
        return redirect("lista_estudiantes")

    estudiante = {
        "persona_id": row[0],
        "nombre": row[1],
        "apellido": row[2],
        "identificacion": row[3],
        "email": row[4],
        "telefono": row[5],
    }

    if request.method == "POST":
        form = EstudianteForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    EXEC Programas.SP_ActualizarEstudiante
                        %s, %s, %s, %s, %s, %s
                    """,
                    [
                        persona_id,
                        cd["nombre"],
                        cd["apellido"],
                        cd["nro_doc"],
                        cd["telefono"],
                        cd["email"],
                    ]
                )
            return redirect("lista_estudiantes")
    else:
        inicial = {
            "nombre": estudiante["nombre"],
            "apellido": estudiante["apellido"],
            "tipo_doc": "",  # esto no viene en la vista
            "nro_doc": estudiante["identificacion"],
            "fecha_nac": None,  # no viene en la vista
            "telefono": estudiante["telefono"],
            "email": estudiante["email"],
            "fecha_bautismo": None,
            "lugar_bautismo": "",
            "observacion": "",
        }
        form = EstudianteForm(initial=inicial)

    return render(request, "catecismo/form_estudiante.html", {
        "form": form,
        "titulo": "Editar catequizado",
    })


def eliminar_estudiante(request, persona_id):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("EXEC Programas.SP_EliminarEstudiante %s", [persona_id])
        return redirect('lista_estudiantes')

    return render(request, 'catecismo/confirmar_eliminar.html', {
        'persona_id': persona_id,
        'titulo': 'Eliminar catequizado',
    })
