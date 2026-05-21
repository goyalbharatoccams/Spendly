from datetime import date
from flask import Flask, render_template, request, redirect, url_for, session, abort
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import get_db, init_db, seed_db, get_user_by_email, create_user, get_user_by_id, get_expenses_by_user_id, create_expense, get_expense_by_id, update_expense

CATEGORIES = ["Food", "Transport", "Bills", "Health", "Entertainment", "Shopping", "Other"]

app = Flask(__name__)
app.secret_key = "dev-secret-change-in-prod"


# ------------------------------------------------------------------ #
# Routes                                                              #
# ------------------------------------------------------------------ #

@app.route("/")
def landing():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    return render_template("landing.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    if request.method == "GET":
        return render_template("register.html")

    name             = request.form.get("name", "").strip()
    email            = request.form.get("email", "").strip()
    password         = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")

    if not name or not email or not password or not confirm_password:
        return render_template("register.html",
                               error="All fields are required.",
                               name=name, email=email)

    if len(password) < 8:
        return render_template("register.html",
                               error="Password must be at least 8 characters.",
                               name=name, email=email)

    if password != confirm_password:
        return render_template("register.html",
                               error="Passwords do not match.",
                               name=name, email=email)

    if get_user_by_email(email):
        return render_template("register.html",
                               error="An account with that email already exists.",
                               name=name, email=email)

    create_user(name, email, generate_password_hash(password))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user_id"):
        return redirect(url_for("profile"))
    if request.method == "GET":
        return render_template("login.html")

    email    = request.form.get("email", "").strip()
    password = request.form.get("password", "")

    if not email or not password:
        return render_template("login.html",
                               error="All fields are required.",
                               email=email)

    user = get_user_by_email(email)
    if not user or not check_password_hash(user["password_hash"], password):
        return render_template("login.html",
                               error="Invalid email or password.",
                               email=email)

    session["user_id"] = user["id"]
    return redirect(url_for("profile"))


# ------------------------------------------------------------------ #
# Placeholder routes — students will implement these                  #
# ------------------------------------------------------------------ #

@app.route("/terms")
def terms():
    return render_template("terms.html")


@app.route("/privacy")
def privacy():
    return render_template("privacy.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/profile")
def profile():
    if not session.get("user_id"):
        return redirect(url_for("login"))
    user     = get_user_by_id(session["user_id"])
    expenses = get_expenses_by_user_id(session["user_id"])
    return render_template("profile.html", user=user, expenses=expenses)


@app.route("/expenses/add", methods=["GET", "POST"])
def add_expense():
    if not session.get("user_id"):
        return redirect(url_for("login"))

    today = date.today().isoformat()

    if request.method == "GET":
        return render_template("add_expense.html",
                               categories=CATEGORIES,
                               today=today,
                               date=today)

    amount_str  = request.form.get("amount", "").strip()
    category    = request.form.get("category", "").strip()
    date_str    = request.form.get("date", "").strip()
    description = request.form.get("description", "").strip() or None

    def redisplay(error):
        return render_template("add_expense.html",
                               categories=CATEGORIES,
                               today=today,
                               error=error,
                               amount=amount_str, category=category,
                               date=date_str, description=description)

    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
    except ValueError:
        return redisplay("Amount must be a positive number.")

    if category not in CATEGORIES:
        return redisplay("Please select a valid category.")

    if not date_str:
        return redisplay("Date is required.")

    create_expense(session["user_id"], amount, category, date_str, description)
    return redirect(url_for("profile"))


@app.route("/expenses/<int:expense_id>/edit", methods=["GET", "POST"])
def edit_expense(expense_id):
    if not session.get("user_id"):
        return redirect(url_for("login"))

    expense = get_expense_by_id(expense_id)
    if expense is None:
        abort(404)
    if expense["user_id"] != session["user_id"]:
        abort(403)

    today = date.today().isoformat()

    if request.method == "GET":
        return render_template("edit_expense.html",
                               categories=CATEGORIES,
                               today=today,
                               amount=expense["amount"],
                               category=expense["category"],
                               date=expense["date"],
                               description=expense["description"],
                               expense_id=expense_id)

    amount_str  = request.form.get("amount", "").strip()
    category    = request.form.get("category", "").strip()
    date_str    = request.form.get("date", "").strip()
    description = request.form.get("description", "").strip() or None

    def redisplay(error):
        return render_template("edit_expense.html",
                               categories=CATEGORIES,
                               today=today,
                               error=error,
                               amount=amount_str, category=category,
                               date=date_str, description=description,
                               expense_id=expense_id)

    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
    except ValueError:
        return redisplay("Amount must be a positive number.")

    if category not in CATEGORIES:
        return redisplay("Please select a valid category.")

    if not date_str:
        return redisplay("Date is required.")

    update_expense(expense_id, session["user_id"], amount, category, date_str, description)
    return redirect(url_for("profile"))


@app.route("/expenses/<int:id>/delete")
def delete_expense(id):
    return "Delete expense — coming in Step 9"


with app.app_context():
    init_db()
    seed_db()


if __name__ == "__main__":
    app.run(debug=True, port=5001)
