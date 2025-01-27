
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
import joblib
import numpy as np
import mysql.connector
import secrets
from flask_bcrypt import Bcrypt

# Initialize Flask app and Bcrypt for hashing
app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = secrets.token_hex(16)

# Load the model
model = joblib.load('iris_model.pkl')

# Map target values to species names
species = ['Setosa', 'Versicolor', 'Virginica']

# Database connection function
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",  # Replace with your database host
            user="root",       # Replace with your MySQL username
            password="Rishabh@6062",  # Replace with your MySQL password
            database="iris_classifier"  # Replace with your database name
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

# for render
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

# Home route
@app.route('/')
def home():
    if 'user_id' in session:
        return render_template('index.html', username=session['username'])
    flash("Please log in first.", "warning")
    return redirect(url_for('login'))


# Register page
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        try:
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor(dictionary=True)
                # Check if username already exists
                cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
                existing_user = cursor.fetchone()
                
                if existing_user:
                    flash('Username already exists. Please choose another.', 'danger')
                    return redirect(url_for('register'))
                
                # Insert new user
                query = "INSERT INTO users (username, password) VALUES (%s, %s)"
                cursor.execute(query, (username, hashed_password))
                conn.commit()
                cursor.close()
                conn.close()
                flash('Registration successful! Please log in.', 'success')
                return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'danger')
    return render_template('register.html')

# Login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        print(f"Attempting login with username: {username} and password: {password}")

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and bcrypt.check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']

            # Log the login to the database
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO logins (user_id, username) VALUES (%s, %s)"
            cursor.execute(query, (user['id'], user['username']))
            conn.commit()
            cursor.close()
            conn.close()

            flash('Login successful!', 'success')
            return redirect(url_for('home'))  # This should redirect to the home page
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from the form
        data = [float(x) for x in request.form.values()]
        # Make prediction
        prediction = model.predict([data])
        predicted_species = species[prediction[0]]

        # Log prediction to the database
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            query = "INSERT INTO predictions (sepal_length, sepal_width, petal_length, petal_width, predicted_species) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query, (*data, predicted_species))
            conn.commit()
            cursor.close()
            conn.close()

        return render_template('index.html', prediction_text=f'Predicted species: {predicted_species}')
    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        return render_template('index.html', prediction_text="An error occurred during prediction.")

if __name__ == '__main__':
    app.run(debug=True)
