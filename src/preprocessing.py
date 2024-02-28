from bs4 import BeautifulSoup
import spacy

nlp = spacy.load("en_core_web_sm")

def process_text(text):
    text = BeautifulSoup(text, "html.parser").get_text()
    text = text.lower()
    doc = nlp(text)
    tokens = [token.lemma_ for token in doc if token.is_alpha and not token.is_stop]


    return tokens



if __name__ == '__main__':
    text = "<p>This is a long, text. That has everything ! Stop words such as the and not is. Lets see if I can tokenize this. ALso lammenizing words such as running </p>"
    print(process_text(text))
