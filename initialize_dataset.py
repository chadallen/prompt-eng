import requests
import psycopg2
import os

# Download the SQuAD dataset
train_url = 'https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v1.1.json'
dev_url = 'https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json'

response_train = requests.get(train_url)
response_dev = requests.get(dev_url)

train_data = response_train.json()
dev_data = response_dev.json()

# Connect to PostgreSQL and create the table
connection = psycopg2.connect(
    host=os.environ['PGHOST'],
    database=os.environ['PGDATABASE'],
    user=os.environ['PGUSER'],
    password=os.eviron['PGPASSWORD']
)

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE squad_data (
        id SERIAL PRIMARY KEY,
        title TEXT NOT NULL,
        paragraph TEXT NOT NULL,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        answer_start INTEGER NOT NULL,
        is_training BOOLEAN NOT NULL,
        generated_question TEXT,
        generated_answer TEXT,
        answer_match BOOLEAN
    )
""")
connection.commit()

# Function to insert data into the database
def insert_data(data, is_training):
    for article in data['data']:
        title = article['title']
        for paragraph in article['paragraphs']:
            context = paragraph['context']
            for qa in paragraph['qas']:
                question = qa['question']
                for answer in qa['answers']:
                    answer_text = answer['text']
                    answer_start = answer['answer_start']
                    cursor.execute("""
                        INSERT INTO squad_data (title, paragraph, question, answer, answer_start, is_training)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (title, context, question, answer_text, answer_start, is_training))
    connection.commit()

# Insert the data
insert_data(train_data, True)
insert_data(dev_data, False)

# Close the cursor and connection
cursor.close()
connection.close()
