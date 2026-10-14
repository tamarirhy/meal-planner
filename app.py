from flask import Flask, jsonify

app = Flask(__name__)
app.json.sort_keys = False

RECIPES = [
    {
        "id": 1,
        "name": "Pancakes",
        "servings": 4,
        "ingredients": [
            {"name": "flour", "quantity": 1, "unit": "cup"},
            {"name": "milk", "quantity": 1, "unit": "cup"},
            {"name": "egg", "quantity": 2, "unit": "each"},
            {"name": "butter", "quantity": 2, "unit": "tbsp"},
            {"name": "sugar", "quantity": 1, "unit": "tbsp"},
        ],
        "instructions": "Whisk the dry ingredients, mix in the milk, eggs and melted butter, then cook on a hot griddle until golden on both sides.",
    },
    {
        "id": 2,
        "name": "Oatmeal",
        "servings": 1,
        "ingredients": [
            {"name": "oats", "quantity": 0.5, "unit": "cup"},
            {"name": "milk", "quantity": 8, "unit": "tbsp"},
            {"name": "brown sugar", "quantity": 1, "unit": "tsp"},
        ],
        "instructions": "Combine the oats and milk in a pot, simmer for 5 minutes while stirring, then top with brown sugar.",
    },
]


@app.get("/")
def home():
    return "Meal Planner is running. Try /recipes"


@app.get("/recipes")
def recipes():
    return jsonify(RECIPES)


if __name__ == "__main__":
    app.run(debug=True)