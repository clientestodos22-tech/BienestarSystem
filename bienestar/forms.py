from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import (
    RespuestaPES,
    PercepcionEmocional,
    AtencionApoyo,
)


# =========================================================
# PES
# =========================================================

class PESForm(forms.ModelForm):

    es_pes = forms.TypedChoiceField(
        label="¿Te identificas como persona especialmente sensible?",
        choices=[
            (True, "Sí"),
            (False, "No"),
        ],
        coerce=lambda value: value == "True",
        widget=forms.RadioSelect,
        required=True,
    )

    necesita_apoyo = forms.TypedChoiceField(
        label="¿Consideras que necesitas algún apoyo o adaptación?",
        choices=[
            (False, "No"),
            (True, "Sí"),
        ],
        coerce=lambda value: value == "True",
        widget=forms.RadioSelect,
        required=True,
    )

    class Meta:

        model = RespuestaPES

        fields = [
            "es_pes",
            "condicion",
            "necesita_apoyo",
            "comentario",
        ]

        widgets = {

            "condicion": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "comentario": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "maxlength": 500,
                    "placeholder": (
                        "Si lo deseas, puedes agregar "
                        "información adicional..."
                    )
                }
            ),
        }

    def clean(self):

        cleaned_data = super().clean()

        es_pes = cleaned_data.get("es_pes")
        condicion = cleaned_data.get("condicion")

        if es_pes and not condicion:

            self.add_error(
                "condicion",
                "Selecciona la condición o situación que corresponda."
            )

        if es_pes is False:

            cleaned_data["condicion"] = ""
            cleaned_data["necesita_apoyo"] = False

        return cleaned_data


# =========================================================
# PERCEPCIÓN EMOCIONAL
# =========================================================

class PercepcionEmocionalForm(forms.ModelForm):

    class Meta:

        model = PercepcionEmocional

        fields = [
            "emocion",
            "tipo_apoyo",
            "comentario",
        ]

        widgets = {

            "tipo_apoyo": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "comentario": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "maxlength": 500,
                    "placeholder": (
                        "Si quieres, puedes contarnos "
                        "brevemente cómo te sientes..."
                    )
                }
            ),
        }


# =========================================================
# CREAR USUARIO
# =========================================================

class CrearUsuarioForm(UserCreationForm):

    first_name = forms.CharField(
        label="Nombre",
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nombre"
            }
        )
    )

    last_name = forms.CharField(
        label="Apellido",
        max_length=150,
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Apellido"
            }
        )
    )

    email = forms.EmailField(
        label="Correo electrónico",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "usuario@empresa.cl"
            }
        )
    )

    rol = forms.ChoiceField(
        label="Rol",
        choices=[
            ("usuario", "Colaborador"),
            ("admin", "Administrador"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-select"
            }
        )
    )

    class Meta:

        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "rol",
            "password1",
            "password2",
        ]

        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Nombre de usuario"
                }
            )
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Contraseña"
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirmar contraseña"
        })

    def clean_email(self):

        email = self.cleaned_data["email"].lower()

        if User.objects.filter(
            email__iexact=email
        ).exists():

            raise forms.ValidationError(
                "Ya existe un usuario con este correo."
            )

        return email

    def save(self, commit=True):

        usuario = super().save(
            commit=False
        )

        usuario.email = self.cleaned_data["email"]

        usuario.is_staff = (
            self.cleaned_data["rol"] == "admin"
        )

        if commit:
            usuario.save()

        return usuario


# =========================================================
# ATENDER SOLICITUD
# =========================================================

class AtenderSolicitudForm(forms.ModelForm):

    class Meta:

        model = AtencionApoyo

        fields = [
            "accion",
            "estado_resultante",
            "comentario",
        ]

        labels = {
            "accion": "Acción realizada",
            "estado_resultante": "Estado de la solicitud",
            "comentario": "Registro de la atención",
        }

        widgets = {

            "accion": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "estado_resultante": forms.Select(
                attrs={
                    "class": "form-select"
                }
            ),

            "comentario": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": (
                        "Describe brevemente la atención, "
                        "medida, conversación o seguimiento realizado..."
                    )
                }
            ),
        }