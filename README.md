# SAT-reading
Files for the QC system for SAT reading

1. Getting AE studio data (for AlphaRead articles)
2. QC Prompts
3. Prompt testing & validation

## 1. Getting data through AE studio API
    ### Requirements:
    - A list of AE studio external IDs
    - API key

    ### Outputs:
    - Full article text
    - Each question, including guiding questions
    - Each correct answer
    - Each distractor

## 2. Prompts
   The question level prompts are provided together with few-shot examples.

## 3. Prompt testing & validation
   The code used to run a single prompt on a series of questions.
   ### Requirements:
   - Anthropic API key
   - Prompt library
   - .csv of questions with: passage, question, correct_answer, distractor1, distractor2, and distractor3 columns
  ### Outputs:
  - .json representation of the quality control results
