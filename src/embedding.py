import json
import os
from gensim.models import Word2Vec
import numpy as np
from preprocessing import process_text


def print_progress_bar(iteration, total, bar_length=50):
    percent = ("{0:.1f}").format(100 * (iteration / float(total)))
    filled_length = int(bar_length * iteration // total)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)
    print(f'\rProgress: |{bar}| {percent}% Complete {iteration}/{total}', end='\r')
    if iteration == total: 
        print()

def create_preprocessed():
    reviews = []
    with open("./Reviews/Train/train_reviews", "r") as file:
        movies = json.load(file)
        for entry in movies:
            for rev in entry["reviews"]:
                if num == 10:
                    num = 0
                    print("movie done")
                    break
                else:
                    reviews.append({"reviews": process_text(rev["review"]),
                                    "rating": rev["rating"],
                                    "date" : rev["date"]
                                    })
                    num += 1

    with open("./Reviews/preprocessed_text.json", "w") as file:
        json.dump(reviews, file, indent=4)
            
def create_corpus():
    with open("./Reviews/Train/train_reviews.json", "r") as file:
        reviews = json.load(file)
    corpus = []
    for entry in reviews:
        corpus.append(entry["review"])
    return corpus

def train_embeding(name, vector_size):
    corpus = create_corpus()
    model = Word2Vec(sentences=corpus, vector_size=vector_size, window=5, min_count=3, workers=6)
    model.save(f"./Models/Embedding/{name}.model")
    return model

def sentence_embedding(sentence, model_name, max_length=266):
    model = Word2Vec.load(f"./Models/Embedding/{model_name}")
    # Create an empty matrix with fixed max_length and vector_size
    sentence_matrix = np.zeros((max_length, model.vector_size))
    
    # Iterate over the sentence
    for i, word in enumerate(sentence):
        # If the word is in the model's vocabulary, add its vector to the matrix
        if word in model.wv.key_to_index:
            # Check if the index is within the max length
            if i < max_length:
                sentence_matrix[i] = model.wv[word]
            else:
                # If the sentence is longer than the max length, stop adding word vectors
                break
    
    # If no words were found in the model's vocabulary, return a zero vector
    if not np.any(sentence_matrix):
        return np.zeros((max_length, model.vector_size))
    
    # Otherwise, return the matrix representing the sentence
    return sentence_matrix


if __name__ == "__main__":
    
    for emb in os.listdir("./Models/Embedding"):
        words = []
        vector_size = int(emb.split("_")[-1].split(".")[0])
        if vector_size == 75 or vector_size == 50:
            print(vector_size)
            path = "./Embeddings/" + str(vector_size) + "_words.json"
            with open("./Reviews/Train/train_reviews.json", "r") as file:
                reviews = json.load(file)
                total_reviews = len(reviews)
                embedded_reviews = []

                for num, entry in enumerate(reviews, start=1): 
                    print_progress_bar(num, total_reviews)
                    embedding = sentence_embedding(entry["review"], emb)
                    embedded_reviews.append(embedding)

                np.save("./Embeddings/" + str(vector_size) + "_embedding.npy", np.array(embedded_reviews))

                
    