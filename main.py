from ast import arg, parse
import os
from urllib import response
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_functions, call_function
import argparse

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

if api_key is None:
    raise RuntimeError("API Key was not found")

client = genai.Client(api_key=api_key)
# Get user input from console
parser = argparse.ArgumentParser(description="AI-Agent")
parser.add_argument("user_prompt", type=str, help="User Prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

# Create list to store user prompts
messages: list[types.Content] = [
    types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
]

for _ in range(20):
    # call the model, handle responses, etc.
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if response.usage_metadata != None:
        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    else:
        raise RuntimeError("usage_metadata empty")

    print("Response:")
    function_calls = response.function_calls
    if function_calls:
        function_results = []
        for call in function_calls:
            # print(f"Calling function: {call.name}({call.args})")
            function_call_result = call_function(call, args.verbose)
            if not function_call_result.parts:
                raise Exception("function_call_result.parts is empty")
            if not function_call_result.parts[0].function_response:
                raise Exception("function_call_result.parts[0].function_response is None")
            if not function_call_result.parts[0].function_response.response:
                raise Exception("function_call_result.parts[0].function_response.response is None")
            function_results.append(function_call_result.parts[0])
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
        messages.append(types.Content(role="user", parts=function_results))
    else:
        print(response.text)
        break