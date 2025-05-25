import streamlit as st
import datetime
import random
import matplotlib.pyplot as plt

st.set_page_config(page_title="TimeBuddy", layout="wide")
st.markdown("<h1 style='color:#333333;'>TimeBuddy</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#666666;'>Tu asistente contra la procrastinación</p>", unsafe_allow_html=True)
st.markdown("---")

# Estado de sesión
if "tareas" not in st.session_state:
    st.session_state.tareas = []
if "usuario" not in st.session_state:
    st.session_state.usuario = {"nombre": "", "carrera": "", "meta": ""}
if "emociones" not in st.session_state:
    st.session_state.emociones = []
if "puntos" not in st.session_state:
    st.session_state.puntos = 0

respuestas_emocion = {
    "motivado": "¡Me alegra saber que estás motivado! Aprovecha ese impulso para avanzar.",
    "estresado": "Tómalo con calma. Respira profundo, divide la tarea en pasos pequeños y empieza con lo más fácil.",
    "aburrido": "A veces solo necesitamos un poco de ritmo. ¿Qué tal si pones música mientras trabajas?",
    "neutral": "Perfecto. Mantén ese equilibrio y empieza poco a poco.",
    "triste": "Lo más importante es que estás aquí y estás intentando. Yo te acompaño. Empieza con algo pequeño."
}

tips = [
    "Divide tareas grandes en metas pequeñas y celebra cada avance.",
    "Pon un temporizador de 25 minutos. Trabaja enfocado y luego toma un pequeño descanso.",
    "Recuerda por qué empezaste: cada tarea te acerca a tu meta.",
    "No necesitas sentirte motivado para empezar. A veces, solo empezar genera motivación.",
    "Tu esfuerzo hoy es la clave del éxito de mañana. ¡Vamos paso a paso!"
]

def nivel_actual(puntos):
    if puntos < 20:
        return "Principiante"
    elif puntos < 50:
        return "Intermedio"
    else:
        return "Proactivo"

menu = st.sidebar.selectbox("Menú", [
    "Perfil de Usuario", "Registrar Tarea", "Ver Horario Semanal", "Diario Emocional",
    "Resumen Semanal", "Ver Tips", "Gamificación"
])

# PERFIL
if menu == "Perfil de Usuario":
    st.markdown("### Perfil del Usuario")
    with st.form("perfil"):
        nombre = st.text_input("Nombre", st.session_state.usuario["nombre"])
        carrera = st.text_input("Carrera", st.session_state.usuario["carrera"])
        meta = st.text_area("Meta académica o personal", st.session_state.usuario["meta"])
        submit = st.form_submit_button("Guardar")
        if submit:
            st.session_state.usuario.update({"nombre": nombre, "carrera": carrera, "meta": meta})
            st.success("Perfil guardado correctamente.")

# REGISTRO DE TAREA
elif menu == "Registrar Tarea":
    st.markdown("### Registrar nueva tarea")
    with st.form("tarea_form"):
        nombre = st.text_input("Nombre de la tarea")
        materia = st.text_input("Materia")
        fecha = st.date_input("Fecha", datetime.date.today())
        hora = st.time_input("Hora")
        emocion = st.selectbox("¿Cómo te sientes?", list(respuestas_emocion.keys()))
        guardar = st.form_submit_button("Guardar tarea")
        if guardar:
            st.session_state.tareas.append({
                "nombre": nombre, "materia": materia, "fecha": fecha,
                "hora": hora.strftime("%H:%M"), "emocion": emocion
            })
            st.session_state.emociones.append({"fecha": fecha, "emocion": emocion})
            st.session_state.puntos += 5
            st.success(f"Tarea guardada. {respuestas_emocion[emocion]} +5 puntos.")

# HORARIO SEMANAL
elif menu == "Ver Horario Semanal":
    st.markdown("### Horario semanal")
    dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    horario = {dia: [] for dia in dias}
    for t in st.session_state.tareas:
        dia_eng = t["fecha"].strftime("%A")
        dia_es = dias[["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"].index(dia_eng)]
        horario[dia_es].append(f"{t['hora']} - {t['nombre']} ({t['materia']})")
    cols = st.columns(7)
    for i, dia in enumerate(dias):
        with cols[i]:
            st.markdown(f"{dia}")
            for tarea in sorted(horario[dia]):
                st.markdown(f"- {tarea}")

# DIARIO EMOCIONAL
elif menu == "Diario Emocional":
    st.markdown("### Diario emocional")
    if st.session_state.emociones:
        fechas = [e["fecha"] for e in st.session_state.emociones]
        emociones = [e["emocion"] for e in st.session_state.emociones]
        fig, ax = plt.subplots()
        ax.plot(fechas, emociones, marker="o", linestyle="-", color="#1f77b4")
        ax.set_title("Emociones durante la semana")
        ax.set_ylabel("Emoción")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.info("Aún no hay emociones registradas.")

# RESUMEN SEMANAL
elif menu == "Resumen Semanal":
    st.markdown("### Resumen semanal")
    total = len(st.session_state.tareas)
    st.write(f"Has registrado *{total} tareas*.")
    if total:
        emociones_contadas = {e: 0 for e in respuestas_emocion}
        for t in st.session_state.tareas:
            emociones_contadas[t["emocion"]] += 1
        st.write("Estado emocional general:")
        st.bar_chart(emociones_contadas)
    st.success("¡Buen trabajo revisando tu semana!")

# TIPS MOTIVACIONALES
elif menu == "Ver Tips":
    st.markdown("### Tip motivacional del día")
    st.info(random.choice(tips))

# GAMIFICACIÓN
elif menu == "Gamificación":
    st.markdown("### Tu progreso")
    puntos = st.session_state.puntos
    nivel = nivel_actual(puntos)
    st.metric("Puntos acumulados", puntos)
    st.metric("Nivel actual", nivel)
    st.progress(min(puntos / 50, 1.0))
    st.markdown("¡Sigue sumando tareas para subir de nivel!")

