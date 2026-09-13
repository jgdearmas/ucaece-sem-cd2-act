"""Plantillas de prompting parametrizables (few-shot y chain-of-thought).

`main.py` no arma prompts a mano: llama a una de estas funciones con la
consulta del usuario y obtiene el prompt final ya armado con la técnica
correspondiente. Reemplazá los ejemplos por los de tu propio caso de uso
(consigna 1) antes de entregar.
"""

# --- Ejemplos few-shot con razonamiento paso a paso (few-shot + chain-of-thought) ---
EJEMPLOS_FEW_SHOT = [
    {
        "consulta": "¿Como agrego usuarios a mi empresa?",
        "respuesta": (
            "Pensemos paso a paso: esta consulta es sobre gestión de accesos, no sobre una "
            "operatoria del día a día, así que corresponde a la sección de Configuración "
            "Dentro de Configuración, el alta de usuarios tiene su propia pantalla dedicada. "
            "Por lo tanto: Andá a Configuración > Usuarios > Alta de Usuario y completá los campos obligatorios."
        ),
    },
    {
        "consulta": "¿Como subo una deuda?",
        "respuesta": (
            "Pensemos paso a paso: esto es una carga de deuda, así que primero hay que definir "
            "en qué formato tenés el archivo. Tenés tres opciones: los formatos ya conocidos "
            "Banelco o Link, o si no tenés ninguno, podes descargar la plantilla de ejemplo y completar "
            "los datos básicos vos mismo. Una vez que el archivo está en cualquiera de esas 3 "
            "variantes, el flujo de carga es el mismo. Por lo tanto: andá al acceso directo "
            "Publicación de Deuda > Cargar Archivo. El sistema muestra el resultado; si hay "
            "errores, corregilos en pantalla y presioná Confirmar Archivo."
        ),
    },
    {
        "consulta": "¿Que medios de pago tengo habilitados?",
        "respuesta": (
            "Pensemos paso a paso: esta consulta es sobre configuración de cobranza, no sobre "
            "una operación puntual, así que hay que revisar qué medios están activados a nivel "
            "cuenta antes de responder cuáles puede usar un cliente. Por lo tanto: "
            "los Medios de pago habilitados son efectivo, tarjeta credito/debito, QR."
        ),
    },
    {
        "consulta": "¿Como puedo adherir debitos automaticos?",
        "respuesta": (
            "Pensemos paso a paso: adherir un débito automático es distinto de publicar una "
            "deuda puntual, porque implica una autorización recurrente del cliente y no una "
            "carga única. Por lo tanto hay que ubicar la sección específica de adhesiones, no la "
            "de publicación de deuda. Por lo tanto: Ir al menu de Acceso Directo > adhesion de debitos"
        ),
    },
]

INSTRUCCION_CHAIN_OF_THOUGHT = (
    "Antes de responder, pensá el problema paso a paso en voz alta. "
    "Al final, escribí la respuesta definitiva precedida por 'Respuesta:'."
)


def construir_prompt_few_shot(consulta: str, ejemplos: list[dict] = EJEMPLOS_FEW_SHOT) -> str:
    """Arma un prompt few-shot: muestra pares consulta/respuesta de ejemplo y
    al final agrega la consulta real del usuario sin responder."""
    bloques_ejemplo = [
        f"Consulta: {ejemplo['consulta']}\nRespuesta: {ejemplo['respuesta']}"
        for ejemplo in ejemplos
    ]
    ejemplos_formateados = "\n\n".join(bloques_ejemplo)

    return (
        f"{ejemplos_formateados}\n\n"
        f"Consulta: {consulta}\n"
        "Respuesta:"
    )


def construir_prompt_chain_of_thought(consulta: str) -> str:
    """Arma un prompt chain-of-thought: le pide al modelo razonar paso a paso
    antes de dar la respuesta final."""
    return f"{INSTRUCCION_CHAIN_OF_THOUGHT}\n\nConsulta: {consulta}"
