import os
import pytest
import logging
from unittest.mock import patch, MagicMock
from example import read_code_file, send_chat_completion_request, analyze_code, measure_execution_time

# Sample test file path for testing purposes
SAMPLE_FILE = "sample_code.py"

# Mock content for testing the code read function
MOCK_CODE_CONTENT = "def add(a, b): return a + b"

# Set up logging to capture logs during tests
logging.basicConfig(level=logging.INFO)


# Test the read_code_file function
def test_read_code_file(tmp_path):
    # Arrange
    file_path = tmp_path / SAMPLE_FILE
    file_path.write_text(MOCK_CODE_CONTENT)

    # Act
    code = read_code_file(file_path)

    # Assert
    assert code == MOCK_CODE_CONTENT


# Mock the API client and simulate a response for send_chat_completion_request
@patch("example.client.chat.completions.create")
def test_send_chat_completion_request(mock_create):
    # Arrange
    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Mocked formatting suggestions."
    mock_create.return_value = mock_response

    # Act
    response = send_chat_completion_request(MOCK_CODE_CONTENT)

    # Assert
    assert response.choices[0].message.content == "Mocked formatting suggestions."


# Test the measure_execution_time decorator
def test_measure_execution_time():
    # Arrange
    @measure_execution_time
    def sample_function():
        time.sleep(1)
        return "Success"

    # Act
    result = sample_function()

    # Assert
    assert result == "Success"


# Test the analyze_code function with mocking for file I/O and API calls
@patch("example.send_chat_completion_request")
@patch("example.read_code_file")
def test_analyze_code(mock_read_code_file, mock_send_chat_completion_request, tmp_path):
    # Arrange
    output_file = tmp_path / "output.txt"
    mock_read_code_file.return_value = MOCK_CODE_CONTENT

    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Mocked formatting suggestions."
    mock_response.usage.prompt_tokens = 100
    mock_response.usage.completion_tokens = 50
    mock_send_chat_completion_request.return_value = mock_response

    args = MagicMock()
    args.output = output_file
    args.token_usage = True
    args.file_size = True
    args.time = True

    # Act
    analyze_code(str(tmp_path / SAMPLE_FILE), args)

    # Assert
    assert output_file.read_text().startswith("Mocked formatting suggestions.")
