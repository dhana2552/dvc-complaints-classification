import logging
import re
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

ps = PorterStemmer()
def clean_text(series):
    series = series.apply(lambda x: re.sub('[^a-zA-Z]|[XX*]', ' ', x).split())
    series = series.apply(lambda x: [ps.stem(i) for i in x])
    # series = series.apply(lambda x: ' '.join(x))
    return series