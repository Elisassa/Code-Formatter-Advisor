#test_utils.py

import os
import time 
# Set a dummy API key for testing
os.environ['GROQ_API_KEY'] = 'dummy_key'
import pytest
from unittest.mock import patch, MagicMock
from analyzer import analyze_code
from utils import read_code_file, send_chat_completion_request, measure_execution_time
import logging
MOCK_CODE_CONTENT = "def multiply(x, y): return x * y"
MOCK_LLM_RESPONSE = {
    "choices": [
        {
            "message": {
                "content": "Mocked formatting suggestions."
            }
        }
    ],
    "usage": {
        "prompt_tokens": 100,
        "completion_tokens": 50
    }
}

logging.basicConfig(level=logging.INFO)

"""
    This test verifies that the read_code_file() function reads the content
    of a file and returns it correctly.
"""
def test_read_code_file(tmp_path):
    file_path = tmp_path / "test_code.py"
    file_path.write_text(MOCK_CODE_CONTENT)
    result = read_code_file(str(file_path))
    assert result == MOCK_CODE_CONTENT, "The content of the file was not read correctly."
    
		
"""
    This test checks that the measure_execution_time decorator correctly logs
    the execution time of the decorated function.
"""
@measure_execution_time
def sample_function():
    time.sleep(0.1)  # Adding slight delay to test execution time logging
    return "Sample Output"

def test_measure_execution_time_decorator(caplog):
    with caplog.at_level(logging.INFO):
        result = sample_function()
    assert result == "Sample Output"
    assert any("Execution time" in record.message for record in caplog.records)