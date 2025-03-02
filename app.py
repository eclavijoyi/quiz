from flask import Flask, render_template, request, redirect, url_for, session
import time

app = Flask(__name__)
app.secret_key = "clave-secreta-para-sessions"  # Cambia esto por una clave segura

# ---------------------------------------------------------------------
# Definición de las preguntas en una lista de diccionarios.
# Cada diccionario contiene:
#   - "number": número de pregunta
#   - "question": enunciado de la pregunta
#   - "options": diccionario con las opciones ("a", "b", "c", "d")
#   - "correct": respuesta correcta ("a", "b", "c" o "d")
#
# IMPORTANTE:
#   - Aquí se muestran 5 preguntas de ejemplo. Deberás completar hasta las 100.
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
        "correct": "c"  # Ajusta según la clave real
    },
    # ---------------------------------------------------------------------
    # Continúa aquí con el resto de las preguntas hasta llegar a 100.
    # ---------------------------------------------------------------------
]

TOTAL_QUESTIONS = len(questions)
PASSING_SCORE = 75  # Se requieren al menos 75 puntos para aprobar
EXAM_DURATION_SECONDS = 3 * 60 * 60 + 30 * 60  # 3 horas 30 minutos

@app.route("/")
def index():
    # Inicia el examen: limpia la sesión, registra el tiempo de inicio y crea el diccionario de respuestas.
    session.clear()
    session["start_time"] = time.time()
    session["answers"] = {}
    return redirect(url_for("question", qnum=1))

@app.route("/question/<int:qnum>", methods=["GET", "POST"])
def question(qnum):
    # Verificar si el tiempo del examen expiró.
    elapsed = time.time() - session.get("start_time", time.time())
    remaining = EXAM_DURATION_SECONDS - elapsed
    if remaining <= 0:
        return redirect(url_for("result"))
    
    # Procesa la respuesta enviada para la pregunta actual.
    if request.method == "POST":
        answer = request.form.get("answer")
        answers = session.get("answers", {})
        answers[str(qnum)] = answer
        session["answers"] = answers
        if qnum < TOTAL_QUESTIONS:
            return redirect(url_for("question", qnum=qnum + 1))
        else:
            return redirect(url_for("result"))
    
    # Obtener la pregunta actual.
    current_question = next((q for q in questions if q["number"] == qnum), None)
    if current_question is None:
        return "Pregunta no encontrada", 404

    return render_template("question.html",
                           question=current_question,
                           remaining=int(remaining),
                           total=TOTAL_QUESTIONS)

@app.route("/result")
def result():
    answers = session.get("answers", {})
    score = 0
    errors = []
    for q in questions:
        q_num = str(q["number"])
        user_ans = answers.get(q_num, None)
        if user_ans == q["correct"]:
            score += 1
        else:
            errors.append({
                "number": q["number"],
                "question": q["question"],
                "correct_answer_key": q["correct"],
                "correct_answer_text": q["options"][q["correct"]]
            })
    passed = (score >= PASSING_SCORE)
    return render_template("result.html",
                           score=score,
                           total=TOTAL_QUESTIONS,
                           passed=passed,
                           errors=errors)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
