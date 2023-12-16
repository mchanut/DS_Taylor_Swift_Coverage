import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

def combine_data(file_path,column_name,output_file_name):
    df = pd.read_csv(file_path, sep="\t")
    df["Combined"] = df["Title"] + " " + df["Description"]
    desired_columns = ['Combined', column_name]
    filtered_df = df[desired_columns]
    filtered_df.to_csv(output_file_name, sep='\t', index=False)
    return df



def preprocess_text(text):
    # lowercase, remove punctuation, remove stopwords, lemmatize
    text = text.lower()
    text = text.replace("’s", "")
    text = text.replace("'s", "")
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    words = nltk.word_tokenize(text)
    lemmatizer = WordNetLemmatizer()
    # lemmatization and remove stopwords
    cleaned_words = [lemmatizer.lemmatize(word) for word in words if word.lower() not in stopwords.words("english")]
    cleaned_text = " ".join(cleaned_words)
    return cleaned_text

def write_preprocessed_data(file_path, output_file_name):
    df = pd.read_csv(file_path, sep="\t")
    df["Combined"] = df["Combined"].apply(preprocess_text)
    df.to_csv(output_file_name, sep="\t", index=False)


if __name__ == "__main__":
    # pass
    combine_data("swift_annotated2.tsv", "Category", "category_preprocessed_data.tsv")
    combine_data("swift_annotated3.tsv", "Sentiment", "sentiment_preprocessed_data.tsv")

    write_preprocessed_data("category_preprocessed_data.tsv", "category_preprocessed_data.tsv")
    write_preprocessed_data("sentiment_preprocessed_data.tsv", "sentiment_preprocessed_data.tsv")
