from flask import Flask, request, jsonify, render_template
import os
import mysql.connector
import json
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables
load_dotenv()

# Connect to MySQL
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
a = """
 <script src="https://cdn.botpress.cloud/webchat/v2.3/inject.js"></script>
  <script src="https://files.bpcontent.cloud/2025/04/08/14/20250408140421-NE9U9VY9.js"></script>
  """
conn = connect_db()
cursor = conn.cursor(dictionary=True) if conn else None

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
@app.route('/contact', methods=['GET'])
def contact():
    return render_template('index.html')
@app.route('/search', methods=['GET'])
def search():
    return render_template('index.html')
@app.route('/books', methods=['GET'])
def books():
    return render_template('index.html')

@app.route('/chat', methods=['GET'])
def chat():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5100, debug=True)