
import getpass
import psycopg

password = getpass.getpass("Enter your PostgreSQL password: ")

try:
    with psycopg.connect(
        dbname="internhship_db",
        user="postgres",
        password=password,
        host="localhost",
        port=5432
    ) as conn:

        with conn.cursor() as cur:
            print("Connected to PostgreSQL successfully!")

            cur.execute("SELECT * FROM students ORDER BY id DESC;")
            students = cur.fetchall()

            print("\nStudent Records:")
            for student in students:
                print(student)

except psycopg.Error as e:
    print("Database error:", e)
