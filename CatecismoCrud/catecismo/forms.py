from django import forms


class EstudianteForm(forms.Form):
    nombre = forms.CharField(
        label="Nombre",
        max_length=80,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Nombre del catequizado"
        })
    )
    apellido = forms.CharField(
        label="Apellido",
        max_length=80,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Apellido del catequizado"
        })
    )
    tipo_doc = forms.CharField(
        label="Tipo de documento",
        max_length=10,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "CI, PAS, etc."
        })
    )
    nro_doc = forms.CharField(
        label="Número de documento",
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Número de identificación"
        })
    )
    fecha_nac = forms.DateField(
        label="Fecha de nacimiento",
        widget=forms.DateInput(attrs={
            "class": "form-control",
            "type": "date"
        })
    )
    telefono = forms.CharField(
        label="Teléfono",
        max_length=80,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "type": "tel",
            "placeholder": "Teléfono de contacto"
        })
    )
    email = forms.EmailField(
        label="Email",
        max_length=120,
        required=False,
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "correo@ejemplo.com"
        })
    )
    fecha_bautismo = forms.DateField(
        label="Fecha de bautismo",
        required=False,
        widget=forms.DateInput(attrs={
            "class": "form-control",
            "type": "date"
        })
    )
    lugar_bautismo = forms.CharField(
        label="Lugar de bautismo",
        max_length=150,
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Parroquia / lugar (opcional)"
        })
    )
    observacion = forms.CharField(
        label="Observación",
        required=False,
        widget=forms.Textarea(attrs={
            "class": "form-control",
            "rows": 3,
            "placeholder": "Notas adicionales (opcional)"
        })
    )