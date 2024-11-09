import os
# Set a dummy API key for testing
os.environ['GROQ_API_KEY'] = 'dummy_key'
import pytest
from unittest.mock import patch, MagicMock
from analyzer import analyze_code
import logging



# Mocked code content and file for testing
SAMPLE_CODE_CONTENT = "def add(a, b): return a + b"
SAMPLE_FILE = "sample_code.py"
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

# Step 3: Mocking LLM API Response in test
@patch("analyzer.send_chat_completion_request")
@patch("analyzer.read_code_file")
def test_analyze_code_with_mocked_llm(mock_read_code_file, mock_send_chat_completion_request, tmp_path):
    # Arrange
    file_path = tmp_path / SAMPLE_FILE
    file_path.write_text(SAMPLE_CODE_CONTENT)
    output_file = tmp_path / "output.txt"

    # Mock the return values of read_code_file and LLM response
    mock_read_code_file.return_value = SAMPLE_CODE_CONTENT
    mock_llm_response = MagicMock()
    mock_llm_response.choices = [MagicMock()]
    mock_llm_response.choices[0].message.content = MOCK_LLM_RESPONSE["choices"][0]["message"]["content"]
    mock_llm_response.usage.prompt_tokens = MOCK_LLM_RESPONSE["usage"]["prompt_tokens"]
    mock_llm_response.usage.completion_tokens = MOCK_LLM_RESPONSE["usage"]["completion_tokens"]
    mock_send_chat_completion_request.return_value = mock_llm_response

    args = MagicMock()
    args.output = output_file
    args.token_usage = True
    args.file_size = True
    args.time = True

    # Act
    analyze_code(file_path=str(file_path), args=args)

    # Assert
    assert output_file.read_text().startswith("Mocked formatting suggestions.")


# Test for missing file_path
def test_analyze_code_with_missing_file(tmp_path, caplog):
    output_file = tmp_path / "output.txt"
    args = MagicMock()
    args.output = output_file
    args.token_usage = True
    args.file_size = True
    args.time = True

    # Simulate an invalid file path
    invalid_file_path = tmp_path / "non_existent_file.py"

    with caplog.at_level(logging.ERROR):
        analyze_code(file_path=str(invalid_file_path), args=args)

    # Check for the appropriate error message in logs
    assert any("An error occurred while analyzing the code" in record.message for record in caplog.records)


# Test for failed API response
@patch("analyzer.send_chat_completion_request")
@patch("analyzer.read_code_file")
def test_analyze_code_with_api_failure(mock_read_code_file, mock_send_chat_completion_request, tmp_path, caplog):
    file_path = tmp_path / SAMPLE_FILE
    file_path.write_text(SAMPLE_CODE_CONTENT)
    output_file = tmp_path / "output.txt"

    mock_read_code_file.return_value = SAMPLE_CODE_CONTENT
    mock_send_chat_completion_request.side_effect = Exception("API failure")

    args = MagicMock()
    args.output = output_file
    args.token_usage = True
    args.file_size = True
    args.time = True

    with caplog.at_level(logging.ERROR):
        analyze_code(file_path=str(file_path), args=args)

    # Check for the "API failure" message in logs
    assert any("API failure" in record.message for record in caplog.records)


# Test analyze_code with file size logging off
@patch("analyzer.send_chat_completion_request")
@patch("analyzer.read_code_file")
def test_analyze_code_without_file_size_logging(mock_read_code_file, mock_send_chat_completion_request, tmp_path):
    file_path = tmp_path / SAMPLE_FILE
    file_path.write_text(SAMPLE_CODE_CONTENT)
    output_file = tmp_path / "output.txt"

    mock_read_code_file.return_value = SAMPLE_CODE_CONTENT

    mock_response = MagicMock()
    mock_response.choices = [MagicMock()]
    mock_response.choices[0].message.content = "Mocked formatting suggestions."
    mock_send_chat_completion_request.return_value = mock_response

    args = MagicMock()
    args.output = output_file
    args.token_usage = True
    args.file_size = False  # Disable file size logging
    args.time = True

    analyze_code(file_path=str(file_path), args=args)

    # Check if output file has expected content
    assert output_file.read_text().startswith("Mocked formatting suggestions.")


# Step 3 Extended: Mock LLM Rate Limit Scenario
@patch("analyzer.send_chat_completion_request")
@patch("analyzer.read_code_file")
def test_analyze_code_with_llm_rate_limit(mock_read_code_file, mock_send_chat_completion_request, tmp_path, caplog):
    file_path = tmp_path / SAMPLE_FILE
    file_path.write_text(SAMPLE_CODE_CONTENT)
    output_file = tmp_path / "output.txt"

    mock_read_code_file.return_value = SAMPLE_CODE_CONTENT
    mock_send_chat_completion_request.side_effect = Exception("Rate limit exceeded")

    args = MagicMock()
    args.output = output_file
    args.token_usage = True
    args.file_size = True
    args.time = True

    with caplog.at_level(logging.ERROR):
        analyze_code(file_path=str(file_path), args=args)

    # Check that rate limit error message is logged
    assert any("Rate limit exceeded" in record.message for record in caplog.records)
