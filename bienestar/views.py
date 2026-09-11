import random

from collections import Counter
from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required,
    user_passes_test,
)
from django.contrib.auth.models import User

from django.core.paginator import Paginator

from django.db import transaction
from django.db.models import (
    Case,
    Count,
    IntegerField,
    Q,
    Value,
    When,
)

from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)

from django.utils import timezone


from .emociones import EMOCIONES_CONFIG

from .forms import (
    AtenderSolicitudForm,
    CrearUsuarioForm,
    PercepcionEmocionalForm,
    PESForm,
)

from .models import (
    PercepcionEmocional,
    RespuestaPES,
    SolicitudApoyo,
)


# =========================================================
# CONFIGURACIÓN GENERAL
# =========================================================

EMOTION_COLORS = {
    "feliz": "#f59e0b",
    "motivado": "#f97316",
    "tranquilo": "#22c55e",
    "estresado": "#eab308",
    "triste": "#3b82f6",
    "agotado": "#8b5cf6",
    "malestar": "#ef4444",
    "otro": "#64748b",
}


MOMENTOS_VALIDOS = {
    "entrada",
    "salida",
}


# =========================================================
# FUNCIONES AUXILIARES
# =========================================================

def es_administrador(user):
    """
    Define quién puede acceder al dashboard,
    solicitudes, usuarios e información administrativa.
    """

    return (
        user.is_authenticated
        and user.is_staff
    )


def obtener_config_emocion(codigo):
    """
    Retorna la configuración visual y textual
    de una emoción.
    """

    return EMOCIONES_CONFIG.get(
        codigo,
        {}
    )


def obtener_color_emocion(codigo):
    """
    Retorna el color asociado a una emoción.
    """

    return EMOTION_COLORS.get(
        codigo,
        "#64748b"
    )


def obtener_solicitud(percepcion):
    """
    Obtiene la solicitud relacionada con una percepción.

    Si no existe solicitud, retorna None.
    """

    return getattr(
        percepcion,
        "solicitud",
        None
    )


def preparar_percepcion(percepcion):
    """
    Convierte una PercepcionEmocional en la estructura
    utilizada por dashboard e historial.
    """

    config = obtener_config_emocion(
        percepcion.emocion
    )

    return {
        "registro": percepcion,

        "emoji": config.get(
            "emoji",
            "💬"
        ),

        "color": obtener_color_emocion(
            percepcion.emocion
        ),

        "solicitud": obtener_solicitud(
            percepcion
        ),
    }


def ordenar_solicitudes(queryset):
    """
    Ordena solicitudes por prioridad:

    1. Pendiente
    2. En proceso
    3. Atendida
    """

    return (
        queryset
        .annotate(
            orden_estado=Case(

                When(
                    estado="pendiente",
                    then=Value(0)
                ),

                When(
                    estado="en_proceso",
                    then=Value(1)
                ),

                default=Value(2),

                output_field=IntegerField(),
            )
        )
        .order_by(
            "orden_estado",
            "-fecha_creacion",
        )
    )


# =========================================================
# INICIO
# =========================================================

@login_required
def inicio(request):

    # ADMINISTRADOR
    if request.user.is_staff:

        return redirect(
            "dashboard"
        )


    # COLABORADOR
    # No mostramos menú ni dashboard.
    return redirect(
        "/emocional/?momento=entrada"
    )

# =========================================================
# PES
# =========================================================

@login_required
def formulario_pes(request):

    if request.method == "POST":

        form = PESForm(request.POST)

        if form.is_valid():

            respuesta = form.save(commit=False)

            respuesta.usuario = request.user

            respuesta.save()

            return redirect("pes_exito")

    else:

        form = PESForm()

    return render(
        request,
        "bienestar/formulario_pes.html",
        {
            "form": form
        }
    )


@login_required
def pes_exito(request):

    return render(
        request,
        "bienestar/pes_exito.html"
    )


# =========================================================
# PERCEPCIÓN EMOCIONAL
# =========================================================

@login_required
def formulario_emocional(request):

    if request.method == "POST":

        momento = request.POST.get(
            "momento",
            "entrada"
        )

    else:

        momento = request.GET.get(
            "momento",
            "entrada"
        )


    if momento not in {
        "entrada",
        "salida",
    }:

        momento = "entrada"


    hoy = timezone.localdate()


    respuesta_existente = (
        PercepcionEmocional.objects
        .filter(
            usuario=request.user,
            momento=momento,
            fecha__date=hoy,
        )
        .first()
    )


    if request.method == "POST":

        if respuesta_existente:

            return render(
                request,
                "bienestar/emocional_ya_respondido.html",
                {
                    "momento": momento,
                    "respuesta": respuesta_existente,
                }
            )


        form = PercepcionEmocionalForm(
            request.POST
        )


        if form.is_valid():

            respuesta = form.save(
                commit=False
            )

            respuesta.usuario = request.user

            respuesta.momento = momento

            respuesta.save()


            # =============================================
            # CREAR SOLICITUD SI PIDE APOYO
            # =============================================

            if respuesta.tipo_apoyo != "ninguno":

                SolicitudApoyo.objects.get_or_create(
                    percepcion=respuesta
                )


            # =============================================
            # MENSAJE EMOCIONAL
            # =============================================

            config = EMOCIONES_CONFIG.get(
                respuesta.emocion,
                {}
            )

            mensajes_emocion = config.get(
                "mensajes",
                []
            )


            if mensajes_emocion:

                mensaje = random.choice(
                    mensajes_emocion
                )

            else:

                mensaje = (
                    "Gracias por registrar "
                    "cómo te sientes hoy."
                )


            request.session[
                "mensaje_emocional"
            ] = mensaje

            request.session[
                "ultima_emocion"
            ] = respuesta.emocion

            request.session[
                "ultimo_momento"
            ] = momento


            return redirect(
                "emocional_exito"
            )


    else:

        if respuesta_existente:

            return render(
                request,
                "bienestar/emocional_ya_respondido.html",
                {
                    "momento": momento,
                    "respuesta": respuesta_existente,
                }
            )


        form = PercepcionEmocionalForm()


    return render(
        request,
        "bienestar/formulario_emocional.html",
        {
            "form": form,
            "emociones_config": EMOCIONES_CONFIG,
            "momento": momento,
        }
    )


@login_required
def emocional_exito(request):

    mensaje = request.session.pop(
        "mensaje_emocional",
        "Gracias por registrar cómo te sientes hoy."
    )

    emocion_codigo = request.session.pop(
        "ultima_emocion",
        None
    )

    momento = request.session.pop(
        "ultimo_momento",
        None
    )

    emocion = EMOCIONES_CONFIG.get(
        emocion_codigo,
        {}
    )

    return render(
        request,
        "bienestar/emocional_exito.html",
        {
            "mensaje": mensaje,
            "emocion": emocion,
            "momento": momento,
        }
    )


# =========================================================
# RESPUESTA EMOCIONAL REGISTRADA
# =========================================================

@login_required
def emocional_exito(request):

    mensaje = request.session.pop(
        "mensaje_emocional",
        (
            "Gracias por registrar "
            "cómo te sientes hoy."
        )
    )


    emocion_codigo = request.session.pop(
        "ultima_emocion",
        None
    )


    momento = request.session.pop(
        "ultimo_momento",
        None
    )


    emocion = obtener_config_emocion(
        emocion_codigo
    )


    return render(
        request,
        "bienestar/emocional_exito.html",
        {
            "mensaje": mensaje,
            "emocion": emocion,
            "momento": momento,
        }
    )


# =========================================================
# DASHBOARD ADMINISTRATIVO
# =========================================================

@login_required
@user_passes_test(es_administrador)
def dashboard(request):

    hoy = timezone.localdate()

    inicio_periodo = (
        hoy
        - timedelta(days=6)
    )


    # =====================================================
    # PERCEPCIONES DE HOY
    # UNA SOLA CONSULTA
    # =====================================================

    percepciones_hoy = list(

        PercepcionEmocional.objects
        .filter(
            fecha__date=hoy
        )
        .select_related(
            "usuario",
            "solicitud",
            "solicitud__atendido_por",
        )
        .order_by(
            "-fecha"
        )

    )


    total_emociones = len(
        percepciones_hoy
    )


    entradas_hoy = sum(

        1

        for percepcion
        in percepciones_hoy

        if percepcion.momento == "entrada"

    )


    salidas_hoy = sum(

        1

        for percepcion
        in percepciones_hoy

        if percepcion.momento == "salida"

    )


    # =====================================================
    # PES
    # =====================================================

    total_pes = (
        RespuestaPES.objects
        .filter(
            es_pes=True
        )
        .values(
            "usuario_id"
        )
        .distinct()
        .count()
    )


    # =====================================================
    # ESTADÍSTICAS SOLICITUDES
    # UNA SOLA CONSULTA
    # =====================================================

    estadisticas_solicitudes = (
        SolicitudApoyo.objects
        .aggregate(

            pendientes=Count(
                "id",
                filter=Q(
                    estado="pendiente"
                )
            ),

            en_proceso=Count(
                "id",
                filter=Q(
                    estado="en_proceso"
                )
            ),

            atendidas_hoy=Count(
                "id",
                filter=Q(
                    estado="atendida",
                    fecha_cierre__date=hoy,
                )
            ),
        )
    )


    solicitudes_pendientes = (
        estadisticas_solicitudes[
            "pendientes"
        ]
        or 0
    )


    solicitudes_proceso = (
        estadisticas_solicitudes[
            "en_proceso"
        ]
        or 0
    )


    atendidas_hoy = (
        estadisticas_solicitudes[
            "atendidas_hoy"
        ]
        or 0
    )


    solicitudes_abiertas = (
        solicitudes_pendientes
        +
        solicitudes_proceso
    )


    # =====================================================
    # CONTADORES EMOCIONES
    # =====================================================

    conteo_emociones = Counter(

        percepcion.emocion

        for percepcion
        in percepciones_hoy

    )


    conteo_entrada = Counter(

        percepcion.emocion

        for percepcion
        in percepciones_hoy

        if percepcion.momento == "entrada"

    )


    conteo_salida = Counter(

        percepcion.emocion

        for percepcion
        in percepciones_hoy

        if percepcion.momento == "salida"

    )


    # =====================================================
    # GRÁFICO PERCEPCIÓN
    # =====================================================

    chart_labels = []

    chart_values = []

    chart_colors = []


    for codigo, nombre in (
        PercepcionEmocional.EMOCIONES
    ):

        chart_labels.append(
            nombre
        )

        chart_values.append(
            conteo_emociones.get(
                codigo,
                0
            )
        )

        chart_colors.append(
            obtener_color_emocion(
                codigo
            )
        )


    emotion_chart = {
        "labels":
            chart_labels,

        "data":
            chart_values,

        "colors":
            chart_colors,
    }


    # =====================================================
    # ENTRADA VS SALIDA
    # =====================================================

    entrada_salida_chart = {

        "labels": [
            nombre

            for _, nombre
            in PercepcionEmocional.EMOCIONES
        ],

        "entrada": [

            conteo_entrada.get(
                codigo,
                0
            )

            for codigo, _
            in PercepcionEmocional.EMOCIONES
        ],

        "salida": [

            conteo_salida.get(
                codigo,
                0
            )

            for codigo, _
            in PercepcionEmocional.EMOCIONES
        ],
    }


    # =====================================================
    # TENDENCIA 7 DÍAS
    #
    # Antes hacíamos consultas dentro de un loop.
    # Ahora son solo 2 consultas.
    # =====================================================

    checkins_por_fecha = {

        item["fecha__date"]:
            item["total"]

        for item in (

            PercepcionEmocional.objects
            .filter(
                fecha__date__range=(
                    inicio_periodo,
                    hoy,
                )
            )
            .values(
                "fecha__date"
            )
            .annotate(
                total=Count("id")
            )

        )
    }


    solicitudes_por_fecha = {

        item["fecha_creacion__date"]:
            item["total"]

        for item in (

            SolicitudApoyo.objects
            .filter(
                fecha_creacion__date__range=(
                    inicio_periodo,
                    hoy,
                )
            )
            .values(
                "fecha_creacion__date"
            )
            .annotate(
                total=Count("id")
            )

        )
    }


    tendencia_labels = []

    tendencia_checkins = []

    tendencia_solicitudes = []


    for dias in range(
        6,
        -1,
        -1
    ):

        fecha = (
            hoy
            - timedelta(days=dias)
        )


        tendencia_labels.append(
            fecha.strftime(
                "%d/%m"
            )
        )


        tendencia_checkins.append(
            checkins_por_fecha.get(
                fecha,
                0
            )
        )


        tendencia_solicitudes.append(
            solicitudes_por_fecha.get(
                fecha,
                0
            )
        )


    trend_chart = {

        "labels":
            tendencia_labels,

        "checkins":
            tendencia_checkins,

        "solicitudes":
            tendencia_solicitudes,
    }


    # =====================================================
    # PERCEPCIONES PARA TABLA
    # =====================================================

    percepciones_dashboard = [

        preparar_percepcion(
            percepcion
        )

        for percepcion
        in percepciones_hoy

    ]


    # =====================================================
    # SOLICITUDES RECIENTES
    # =====================================================

    solicitudes_recientes = ordenar_solicitudes(

        SolicitudApoyo.objects
        .select_related(
            "percepcion",
            "percepcion__usuario",
            "atendido_por",
        )

    )[:8]


    # =====================================================
    # CONTEXTO
    # =====================================================

    context = {

        "total_emociones":
            total_emociones,

        "entradas_hoy":
            entradas_hoy,

        "salidas_hoy":
            salidas_hoy,

        "total_pes":
            total_pes,

        "solicitudes_pendientes":
            solicitudes_pendientes,

        "solicitudes_proceso":
            solicitudes_proceso,

        "solicitudes_abiertas":
            solicitudes_abiertas,

        "atendidas_hoy":
            atendidas_hoy,

        "percepciones_recientes":
            percepciones_dashboard,

        "emotion_chart":
            emotion_chart,

        "entrada_salida_chart":
            entrada_salida_chart,

        "trend_chart":
            trend_chart,

        "solicitudes_recientes":
            solicitudes_recientes,
    }


    return render(
        request,
        "bienestar/dashboard.html",
        context
    )


# =========================================================
# LISTADO DE SOLICITUDES
# =========================================================

@login_required
@user_passes_test(es_administrador)
def listado_solicitudes(request):

    # Por defecto mostramos TODAS,
    # como pediste para los líderes.

    estado = request.GET.get(
        "estado",
        "todas"
    )


    busqueda = request.GET.get(
        "q",
        ""
    ).strip()


    solicitudes = (
        SolicitudApoyo.objects
        .select_related(
            "percepcion",
            "percepcion__usuario",
            "atendido_por",
        )
        .all()
    )


    # =====================================================
    # FILTRO ESTADO
    # =====================================================

    if estado == "abiertas":

        solicitudes = (
            solicitudes
            .exclude(
                estado="atendida"
            )
        )


    elif estado in {
        "pendiente",
        "en_proceso",
        "atendida",
    }:

        solicitudes = (
            solicitudes
            .filter(
                estado=estado
            )
        )


    # =====================================================
    # BUSCADOR
    # =====================================================

    if busqueda:

        solicitudes = (
            solicitudes
            .filter(

                Q(
                    percepcion__usuario__username__icontains=busqueda
                )

                |

                Q(
                    percepcion__usuario__first_name__icontains=busqueda
                )

                |

                Q(
                    percepcion__usuario__last_name__icontains=busqueda
                )

                |

                Q(
                    percepcion__comentario__icontains=busqueda
                )

            )
        )


    solicitudes = ordenar_solicitudes(
        solicitudes
    )


    paginator = Paginator(
        solicitudes,
        20
    )


    pagina = paginator.get_page(
        request.GET.get(
            "page"
        )
    )


    return render(
        request,
        "bienestar/listado_solicitudes.html",
        {
            "pagina":
                pagina,

            "estado_actual":
                estado,

            "busqueda":
                busqueda,
        }
    )


# =========================================================
# ATENDER SOLICITUD
# =========================================================

@login_required
@user_passes_test(es_administrador)
def atender_solicitud(request, pk):

    solicitud = get_object_or_404(

        SolicitudApoyo.objects
        .select_related(
            "percepcion",
            "percepcion__usuario",
            "atendido_por",
        ),

        pk=pk
    )


    # =====================================================
    # POST
    # =====================================================

    if request.method == "POST":

        form = AtenderSolicitudForm(
            request.POST
        )


        if form.is_valid():

            with transaction.atomic():

                # Bloqueo de fila para evitar
                # dos administradores escribiendo
                # simultáneamente.

                solicitud_bloqueada = (
                    SolicitudApoyo.objects
                    .select_for_update()
                    .get(
                        pk=solicitud.pk
                    )
                )


                atencion = form.save(
                    commit=False
                )


                atencion.solicitud = (
                    solicitud_bloqueada
                )


                atencion.realizado_por = (
                    request.user
                )


                atencion.save()


                ahora = timezone.now()


                nuevo_estado = (
                    atencion.estado_resultante
                )


                solicitud_bloqueada.estado = (
                    nuevo_estado
                )


                solicitud_bloqueada.atendido_por = (
                    request.user
                )


                solicitud_bloqueada.fecha_ultima_atencion = (
                    ahora
                )


                if nuevo_estado == "atendida":

                    solicitud_bloqueada.fecha_cierre = (
                        ahora
                    )

                else:

                    solicitud_bloqueada.fecha_cierre = (
                        None
                    )


                solicitud_bloqueada.save(
                    update_fields=[
                        "estado",
                        "atendido_por",
                        "fecha_ultima_atencion",
                        "fecha_cierre",
                    ]
                )


            messages.success(
                request,
                (
                    "La atención fue registrada "
                    "correctamente."
                )
            )


            return redirect(
                "atender_solicitud",
                pk=solicitud.pk
            )


    # =====================================================
    # GET
    # =====================================================

    else:

        estado_inicial = (
            solicitud.estado
        )


        if estado_inicial == "pendiente":

            estado_inicial = (
                "en_proceso"
            )


        form = AtenderSolicitudForm(
            initial={
                "estado_resultante":
                    estado_inicial
            }
        )


    # =====================================================
    # HISTORIAL
    # =====================================================

    historial = (

        solicitud.atenciones
        .select_related(
            "realizado_por"
        )
        .order_by(
            "-fecha"
        )

    )


    config_emocion = (
        obtener_config_emocion(
            solicitud.percepcion.emocion
        )
    )


    return render(
        request,
        "bienestar/atender_solicitud.html",
        {
            "solicitud":
                solicitud,

            "form":
                form,

            "historial":
                historial,

            "emoji":
                config_emocion.get(
                    "emoji",
                    "💬"
                ),

            "recomendaciones_lider":
                config_emocion.get(
                    "recomendaciones_lider",
                    []
                ),
        }
    )


# =========================================================
# HISTORIAL DE PERCEPCIONES EMOCIONALES
# =========================================================

@login_required
@user_passes_test(es_administrador)
def listado_emociones(request):

    # =====================================================
    # FILTROS
    # =====================================================

    busqueda = request.GET.get(
        "q",
        ""
    ).strip()


    emocion = request.GET.get(
        "emocion",
        ""
    )


    momento = request.GET.get(
        "momento",
        ""
    )


    apoyo = request.GET.get(
        "apoyo",
        ""
    )


    # =====================================================
    # QUERY BASE
    # =====================================================

    respuestas = (
        PercepcionEmocional.objects
        .select_related(
            "usuario",
            "solicitud",
            "solicitud__atendido_por",
        )
        .all()
        .order_by(
            "-fecha"
        )
    )


    # =====================================================
    # BUSCAR
    # =====================================================

    if busqueda:

        respuestas = (
            respuestas
            .filter(

                Q(
                    usuario__username__icontains=busqueda
                )

                |

                Q(
                    usuario__first_name__icontains=busqueda
                )

                |

                Q(
                    usuario__last_name__icontains=busqueda
                )

                |

                Q(
                    comentario__icontains=busqueda
                )

            )
        )


    # =====================================================
    # EMOCIÓN
    # =====================================================

    codigos_emociones = {
        codigo

        for codigo, _
        in PercepcionEmocional.EMOCIONES
    }


    if emocion in codigos_emociones:

        respuestas = (
            respuestas
            .filter(
                emocion=emocion
            )
        )


    # =====================================================
    # ENTRADA / SALIDA
    # =====================================================

    if momento in MOMENTOS_VALIDOS:

        respuestas = (
            respuestas
            .filter(
                momento=momento
            )
        )


    # =====================================================
    # APOYO
    # =====================================================

    if apoyo == "si":

        respuestas = (
            respuestas
            .exclude(
                tipo_apoyo="ninguno"
            )
        )


    elif apoyo == "no":

        respuestas = (
            respuestas
            .filter(
                tipo_apoyo="ninguno"
            )
        )


    # =====================================================
    # PAGINACIÓN
    # =====================================================

    paginator = Paginator(
        respuestas,
        25
    )


    pagina = paginator.get_page(
        request.GET.get(
            "page"
        )
    )


    # Solo decoramos los 25 registros visibles,
    # no todo el historial.

    pagina.object_list = [

        preparar_percepcion(
            respuesta
        )

        for respuesta
        in pagina.object_list

    ]


    return render(
        request,
        "bienestar/listado_emociones.html",
        {
            "pagina":
                pagina,

            "emociones":
                PercepcionEmocional.EMOCIONES,

            "busqueda":
                busqueda,

            "emocion_actual":
                emocion,

            "momento_actual":
                momento,

            "apoyo_actual":
                apoyo,
        }
    )


# =========================================================
# LISTADO PES
# =========================================================

@login_required
@user_passes_test(es_administrador)
def listado_pes(request):

    respuestas = (
        RespuestaPES.objects
        .select_related(
            "usuario"
        )
        .order_by(
            "-fecha"
        )
    )


    return render(
        request,
        "bienestar/listado_pes.html",
        {
            "respuestas":
                respuestas
        }
    )


# =========================================================
# CREAR USUARIO
# =========================================================

@login_required
@user_passes_test(es_administrador)
def crear_usuario(request):

    if request.method == "POST":

        form = CrearUsuarioForm(
            request.POST
        )


        if form.is_valid():

            nuevo_usuario = (
                form.save()
            )


            messages.success(
                request,
                (
                    f"Usuario "
                    f"{nuevo_usuario.username} "
                    "creado correctamente."
                )
            )


            return redirect(
                "listado_usuarios"
            )


    else:

        form = CrearUsuarioForm()


    return render(
        request,
        "bienestar/crear_usuario.html",
        {
            "form":
                form
        }
    )


# =========================================================
# LISTADO DE USUARIOS
# =========================================================

@login_required
@user_passes_test(es_administrador)
def listado_usuarios(request):

    busqueda = request.GET.get(
        "q",
        ""
    ).strip()


    usuarios = (
        User.objects
        .all()
        .order_by(
            "username"
        )
    )


    if busqueda:

        usuarios = (
            usuarios
            .filter(

                Q(
                    username__icontains=busqueda
                )

                |

                Q(
                    first_name__icontains=busqueda
                )

                |

                Q(
                    last_name__icontains=busqueda
                )

                |

                Q(
                    email__icontains=busqueda
                )

            )
        )


    return render(
        request,
        "bienestar/listado_usuarios.html",
        {
            "usuarios":
                usuarios,

            "busqueda":
                busqueda,
        }
    )