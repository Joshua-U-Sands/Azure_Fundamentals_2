import csv
import re
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

credentials = AzureKeyCredential("de287d777a34405590f71ade62da840c")
endpoint = "https://fundamentalslanguage.cognitiveservices.azure.com/"

def main():
    client = TextAnalyticsClient(endpoint=endpoint, credential=credentials)
    sentiment_analysis_example(client)

def sentiment_analysis_example(client):
    input_text = "I recently watched a highly anticipated movie that had received rave reviews from critics. The film had a captivating storyline and kept me engaged from start to finish. The acting performances were outstanding, with the lead actors delivering powerful and emotive portrayals. The visual effects were breathtaking, adding a whole new dimension to the viewing experience. I was thoroughly impressed and couldn't help but feel a sense of awe and wonder throughout the movie. It was an absolute delight to watch and exceeded all my expectations. This film is definitely a must-see for any movie enthusiast!"
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s", input_text)  # Split input into sentences

    sentiment_data = []
    for sentence in sentences:
        document_sentiment = client.analyze_sentiment(documents=[sentence])[0]

        sentiment_data.append({
            "Text": sentence,
            "Sentiment": document_sentiment.sentiment,
            "Positive Score": document_sentiment.confidence_scores.positive,
            "Negative Score": document_sentiment.confidence_scores.negative,
            "Neutral Score": document_sentiment.confidence_scores.neutral
        })


    file_path = "sentiment_data.csv"
    with open(file_path, mode="a", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=sentiment_data[0].keys())
        if file.tell() == 0:  # Check if the file is empty
            writer.writeheader()
        writer.writerows(sentiment_data)

    print(f"Sentiment data appended to {file_path}")

if __name__ == "__main__":
    main()
