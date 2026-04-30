from flask import Flask, render_template, request

app = Flask(__name__)

programs = {
    "Fat Loss (FL)": {
        "workout": """Mon: Back Squat 5x5 + Core
Tue: EMOM 20min Assault Bike
Wed: Bench Press + 21-15-9
Thu: Deadlift + Box Jumps
Fri: Zone 2 Cardio 30min""",
        "diet": """Breakfast: Egg Whites + Oats
Lunch: Grilled Chicken + Brown Rice
Dinner: Fish Curry + Millet Roti
Target: ~2000 kcal""",
        "calorie_factor": 22
    },
    "Muscle Gain (MG)": {
        "workout": """Mon: Squat 5x5
Tue: Bench 5x5
Wed: Deadlift 4x6
Thu: Front Squat 4x8
Fri: Incline Press 4x10
Sat: Barbell Rows 4x10""",
        "diet": """Breakfast: Eggs + Peanut Butter Oats
Lunch: Chicken Biryani
Dinner: Mutton Curry + Rice
Target: ~3200 kcal""",
        "calorie_factor": 35
    },
    "Beginner (BG)": {
        "workout": """Full Body Circuit:
- Air Squats
- Ring Rows
- Push-ups
Focus: Technique & Consistency""",
        "diet": """Balanced Tamil Meals
Idli / Dosa / Rice + Dal
Protein Target: 120g/day""",
        "calorie_factor": 26
    }
}

clients = []


@app.route("/", methods=["GET", "POST"])
def home():
    workout = ""
    diet = ""
    calories = None

    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        weight = float(request.form.get("weight", 0))
        program = request.form.get("program")
        adherence = request.form.get("adherence")

        if program in programs:
            data = programs[program]
            workout = data["workout"]
            diet = data["diet"]
            calories = int(weight * data["calorie_factor"])

        if name and program:
            clients.append((name, age, weight, program, adherence))

    return render_template(
        "index.html",
        programs=programs.keys(),
        workout=workout,
        diet=diet,
        calories=calories,
        clients=clients
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)