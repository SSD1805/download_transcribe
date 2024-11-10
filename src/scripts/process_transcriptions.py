import spacy
import pandas as pd
import nltk
from tqdm import tqdm
from pathlib import Path

# Download NLTK data
nltk.download('punkt')

# Load spaCy's English model for NER and sentence segmentation
nlp = spacy.load("en_core_web_sm")

# Define paths (these can be adjusted to match your setup or config file)
TRANSCRIPTIONS_DIR = "/app/transcriptions"
OUTPUT_DIR = "/app/processed_transcriptions"

# Create output directory if it doesn't exist
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

def process_transcriptions():
    """
    Process each transcription file in the transcription directory by:
    - Segmenting text into sentences
    - Performing named entity recognition (NER)
    - Tokenizing sentences using NLTK
    - Saving processed output to a new file in a structured format
    """
    # Iterate over each transcription file
    for file_name in tqdm(os.listdir(TRANSCRIPTIONS_DIR), desc="Processing transcriptions"):
        if file_name.endswith(".txt"):
            file_path = os.path.join(TRANSCRIPTIONS_DIR, file_name)
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()

            # Process content with spaCy
            doc = nlp(content)

            # Segment text and extract entities
            segmented_text = []
            for sent in doc.sents:
                entities = [(ent.text, ent.label_) for ent in sent.ents]
                tokens = nltk.word_tokenize(sent.text)
                segmented_text.append({"sentence": sent.text, "entities": entities, "tokens": tokens})

            # Convert to DataFrame for easy CSV export
            df = pd.DataFrame(segmented_text)

            # Save processed file as CSV in the output directory
            output_file_path = os.path.join(OUTPUT_DIR, f"{Path(file_name).stem}_processed.csv")
            df.to_csv(output_file_path, index=False, encoding="utf-8")
            print(f"Processed transcription saved to: {output_file_path}")

if __name__ == "__main__":
    process_transcriptions()