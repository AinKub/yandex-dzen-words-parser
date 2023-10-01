import nltk
from pathlib import Path


if __name__ == '__main__':
    destination = Path(__file__).parent.parent / 'venv' / 'nltk_data'
    if not destination.exists():
        destination.mkdir()

    nltk.download('stopwords', download_dir=destination)
    nltk.download('punkt', download_dir=destination)