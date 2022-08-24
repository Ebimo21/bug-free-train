## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 


## Endpoints
## GET '/categories'
- General:
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category and its success value
    - Request Arguments: None
    - Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
- Sample: `curl http://127.0.0.1:5000/categories`

{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}

## GET '/questions'
- General:
    - Fetches a dictionary of questions with question, answer, difficulty, category and id as key and their corresponding values
    - Request Arguments: None
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
    - Returns: An object with keys categories, questions, total questions, current category and success
- Sample: `curl http://127.0.0.1:5000/questions`

{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": "Science",
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "status": true,
  "total_questions": 22
}


#### DELETE '/questions/{question_id}'
- Deletes the question of the given ID if it exists. Returns the id of the deleted book id, success value, total questions, and question list based on current page number to update the frontend. 
- Sample: `curl -X DELETE http://127.0.0.1:5000/questions/16?page=2`

{
  "deleted": 15,
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }
  ],
  "success": true,
  "total_questions": 20
}


#### POST '/questions'
- General: 
    - Searches for questions using a search term
    - Request Body: json object with searchTerm as `key` and search search string as `value`
    - Returns: An object with keys categories, questions, total questions, current category and success 
- Sample: `curl -X POST http://localhost:5000/questions -H "Content-Type:application/json" -d "{\"searchTerm\": \"first\"}"`

{
  "current_category": "Null",
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
  ],
  "success": true,
  "total_questions": 4
}


#### GET '/categories/{category_id}/questions'
- General: 
    - Fetches a dictionary of questions, success, and total questions
    - Request Parameter: None
    - Returns: An object with  questions, total questions, and success 
- Sample: `curl -X GET http://localhost:5000/categories/1/questions`

{
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    }
  ],
  "success": true,
  "total_questions": 3
}



#### GET '/quizzes'
- General: 
    - Fetches a dictionary of questions, success, and total questions
    - Request Parameter: None
    - Returns: An object with  questions, total questions, and success 
- Sample: `curl -X POST http://localhost:5000/quizzes -H "Content-Type:application/json" -d "{\"previous_questions\":[1], \"quiz_category\":{\"id\": \"1\"}}"`

{
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    }
  ],
  "success": true,
}



## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```





# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.
