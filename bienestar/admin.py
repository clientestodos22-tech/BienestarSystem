from django.contrib import admin

from .models import (
    RespuestaPES,
    PercepcionEmocional,
    SolicitudApoyo,
    AtencionApoyo,
)


@admin.register(RespuestaPES)
class RespuestaPESAdmin(admin.ModelAdmin):

    list_display = (
        "usuario",
        "es_pes",
        "condicion",
        "necesita_apoyo",
        "fecha",
    )

    list_filter = (
        "es_pes",
        "condicion",
        "necesita_apoyo",
    )

    search_fields = (
        "usuario__username",
        "usuario__first_name",
        "usuario__last_name",
    )


@admin.register(PercepcionEmocional)
class PercepcionEmocionalAdmin(admin.ModelAdmin):

    list_display = (
        "usuario",
        "momento",
        "emocion",
        "tipo_apoyo",
        "fecha",
    )

    list_filter = (
        "momento",
        "emocion",
        "tipo_apoyo",
    )

    search_fields = (
        "usuario__username",
        "usuario__first_name",
        "usuario__last_name",
    )


@admin.register(SolicitudApoyo)
class SolicitudApoyoAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "trabajador",
        "tipo_apoyo",
        "estado",
        "atendido_por",
        "fecha_creacion",
    )

    list_filter = (
        "estado",
        "fecha_creacion",
    )

    search_fields = (
        "percepcion__usuario__username",
        "percepcion__usuario__first_name",
        "percepcion__usuario__last_name",
    )

    def trabajador(self, obj):

        return obj.percepcion.usuario.username

    trabajador.short_description = "Trabajador"

    def tipo_apoyo(self, obj):

        return obj.percepcion.get_tipo_apoyo_display()

    tipo_apoyo.short_description = "Tipo de apoyo"


@admin.register(AtencionApoyo)
class AtencionApoyoAdmin(admin.ModelAdmin):

    list_display = (
        "solicitud",
        "realizado_por",
        "accion",
        "estado_resultante",
        "fecha",
    )

    list_filter = (
        "accion",
        "estado_resultante",
        "fecha",
    )