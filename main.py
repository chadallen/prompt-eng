import openai
import psycopg2
import os

#Config some variables that you might like to turn the knobs on
generate_question_temperature = 0.2
generate_question_max_tokens = 50
generate_answer_temperature = 0.2
generate_answer_max_tokens = 50
rows_to_process = 10

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

# Function to generate a question using GPT-3.5-turbo
def generate_question(context, answer):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Create a question that would yield the answer given the context."},
            {"role": "user", "content": f"context: {context}\nanswer: {answer}"}
        ],
        temperature=generate_question_temperature,
        max_tokens=generate_question_max_tokens,
    )

    return response.choices[0].message['content'].strip()

# Function to generate an answer using GPT-3.5-turbo
def generate_answer(context, question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"context: {context}\nquestion: {question}"}
        ],
        temperature=generate_answer_temperature,
        max_tokens=generate_answer_max_tokens,
    )
    return response.choices[0].message['content'].strip()
    

# Fetch data from the database. We'll just get some random rows for now since we aren't planning to fetch the whole data set.
cursor.execute("SELECT id, paragraph, question, answer FROM squad_data order by random() LIMIT " + str(rows_to_process))
rows = cursor.fetchall()

# Generate questions and answers, and compare them with the original answers
for row in rows:
    record_id, context, original_question, original_answer = row
    generated_question = generate_question(context, original_answer)
    generated_answer = generate_answer(context, generated_question)
    # This is obviously not an actual good way to see if the answers really match
    answer_match = (generated_answer.lower() == original_answer.lower())

    # Cheap debugging
    print('context: ' + context)
    print('original question: ' + original_question)
    print('generated question: ' + generated_question)
    print('orignal answer: ' + original_answer)
    print('generated_answer: ' + generated_answer)  
    # print('answer match: ' + str(answer_match))
    print('~~~~~~~')
    
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
