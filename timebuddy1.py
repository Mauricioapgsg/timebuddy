import streamlit as st
from datetime import date, datetime, timedelta
import random

# ------------------------------
# Inicialización de variables
# ------------------------------
if "perfil" not in st.session_state:
    st.session_state["perfil"] = {}
if "diario_emocional" not in st.session_state:
    st.session_state["diario_emocional"] = {}
if "puntos" not in st.session_state:
    st.session_state["puntos"] = 0
if "logros" not in st.session_state:
    st.session_state["logros"] = set()
if "tareas" not in st.session_state:
    st.session_state["tareas"] = []
if "chat_historial" not in st.session_state:
    st.session_state["chat_historial"] = []

# ------------------------------
# Respuestas y tips
# ------------------------------
respuestas_emocion = {
    "motivado": "¡Me alegra saber que estás motivado! Aprovecha ese impulso para avanzar.",
    "estresado": "Tómalo con calma. Respira profundo, divide la tarea en pasos pequeños y empieza con lo más fácil.",
    "aburrido": "A veces solo necesitamos un poco de ritmo. ¿Qué tal si pones música mientras trabajas?",
    "neutral": "Perfecto. Mantén ese equilibrio y empieza poco a poco.",
    "triste": "Lo más importante es que estás aquí y estás intentando. Yo te acompaño. Empieza con algo pequeño."
}

motivational_tips = [
    "Divide tareas grandes en metas pequeñas y celebra cada avance.",
    "Pon un temporizador de 25 minutos. Trabaja enfocado y luego toma un pequeño descanso.",
    "Recuerda por qué empezaste: cada tarea te acerca a tu meta.",
    "No necesitas sentirte motivado para empezar. A veces, solo empezar genera motivación.",
    "Tu esfuerzo hoy es la clave del éxito de mañana. ¡Vamos paso a paso!"
]

# ------------------------------
# Interfaz de chat
# ------------------------------
st.title("TimeBuddy - Tu asistente contra la procrastinación")

chat_input = st.chat_input("¿En qué puedo ayudarte hoy?")

if chat_input:
    st.session_state["chat_historial"].append(("usuario", chat_input))

    respuesta = "No estoy seguro de cómo responder a eso. ¿Podrías reformularlo?"

    mensaje = chat_input.lower()
    if "hola" in mensaje:
        respuesta = "¡Hola! Soy TimeBuddy, tu compañero para vencer la procrastinación. ¿Quieres registrar una tarea, revisar tus pendientes o necesitas un tip de motivación?"
    elif "tip" in mensaje or "motivación" in mensaje:
        respuesta = random.choice(motivational_tips)
    elif "tarea" in mensaje:
        respuesta = "Recuerda que puedes registrar una tarea en la sección de tareas. Solo indícame el nombre, materia, fecha y prioridad."
    elif "emocion" in mensaje or "emocional" in mensaje:
        respuesta = "¿Cómo te sientes ahora? motivado, estresado, aburrido, neutral o triste?"
    elif any(e in mensaje for e in respuestas_emocion):
        for k in respuestas_emocion:
            if k in mensaje:
                respuesta = respuestas_emocion[k]
                break
    elif "gracias" in mensaje:
        respuesta = "¡Para eso estoy! Sigue avanzando, lo estás haciendo bien."
    elif "resumen" in mensaje:
        respuesta = "¡Buen trabajo revisando tu semana! Recuerda: organizarse es el primer paso para lograrlo todo."

    st.session_state["chat_historial"].append(("timebuddy", respuesta))

# Mostrar historial de chat
for autor, mensaje in st.session_state["chat_historial"]:
    with st.chat_message("assistant" if autor == "timebuddy" else "user"):
        st.markdown(mensaje)