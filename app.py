from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import random

# Initialize the app, database, login manager, and bcrypt
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

# Set the login view for login_required
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

# Initialize database (run once to create the tables)
with app.app_context():
    db.create_all()

# Mock question bank
questions = {
    "easy": [
        "Reverse a string.",
        "Find the largest number in an array.",
        "Check if a number is prime."
    ],
    "medium": [
        "Find the first non-repeating character in a string.",
        "Rotate an array by k positions.",
        "Determine if two strings are anagrams."
    ],
    "hard": [
        "Implement a Sudoku solver.",
        "Find the longest increasing subsequence in an array.",
        "Solve the N-Queens problem."
    ]
}

# Load user by ID for login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home route
@app.route('/')
@login_required
def home():
    return render_template('index.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
            return redirect(url_for('register'))

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)

            # Redirect to the page the user originally wanted to visit
            next_page = request.args.get('next')
            return redirect(next_page or url_for('home'))
        else:
            flash('Login failed. Check your username and/or password.', 'danger')

    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Question generation route
@app.route('/generate', methods=['POST'])
@login_required
def generate_question():
    difficulty = request.json.get('difficulty', 'easy')
    question_list = questions.get(difficulty, [])

    if not question_list:
        return jsonify({"error": "Invalid difficulty level"}), 400

    question = random.choice(question_list)
    return jsonify({"question": question})

if __name__ == '__main__':
    app.run(debug=True)
