from flask import Flask, render_template, request, redirect, url_for, session
import time
import random

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
#   - Aquí se muestran 10 preguntas de ejemplo. Deberás completar hasta las 100.
# ---------------------------------------------------------------------

questions = [
   {
        "number": 1,
        "question": "La administración de propiedades incluye todas estas funciones excepto:",
        "options": {
            "a": "el cobro de la renta",
            "b": "el alquiler de la propiedad",
            "c": "la representación del propietario",
            "d": "la supervisión y mantenimiento de la propiedad."
        },
        "correct": "c"
    },
    {
        "number": 2,
        "question": "El asociado de ventas Luis realiza una opinión de precio para una propiedad. ¿El asociado de ventas cobra honorarios por sus servicios por concepto de una valuación (appraisal) Esto es?",
        "options": {
            "a": "una violación al Capítulo 120.",
            "b": "una violación a la ley de vivienda justa de 1968.",
            "c": "una violación al capítulo 475 por lo que Luis recibirá una sanción.",
            "d": "una violación a la ley de los derechos civiles de 1866."
        },
        "correct": "c"
    },
    {
        "number": 3,
        "question": "Cuando un concesionario recolecta información para ser presentada referente a propiedades que se vendieron, propiedades que están en el mercado y propiedades que han expirado. El concesionario está haciendo:",
        "options": {
            "a": "una Valoración",
            "b": "un estimado de gastos",
            "c": "un análisis comparativo del mercado",
            "d": "un GRM"
        },
        "correct": "c"
    },
    {
        "number": 4,
        "question": "Cuando un tasador de bienes raíces o un corredor de bienes raíces realizan una tasación deben regirse conforme a las normas de:",
        "options": {
            "a": "FREC",
            "b": "USPAP",
            "c": "FREAB",
            "d": "RESPA"
        },
        "correct": "b"
    },
    {
        "number": 5,
        "question": "La administración de propiedades incluye todas estas funciones excepto:",
        "options": {
            "a": "el cobro de la renta",
            "b": "el alquiler de la propiedad",
            "c": "la representación del propietario",
            "d": "la supervisión y mantenimiento de la propiedad."
        },
        "correct": "c"
    },
    {
        "number": 6,
        "question": "¿Quién se preocupa de promover la educación y la ética en la industria de bienes raíces?",
        "options": {
            "a": "FREC",
            "b": "DBPR",
            "c": "La Asociación Nacional de Realtors",
            "d": "Las oficinas de bienes raíces"
        },
        "correct": "c"
    },
    {
        "number": 7,
        "question": "¿Los dueños ausentes (absentee owners) han aumentado la demanda en qué campo del corretaje?",
        "options": {
            "a": "corretaje de oportunidades de negocios",
            "b": "ventas comerciales",
            "c": "ventas de propiedades agrícolas",
            "d": "manejo de propiedades."
        },
        "correct": "d"
    },
    {
        "number": 8,
        "question": "El propietario de una estación de gasolina quien posee una licencia de vendedor asociado inactiva ha sido nombrado por la corte para que haga la tasación (appraisal) de otra estación de gasolina. ¿Cuál de las siguientes afirmaciones aplica a esta situación?",
        "options": {
            "a": "Dado que esta persona posee una licencia de bienes raíces, él puede recibir compensación por este servicio de bienes raíces",
            "b": "Él tendría que tener su licencia activa para poder recibir pago por su trabajo",
            "c": "Él puede recibir compensación económica pero solamente de manos de un corredor",
            "d": "Él puede recibir compensación directamente por sus servicios."
        },
        "correct": "d"
    },
    {
        "number": 9,
        "question": "Un broker de Georgia trae un prospecto a Jacksonville, FL. para que compre una propiedad. El broker de Georgia participa en la negociación de la propiedad. ¿Cuál de las siguientes declaraciones es la verdadera? El broker de la Florida puede:",
        "options": {
            "a": "Expresarle un sincero agradecimiento al broker de Georgia",
            "b": "Pagarle al broker de Georgia sus gastos de estadía en la Florida",
            "c": "Pagar al broker de Georgia un porcentaje de la comisión",
            "d": "Hacer nada, debido a que, por ley, el broker de la Florida no puede repartir comisión o pagar gastos a un broker foráneo en estas circunstancias."
        },
        "correct": "d"
    },
    {
        "number": 10,
        "question": "Jorge es un inversionista muy exitoso en bienes raíces, últimamente él ha estado muy ocupado en sus negocios, por eso, le pide a su hija (no licenciada) que lo ayude con la venta de una de sus propiedades y como recompensa le entregará $2,000. Según la situación descrita anteriormente ¿Cuál de los siguientes enunciados es el correcto?",
        "options": {
            "a": "Ella puede hacer esto porque es su hija y su padre no tiene tiempo para hacerlo",
            "b": "Esto es una violación al capítulo 475.",
            "c": "Esto es legal si ella hubiera recibido menos de $2000 de compensación",
            "d": "Esto no es una violación del capítulo 475"
        },
        "correct": "b"
    }
    # ---------------------------------------------------------------------
    # Continúa aquí con el resto de las preguntas hasta llegar a 100.
    # ---------------------------------------------------------------------
]

TOTAL_QUESTIONS = len(questions)
PASSING_SCORE = 75  # Se requieren al menos 75 puntos para aprobar
EXAM_DURATION_SECONDS = 90 * 60  # 90 minutos

# ----------------------------------------------------------
# Inicio del examen: se limpia la sesión y se establece el orden normal (sin mezclar)
# ----------------------------------------------------------
@app.route("/")
def index():
    session.clear()
    session["start_time"] = time.time()
    session["answers"] = {}
    # Orden normal: del 1 al TOTAL_QUESTIONS sin mezclar.
    session["questions_order"] = list(range(1, TOTAL_QUESTIONS + 1))
    return redirect(url_for("question", qnum=1))

# ----------------------------------------------------------
# Ruta para activar el modo aleatorio cuando el usuario lo presiona.
# ----------------------------------------------------------
@app.route("/randomize")
def randomize():
    session["questions_order"] = list(range(1, TOTAL_QUESTIONS + 1))
    random.shuffle(session["questions_order"])
    return redirect(url_for("question", qnum=1))

# ----------------------------------------------------------
# Ruta que muestra cada pregunta de forma secuencial según el orden definido.
# Se muestra también cuántas preguntas faltan.
# ----------------------------------------------------------
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
        # Se obtiene el número real de la pregunta según el orden guardado.
        current_qnum = session.get("questions_order")[qnum - 1]
        answers[str(current_qnum)] = answer
        session["answers"] = answers
        if qnum < TOTAL_QUESTIONS:
            return redirect(url_for("question", qnum=qnum + 1))
        else:
            return redirect(url_for("result"))
    
    # Obtener el número real de la pregunta a mostrar.
    real_qnum = session.get("questions_order")[qnum - 1]
    current_question = next((q for q in questions if q["number"] == real_qnum), None)
    if current_question is None:
        return "Pregunta no encontrada", 404

    # Calcular cuántas preguntas faltan para terminar el examen.
    remaining_count = TOTAL_QUESTIONS - qnum

    return render_template("question.html",
                           question=current_question,
                           remaining=int(remaining),
                           remaining_count=remaining_count,
                           total=TOTAL_QUESTIONS)

# ----------------------------------------------------------
# Ruta que muestra el resultado del examen, incluyendo las preguntas erróneas.
# ----------------------------------------------------------
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
