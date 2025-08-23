from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from techquiz import get_random_question
from images import get_random_image
from truthorlie import get_random_truth_question
from reverselet import getreverselet
from riddles import get_random_riddle
from QUESTIONS import questions
import secrets
import threading
import time
import os
import webbrowser
import shutil 
def open_fullscreen_browser():
    time.sleep(5)
    url = "http://127.0.0.1:5001/"   
    # Try to locate Chrome automatically
    chrome_path = shutil.which("chrome") or shutil.which("google-chrome") or shutil.which("chrome.exe")
    if chrome_path:
        os.system(f'start "" "{chrome_path}" --kiosk {url} --no-first-run --disable-infobars')
    else:
        # fallback to default browser
        webbrowser.open(url, new=1)
# Flask app initialization
app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Global flags for browser opening
browser_opened = False

# Home page route
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        session['teamname'] = request.form.get("team_name")
        questions.copy_round_files(session.get('teamname'))
        session['unlocked'] = False
        return redirect(url_for("unlock"))
    return render_template("index.html")

# Unlock page route
@app.route("/unlock", methods=["GET", "POST"])
def unlock():
    if request.method == "POST":
        key = request.form.get("unlock_code")
        if key == "csi":
            session['unlocked'] = True
            session['questions_taken'] = 0
            session['questions_correct'] = 0
            return render_template("dashboard.html")
        else:
            return render_template("unlock.html", error="Invalid unlock code.")
    return render_template("unlock.html")

# Dashboard page route
@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if not session.get('unlocked'):
        return redirect(url_for('unlock'))
    return render_template("dashboard.html", team_name=session.get('teamname'),
                           questions_taken=session.get('questions_taken', 0),
                           questions_correct=session.get('questions_correct', 0))

# Tech Quiz route
@app.route("/tech")
def tech_quiz():
    return render_template("techquiz.html")

# Tech Quiz - get random question
@app.route("/tech/get-question")
def get_tech_question():
    qdata = get_random_question()
    session['answer'] = qdata['answer']
    session['questions_taken'] = session.get('questions_taken', 0) + 1
    return jsonify({
        "question": qdata['code'],
        "options": qdata['options']
    })

# Tech Quiz - submit answer
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

# Image Quiz route
@app.route("/imagequiz")
def imagequiz():
    return render_template('imagequiz.html')


# Image Quiz - get random image question (updated to use text box)
@app.route("/image/get-question", methods=['GET'])
def get_image_question():
    question = get_random_image()
    if not question:
        return jsonify({"error": "Could not load question."}), 500

    session['answer'] = question['answer']
    session['questions_taken'] = session.get('questions_taken', 0) + 1

    return jsonify({
        "id": question['id'],
        "image": '/' + question['image']
    })


@app.route("/image/submit", methods=['POST'])
def image_submit():
    data = request.get_json()
    user_answer = data.get("answer")
    timeout = data.get("timeout", False)

    correct_answer = session.get('answer')

    if timeout or not user_answer:
        return jsonify({"result": "timeout"})

    if user_answer.strip().lower() == correct_answer.strip().lower():
        session['questions_correct'] = session.get('questions_correct', 0) + 1
        return jsonify({"result": "correct","correct": correct_answer})
    else:
        return jsonify({
            "result": "wrong",
            "correct": correct_answer
        })



# Truth Quiz route
@app.route("/truthquiz")
def truth_quiz():
    return render_template('truthquiz.html')

# Truth Quiz - get random question
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

# Truth Quiz - submit answer
@app.route('/truth/submit', methods=['POST'])
def submit_truth_answer():
    global current_answer
    data = request.get_json()
    user_answer = data.get("answer")
    timeout = data.get("timeout", False)

    if timeout:
        return jsonify({"result": "timeout"})
    if not user_answer:
        return jsonify({"result": "timeout"})

    result = "correct" if user_answer.strip().lower() == current_answer.strip().lower() else "wrong"
    if result == "correct":
        session['questions_correct'] = session.get('questions_correct', 0) + 1
    return jsonify({"result": result})

# Reverse Quiz route
@app.route("/reverse")
def reverse_page():
    return render_template("reverse.html")

# Reverse Quiz - get reverselet question
@app.route("/reverse/get-question")
def get_reverse_question():
    global current_reverse_answer
    q = getreverselet()
    current_reverse_answer = q["answer"].strip().lower()
    session['questions_taken'] = session.get('questions_taken', 0) + 1
    return jsonify({"question": q["code"]})

# Reverse Quiz - submit answer
@app.route("/reverse/submit", methods=["POST"])
def submit_reverse_answer():
    global current_reverse_answer
    data = request.get_json()
    user_answer = (data.get("answer") or "").strip().lower()
    timeout = data.get("timeout", False)

    if timeout or not user_answer:
        return jsonify({"result": "timeout"})
    if user_answer == current_reverse_answer:
        session['questions_correct'] = session.get('questions_correct', 0) + 1
        return jsonify({"result": "correct"})
    else:
        return jsonify({"result": "wrong"})

# Riddle Quiz route
@app.route("/riddles")
def riddles():
    return render_template("riddles.html")

# Riddle Quiz - get random riddle
@app.route("/riddles/get-question")
def get_riddle_question():
    qdata = get_random_riddle()
    session['answer'] = qdata['answer']
    session['questions_taken'] = session.get('questions_taken', 0) + 1
    return jsonify({
        "question": qdata['code'],
        "options": qdata['options']
    })

# Riddle Quiz - submit answer
@app.route("/riddles/submit", methods=["POST"])
def riddle_submit():
    data = request.get_json()
    selected = data.get("answer")
    timeout = data.get("timeout", False)
    correct_answer = session.get('answer')

    if timeout:
        return jsonify({"result": "timeout"})
    if not selected:
        return jsonify({"result": "timeout"})
    if selected == correct_answer:
        session['questions_correct'] = session.get('questions_correct', 0) + 1
        return jsonify({"result": "correct"})
    else:
        return jsonify({"result": "wrong"})

@app.route("/return") 
def returnback():
    if not session.get('unlocked'): 
        return redirect(url_for('unlock'))
    return redirect(url_for('dashboard'))
# Return to the main page
@app.route("/returntomain")
def returntomain():
    return render_template("index.html")

# Prevent double redirection by checking if the user is unlocked
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

# Handle browser opening in fullscreen only once
@app.before_request
def open_browser_once():
    global browser_opened
    if not browser_opened:
        browser_opened = True
        threading.Thread(target=open_fullscreen_browser).start()

if __name__ == "__main__":
    app.run(debug=True)
