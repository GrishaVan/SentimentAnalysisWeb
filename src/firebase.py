import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import os


class Review:
    def __init__(self, id, text, sentiment):
        self.id = id
        self.text = text
        self.sentiment = sentiment

class TMD:
    def __init__(self, id, title, text):
        self.id = id
        self.title = title
        self.text = text


def permission():
    firebase_cred_content = os.environ.get('CRED')
    firebase_cred = json.loads(firebase_cred_content)

    

    cred = credentials.Certificate(firebase_cred)
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://arctic-app-415800-default-rtdb.europe-west1.firebasedatabase.app/'
    })

def insert_text(review):
    ref = db.reference('Reviews')
    ref.child(str(review.id)).set({
        'id': review.id,
        'review': review.text,
        'sentiment': review.sentiment
    })

def inser_movie_review(tmd, id):
    ref = db.reference('Training_Reviews')
    ref.child(str(id)).set({
        'id': tmd.id,
        'title': tmd.title,
        'review': tmd.text
    })

def get_every_review():
    ref = db.reference('Training_Reviews')
    data = ref.get()
    data_key = {}
    for num, item in enumerate(data, 0):
        data_key[num] = item
    return data_key

def insert_analysis(text, sentiment):
    ref = db.reference('Analyzed_Reviews')
    num = get_analysis_id()
    ref.child(str(num)).set({
        'text': text,
        "sentiment": sentiment
    })

def delete_review(id):
    ref = db.reference(f'Training_Reviews/{id}')
    ref.delete()

def get_review_data(id):
    ref = db.reference(f'Training_Reviews/{id}')
    data = ref.get()
    return data

def get_analysis_id():
    ref = db.reference('Analyzed_Reviews')
    data = ref.get()
    if data is None:
        return 1
    else:
        return len(data)

def get_last_entry_id():
    ref = db.reference('Reviews')
    reviews = ref.get()
    if reviews:
        last_key = reviews[-1]
        return last_key['id']
    else:
        return None 

def read_sentiment(id):
    ref = db.reference(f'Reviews/{id}')
    data = ref.get()
    return data['sentiment']

def update_value(id, sentiment):
    ref = db.reference(f'Reviews/{id}')
    ref.update({
            'sentiment': sentiment
        })
    
def get_reviews():
    ref = db.reference("/Reviews")
    reviews_data = ref.get()
    review_list = []
    if len(reviews_data) > 0:
        for item in reviews_data:
            if item is None:
                continue
            else:
                review_list.append({"review": item["review"], "sentiment": item["sentiment"]})
        return review_list
    else:
        return []