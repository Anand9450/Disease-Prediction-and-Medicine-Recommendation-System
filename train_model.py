import pandas as pd
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import json

# Load dataset
df = pd.read_csv('Training.csv')

# Split features and target
X = df.drop('prognosis', axis=1)
y = df['prognosis']

# Split into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train model
# Using Random Forest as it's generally more robust for this type of classification
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
print(f"Model Accuracy: {accuracy * 100:.2f}%")

# Save the model
with open('disease_model.pkl', 'wb') as f:
    pickle.dump(model, f)

# Save the symptoms list (feature names) to ensure consistent ordering
symptoms = list(X.columns)
with open('symptoms_list.json', 'w') as f:
    json.dump(symptoms, f)

print("Model trained and saved as 'disease_model.pkl'")
print("Symptoms list saved as 'symptoms_list.json'")
