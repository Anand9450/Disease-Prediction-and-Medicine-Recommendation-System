import os
from flask import Flask, request, render_template, flash, redirect, url_for, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import pickle

# Create app and basic config
app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY', 'change-me-in-production')

# Base path for data/model files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Helper to load CSV safely relative to project
def _csv(path):
    return pd.read_csv(os.path.join(BASE_DIR, path))

# Load CSV data
sym_des = _csv("symptoms.csv")
precautions = _csv("precautions.csv")
workout = _csv("workout.csv")
description = _csv("description.csv")
medications = _csv("medications.csv")
diets = _csv("diets.csv")

# Load the model
import json

# Load the model
svc_path = os.path.join(BASE_DIR, 'disease_model.pkl')
with open(svc_path, 'rb') as _f:
    svc = pickle.load(_f)

# Load symptoms list
symptoms_path = os.path.join(BASE_DIR, 'symptoms_list.json')
with open(symptoms_path, 'r') as _f:
    symptoms_list = json.load(_f)

# Create symptoms dict for mapping
symptoms_dict = {symptom: index for index, symptom in enumerate(symptoms_list)}

# Helper function to get details based on disease
def helper(dis):
    # Check if the disease data is available in each dataset
    desc = description[description['Disease'] == dis]['Description']
    if not desc.empty:
        desc = " ".join([w for w in desc])
    else:
        desc = "Description not available."
    
    pre = precautions[precautions['Disease'] == dis][['Precaution_1', 'Precaution_2', 'Precaution_3', 'Precaution_4']]
    pre = [list(row) for row in pre.values] if not pre.empty else ["Precautions not available."]
    
    med = medications[medications['Disease'] == dis]['Medication']
    med = [medication for medication in med.values] if not med.empty else ["Medications not available."]
    
    die = diets[diets['Disease'] == dis]['Diet']
    die = [diet for diet in die.values] if not die.empty else ["Diet not available."]
    
    workout_plan = workout[workout['disease'] == dis]['workout']
    workout_plan = [w for w in workout_plan.values] if not workout_plan.empty else ["Workout plan not available."]
    
    return desc, pre, med, die, workout_plan




# Predict function to predict the disease based on symptoms
def get_predicted_value(patient_symptoms):
    input_vector = np.zeros(len(symptoms_dict))
    for item in patient_symptoms:
        if item in symptoms_dict:
            input_vector[symptoms_dict[item]] = 1
    predicted_disease = svc.predict([input_vector])[0]
    return predicted_disease

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/symptoms', methods=['GET'])
def get_symptoms():
    # Return list of symptoms for the frontend dropdown
    return jsonify({'symptoms': list(symptoms_dict.keys())})

@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json()
    if not data or 'symptoms' not in data:
        return jsonify({'error': 'No symptoms provided'}), 400
    
    user_symptoms = data['symptoms']
    # Filter valid symptoms
    valid_symptoms = [s for s in user_symptoms if s in symptoms_dict]
    
    if not valid_symptoms:
        return jsonify({'error': 'No valid symptoms found'}), 400
        
    predicted_disease = get_predicted_value(valid_symptoms)
    
    desc, pre, med, die, workout_plan = helper(predicted_disease)
    
    return jsonify({
        'disease': predicted_disease,
        'description': desc,
        'precautions': pre,
        'medications': med,
        'diet': die,
        'workout': workout_plan
    })

@app.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        symptoms = request.form.get('symptoms')
        
        # Validate input
        if not symptoms:
            flash("Please enter symptoms!")
            return redirect(url_for('index'))
        
        user_symptoms = [s.strip() for s in symptoms.split(',')]
        predicted_disease = get_predicted_value(user_symptoms)
        
        if predicted_disease is None:
            flash("Sorry, we couldn't predict the disease. Please try again with different symptoms.")
            return redirect(url_for('index'))
        
        # Get details from helper function
        desc, pre, med, die, workout = helper(predicted_disease)
        
        return render_template(
            'index.html', 
            predicted_disease=predicted_disease,
            dis_des=desc, 
            dis_pre=pre, 
            dis_med=med, 
            dis_die=die, 
            dis_workout=workout
        )

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contacts():
    return render_template('contact.html')

@app.route('/developer')
def developer():
    return render_template('developer.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/health')
def health():
    # Simple health check for hosting platforms (Render, Heroku, etc.)
    return 'ok', 200

if __name__ == "__main__":
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    app.run(host=host, port=port, debug=debug)
