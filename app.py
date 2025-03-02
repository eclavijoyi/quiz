from flask import Flask, render_template, request, redirect, url_for, session
import time

app = Flask(__name__)
app.secret_key = "clave-secreta-para-sessions"  # Cambia esto por seguridad

# ---------------------------------------------------------------------
# Definición de las 100 preguntas en una lista de diccionarios.
# Cada diccionario contiene:
#  - 'number': número de pregunta
#  - 'question': el enunciado
#  - 'options': un diccionario con las opciones (a, b, c, d)
#  - 'correct': la respuesta correcta ("a", "b", "c" o "d")
#
# IMPORTANTE:
#  - Reemplaza las respuestas de ejemplo por las correctas según tu clave.
# ---------------------------------------------------------------------

questions = [
    {
        "number": 1,
        "question": "La administración de propiedades incluye todas estas funciones EXCEPTO:",
        "options": {
            "a": "El cobro de la renta",
            "b": "El alquiler de la propiedad",
            "c": "La representación del propietario",
            "d": "La supervisión y mantenimiento de la propiedad"
        },
        "correct": "c"  # Ajusta según la clave real
    },
    {
        "number": 2,
        "question": "El asociado de ventas Luis realiza una opinión de precio... Esto es:",
        "options": {
            "a": "Una violación al Capítulo 120.",
            "b": "Una violación a la ley de vivienda justa de 1968.",
            "c": "Una violación al capítulo 475 por lo que Luis recibirá una sanción.",
            "d": "Una violación a la ley de derechos civiles de 1866."
        },
        "correct": "c"  # Ajusta según la clave real
    },
    {
        "number": 3,
        "question": "Cuando un concesionario recolecta información sobre propiedades vendidas, en mercado y expiradas, está haciendo:",
        "options": {
            "a": "Una valoración",
            "b": "Un estimado de gastos",
            "c": "Un análisis comparativo de mercado (CMA)",
            "d": "Un GRM"
        },
        "correct": "c"  # Ajusta según la clave real
    },
    {
        "number": 4,
        "question": "Cuando un tasador o un corredor realizan una tasación, deben regirse conforme a las normas de:",
        "options": {
            "a": "FREC",
            "b": "USPAP",
            "c": "FREAB",
            "d": "RESPA"
        },
        "correct": "b"  # Ajusta según la clave real
    },
    {
        "number": 5,
        "question": "La administración de propiedades incluye todas estas funciones EXCEPTO:",
        "options": {
            "a": "El cobro de la renta",
            "b": "El alquiler de la propiedad",
            "c": "La representación del propietario",
            "d": "La supervisión y mantenimiento de la propiedad"
        },
        "correct": "c"  # Observa que es la misma que la #1 en el PDF
    },
    # ---------------------------------------------------------------------
    # Continúa aquí con el resto de las preguntas hasta llegar a las 100.
    # ---------------------------------------------------------------------
]

# Parámetros de configuración
TOTAL_QUESTIONS = len(questions)
PASSING_SCORE = 75  # Se requiere al menos 75 puntos para aprobar
EXAM_DURATION_SECONDS = 3 * 60 * 60 + 30 * 60  # 3 horas 30 minutos en segundos

@app.route("/", methods=["GET", "POST"])
def exam():
    if request.method == "POST":
        # Recoger las respuestas del usuario
        user_answers = {}
        for q in questions:
            q_number = str(q["number"])
            user_answers[q_number] = request.form.get(q_number, None)

        # Calcular el puntaje y recopilar los errores
        score = 0
        errors = []
        for q in questions:
            q_num = str(q["number"])
            if user_answers[q_num] == q["correct"]:
                score += 1
            else:
                errors.append({
                    "number": q["number"],
                    "question": q["question"],
                    "correct_answer_key": q["correct"],
                    "correct_answer_text": q["options"][q["correct"]]
                })

        passed = (score >= PASSING_SCORE)

        return render_template("exam.html",
                               submitted=True,
                               score=score,
                               total=TOTAL_QUESTIONS,
                               passed=passed,
                               questions=questions,
                               user_answers=user_answers,
                               errors=errors)

    # Muestra el formulario si es GET
    return render_template("exam.html",
                           submitted=False,
                           questions=questions,
                           total=TOTAL_QUESTIONS)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
