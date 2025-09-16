import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    
    load_dotenv(dotenv_path="ai_project.env")
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print("GEMINI_API_KEY not found in environment variables.")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: python main.py <prompt> [--verbose]")
        sys.exit(1)

    # Determine if --verbose flag is present
    verbose = "--verbose" in sys.argv

    # Get the prompt by slicing the arguments list and removing the verbose flag if present
    prompt_args = sys.argv[1:]
    if verbose:
        prompt_args.remove("--verbose")

    # If the prompt is empty after removing --verbose, exit
    if not prompt_args:
        print("Usage: python main.py <prompt> [--verbose]")
        sys.exit(1)

    user_prompt = " ".join(prompt_args)

    # Create the list of messages in the new format
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    try:
        client = genai.Client(api_key=api_key)

        # Update the API call to use the new `messages` list
        response = client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=messages
        )

        # Print verbose output if the flag is set
        if verbose:
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        # Always print the model's text response
        print(response.text)

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()