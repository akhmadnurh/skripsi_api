# Remove punctuation, numbers, and emojis
import string
from cleantext import clean
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import SnowballStemmer


def remove_punc(val):
    for i in string.punctuation:
        val = val.replace(i, " ")

    return clean(
        val,
        lower=True,
        no_line_breaks=True,
        no_emoji=True,
        no_urls=True,
        no_emails=True,
        no_phone_numbers=True,
        no_numbers=True,
        no_digits=True,
        no_currency_symbols=True,
        no_punct=True,
        replace_with_punct=" ",
        replace_with_url=" ",
        replace_with_email=" ",
        replace_with_phone_number=" ",
        replace_with_number=" ",
        replace_with_digit=" ",
        replace_with_currency_symbol=" ",
    )


# Tokenizing
def tokenizing(val):
    return word_tokenize(val)


# Remove stopwords
def remove_stopword(val):
    stopwords = nltk.corpus.stopwords.words("english")
    extended_stopwords = f = open("./src/misc/stopwords.txt").read().splitlines()
    stopwords.extend(extended_stopwords)

    return [not_stopword for not_stopword in val if not_stopword not in stopwords]


# Snowball Stemming
def snow_stemming(val):
    snowball = SnowballStemmer(language="english")
    return [snowball.stem(word) for word in val]


remove_stopword("ok")
