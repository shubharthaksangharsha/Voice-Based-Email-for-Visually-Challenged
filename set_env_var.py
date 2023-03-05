import os
from dotenv import load_dotenv, set_key

# Load the .env file if it exists
load_dotenv()

while True:
    # Prompt the user for the environment variable name and value
    name = input("Enter the name of the environment variable: ")
    value = input("Enter the value of the environment variable: ")
    if name == 'exit':
        break
    # Set the environment variable in the current process
    os.environ[name] = value
    
    # Store the environment variable persistently in the .env file
    set_key('.env', name, value)
