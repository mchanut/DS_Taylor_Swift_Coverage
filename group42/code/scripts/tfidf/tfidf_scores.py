import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import math


def compute_tfidf(df, label_column='Sentiment'):  
    label_documents = defaultdict(list)
    for _, row in df.iterrows():
        # label = row['Category']
        # label = row['Sentiment']
        label = row[label_column]
        text = row['Combined']
        label_documents[label].append(text)

    top_tfidf_words_by_label = {}

    for label, documents in label_documents.items():
        tokenized_documents = [document.split() for document in documents]
        unique_words = set(word for document in tokenized_documents for word in document)
        term_frequency = {}
        for word in unique_words:
            term_frequency[word] = sum(1 for document in tokenized_documents if word in document)
        document_count = len(documents)
        inverse_document_frequency = {}
        for word in unique_words:
            
            word_count = sum(1 for document in tokenized_documents if word in document)
            # prevent 0 division error
            inverse_document_frequency[word] = math.log(document_count / (1 + word_count))
        
        tfidf_scores = {}
        for word in unique_words:
            tfidf_scores[word] = term_frequency[word] * inverse_document_frequency[word]
        top_words = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)[:10]
        top_tfidf_words_by_label[label] = top_words

    for label, top_words in top_tfidf_words_by_label.items():
        print(f"Label: {label}")
        for word, tfidf_score in top_words:
            print(f"Word: {word}, TF-IDF: {tfidf_score}")

if __name__ == '__main__':
    df_c = pd.read_csv("category_preprocessed_data.tsv", sep="\t")
    df_s = pd.read_csv("sentiment_preprocessed_data.tsv", sep="\t")
    compute_tfidf(df_c, label_column='Category')
    compute_tfidf(df_s, label_column='Sentiment')