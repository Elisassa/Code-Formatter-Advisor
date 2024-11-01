import os
import logging
import argparse
import tomli
from dotenv import load_dotenv  # For loading environment variables from a .env file
from analyzer import analyze_code
from utils import measure_execution_time

# Load environment variables from a .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)


@measure_execution_time
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
