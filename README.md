# Library Chatbot API  

## Overview  
This is a Flask-based chatbot API for retrieving book details from a MySQL database. The chatbot can handle various user queries such as finding books by genre, author, ISBN, availability, and book status.  

## Features  
- Retrieve available books.  
- Find books by genre, author, or ISBN.  
- Check book availability and status.  
- Handles multiple values for query parameters.  
- ia deployed on render
   - ```bash
     https://library-chatbot-eprk.onrender.com/
     ```
## Setup Instructions  

### Prerequisites  
- Python 3.x  
- MySQL database  
- `pip install -r requirements.txt` (ensure dependencies are installed)  

### Configuration  
1. Create a `.env` file and add your MySQL database credentials:  
   ```env
   DB_HOST=your_host
   DB_PASSWORD=your_password
   ```  
2. Ensure the `BOOK_DETAILS` table exists in your MySQL database.  

### Running the Application  
Start the Flask server:  
```bash
python app.py
```  

## API Endpoints  

### `POST /webhook`  
Handles chatbot queries and returns relevant book details.  

### Request Format  
```json
{
  "queryResult": {
    "parameters": {
      "genre": ["Fiction", "Sci-Fi"],
      "author": ["Author Name"],
      "isbn": ["1234567890"],
      "availability": ["y"],
      "book_status": ["new"]
    }
  }
}
```  

### Response Format  
```json
{
  "fulfillmentText": "Books by these parameters: Book1, Book2"
}
```  

## Query Optimization  
- The chatbot dynamically builds SQL queries based on provided parameters.  
- Supports multiple values for each parameter using `IN` clauses.  
- Ensures efficient data retrieval with proper indexing in MySQL.  

## Error Handling  
- Returns appropriate responses if the database connection fails.  
- Handles missing or incorrect parameters gracefully.  
- Provides meaningful error messages for unexpected issues.  

## Future Enhancements  
- Add more book recommendation features.  
- Integrate NLP for better user interaction.  
- Improve response formatting.  

---
