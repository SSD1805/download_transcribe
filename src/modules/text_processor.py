import spacy
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import pandas as pd
from logger import LoggerManager

log_manager = LoggerManager()
logger = log_manager.get_logger()

# Ensure the necessary NLTK data is downloaded
nltk.download('punkt')
nltk.download('stopwords')


class TextProcessor:
    def __init__(self, spacy_model='en_core_web_sm'):
        """
        Initialize the TextProcessor with a specified spaCy model.
        """
        self.spacy_model = spacy.load(spacy_model)
        self.nltk_stopwords = set(stopwords.words('english'))
        self.input_text = ""
        self.processed_data = pd.DataFrame()  # DataFrame to store processed sentences and NER results

    def load_text(self, text):
        """
        Load the input text for processing.

        Args:
            text (str): The input text to be processed.
        """
        self.input_text = text
        logger.info("Text loaded for processing.")

    def segment_sentences(self):
        """
        Segment the input text into sentences using NLTK.

        Returns:
            list: A list of segmented sentences.
        """
        sentences = sent_tokenize(self.input_text)
        logger.info(f"Segmented text into {len(sentences)} sentences.")
        return sentences

    def perform_ner(self):
        """
        Perform named entity recognition (NER) on the input text using spaCy.

        Returns:
            list of dict: A list of entities with their labels and positions.
        """
        doc = self.spacy_model(self.input_text)
        entities = [{'text': ent.text, 'label': ent.label_, 'start': ent.start_char, 'end': ent.end_char} for ent in
                    doc.ents]
        logger.info(f"Found {len(entities)} named entities.")
        return entities

    def tokenize_text(self):
        """
        Tokenize the input text and remove stopwords using NLTK.

        Returns:
            list: A list of tokens without stopwords.
        """
        words = word_tokenize(self.input_text)
        tokens = [word for word in words if word.isalnum() and word.lower() not in self.nltk_stopwords]
        logger.info(f"Tokenized text into {len(tokens)} tokens after removing stopwords.")
        return tokens

    def save_processed_text(self, filepath):
        """
        Save the segmented sentences and NER results to a CSV file.

        Args:
            filepath (str): The path to save the CSV file.
        """
        sentences = self.segment_sentences()
        entities = self.perform_ner()

        # Create a DataFrame from the segmented sentences and entities
        self.processed_data = pd.DataFrame({
            'Sentence': sentences,
            'Entities': [self.perform_ner() for _ in range(len(sentences))]
        })

        # Save to CSV
        self.processed_data.to_csv(filepath, index=False)
        logger.info(f"Processed text saved to {filepath}.")