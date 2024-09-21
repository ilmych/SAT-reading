import requests
import pandas as pd

# Define the base URL and API key
BASE_URL = 'https://alpha-content-api-production-28c7519a08f9.herokuapp.com/articles/'
API_KEY = 'AE Studio API Key' # Edit with your API key

# Load the CSV file with article IDs
df = pd.read_csv('path_to_file.csv')  # Edit with the exact file path that includes a list of AE studio IDs 

# Call the fetch_article endpoint
def get_article_data(article_id):
    url = f"{BASE_URL}{article_id}?parsed=false"
    headers = {
        'accept': 'application/json',
        'X-API-Key': API_KEY
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data for article ID {article_id}: {response.status_code}")
        return None

# Extract question data from the response
def extract_questions(data):
    questions = data.get('questions', [])
    for section in data.get('sections', []):
        questions.extend(section.get('questions', []))
    return questions

#Extract article text, all questions, correct answers and distractors separately
def process_article(article_data):
    if not article_data:
        return None

    content = " ".join(section.get('content', '') for section in article_data.get('sections', []))
    questions = extract_questions(article_data)

    processed_data = []
    for q in questions:
        correct_answer = next((a['_title'] for a in q['answers'] if a['is_correct']), "")
        incorrect_answers = [a['_title'] for a in q['answers'] if not a['is_correct']]
        processed_data.append({
            'ID': article_data['external_id'],
            'passage': content,
            'question': q['_title'],
            'correct_answer': correct_answer,
            'distractor1': incorrect_answers[0] if len(incorrect_answers) > 0 else '',
            'distractor2': incorrect_answers[1] if len(incorrect_answers) > 1 else '',
            'distractor3': incorrect_answers[2] if len(incorrect_answers) > 2 else ''
        })

    return processed_data

# Create a list to store the results
results = []

# Iterate over each article ID in the DataFrame
for index, row in df.iterrows():
    article_id = row['ID']
    article_data = get_article_data(article_id)
    processed_data = process_article(article_data)
    if processed_data:
        results.extend(processed_data)

# Create a new DataFrame from the results
results_df = pd.DataFrame(results)

# Save the results to a new CSV file
results_df.to_csv('full_article_content.csv', index=False)
print("CSV file saved successfully.")
