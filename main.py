import os  
import time
from dotenv import load_dotenv  # For loading environment variables from a .env file
import argparse  # For parsing command line arguments
from groq import Groq  # GroqCloud API client
import tomli  # For parsing TOML configuration files

# Load environment variables from a .env file
load_dotenv()

# get mt api key from .env file
my_api_key = os.environ.get("GROQCLOUD_API_KEY")
#print(f"Loaded API Key: {api_key}") 

client = Groq(api_key=my_api_key) #use my api key to send request to  Groq


def analyze_code(file_path, args):
    try:
        if args.time:#start time
            start_time = time.time()
        # Open and read the code file
        with open(file_path, 'r') as file:# use with... as syntax so no need to manually close
            code = file.read()  

        # If the --file-size argument is provided, calculate and display the size of the file
        if args.file_size:
            file_size = os.path.getsize(file_path)
            print(f"The file {file_path} has a size of {file_size} bytes.")

        # Send a chat completion request to get formatting suggestions
        chat_completion = client.chat.completions.create( #.create same as js .then use for promise
            messages=[
                {
                    "role": "user",
                    #prompt!!!
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

        # Retrieve from api see groqcloud response json file
        suggestions = chat_completion.choices[0].message.content.strip() #use strip remove others space

        # Append the token usage information if the --token-usage flag is provided
        if args.token_usage:
            tokens = f"Message Token: {chat_completion.usage.prompt_tokens}\nResponse Token: {chat_completion.usage.completion_tokens}"
            suggestions = f"{suggestions}\n\n{tokens}"

        # Save suggestions to a file or print to the terminal
        if args.output:
            output_file = args.output
            with open(output_file, 'w') as f:
                f.write(suggestions)
            print(f"Suggestions have been written to {output_file}")
        else:
            print(f"\nFormatting Suggestions:\n{suggestions}")
        

        #record the time
        if args.time:
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Analysis of {file_path} completed in {execution_time:.2f} seconds.")

    except Exception as err:
        print(f"An error occurred: {err}")

def main():

    # check if toml file is present
    toml_file_path = "./.advisor-config.toml"
    toml_dict = {}
    if os.path.exists(toml_file_path):
        print(f"{toml_file_path} is present. Parsing now")
        with open(toml_file_path, "rb") as f:
            try:
                toml_dict = tomli.load(f)
            except tomli.TOMLDecodeError:
                print(toml_file_path, "toml file is not valid")
                return -1
    else:
        print(f"{toml_file_path} is not present. Ignoring the TOML configs")


    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="CodeFormatterAdvisor: A tool to provide code formatting improvement suggestions")
    parser.add_argument('--version', '-v', action='version', version='CodeFormatterAdvisor 0.1')  # Version information
    parser.add_argument('--output', '-o', type=str, help='Specify the output file name')  # Output file option
    parser.add_argument('--token-usage', '-t', action='store_true', help='Display token information along with the improved code')  # Token usage option
    parser.add_argument('--file-size', '-s', action='store_true', help='Calculate and display file size before analysis')  # Enable file size calculation
    parser.add_argument('files', nargs='+', help='The code files to be analyzed')  # Accept one or more input files
    parser.add_argument('--time', action='store_true', help='Measure and display execution time for the analysis')  # Enable time measurement
    args = parser.parse_args() 

    # override the default values with the values from the toml file
    if toml_dict:
        if "output" in toml_dict:
            args.output = toml_dict["output"]
        if "token-usage" in toml_dict:
            args.token_usage = toml_dict["token-usage"]
        if "file-size" in toml_dict:
            args.file_size = toml_dict["file-size"]
        if "time" in toml_dict:
            args.time = toml_dict["time"]

    # Iterate through each input file and analyze it
    for file_path in args.files:
        if os.path.exists(file_path):
            print(f"Analyzing file: {file_path}")
            analyze_code(file_path, args)
        else:
            print(f"File {file_path} does not exist")

if __name__ == "__main__":
    main()  # Run the main function
