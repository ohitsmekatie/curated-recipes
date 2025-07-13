from flask import Blueprint, render_template, request, redirect, flash, url_for, jsonify
import re
from .utils import get_random_recipe, add_recipe_to_sheet

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/generate", methods=["GET"])
def generate():
    meal_type = request.args.get("meal")
    recipe = get_random_recipe(meal_type)
    return jsonify(recipe)


@main.route("/about")
def about():
    return render_template("about.html")

@main.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        meal_type = request.form.get("meal_type")
        name = request.form.get("name")
        link = request.form.get("link")

        # Simple link validation
        url_pattern = re.compile(
            r'^(https?://)?(www\.)?([a-zA-Z0-9_-]+\.)+[a-zA-Z]{2,}(/[^\s]*)?$'
        )
        if not url_pattern.match(link):
            flash("Please enter a valid URL.", "danger")
            return redirect(url_for("main.submit"))

        if not all([meal_type, name, link]):
            flash("All fields are required.", "danger")
            return redirect(url_for("main.submit"))

        # Add to Google Sheet
        success = add_recipe_to_sheet(meal_type, name, link)
        if success:
            flash("Recipe submitted successfully!", "success")
        else:
            flash("Something went wrong. Please try again.", "danger")

        return redirect(url_for("main.submit"))

    return render_template("submit.html")