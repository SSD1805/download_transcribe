# progress_bar_test.py
from tqdm import tqdm

class ProgressBar:
    @staticmethod
    def progress_bar(iterable, description="Processing"):
        return tqdm(iterable, desc=description)