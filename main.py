from flask import Flask, render_template, request, redirect

app = Flask(__name__)

clients = []

programs = {
    "Fat Loss (FL)": {
        "workout": "Back Squat, Cardio, Bench, Deadlift, Recovery",
        "diet": "Egg Whites, Chicken, Fish Curry",
        "calorie_factor": 22
    },
    "Muscle Gain (MG)": {
        "workout": "Squat, Bench, Deadlift, Press, Rows",
        "diet": "Eggs, Biryani, Mutton Curry",
        "calorie_factor": 35
    },
    "Beginner (BG)": {
        "workout": "Air Squats, Ring Rows, Push-ups",
        "diet": "Balanced Tamil Meals",
        "calorie_factor": 26
    }
}

@app.route("/", methods=["GET", "POST"])
def home():
    selected_program = None
    workout = ""
    diet = ""
    calories = None

    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        weight = float(request.form.get("weight", 0))
        program = request.form.get("program")
        adherence = request.form.get("adherence")
        notes = request.form.get("notes")

        if program in programs:
            selected_program = programs[program]
            workout = selected_program["workout"]
            diet = selected_program["diet"]
            calories = int(weight * selected_program["calorie_factor"])

        if name and program:
            clients.append((name, age, weight, program, adherence, notes))

    return render_template("index.html",
                           programs=programs.keys(),
                           workout=workout,
                           diet=diet,
                           calories=calories,
                           clients=clients)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)