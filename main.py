import os  
from dotenv import load_dotenv  # For loading environment variables from a .env file
import argparse  # For parsing command line arguments
from groq import Groq  # GroqCloud API client

# Load environment variables from a .env file
load_dotenv()

# get mt api key from .env file
my_api_key = os.environ.get("GROQCLOUD_API_KEY")
#print(f"Loaded API Key: {api_key}") 

client = Groq(api_key=my_api_key) #use my api key to send request to  Groq


def analyze_code(file_path, output_file=None):
    try:
        # Open and read the code file
        with open(file_path, 'r') as file:# use with... as syntax so no need to manually close
            code = file.read()  

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

        # Save suggestions to a file or print to the terminal
        if output_file:
            with open(output_file, 'w') as f:
                f.write(suggestions)
            print(f"Suggestions have been written to {output_file}")
        else:
            print(f"\nFormatting Suggestions:\n{suggestions}")

    except Exception as err:
        print(f"An error occurred: {err}")

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description="CodeFormatterAdvisor: A tool to provide code formatting improvement suggestions")
    parser.add_argument('--version', '-v', action='version', version='CodeFormatterAdvisor 0.1')  # Version information
    parser.add_argument('--output', '-o', type=str, help='Specify the output file name')  # Output file option
    parser.add_argument('files', nargs='+', help='The code files to be analyzed')  # Accept one or more input files
    args = parser.parse_args() 

    # Iterate through each input file and analyze it
    for file_path in args.files:
        if os.path.exists(file_path):
            print(f"Analyzing file: {file_path}")
            analyze_code(file_path, args.output)
        else:
            print(f"File {file_path} does not exist")

if __name__ == "__main__":
    main()  # Run the main function
