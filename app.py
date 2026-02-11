from flask import Flask, render_template, request, redirect, flash, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employee.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "supersecretkey"

db = SQLAlchemy(app)

class Employee(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(500), nullable=False)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

        if not name or not email:
            flash("All fields are required!", "danger")
            return redirect(url_for("home"))

        emp = Employee(name=name, email=email)
        db.session.add(emp)
        db.session.commit()

        flash("Employee added successfully!", "success")
        return redirect(url_for("home"))

    # GET request
    allemployee = Employee.query.all()
    return render_template("index.html", allemployee=allemployee)

@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    emp = Employee.query.get_or_404(sno)

    if request.method == "POST":
        emp.name = request.form.get("name", "").strip()
        emp.email = request.form.get("email", "").strip()

        if not emp.name or not emp.email:
            flash("All fields are required!", "danger")
            return redirect(url_for("update", sno=sno))

        db.session.commit()
        flash("Employee updated successfully!", "success")
        return redirect(url_for("home"))

    return render_template("update.html", emp=emp)

@app.route("/delete/<int:sno>")
def delete(sno):
    emp = Employee.query.get_or_404(sno)
    db.session.delete(emp)
    db.session.commit()
    flash("Employee deleted successfully!", "success")
    return redirect(url_for("home"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

app.py