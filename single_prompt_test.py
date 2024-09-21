import anthropic
import io
import json
import pandas as pd
import re
import sys

from getpass import getpass
def get_api_key():
    return getpass('Enter your Anthropic API key: ')

api_key = getpass("Enter your Anthropic key: ")

df = pd.read_csv('path_to_your_file.csv') # Replace with the actual path to the .csv file that contains passage, question, correct_answer, distractor1, distractor2, and distractor3 columns

examples = """ list of examples used """ # Choose from examples shared in the prompts file

def find_type (passage, question, examples, api_key): # Replace with the prompt being tested and its inputs
    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620", # Replace with the desired model, if necessary
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": f""" INSERT PROMPT HERE """ # Choose from the prompts shared in the prompts file
        }]
    )
    output = message.content
    return output

def extract_answers(result):
    # Remove newline characters from the input string
    result = result.replace('\n', '')

    # Remove wrongly escaped single quotes from the input string

    result = result.replace("\\'", "'")
    
    # Use regular expression to find all occurrences between <answer> and </answer>
    pattern = r'<answer>(.*?)</answer>'
    
    # Find all matches using re.findall
    answers = re.findall(pattern, result)
    
    return answers

results = []

for index, row in df.iterrows():
    try:
        passage = row['passage']
        question = row['question']
        
        # Select the inputs required for the prompt tested
        # correct_answer = row['correct_answer']
        # distractor1 = row['distractor1']
        # distractor2 = row['distractor2']
        # distractor3 = row['distractor3']
        # distractors = [distractor1, distractor2, distractor3]
        
        # Call the function that processes the passage and question
        result = find_type(passage, question, examples, api_key)
        
        # Convert the result to string and extract answers using the extract_answers function
        clean_result = extract_answers(str(result))
        
        # Print the extracted result for verification
        print(clean_result)
        
        # Append the cleaned result to the results list
        results.append({
            'index': index,
            'passage': passage,
            'question': question,
            'extracted_answers': clean_result
        })

    except Exception as e:
        # Handle any error and print an informative message along with the index
        print(f"An error occurred on row {index}: {str(e)}")
        continue  # Move to the next iteration in case of an error

# Save the results to a JSON file with error handling
try:
    with open('extracted_results.json', 'w') as json_file:
        json.dump(results, json_file, indent=4)
    print(f"Extracted results successfully saved to 'extracted_results.json'.")

except Exception as e:
    print(f"An error occurred while saving to JSON: {str(e)}")