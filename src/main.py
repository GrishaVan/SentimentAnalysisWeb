from dotenv import load_dotenv
from flask import Flask, request, render_template, redirect, url_for, jsonify
from embedding import *
from neural import *
import tensorflow as tf
import os
from flask_cors import CORS
from firebase import *
import random

model = tf.keras.models.load_model("./Models/CNN/cnn_150")

load_dotenv()
permission()

app = Flask(__name__, template_folder="templates", static_folder='./styles')
CORS(app)


app.config["DEBUG"] = os.environ.get("FLASK_DEBUG")

@app.route('/', methods=['GET'])
def index():
    return render_template('cover.html')

@app.route('/bot', methods=['GET'])
def affectobot():
    # Get sentiment from query string if available
    sentiment = request.args.get('sentiment', '')
    return render_template('index.html', sentiment=sentiment)

@app.route('/predict', methods=['POST'])
def predict():
    

    text_data = request.form['inputText']
    print("got the text")
    preprocess = process_text(text_data)
    emb = sentence_embedding(preprocess, "embedding_150.model")
    result = predict_sentiment(model, emb)

    id = get_last_entry_id()

    if id is None:
        id = 1
    else:
        id += 1
    rev = Review(id, text_data, result)
    insert_text(rev)

    return redirect(url_for('affectobot') + '?sentiment=' + result)

@app.route('/feedback', methods=['POST'])
def feedback():
    feedback = request.form['feedback']
    id = get_last_entry_id()
    if feedback != "correct":
        if read_sentiment(id) == "Positive":
            update_value(id, "Negative")
        else:
            update_value(id, "Negative")

    return redirect(url_for('affectobot'))

@app.route('/train', methods=['GET', 'POST'])
def train():
    if request.method == 'POST':
        review_id = request.form['review_id']
        sentiment = request.form['sentiment']
        data = get_review_data(review_id)
        delete_review(review_id)
        insert_analysis(data["review"], sentiment)
        return redirect(url_for('train'))

    review = get_every_review()
    review_ids = list(review.keys())
    random_review_id = random.choice(review_ids)
    random_rev = review[random_review_id]
    random_rev['id'] = random_review_id

    return render_template('train.html', review=random_rev)



if __name__ == '__main__':
  
    app.run()
    
