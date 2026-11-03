from pathlib import Path
from getpass import getpass

import psycopg
from flask import Flask, render_template, request, redirect, url_for, flash

BASE_DIR = Path(__file__).resolve().parent

app = Flask(__name__)
app.secret_key = "student-management-secret-key"

# Ask for PostgreSQL password when running app.py
DB_PASSWORD = getpass("Enter PostgreSQL password: ")

def get_connection():
    return psycopg.connect(
        dbname="internhship_db",
        user="postgres",
        password=DB_PASSWORD,
        host="localhost",
        port=5432
    )
def initialize_database():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS students (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    course VARCHAR(100) NOT NULL,
                    fee NUMERIC(10,2) NOT NULL DEFAULT 0
                )
                """
            )
            conn.commit()


initialize_database()


@app.route("/")
def index():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
    SELECT id, name, course, fee
    FROM students
    ORDER BY id ASC
""")
                students = cur.fetchall()

        return render_template("index.html", students=students)

    except Exception as e:
        return f"Error loading students: {e}", 500

@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
def edit_student(student_id):

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        course = request.form.get("course", "").strip()
        fee_input = request.form.get("fee", "").strip()

        if not name or not course or not fee_input:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("edit_student", student_id=student_id))

        try:
            fee = float(fee_input)

            if fee < 0:
                flash("Fee cannot be negative.", "error")
                return redirect(url_for("edit_student", student_id=student_id))

            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("""
                        UPDATE students
                        SET name = %s, course = %s, fee = %s
                        WHERE id = %s
                    """, (name, course, fee, student_id))

                    if cur.rowcount == 0:
                        flash("Student not found.", "error")
                    else:
                        flash("Student updated successfully!", "success")

            return redirect(url_for("index"))

        except ValueError:
            flash("Please enter a valid fee.", "error")
            return redirect(url_for("edit_student", student_id=student_id))

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, name, course, fee
                FROM students
                WHERE id = %s
            """, (student_id,))

            student = cur.fetchone()

    if student is None:
        return "Student not found", 404

    return render_template("edit.html", student=student)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        course = request.form.get("course", "").strip()
        fee_input = request.form.get("fee", "").strip()

        if course and not fee_input:
            fee_input = str(COURSE_FEES.get(course, 0))

        if not name or not course or not fee_input:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("register"))

        try:
            fee = float(fee_input)

            if fee < 0:
                flash("Fee cannot be negative.", "error")
                return redirect(url_for("register"))

            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO students (name, course, fee)
                        VALUES (%s, %s, %s)
                        """,
                        (name, course, fee)
                    )

            flash("Student registered successfully!", "success")
            return redirect(url_for("index"))

        except ValueError:
            flash("Please enter a valid fee.", "error")
            return redirect(url_for("register"))

        except Exception as e:
            return f"Error registering student: {e}", 500

    return render_template("register.html")


@app.route("/delete/<int:student_id>", methods=["POST"])
def delete_student(student_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "DELETE FROM students WHERE id = %s",
                    (student_id,)
                )

                if cur.rowcount == 0:
                    flash("Student not found.", "error")
                else:
                    flash("Student deleted successfully!", "success")

        return redirect(url_for("index"))

    except Exception as e:
        return f"Error deleting student: {e}", 500

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)