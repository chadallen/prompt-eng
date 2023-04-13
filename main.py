import json
import requests
import psycopg2
from psycopg2 import OperationalError
import openai

# Set your OpenAI API key
openai.api_key = "your_openai_api_key"

def generate_gpt_chat_prompt(paragraph, question, answer):
    # (same as before)

def generate_gpt_answer(context, gpt_chat_prompt):
    # (same as before)

def compare_answers(original_answer, gpt_generated_answer):
    # (same as before)

# Set the number of articles to process
num_articles_to_process = 10

# Set the number of records to download
num_records_to_download = 50

# Connect to PostgreSQL database
try:
    connection = psycopg2.connect(
        host='localhost',
        user='your_username',
        password='your_password',
        dbname='squad'
    )

    cursor = connection.cursor()

    # Retrieve dev set articles and their questions (limited by num_records_to_download)
    cursor.execute("SELECT a.id, p.id, q.id, p.context, q.question, an.text, an.answer_start FROM articles a JOIN paragraphs p ON a.id = p.article_id JOIN questions q ON p.id = q.paragraph_id JOIN answers an ON q.id = an.question_id WHERE a.is_dev_set = 1 LIMIT %s", (num_records_to_download,))
    data = cursor.fetchall()

    # Generate GPT-chat prompts and store them in the database
    for record in data:
        article_id, paragraph_id, question_id, context, question, answer_text, answer_start = record
        answer = {"text": answer_text, "answer_start": answer_start}

        gpt_chat_prompt = generate_gpt_chat_prompt(context, question, answer)

        cursor.execute("INSERT INTO gpt_chat_prompts (prompt, question_id) VALUES (%s, %s)", (gpt_chat_prompt, question_id))
        connection.commit()

    # Retrieve dev set articles, their questions, GPT-chat prompts, and answers (limited by num_articles_to_process)
    cursor.execute("SELECT a.id, p.id, q.id, p.context, q.question, an.text, an.answer_start, gcp.prompt FROM articles a JOIN paragraphs p ON a.id = p.article_id JOIN questions q ON p.id = q.paragraph_id JOIN answers an ON q.id = an.question_id JOIN gpt_chat_prompts gcp ON q.id = gcp.question_id WHERE a.is_dev_set = 1 LIMIT %s", (num_articles_to_process,))
    data = cursor.fetchall()

    # Generate GPT answers and store them in the database
    for record in data:
        article_id, paragraph_id, question_id, context, question, answer_text, answer_start, gpt_chat_prompt = record

        gpt_generated_answer = generate_gpt_answer(context, gpt_chat_prompt)

        cursor.execute("INSERT INTO gpt_generated_answers (answer, question_id) VALUES (%s, %s)", (gpt_generated_answer, question_id))
        connection.commit()

    # Retrieve dev set articles, their questions, GPT-chat prompts, and answers (limited by num_articles_to_process)
    cursor.execute("SELECT a.id, p.id, q.id, p.context, q.question, an.text, an.answer_start, gcp.prompt, gga.answer FROM articles a JOIN paragraphs p ON a.id = p.article_id JOIN questions q ON p.id = q.paragraph_id JOIN answers an ON q.id = an.question_id JOIN gpt_chat_prompts gcp ON q.id = gcp.question_id JOIN gpt_generated_answers gga ON q.id = gga.question_id WHERE a.is_dev_set = 1 LIMIT %s", (num_articles_to_process,))
  
data = cursor.fetchall()

    # Compare GPT-generated answers with original answers and store the comparisons in the database
    for record in data:
        article_id, paragraph_id, question_id, context, question, answer_text, answer_start, gpt_chat_prompt, gpt_generated_answer = record

        is_match = compare_answers(answer_text, gpt_generated_answer)

        cursor.execute("INSERT INTO answer_comparisons (is_match, question_id) VALUES (%s, %s)", (is_match, question_id))
        connection.commit()

except OperationalError as e:
    print(f"The error '{e}' occurred")

finally:
    if connection:
        cursor.close()
        connection.close()