from flask import Flask, render_template, request, redirect
import mysql.connector
import os

app = Flask(__name__)

# ✅ Database connection (Railway)
def get_db():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

# ✅ Home page
@app.route('/')
def home():
    return render_template('index.html')

# ✅ Contact form
@app.route('/contact', methods=['POST'])
def contact():
    try:
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO contacts (name, email, message) VALUES (%s, %s, %s)",
            (name, email, message)
        )

        db.commit()
        cursor.close()
        db.close()

    except Exception as e:
        print("Error:", e)

    return redirect('/')

# ✅ Render compatible
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))