from flask import Flask, render_template, request, send_file
import time
import csv
import os

app = Flask(__name__)

questions = [
    "Do you feel tired most of the time?",
    "Do you have trouble sleeping?",
    "Do you feel anxious frequently?",
    "Do you get irritated easily?",
    "Do you find it hard to concentrate?",
    "Do you feel overwhelmed with work/studies?",
    "Do you avoid social interactions?",
    "Do you experience frequent headaches?",
    "Do you feel sad without reason?",
    "Do you feel low energy most of the day?"
]

@app.route('/')
def index():
    return render_template("index.html", questions=questions)

@app.route('/submit', methods=['POST'])
def submit():
    score = 0

    name = request.form.get("name")

    start_time = float(request.form['start_time'])
    end_time = time.time()

    for i in range(len(questions)):
        if request.form.get(f'q{i}') == "yes":
            score += 1

    total_time = end_time - start_time
    speed = round(len(questions) / total_time * 60, 2)

    # Stress level + suggestions
    if score <= 3:
        stress = "Low"
        suggestions = [
            "Keep maintaining your healthy lifestyle",
            "Continue regular exercise",
            "Stay socially active"
        ]
    elif score <= 6:
        stress = "Moderate"
        suggestions = [
            "Try meditation or deep breathing",
            "Take regular breaks",
            "Maintain proper sleep schedule"
        ]
    else:
        stress = "High"
        suggestions = [
            "Take immediate rest",
            "Talk to friends or family",
            "Practice relaxation techniques",
            "Consider professional help if needed"
        ]

    file_exists = os.path.isfile("results.csv")

    # SAVE CORRECT ORDER
    with open("results.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Name", "Score", "Speed", "Stress"])

        writer.writerow([name, score, speed, stress])

    return render_template("result.html",
                           name=name,
                           score=score,
                           speed=speed,
                           stress=stress,
                           suggestions=suggestions)

@app.route('/history')
def history():
    data = []

    if os.path.exists("results.csv"):
        with open("results.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)
            data = list(reader)

    return render_template("history.html", data=data)

@app.route('/clear')
def clear():
    open("results.csv", "w").close()
    return "<h3>History Cleared ✅</h3><a href='/'>Go Back</a>"

@app.route('/download')
def download():
    return send_file("results.csv", as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
