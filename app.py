import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
import re
from dotenv import load_dotenv

# Load the hidden environment variables from the .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_sessions'

# Fetch credentials securely from the environment
db_config = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'), 
    'database': os.getenv('DB_NAME')
}

def get_db_connection():
    try:
        return mysql.connector.connect(**db_config)
    except Error as e:
        print(f"MySQL Error: {e}")
        return None

# --- MAIN PAGES ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

@app.route('/checkout')
def checkout():
    return render_template('checkout.html')

# --- AUTHENTICATION & PORTAL ---
@app.route('/portal')
def portal():
    return render_template('portal.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email or not password:
        return "Missing email or password", 400

    email = email.strip().lower()
    hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')

    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO accounts (email, password_hash) VALUES (%s, %s)", (email, hashed_pw))
            connection.commit()
            
            session['account_id'] = cursor.lastrowid
            session['email'] = email
            return redirect(url_for('dashboard'))
            
        except mysql.connector.IntegrityError:
            return "Email already registered. Go back and log in."
        finally:
            cursor.close()
            connection.close()
            
    return "Database error."

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email or not password:
        return "Missing email or password", 400

    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM accounts WHERE email = %s", (email.strip().lower(),))
            account = cursor.fetchone()

            if account and check_password_hash(account['password_hash'], password):
                session['account_id'] = account['id']
                session['email'] = account['email']
                return redirect(url_for('dashboard'))
            else:
                return "Invalid email or password."
        finally:
            cursor.close()
            connection.close()
            
    return "Database error."

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# --- PROTECTED DASHBOARD ---
@app.route('/dashboard')
def dashboard():
    if 'account_id' not in session:
        return redirect(url_for('portal'))
    return render_template('dashboard.html', email=session['email'])

# --- API ROUTE FOR HERO FORM ---
@app.route('/api/subscribe', methods=['POST'])
def subscribe():
    data = request.get_json()
    email = data.get('email', '').strip().lower()
    
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return jsonify({"status": "error", "message": "Invalid email."}), 400

    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO subscribers (email) VALUES (%s)", (email,))
            connection.commit()
            return jsonify({"status": "success", "message": "Trial activated!"}), 201
        except mysql.connector.IntegrityError:
            return jsonify({"status": "error", "message": "Already registered."}), 409
        finally:
            cursor.close()
            connection.close()
            
    return jsonify({"status": "error", "message": "DB failed."}), 500

# MUST BE LAST
if __name__ == '__main__':
    app.run(debug=True)