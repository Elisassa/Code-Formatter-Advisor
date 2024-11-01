import os  
import time
import logging
from dotenv import load_dotenv  # For loading environment variables from a .env file
import argparse  # For parsing command line arguments
from groq import Groq  # GroqCloud API client
import tomli  # For parsing TOML configuration files

# Load environment variables from a .env file
load_dotenv()

# Get API key from .env file
my_api_key = os.environ.get("GROQCLOUD_API_KEY")

client = Groq(api_key=my_api_key)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)


# Function to read the code file
def read_code_file(file_path):
    with open(file_path, 'r') as file:
        code = file.read()
    return code


# Function to send a chat completion request
def send_chat_completion_request(code):
    return client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"""Analyze the following code and provide detailed formatting and improvement suggestions. Focus on the following aspects:
                1. Standardize indentation and spacing for better readability.
                2. Suggest descriptive and meaningful function and variable names.
                3. Add appropriate docstrings to functions to explain their purpose, inputs, and outputs.
                4. Include type hints for function arguments and return values to enhance code clarity.
                5. Highlight any unused imports or redundant code that can be removed.
                6. Suggest improvements to make the code adhere to best practices and improve its overall structure.

                Here is the code:{code}
                """,
            }
        ],
        model="mixtral-8x7b-32768",
    )


# Measure execution time
def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logging.info(f"Execution time: {end_time - start_time:.2f} seconds.")
        return result
    return wrapper


@measure_execution_time
def analyze_code(file_path, args):
    try:
        logging.info(f"Starting analysis for file: {file_path}")

        # Open and read the code file
        code = read_code_file(file_path)

        # Log the file size if required
        if args.file_size:
            file_size = os.path.getsize(file_path)
            logging.info(f"The file {file_path} has a size of {file_size} bytes.")

        # Send a chat completion request to get formatting suggestions
        chat_completion = send_chat_completion_request(code)

        # Retrieve suggestions from the API
        suggestions = chat_completion.choices[0].message.content.strip()

        # Append the token usage information if the --token-usage flag is provided
        if args.token_usage:
            tokens = f"Message Token: {chat_completion.usage.prompt_tokens}\nResponse Token: {chat_completion.usage.completion_tokens}"
            suggestions = f"{suggestions}\n\n{tokens}"

        # Save suggestions to a file or print to the terminal
        if args.output:
            output_file = args.output
            with open(output_file, 'w') as f:
                f.write(suggestions)
            logging.info(f"Suggestions have been written to {output_file}")
        else:
            logging.info(f"\nFormatting Suggestions:\n{suggestions}")

    except Exception as err:
        logging.error(f"An error occurred while analyzing the code: {err}")


def main():
    # Check if toml file is present
    toml_file_path = "./.advisor-config.toml"
    toml_dict = {}
    if os.path.exists(toml_file_path):
        logging.info(f"{toml_file_path} is present. Parsing now")
        with open(toml_file_path, "rb") as f:
            try:
                toml_dict = tomli.load(f)
            except tomli.TOMLDecodeError:
                logging.error(f"{toml_file_path} is not a valid TOML file")
                return -1
    else:
        logging.warning(f"{toml_file_path} is not present. Ignoring the TOML configs")

    # Set up command line argument parsing
    parser = argparse.ArgumentParser(
        description="CodeFormatterAdvisor: A tool to provide code formatting improvement suggestions"
    )
    parser.add_argument(
        '--version', '-v', action='version', version='CodeFormatterAdvisor 0.1'
    )  # Version information
    parser.add_argument(
        '--output', '-o', type=str, help='Specify the output file name'
    )  # Output file option
    parser.add_argument(
        '--token-usage',
        '-t',
        action='store_true',
        help='Display token information along with the improved code',
    )  # Token usage option
    parser.add_argument(
        '--file-size',
        '-s',
        action='store_true',
        help='Calculate and display file size before analysis',
    )  # Enable file size calculation
    parser.add_argument(
        'files', nargs='+', help='The code files to be analyzed'
    )  # Accept one or more input files
    parser.add_argument(
        '--time',
        action='store_true',
        help='Measure and display execution time for the analysis',
    )  # Enable time measurement
    args = parser.parse_args()

    # Override the default values with the values from the toml file
    if toml_dict:
        if not args.output and "output" in toml_dict:
            args.output = toml_dict["output"]
        if not args.token_usage and "token-usage" in toml_dict:
            args.token_usage = toml_dict["token-usage"]
        if not args.file_size and "file-size" in toml_dict:
            args.file_size = toml_dict["file-size"]
        if not args.time and "time" in toml_dict:
            args.time = toml_dict["time"]

    # Iterate through each input file and analyze it
    for file_path in args.files:
        if os.path.exists(file_path):
            analyze_code(file_path, args)
        else:
            logging.error(f"File {file_path} does not exist")


if __name__ == "__main__":
    main()  # Run the main function
