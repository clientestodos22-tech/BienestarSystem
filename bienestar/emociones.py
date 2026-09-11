# bienestar/emociones.py


EMOCIONES_CONFIG = {

    "feliz": {
        "nombre": "Feliz / contento(a)",
        "emoji": "😊",

        "mensajes": [
            "¡Qué bueno saberlo! Aprovecha esta energía positiva durante tu jornada.",
            "Tu bienestar también suma al equipo. ¡Que tengas una excelente jornada!",
            "Disfruta este buen momento y compártelo con quienes te rodean.",
            "Los buenos días también cuentan. ¡Aprovéchalo!",
        ],

        "acciones": [],

        "recomendaciones_lider": [],
    },


    "motivado": {
        "nombre": "Motivado(a) / con energía",
        "emoji": "⚡",

        "mensajes": [
            "¡Excelente! Aprovecha tu energía para avanzar en tus objetivos de hoy.",
            "Tu motivación es un gran impulso. Recuerda mantener un ritmo saludable.",
            "¡Vamos por un buen día! Mantén esa energía cuidando también tus pausas.",
            "Una buena energía puede hacer una gran diferencia en la jornada.",
        ],

        "acciones": [],

        "recomendaciones_lider": [],
    },


    "tranquilo": {
        "nombre": "Tranquilo(a)",
        "emoji": "😌",

        "mensajes": [
            "La tranquilidad también es bienestar. Mantén ese equilibrio durante tu jornada.",
            "Un día tranquilo es una buena oportunidad para trabajar con foco y equilibrio.",
            "Sigue cuidando ese espacio de calma durante tu jornada.",
            "El equilibrio también es parte de un trabajo seguro y saludable.",
        ],

        "acciones": [],

        "recomendaciones_lider": [],
    },


    "estresado": {
        "nombre": "Preocupado(a) / estresado(a)",
        "emoji": "😟",

        "mensajes": [
            "Recuerda que puedes solicitar apoyo cuando lo necesites.",
            "Una pequeña pausa puede ayudarte a recuperar el foco.",
            "No dudes en conversar con tu líder o una persona de confianza.",
            "Revisar tus prioridades puede ayudarte a reducir la sobrecarga.",
        ],

        "acciones": [
            {
                "id": "conversar_lider",
                "texto": "Conversar con mi Manager / líder o una persona de confianza.",
            },
            {
                "id": "solicitar_apoyo",
                "texto": "Solicitar apoyo cuando lo requiera.",
            },
            {
                "id": "pausa_activa",
                "texto": "Utilizar técnicas de respiración o realizar una pausa activa.",
            },
            {
                "id": "revisar_prioridades",
                "texto": "Revisar mis prioridades y evitar sobrecargarme.",
            },
        ],

        "recomendaciones_lider": [
            "Realizar una conversación individual de apoyo.",
            "Revisar prioridades y carga de trabajo.",
            "Identificar posibles factores laborales relacionados con el estrés.",
            "Facilitar el acceso a los canales de apoyo disponibles.",
        ],
    },


    "triste": {
        "nombre": "Desanimado(a) / triste",
        "emoji": "😔",

        "mensajes": [
            "Conversar con alguien de confianza puede ayudarte.",
            "Recuerda que puedes solicitar apoyo si lo necesitas.",
            "Cuidar tu bienestar también es parte de tu jornada.",
        ],

        "acciones": [
            {
                "id": "conversar_confianza",
                "texto": "Conversar con alguien de confianza.",
            },
            {
                "id": "evitar_aislarse",
                "texto": "Evitar aislarme y buscar compañía si lo necesito.",
            },
            {
                "id": "solicitar_apoyo_persistente",
                "texto": "Solicitar apoyo si esta sensación persiste.",
            },
            {
                "id": "usar_recursos",
                "texto": "Utilizar los recursos de apoyo disponibles.",
            },
        ],

        "recomendaciones_lider": [
            "Generar un espacio seguro y respetuoso de conversación.",
            "Escuchar sin juzgar.",
            "Mostrar interés genuino por el bienestar de la persona.",
            "Facilitar apoyo y seguimiento cuando corresponda.",
        ],
    },


    "agotado": {
        "nombre": "Agotado(a) / con poca energía",
        "emoji": "😴",

        "mensajes": [
            "La recuperación también es parte de una jornada segura.",
            "Escuchar las señales de cansancio ayuda a prevenir riesgos.",
            "Recuerda realizar tus pausas y comunicar si necesitas apoyo.",
        ],

        "acciones": [
            {
                "id": "informar_condicion",
                "texto": "Informar oportunamente cómo me encuentro.",
            },
            {
                "id": "pausa_recuperacion",
                "texto": "Realizar pausas de recuperación.",
            },
            {
                "id": "hidratacion",
                "texto": "Mantener una hidratación adecuada.",
            },
            {
                "id": "revisar_descanso",
                "texto": "Revisar mis períodos de descanso.",
            },
            {
                "id": "informar_riesgo",
                "texto": "Comunicar si la fatiga afecta la realización segura de mis tareas.",
            },
        ],

        "recomendaciones_lider": [
            "Evaluar posibles factores de fatiga física o mental.",
            "Revisar jornadas, descansos y carga de trabajo.",
            "Reorganizar tareas cuando corresponda.",
            "Favorecer la recuperación antes de que la fatiga afecte la seguridad.",
        ],
    },


    "malestar": {
        "nombre": "Con malestar físico / enfermo(a)",
        "emoji": "🤒",

        "mensajes": [
            "Tu salud y seguridad son importantes.",
            "Comunica oportunamente si tu estado afecta la realización segura de tus tareas.",
            "Recuerda utilizar los canales de apoyo disponibles cuando lo necesites.",
        ],

        "acciones": [
            {
                "id": "informar_salud",
                "texto": "Informar oportunamente mi condición.",
            },
            {
                "id": "seguir_indicaciones",
                "texto": "Seguir las indicaciones médicas que correspondan.",
            },
            {
                "id": "ajuste_temporal",
                "texto": "Consultar si necesito ajustes temporales en mis tareas.",
            },
            {
                "id": "evitar_riesgo",
                "texto": "Evitar actividades que no pueda realizar de forma segura.",
            },
        ],

        "recomendaciones_lider": [
            "Evaluar si existen medidas temporales de apoyo o adaptación.",
            "Facilitar los canales correspondientes.",
            "Revisar si la condición puede afectar la ejecución segura de las tareas.",
            "Respetar la privacidad y confidencialidad de la persona.",
        ],
    },


    "otro": {
        "nombre": "Otro",
        "emoji": "💬",

        "mensajes": [
            "Gracias por contarnos cómo te sientes.",
            "Recuerda que los canales de apoyo están disponibles cuando los necesites.",
        ],

        "acciones": [
            {
                "id": "conversar_confianza",
                "texto": "Conversar con alguien de confianza.",
            },
            {
                "id": "solicitar_apoyo",
                "texto": "Solicitar apoyo.",
            },
            {
                "id": "usar_canales",
                "texto": "Utilizar los canales de comunicación disponibles.",
            },
        ],

        "recomendaciones_lider": [
            "Escuchar activamente.",
            "Comprender la situación antes de actuar.",
            "Identificar necesidades específicas.",
            "Gestionar apoyo interno o externo cuando corresponda.",
        ],
    },

}