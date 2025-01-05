import re
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import nltk

nltk.download('stopwords')
nltk.download('wordnet')

french_stopwords = stopwords.words('french')
dutch_stopwords = stopwords.words('dutch')

def preprocess(text):
    text = re.sub(r"[^a-zA-ZÀ-ÿ0-9\s]", "", text.lower())
    lemmatizer = WordNetLemmatizer()
    words = text.split()
    words = [lemmatizer.lemmatize(word) for word in words if word not in stopwords.words("english")]
    words = [lemmatizer.lemmatize(word) for word in words if word not in french_stopwords]
    words = [lemmatizer.lemmatize(word) for word in words if word not in dutch_stopwords]
    return " ".join(words)
