from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from techquiz import get_random_question
from images import get_random_image
from truthorlie import get_random_truth_question
from reverselet import getreverselet
from riddles import get_random_riddle
import secrets
import threading
import time
import os
def open_fullscreen_browser():
    time.sleep(1)
    chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
    url = "http://127.0.0.1:5000/"
    user_data_dir = "C:/ChromeKioskProfile"
    os.system(f'start "" "{chrome_path}" --kiosk {url} --no-first-run --disable-infobars --user-data-dir="{user_data_dir}"')
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        session['teamname'] = request.form.get("team_name")
        session['unlocked'] = False
        return redirect(url_for("unlock"))
    return render_template("index.html")
@app.route("/unlock", methods=["GET", "POST"])
def unlock():
    if request.method == "POST":
        key = request.form.get("unlock_code")
        if key == "umesh":
            session['unlocked'] = True
            session['questions_taken'] = 0
            session['questions_correct'] = 0
            return render_template("unlock.html")
        else:
            return render_template("unlock.html", error="Invalid unlock code.")
    return render_template("unlock.html")
@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if not session.get('unlocked'):
        return redirect(url_for('unlock'))
    return render_template("dashboard.html", team_name=session.get('teamname'),
                           questions_taken=session.get('questions_taken', 0),
                           questions_correct=session.get('questions_correct', 0))
@app.route("/tech")
def tech_quiz():
    return render_template("techquiz.html")
@app.route("/tech/get-question")
def get_tech_question():
    qdata = get_random_question()
    session['answer'] = qdata['answer']
    session['questions_taken'] = session.get('questions_taken', 0) + 1
    return jsonify({
        "question": qdata['code'],
        "options": qdata['options']
    })
@app.route("/tech/submit", methods=["POST"])
def tech_submit():
    data = request.get_json()
    selected = data.get("answer")
    correct_answer = session.get('answer')
    if selected == '':
        return "empty"
    elif not selected:
        return jsonify({"result": "timeout"})
    elif selected == correct_answer:
        session['questions_correct'] = session.get('questions_correct', 0) + 1
        return jsonify({"result": "correct"})
    else:
        return jsonify({"result": "wrong"})
@app.route("/imagequiz")
def imagequiz():
    return render_template('imagequiz.html')
@app.route("/image/get-question", methods=['GET'])
def get_image_question():
    global current_answer
    question = get_random_image()
    if not question:
        return jsonify({"error": "Could not load question."}), 500
    current_answer = question['answer']
    session['questions_taken'] = session.get('questions_taken', 0) + 1
    return jsonify({
        "id": question['id'],
        "image": '/' + question['image'],
        "options": question['options']
    })
@app.route("/image/submit", methods=['POST'])
def image_submit():
    global current_answer
    data = request.get_json()
    user_answer = data.get("answer")
    if user_answer == '':
        return "empty"
    if not user_answer:
        return jsonify({"result": "timeout"})
    if user_answer == current_answer:
        session['questions_correct'] = session.get('questions_correct', 0) + 1
        return jsonify({"result": "correct"})
    else:
        return jsonify({"result": "wrong"})
@app.route("/truthquiz")
def truth_quiz():
    return render_template('truthquiz.html')
@app.route("/truth/get-question", methods=['GET'])
def get_truth_question():
    global current_answer
    question = get_random_truth_question()
    if not question:
        return jsonify({"error": "Failed to load question."}), 500
    current_answer = question['answer']
    session['questions_taken'] = session.get('questions_taken', 0) + 1
    return jsonify({
        "id": question['id'],
        "question": question['question'],
        "options": question['options']
    })
@app.route('/truth/submit', methods=['POST'])
def submit_truth_answer():
    global current_answer
    data = request.get_json()
    user_answer = data.get("answer")
    if user_answer == '':
        return "empty"
    if not user_answer:
        return jsonify({"result": "timeout"})
    result = "correct" if user_answer.strip().lower() == current_answer.strip().lower() else "wrong"
    if result == "correct":
        session['questions_correct'] = session.get('questions_correct', 0) + 1
    return jsonify({"result": result})
@app.route("/reverse")
def reverse_page():
    return render_template("reverse.html")
@app.route("/reverse/get-question")
def get_reverse_question():
    global current_reverse_answer
    q = getreverselet()
    current_reverse_answer = q["answer"].strip().lower()
    session['questions_taken'] = session.get('questions_taken', 0) + 1
    return jsonify({"question": q["code"]})
@app.route("/reverse/submit", methods=["POST"])
def submit_reverse_answer():
    global current_reverse_answer
    data = request.get_json()
    user_answer = (data.get("answer") or "").strip().lower()
    if not user_answer:
        return jsonify({"result": "empty"})
    if user_answer == current_reverse_answer:
        session['questions_correct'] = session.get('questions_correct', 0) + 1
        return jsonify({"result": "correct"})
    else:
        return jsonify({"result": "wrong"})
@app.route("/riddles")
def riddles():
    return render_template("riddles.html")
@app.route("/riddles/get-question")
def get_riddle_question():
    qdata = get_random_riddle()
    session['answer'] = qdata['answer']
    session['questions_taken'] = session.get('questions_taken', 0) + 1
    return jsonify({
        "question": qdata['code'],
        "options": qdata['options']
    })
@app.route("/riddles/submit", methods=["POST"])
def riddle_submit():
    data = request.get_json()
    selected = data.get("answer")
    correct_answer = session.get('answer')
    if selected == '':
        return "empty"
    elif not selected:
        return jsonify({"result": "timeout"})
    elif selected == correct_answer:
        session['questions_correct'] = session.get('questions_correct', 0) + 1
        return jsonify({"result": "correct"})
    else:
        return jsonify({"result": "wrong"})
@app.route("/return")
def returnback():
    if not session.get('unlocked'):
        return redirect(url_for('unlock'))
    return redirect(url_for('dashboard'))
@app.before_request
def require_unlock():
    protected_paths = [
        '/dashboard', '/tech', '/tech/get-question', '/tech/submit',
        '/imagequiz', '/image/get-question', '/image/submit',
        '/truthquiz', '/truth/get-question', '/truth/submit',
        '/reverse', '/reverse/get-question', '/reverse/submit',
        '/riddles', '/riddles/get-question', '/riddles/submit',
        '/return'
    ]
    if request.path in ['/', '/unlock']:
        return
    if any(request.path.startswith(p) for p in protected_paths):
        if not session.get('unlocked'):
            return redirect(url_for('unlock'))
if __name__ == "__main__":
    threading.Thread(target=open_fullscreen_browser).start()
    app.run(debug=True)
