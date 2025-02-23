import pickle

# Load the saved model and vectorizer
with open("text_classifier.pkl", "rb") as model_file:
    clf = pickle.load(model_file)

with open("tfidf_vectorizer.pkl", "rb") as vec_file:
    vectorizer = pickle.load(vec_file)

# Function to predict if a comment is "bad"
def predict_comment(comment):
    transformed_comment = vectorizer.transform([comment])  # Transform input text
    prediction = clf.predict(transformed_comment)  # Predict using the model
    return int(prediction[0])




