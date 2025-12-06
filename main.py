import os
import csv
import json
import pickle
import numpy as np
from flask import Flask, request, render_template, flash, redirect, url_for, jsonify
from flask_cors import CORS

# Create app and basic config
app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY', 'change-me-in-production')

# Base path for data/model files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Helper to load CSV into a list of dictionaries
def load_csv(filename):
    path = os.path.join(BASE_DIR, filename)
    data = []
    try:
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
    return data

# Load CSV data into memory
precautions_data = load_csv("precautions.csv")
workout_data = load_csv("workout.csv")
description_data = load_csv("description.csv")
medications_data = load_csv("medications.csv")
diets_data = load_csv("diets.csv")

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
    # Description
    desc = "Description not available."
    for row in description_data:
        if row.get('Disease') == dis:
            desc = row.get('Description', "")
            break
    
    # Precautions
    pre = []
    for row in precautions_data:
        if row.get('Disease') == dis:
            # Filter out empty precautions
            p_list = [row.get(f'Precaution_{i}') for i in range(1, 5)]
            pre = [[p for p in p_list if p]]
            break
    if not pre:
        pre = ["Precautions not available."]

    # Medications
    med = []
    for row in medications_data:
        if row.get('Disease') == dis:
            # Medications CSV structure might vary, assuming 'Medication' column contains JSON string or list
            # Based on previous code: med = medications[medications['Disease'] == dis]['Medication']
            # It seems it returns a list of values.
            # Let's assume one row per disease with a 'Medication' column
            m = row.get('Medication')
            if m:
                # If it's a string representation of a list, we might need to parse it, 
                # but previous code just returned the value.
                med = [m] 
    if not med:
        med = ["Medications not available."]

    # Diet
    die = []
    for row in diets_data:
        if row.get('Disease') == dis:
            d = row.get('Diet')
            if d:
                die = [d]
    if not die:
        die = ["Diet not available."]

    # Workout
    workout_plan = []
    for row in workout_data:
        if row.get('disease') == dis:
            w = row.get('workout')
            if w:
                workout_plan.append(w)
    if not workout_plan:
        workout_plan = ["Workout plan not available."]
    
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
    return jsonify({'symptoms': list(symptoms_dict.keys())})

@app.route('/api/predict', methods=['POST'])
def api_predict():
    data = request.get_json()
    if not data or 'symptoms' not in data:
        return jsonify({'error': 'No symptoms provided'}), 400
    
    user_symptoms = data['symptoms']
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
        if not symptoms:
            flash("Please enter symptoms!")
            return redirect(url_for('index'))
        
        user_symptoms = [s.strip() for s in symptoms.split(',')]
        predicted_disease = get_predicted_value(user_symptoms)
        
        if predicted_disease is None:
            flash("Sorry, we couldn't predict the disease. Please try again with different symptoms.")
            return redirect(url_for('index'))
        
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
    return 'ok', 200

if __name__ == "__main__":
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', '0') == '1'
    app.run(host=host, port=port, debug=debug)
