import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_PATH = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_PATH))

import pytest

from preprocessor import normalize_prompt, get_prompt_features


def test_normalize_prompt_lowercase():
    result = normalize_prompt("HELLO WORLD")

    assert result == "hello world"


def test_normalize_prompt_removes_extra_spaces():
    result = normalize_prompt("   Hello     World   ")

    assert result == "hello world"


def test_normalize_prompt_handles_newlines():
    result = normalize_prompt("Hello\n\nWorld")

    assert result == "hello world"


def test_normalize_prompt_invalid_input():
    with pytest.raises(TypeError):
        normalize_prompt(123)


def test_prompt_features():
    prompt = "Hello World! 123"

    features = get_prompt_features(prompt)

    assert features["character_count"] == len(prompt)
    assert features["word_count"] == 3
    assert features["uppercase_count"] == 2
    assert features["digit_count"] == 3
    assert features["special_character_count"] == 1