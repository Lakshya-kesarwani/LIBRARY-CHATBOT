from flask import Flask, request, jsonify
import mysql.connector
import requests

app = Flask(__name__)
from dotenv import load_dotenv
load_dotenv()
import os
# Database Connection
conn = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    user='avnadmin',
    password=os.getenv('DB_PASSWORD'),
    database='chatbot_library',
    port=26060,
)
cursor = conn.cursor(dictionary=True)

# Dialogflow Webhook
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    intent = data['queryResult']['intent']['displayName']
    response_text = "I didn't understand that."

    if intent == "Show Available Books":
        cursor.execute("SELECT title, author, location FROM books WHERE availability = 'available'")
        books = cursor.fetchall()
        response_text = "Here are available books: " + ", ".join([f"{b['title']} by {b['author']} (Location: {b['location']})" for b in books])

    elif intent == "Recommend Book":
        cursor.execute("SELECT title, author FROM books ORDER BY RAND() LIMIT 1")
        book = cursor.fetchone()
        response_text = f"I recommend: {book['title']} by {book['author']}."
    
    return jsonify({"fulfillmentText": response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
