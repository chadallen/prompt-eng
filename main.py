import openai
import psycopg2
import os

# Set up the OpenAI API client
openai.api_key = os.environ['openai_key']

# Connect to the PostgreSQL database
connection = psycopg2.connect(
    host=os.environ['PGHOST'],
    database=os.environ['PGDATABASE'],
    user=os.environ['PGUSER'],
    password=os.environ['PGPASSWORD']
)

cursor = connection.cursor()

# Function to generate a question using ChatGPT-3
def generate_question(context, answer):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Create a question that would yield the answer '{answer}' given the following context:\n\n{context}\n\nQuestion:",
        temperature=0.8,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"],
    )

    return response.choices[0].text.strip()

# Function to generate an answer using ChatGPT-3
def generate_answer(context, question):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"{context}\n\nQuestion: {question}\nAnswer:",
        temperature=0.8,
        max_tokens=100,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=["\n"],
    )
   
    return response.choices[0].text.strip()
    

# Fetch data from the database
cursor.execute("SELECT id, paragraph, question, answer FROM squad_data LIMIT 10")
rows = cursor.fetchall()

# Generate questions and answers, and compare them with the original answers
for row in rows:
    record_id, context, original_question, original_answer = row
    generated_question = generate_question(context, original_answer)
    generated_answer = generate_answer(context, generated_question)
    answer_match = (generated_answer.lower() == original_answer.lower())
    print('context: ' + context)
    print('original question: ' + original_question)
    print('generated question: ' + generated_question)
    print('orignal answer: ' + original_answer)
    print('generated_answer: ' + generated_answer)  
    print('answer match: ' + answer_match)
    print('---------')
    
    # Update the generated_question, generated_answer, and answer_match columns in the database
    cursor.execute("""
        UPDATE squad_data
        SET generated_question = %s,
            generated_answer = %s,
            answer_match = %s
        WHERE id = %s
    """, (generated_question, generated_answer, answer_match, record_id))

connection.commit()

# Close the cursor and connection
cursor.close()
connection.close()
