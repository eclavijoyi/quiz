from flask import Flask, render_template, request, redirect, url_for, session, flash
import os
import json
from dotenv import load_dotenv
from flask_session import Session
import time
import random
import uuid
import functools
from questions1 import questions as q1
from questions2 import questions as q2
from questions3 import questions as q3
from questions4 import questions as q4

load_dotenv()  # Cargar variables del .env

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY')

# Configuración del sistema de archivos
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "/tmp/flask_sessions"

# Inicializa la extensión de sesiones
Session(app)

# Credenciales de usuario (en un entorno real, esto debería estar en una base de datos)
users_env = os.getenv("USERS", "{}")  # Obtener la variable como string
USERS = json.loads(users_env)  # Convertir el string en un diccionario


# Decorador para proteger rutas
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "user" not in session:
            flash("Por favor inicia sesión para acceder a esta página", "error")
            return redirect(url_for("login", from_redirect=1))
        return view(**kwargs)
    return wrapped_view

# Almacenamiento de sesiones en el servidor
active_quizzes = {}

def create_mixed_quiz():
    mixed = []
    question_number = 1
    for q_set in [q1, q2, q3, q4]:
        shuffled = random.sample(q_set, 25)
        for q in shuffled:
            new_q = q.copy()
            new_q["number"] = question_number
            mixed.append(new_q)
            question_number += 1
    random.shuffle(mixed)
    return mixed

# Nueva ruta principal que redirecciona automáticamente
@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if username in USERS and USERS[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            flash("Credenciales incorrectas", "error")
    
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Has cerrado sesión correctamente", "success")
    return redirect(url_for("login"))

# Ruta del dashboard (antes era 'index')
@app.route("/dashboard")
@login_required
def dashboard():
    session.pop("quiz_id", None)  # Mantener la sesión de usuario, pero borrar datos de quiz
    return render_template("quiz_selector.html")

@app.route("/select_quiz", methods=["POST"])
@login_required
def select_quiz():
    quiz_number = int(request.form.get("quiz_number"))
    
    # Crear ID único para el quiz
    quiz_id = str(uuid.uuid4())
    
    # Configurar preguntas según selección
    if quiz_number == 5:
        questions = create_mixed_quiz()
    else:
        questions = globals()[f"q{quiz_number}"]
    
    # Almacenar en servidor
    active_quizzes[quiz_id] = {
        "quiz_number": quiz_number,
        "questions": questions,
        "start_time": time.time(),
        "answers": {},
        "questions_order": random.sample(range(len(questions)), len(questions)),
        "current_question": 0
    }
    
    # Guardar solo el ID en la sesión
    session["quiz_id"] = quiz_id
    return redirect(url_for("question"))

@app.route("/question", methods=["GET", "POST"])
@login_required
def question():
    if "quiz_id" not in session:
        return redirect(url_for("dashboard"))
    
    quiz_id = session["quiz_id"]
    quiz_data = active_quizzes.get(quiz_id)
    
    if not quiz_data:
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        # Procesar respuesta
        answer = request.form.get("answer")
        current_q_index = quiz_data["current_question"]
        quiz_data["answers"][current_q_index] = answer
        quiz_data["current_question"] += 1
    
    if quiz_data["current_question"] >= len(quiz_data["questions"]):
        return redirect(url_for("result"))
    
    # Obtener pregunta actual
    q_index = quiz_data["questions_order"][quiz_data["current_question"]]
    current_question = quiz_data["questions"][q_index]
    current_question["number"] = quiz_data["current_question"] + 1
    
    # Calcular tiempo restante
    elapsed = time.time() - quiz_data["start_time"]
    # Si es el quiz 5 (mixto), dar 210 minutos, sino 90 minutos
    if quiz_data["quiz_number"] == 5:
        remaining = 12600 - elapsed  # 210 minutos (3.5 horas)
    else:
        remaining = 5400 - elapsed  # 90 minutos
    
    return render_template(
        "question.html",
        question=current_question,
        remaining=int(remaining),
        total=len(quiz_data["questions"]),
        current=quiz_data["current_question"] + 1
    )

@app.route("/result")
@login_required
def result():
    if "quiz_id" not in session:
        return redirect(url_for("dashboard"))
    
    quiz_id = session["quiz_id"]
    quiz_data = active_quizzes.get(quiz_id)
    
    if not quiz_data:
        return redirect(url_for("dashboard"))
    
    # Calcular resultados
    score = 0
    errors = []
    
    for idx, q_index in enumerate(quiz_data["questions_order"]):
        user_ans = quiz_data["answers"].get(idx)
        question_data = quiz_data["questions"][q_index]

        # Obtener la respuesta correcta con un manejo seguro
        correct_ans = question_data.get("correct")  # Usa .get() para evitar KeyError

        # Validar si correct_ans es válido
        if correct_ans is None or correct_ans not in question_data.get("options", {}):
            print(f"Advertencia: La pregunta {idx+1} tiene un valor 'correct' inválido: {correct_ans}")
            continue  # Saltar esta pregunta para evitar el error
        
        correct_text = question_data["options"][correct_ans]
        
        # Si hay respuesta del usuario, obtener el texto
        user_ans_text = question_data["options"].get(user_ans, "Sin respuesta") if user_ans else "Sin respuesta"

        if user_ans == correct_ans:
            score += 1
        else:
            errors.append({
                "number": idx + 1,
                "question": question_data["question"],
                "user_answer_key": user_ans,
                "user_answer_text": user_ans_text,
                "correct_answer_key": correct_ans,
                "correct_answer_text": correct_text
            })

    # Limpiar datos
    del active_quizzes[quiz_id]
    session.pop("quiz_id", None)

    return render_template(
        "result.html",
        score=score,
        total=len(quiz_data["questions"]),
        passed=score >= 75,
        errors=errors,
        quiz_number=quiz_data["quiz_number"]
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)# debug=False para producción