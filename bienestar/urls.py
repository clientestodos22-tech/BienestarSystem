from django.urls import path
from . import views


urlpatterns = [

    # =====================================================
    # INICIO
    # =====================================================

    path(
        "",
        views.inicio,
        name="inicio"
    ),


    # =====================================================
    # PES
    # =====================================================

    path(
        "pes/",
        views.formulario_pes,
        name="formulario_pes"
    ),

    path(
        "pes/gracias/",
        views.pes_exito,
        name="pes_exito"
    ),


    # =====================================================
    # PERCEPCIÓN EMOCIONAL
    # =====================================================

    path(
        "emocional/",
        views.formulario_emocional,
        name="formulario_emocional"
    ),

    path(
        "emocional/gracias/",
        views.emocional_exito,
        name="emocional_exito"
    ),


    # =====================================================
    # DASHBOARD
    # =====================================================

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),

    path(
        "dashboard/emociones/",
        views.listado_emociones,
        name="listado_emociones"
    ),

    path(
        "dashboard/pes/",
        views.listado_pes,
        name="listado_pes"
    ),


    # =====================================================
    # SOLICITUDES DE APOYO
    # =====================================================

    path(
        "dashboard/solicitudes/",
        views.listado_solicitudes,
        name="listado_solicitudes"
    ),

    path(
        "dashboard/solicitudes/<int:pk>/",
        views.atender_solicitud,
        name="atender_solicitud"
    ),


    # =====================================================
    # USUARIOS
    # =====================================================

    path(
        "usuarios/",
        views.listado_usuarios,
        name="listado_usuarios"
    ),

    path(
        "usuarios/crear/",
        views.crear_usuario,
        name="crear_usuario"
    ),
    path(
        "dashboard/emociones/",
        views.listado_emociones,
        name="listado_emociones"
    ),

]