import os
import logging
from utils import read_code_file, send_chat_completion_request


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
