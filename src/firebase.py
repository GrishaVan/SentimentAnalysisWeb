import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from google.cloud import secretmanager

class Review:
    def __init__(self, id, text, sentiment):
        self.id = id
        self.text = text
        self.sentiment = sentiment

def access_secret_version(project_id, secret_id, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

def permission():
    project_id = "836401169728"
    secret_id = "FIREBASECRED"
    
    # Fetch the secret
    secret_content = access_secret_version(project_id, secret_id)
    
    # Parse the JSON string to a dictionary
    cred_dict = json.loads(secret_content)

    cred = credentials.Certificate(cred_dict)
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