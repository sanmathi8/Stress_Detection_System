from flask import Flask, render_template, request
import time
import csv
import os

app = Flask(__name__)

# Questions
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

# Home Page
@app.route('/')
def index():
    return render_template("index.html", questions=questions)

# Submit Form
@app.route('/submit', methods=['POST'])
def submit():
    score = 0

    # Time tracking
    start_time = float(request.form['start_time'])
    end_time = time.time()

    # Calculate score
    for i in range(len(questions)):
        if request.form.get(f'q{i}') == "yes":
            score += 1

    # Typing speed
    total_time = end_time - start_time
    speed = round(len(questions) / total_time * 60, 2)

    # Stress level
    if score <= 3:
        stress = "Low 😊"
        suggestions = [
            "Keep maintaining your healthy lifestyle",
            "Continue regular exercise",
            "Stay socially active"
        ]
    elif score <= 6:
        stress = "Moderate 😐"
        suggestions = [
            "Try meditation or deep breathing",
            "Take regular breaks",
            "Maintain proper sleep schedule"
        ]
    else:
        stress = "High 😟"
        suggestions = [
            "Take immediate rest",
            "Talk to friends or family",
            "Practice relaxation techniques",
            "Consider professional help if needed"
        ]

    # Save to CSV
    file_exists = os.path.isfile("results.csv")

    with open("results.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow(["Score", "Speed", "Stress"])

        writer.writerow([score, speed, stress])

    # Return result page
    return render_template("result.html",
                           score=score,
                           speed=speed,
                           stress=stress,
                           suggestions=suggestions)

# History Page
@app.route('/history')
def history():
    data = []

    if os.path.exists("results.csv"):
        with open("results.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # skip header
            data = list(reader)

    return render_template("history.html", data=data)

# Run App
if __name__ == '__main__':
    app.run(debug=True)