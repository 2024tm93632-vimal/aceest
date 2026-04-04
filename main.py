from flask import Flask, render_template, request

app = Flask(__name__)

programs = {
    "Fat Loss (FL)": {
        "workout": "Mon: 5x5 Back Squat...",
        "diet": "B: 3 Egg Whites...",
        "color": "#e74c3c"
    },
    "Muscle Gain (MG)": {
        "workout": "Mon: Squat 5x5...",
        "diet": "B: 4 Eggs...",
        "color": "#2ecc71"
    },
    "Beginner (BG)": {
        "workout": "Circuit Training...",
        "diet": "Balanced Tamil Meals...",
        "color": "#3498db"
    }
}

@app.route("/", methods=["GET", "POST"])
def home():
    selected = None
    data = None

    if request.method == "POST":
        selected = request.form.get("program")
        data = programs.get(selected)

    return render_template("index.html", programs=programs, data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)