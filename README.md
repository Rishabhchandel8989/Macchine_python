Iris Classification Web Application

This project is a web application for classifying iris flower species based on user-provided measurements. It is built using Flask and deployed on Render. The application also includes user authentication, with login and registration details stored in a MySQL database.

Features

Iris Classification: Predicts iris flower species (Setosa, Versicolor, Virginica) based on petal and sepal dimensions.

User Authentication: Includes user registration and login functionality.

MySQL Integration: User data and predictions are stored in a MySQL database.

Responsive Frontend: Simple and user-friendly UI built with HTML templates.

Deployment: Hosted on Render.

Technology Stack

Backend: Flask

Frontend: HTML, CSS

Database: MySQL

Machine Learning Model: Pre-trained Scikit-learn model

Deployment: Render

Setup and Installation

Prerequisites

Python 3.8+

MySQL database

Clone the Repository

git clone https://github.com/<your-username>/<repo-name>.git
cd <repo-name>

Install Dependencies

Create a virtual environment:

python -m venv venv
source venv/bin/activate   # For Linux/macOS
venv\Scripts\activate     # For Windows

Install required packages:

pip install -r requirements.txt

Configure Database

Create a MySQL database (e.g., iris_classifier).

Add Pre-trained Model

Place your pre-trained iris_model.pkl file in the root directory.

Run the Application

python app.py

Visit http://127.0.0.1:5000 in your browser.

Deployment on Render

Create a requirements.txt:

pip freeze > requirements.txt

Add a start Command:
Create a Procfile with the following content:

web: gunicorn app:app

Push to GitHub:

git add .
git commit -m "Prepare for Render deployment"
git push origin main

Deploy on Render:

Go to the Render dashboard.

Select "New Web Service" and connect your repository.

Set up environment variables (e.g., DATABASE_URL).

Scikit-learn for the ML model

Flask for the web framework

Render for deployment
