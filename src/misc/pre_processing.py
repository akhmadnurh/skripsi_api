# Remove punctuation, numbers, and emojis
import string
from cleantext import clean


def remove_punc(val):
    # string.punctuation = "".join([string.punctuation, "➧", "·"])
    for i in string.punctuation:
        val = val.replace(i, " ")
    # using regex

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
