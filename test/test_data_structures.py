
import sys
from pathlib import Path

# Add the project root folder to Python's import path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from data_structures import word_frequency


def test_word_frequency():
    result = word_frequency("python is easy python")

    expected = {
        "python": 2,
        "is": 1,
        "easy": 1
    }

    assert result == expected


def test_word_frequency_empty_text():
    result = word_frequency("")

    assert result == {}
