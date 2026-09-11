from django.db import models
from django.contrib.auth.models import User


# =========================================================
# PES
# =========================================================

class RespuestaPES(models.Model):

    CONDICIONES = [
        ("embarazo", "Embarazo"),
        ("lactancia", "Período de lactancia"),
        ("discapacidad", "Discapacidad física, cognitiva o sensorial"),
        ("adulto_mayor", "Persona adulta mayor"),
        ("adolescente", "Adolescente con edad para trabajar"),
        ("perimenopausia", "Perimenopausia"),
        ("menopausia", "Menopausia"),
        ("menstrual", "Período menstrual"),
        ("otra", "Otra condición"),
        ("prefiero_no_indicar", "Prefiero no especificar"),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="respuestas_pes"
    )

    es_pes = models.BooleanField(
        verbose_name="¿Se identifica como persona especialmente sensible?"
    )

    condicion = models.CharField(
        max_length=50,
        choices=CONDICIONES,
        blank=True
    )

    necesita_apoyo = models.BooleanField(
        default=False
    )

    comentario = models.TextField(
        blank=True
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Respuesta PES"
        verbose_name_plural = "Respuestas PES"
        ordering = ["-fecha"]

    def __str__(self):
        return (
            f"{self.usuario.username} - "
            f"{self.fecha:%d/%m/%Y}"
        )


# =========================================================
# PERCEPCIÓN EMOCIONAL
# =========================================================

class PercepcionEmocional(models.Model):

    MOMENTOS = [
        ("entrada", "Entrada"),
        ("salida", "Salida"),
    ]

    EMOCIONES = [
        ("feliz", "Feliz / contento(a)"),
        ("motivado", "Motivado(a) / con energía"),
        ("tranquilo", "Tranquilo(a)"),
        ("estresado", "Preocupado(a) / estresado(a)"),
        ("triste", "Desanimado(a) / triste"),
        ("agotado", "Agotado(a) / con poca energía"),
        ("malestar", "Con malestar físico / enfermo(a)"),
        ("otro", "Otro"),
    ]

    TIPOS_APOYO = [
        ("ninguno", "No necesito apoyo"),
        ("manager", "Manager / Líder"),
        ("rrhh", "RR.HH."),
        ("prevencion", "Prevención de Riesgos"),
        ("otro", "Otro"),
    ]

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="percepciones_emocionales"
    )

    momento = models.CharField(
        max_length=10,
        choices=MOMENTOS,
        default="entrada"
    )

    emocion = models.CharField(
        max_length=30,
        choices=EMOCIONES
    )

    # Lo dejamos para no romper migraciones anteriores.
    acciones = models.JSONField(
        default=list,
        blank=True
    )

    tipo_apoyo = models.CharField(
        max_length=30,
        choices=TIPOS_APOYO,
        default="ninguno"
    )

    comentario = models.TextField(
        blank=True
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Percepción emocional"
        verbose_name_plural = "Percepciones emocionales"
        ordering = ["-fecha"]

    @property
    def necesita_apoyo(self):
        return self.tipo_apoyo != "ninguno"

    def __str__(self):
        return (
            f"{self.usuario.username} - "
            f"{self.get_momento_display()} - "
            f"{self.get_emocion_display()}"
        )


# =========================================================
# SOLICITUD DE APOYO
# =========================================================

class SolicitudApoyo(models.Model):

    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("en_proceso", "En proceso"),
        ("atendida", "Atendida"),
    ]

    percepcion = models.OneToOneField(
        PercepcionEmocional,
        on_delete=models.CASCADE,
        related_name="solicitud"
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="pendiente"
    )

    # Último administrador que atendió la solicitud
    atendido_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="solicitudes_atendidas"
    )

    fecha_creacion = models.DateTimeField(
        auto_now_add=True
    )

    fecha_ultima_atencion = models.DateTimeField(
        null=True,
        blank=True
    )

    fecha_cierre = models.DateTimeField(
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = "Solicitud de apoyo"
        verbose_name_plural = "Solicitudes de apoyo"
        ordering = ["-fecha_creacion"]

    def __str__(self):
        return (
            f"Solicitud #{self.pk} - "
            f"{self.percepcion.usuario.username}"
        )


# =========================================================
# HISTORIAL DE ATENCIÓN
# =========================================================

class AtencionApoyo(models.Model):

    ACCIONES = [
        ("contacto", "Contacto realizado"),
        ("conversacion", "Conversación con trabajador"),
        ("seguimiento", "Seguimiento"),
        ("derivacion", "Derivación"),
        ("ajuste", "Medida / ajuste implementado"),
        ("orientacion", "Orientación entregada"),
        ("cierre", "Cierre de solicitud"),
        ("otro", "Otro"),
    ]

    solicitud = models.ForeignKey(
        SolicitudApoyo,
        on_delete=models.CASCADE,
        related_name="atenciones"
    )

    realizado_por = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="registros_atencion"
    )

    accion = models.CharField(
        max_length=30,
        choices=ACCIONES
    )

    comentario = models.TextField()

    estado_resultante = models.CharField(
        max_length=20,
        choices=SolicitudApoyo.ESTADOS
    )

    fecha = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = "Atención de apoyo"
        verbose_name_plural = "Atenciones de apoyo"
        ordering = ["-fecha"]

    def __str__(self):
        return (
            f"Atención #{self.pk} - "
            f"{self.realizado_por.username}"
        )