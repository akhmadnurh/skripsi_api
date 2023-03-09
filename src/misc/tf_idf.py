from sklearn.feature_extraction.text import TfidfVectorizer
import json


def tf_idf(datas):
    # Process data
    processed_data = []

    for data in datas:
        processed_data.append(" ".join(data["result"]["stem"]))

    vectorizer = TfidfVectorizer()
    tf_idf_response = vectorizer.fit_transform(processed_data)

    # Merge data
    feature_names = vectorizer.get_feature_names_out().tolist()
    tf_idf_results = (
        tf_idf_response.todense().tolist()
    )  # Convert from np matrix to list

    return [feature_names, tf_idf_results]
