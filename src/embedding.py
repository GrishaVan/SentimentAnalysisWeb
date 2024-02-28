import json
import os
from gensim.models import Word2Vec
import numpy as np
from preprocessing import process_text

def sentence_embedding(sentence, model_name, max_length=266):
    model = Word2Vec.load(f"../Models/Embedding/{model_name}")
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
    
    print("Here")

                
    