from flask import Flask, render_template, request, redirect, url_for, session
import time
import random
from questions import questions, TOTAL_QUESTIONS, PASSING_SCORE, EXAM_DURATION_SECONDS

app = Flask(__name__)
app.secret_key = "clave-secreta-para-sessions"  # Cambia esto por una clave segura

# Ruta principal: inicia el examen en orden normal (1, 2, 3, …)
@app.route("/")
def index():
    session.clear()
    session["start_time"] = time.time()
    session["answers"] = {}
    # Orden normal: del 1 al TOTAL_QUESTIONS sin mezclar.
    session["questions_order"] = list(range(1, TOTAL_QUESTIONS + 1))
    return redirect(url_for("question", qnum=1))

# Ruta para activar el modo aleatorio cuando el usuario lo presione.
@app.route("/randomize")
def randomize():
    session["questions_order"] = list(range(1, TOTAL_QUESTIONS + 1))
    random.shuffle(session["questions_order"])
    return redirect(url_for("question", qnum=1))

# Ruta que muestra cada pregunta de forma secuencial según el orden definido.
# Se muestra también cuántas preguntas faltan.
@app.route("/question/<int:qnum>", methods=["GET", "POST"])
def question(qnum):
    # Verificar si el tiempo del examen expiró.
    elapsed = time.time() - session.get("start_time", time.time())
    remaining = EXAM_DURATION_SECONDS - elapsed
    if remaining <= 0:
        return redirect(url_for("result"))
    
    # Procesar la respuesta enviada para la pregunta actual.
    if request.method == "POST":
        answer = request.form.get("answer")
        answers = session.get("answers", {})
        # Se obtiene el número real de la pregunta según el orden (ya sea normal o aleatorio).
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

# Ruta que muestra el resultado del examen, incluyendo las preguntas erróneas.
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

