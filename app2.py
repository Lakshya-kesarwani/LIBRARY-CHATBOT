from flask import Flask, request, jsonify, render_template
import os
import mysql.connector
import json
from dotenv import load_dotenv
import requests
import google.generativeai as genai
# from code2 import ask_model
from gemini_api import ask_model
app = Flask(__name__)

def connect_db():
    try:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user='avnadmin',
            password=os.getenv('DB_PASSWORD'),
            database='chatbot_library',
            port=26060
        )
        print("✅ Database connected successfully!")
        return conn
    except mysql.connector.Error as err:
        print(f"❌ Database connection error: {err}")
        return None

def query_prompt_generator(user_prompt: str) -> str:
    """Generates schema-aware prompt for SQL generation"""
    schema_description = """
    Database Schema:
    - users (user_id, full_name, role, email, phone_number, password)
    - books_details (book_id, title, genre, author, publication, description, keywords)
    - book_meta (book_id, isbn, ddc, floor, quantity, status)
    - user_books (issue_id, user_id, book_id, issue_date, return_date, status)
    - faqss (faq_id, query, response)
    
    Relationships:
    - user_books.user_id → users.user_id
    - user_books.book_id → books_details.book_id
    - book_meta.book_id → books_details.book_id
    """
    
    return f"""
    You are a SQL expert. Convert this natural language query to PostgreSQL.
    Use ONLY these tables/columns. Never invent new fields.
    Return ONLY SQL code, no explanations.
    
    Schema:
    {schema_description}
    
    User query: "{user_prompt}"
    
    Important:
    - status could be any of these ('av','nav','borrowed')
    - Use CAST() for date comparisons
    - Use ILIKE for text searches
    - Never return passwords
    - Limit to 5 results unless specified
    """

def response_generator(results: list, original_query: str) -> str:
    """Converts raw SQL results to natural language"""
    return f"""
    Convert these database results to friendly response:
    Original query: "{original_query}"
    Data: {results}
    
    Guidelines:
    1. Use simple, conversational language
    2. Highlight key numbers/statistics
    3. Format dates as 'April 15, 2024'
    4. For book searches, show title/author/floor
    5. Mask email addresses (e.g: p***@gmail.com)
    """
    
conn = connect_db()
cursor = conn.cursor(dictionary=True) if conn else None


@app.route('/')
def index():
    return render_template('index.html')
queries =""
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        if not request.data:
            print("❌ No request data received!")
            return jsonify({"fulfillmentText": "No request data received."})

        raw_data = request.data.decode('utf-8')
        req = json.loads(raw_data)
        intent = req.get('queryResult', {}).get('intent', {}).get('displayName', "")
        prompt = req.get('queryResult', {}).get('queryText', "")

        response_query  = ask_model(query_prompt_generator(prompt))
        queries = response_query[6:-4]
        print(queries)
        results = cursor.execute(queries)
        results = cursor.fetchall()
        print(f"Results: {results}")
        user_response = ask_model(response_generator(results, prompt))

        return jsonify({"fulfillmentText":user_response})
    
    except json.JSONDecodeError as e:
        print(f"❌ JSON Decode Error: {e}")
        return jsonify({"fulfillmentText": "Error parsing JSON request."})

    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        return jsonify({"fulfillmentText": "An unexpected error occurred."})


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)