# Meal Planner + Grocery List Generator

A web app where you save recipes, drag them onto a weekly calendar, and get one
shopping list with ingredients merged and totaled (for example, 1 cup + 8 tbsp
of milk becomes 1 1/2 cups).

Senior Design final project. Status: hello world stage (proposal).

## What's here

- `app.py`: Flask app. `GET /recipes` returns two hardcoded recipes with ingredients.
- `merge.py`: unit-aware ingredient merging (the core algorithm).
- `test_merge.py`: 13 tests for the merging logic.

## Install

```
pip install -r requirements.txt
```

## Run the app

```
python app.py
```

Then open http://127.0.0.1:5000/recipes

## Run the tests

```
pytest
```
