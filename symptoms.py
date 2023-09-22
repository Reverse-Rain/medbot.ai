
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier


# Define the dataset or knowledge base associating symptoms with diseases
symptoms_to_diseases = {
    'cough': ['common cold', 'influenza', 'pneumonia'],
    'fever': ['common cold', 'influenza', 'pneumonia', 'malaria'],
    'headache': ['migraine', 'tension headache'],
    'sore throat': ['common cold', 'streptococcal infection'],
    'fatigue': ['chronic fatigue syndrome', 'anemia', 'depression'],
    'nausea': ['gastroenteritis', 'migraine', 'pregnancy'],
    'vomiting': ['gastroenteritis', 'food poisoning'],
    'diarrhea': ['gastroenteritis', 'food poisoning', 'irritable bowel syndrome'],
    'abdominal pain': ['gastroenteritis', 'appendicitis', 'peptic ulcer'],
    'chest pain': ['angina', 'heart attack', 'acid reflux'],
    'shortness of breath': ['asthma', 'pneumonia', 'chronic obstructive pulmonary disease'],
    'joint pain': ['arthritis', 'gout', 'fibromyalgia'],
    'muscle weakness': ['myasthenia gravis', 'polymyositis', 'hypothyroidism'],
    'rash': ['allergic reaction', 'eczema', 'psoriasis'],
    'swollen lymph nodes': ['infection', 'lymphoma', 'mononucleosis'],
    'weight loss': ['cancer', 'diabetes', 'hyperthyroidism'],
    'excessive thirst': ['diabetes', 'dehydration', 'diabetes insipidus'],
    'frequent urination': ['urinary tract infection', 'diabetes', 'overactive bladder'],
    'difficulty swallowing': ['gastroesophageal reflux disease', 'esophageal stricture'],
    'memory loss': ['Alzheimer','sdisease','dementia', 'brain injury'],
    'decreased appetite': ['anorexia', 'depression', 'cancer'],
    'sleep disturbances': ['insomnia', 'sleep apnea', 'restless leg syndrome'],
    'back pain': ['muscle strain', 'herniated disc', 'kidney stones'],
    'dizziness': ['vertigo', 'low blood pressure', 'inner ear infection'],
    'vision changes': ['cataracts', 'glaucoma', 'macular degeneration'],
    'irritability': ['anxiety', 'bipolar disorder', 'premenstrual syndrome'],
    'hair loss': ['alopecia', 'thyroid disorders', 'chemotherapy'],
    'sweating': ['hyperhidrosis', 'menopause', 'anxiety disorders'],
    'stomach bloating': ['gas', 'indigestion', 'constipation'],
    'throat clearing': ['postnasal drip', 'acid reflux', 'vocal cord dysfunction'],
    'nosebleeds': ['dry air', 'nasal trauma', 'high blood pressure'],
    'fainting': ['vasovagal syncope', 'heart arrhythmia', 'hypoglycemia'],
    'muscle cramps': ['dehydration', 'electrolyte imbalance', 'peripheral artery disease'],
    'tingling sensation': ['nerve compression', 'diabetic neuropathy', 'multiple sclerosis'],
    'swollen joints': ['rheumatoid arthritis', 'gout', 'inflammatory osteoarthritis'],
    # Add more symptoms and corresponding diseases as needed
}

# Prepare the dataset for training the classifier
symptoms = []
diseases = []
for symptom, associated_diseases in symptoms_to_diseases.items():
    symptoms.append(symptom)
    diseases.append(', '.join(associated_diseases))

# Vectorize the symptoms
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(symptoms)

# Encode the diseases
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(diseases)

# Train the classifier
classifier = RandomForestClassifier()
classifier.fit(X, y)

# Get user input for symptoms
user_input = input("Enter symptoms (comma-separated): ")
user_symptoms = user_input.split(',')

# Vectorize the user symptoms
X_user = vectorizer.transform(user_symptoms)

# Predict diseases based on user symptoms
predicted_diseases_encoded = classifier.predict(X_user)

# Decode the predicted disease labels
predicted_diseases = label_encoder.inverse_transform(predicted_diseases_encoded)

# Print the predicted diseases
if len(predicted_diseases) > 0:
    print("Predicted diseases based on the given symptoms:")
    for disease in predicted_diseases:
        print("- " + disease)
else:
    print("No diseases predicted for the given symptoms.")
