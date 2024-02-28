from flask import Flask, request, render_template, redirect, url_for, jsonify
from embedding import *
from neural import *
import tensorflow as tf

app = Flask(__name__, template_folder="templates", static_folder='./styles')

@app.route('/', methods=['GET'])
def index():
    # Get sentiment from query string if available
    sentiment = request.args.get('sentiment', '')
    return render_template('index.html', sentiment=sentiment)

@app.route('/predict', methods=['POST'])
def predict():
    model = tf.keras.models.load_model("./Models/CNN/cnn_150")

    text_data = request.form['inputText']
    preprocess = process_text(text_data)
    emb = sentence_embedding(preprocess, "embedding_150.model")
    result = predict_sentiment(model, emb)
    print(result)


    return redirect(url_for('index') + '?sentiment=' + result)

@app.route('/feedback', methods=['POST'])
def feedback():
    feedback = request.form['feedback']
    print(f"Feedback received: {feedback}")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
