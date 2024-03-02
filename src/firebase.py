import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class Review:
    def __init__(self, id, text, sentiment):
        self.id = id
        self.text = text
        self.sentiment = sentiment

def permission():
    path = "./arctic-app-415800-firebase-adminsdk-j43fz-8ca974f717.json"

    cred = credentials.Certificate(path)
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