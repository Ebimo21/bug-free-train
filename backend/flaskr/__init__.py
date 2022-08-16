import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import logging
import json
from logging import Formatter, FileHandler

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
      return response
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
 
  @app.route('/categories')
  def get_all_categories():
      
      # categories = Category.query.all()

      # obj_str ="{"

      # for category in categories:
      #     obj_str += f'"{category.id}" : "{category.type}", '

      # obj_str += "}"
      # obj_str =obj_str[0:len(obj_str)-3]
      # obj_str +="}"
      # formatted_categories = json.loads(obj_str)
      formatted_categories = {category.id : category.type  for category in categories}

      return jsonify({
        'categories': formatted_categories,
      })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  @app.route('/questions')
  def get_all_questions():
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * 10
      end = start + QUESTIONS_PER_PAGE
    
      questions = Question.query.all()
      categories = Category.query.all()

      formatted_questions = [question.format() for question in questions]
      formatted_categories = {category.id : category.type  for category in categories}

      # obj_str ="{"

      # for category in categories:
      #   obj_str += f'"{category.id}" : "{category.type}", '

      # obj_str += "}"
      # obj_str =obj_str[0:len(obj_str)-3]
      # obj_str +="}"
      # formatted_categories = json.loads(obj_str)

      return jsonify({
        'questions': formatted_questions[start:end],
        'total_questions': len(formatted_questions),
        'categories': formatted_categories,
        'current_category': "Null",
      })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_a_category(question_id):
      
      item = Question.query.get(question_id)
      item.delete()

      return jsonify({
        'status': "success",
      })


  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions/new', methods=['POST'])
  def create_new_question():
    req = request.get_json()

    question = Question(question=req['question'],
                        answer=req['answer'],
                        difficulty=req['difficulty'],
                        category=req['category'])
    question.insert()
    return jsonify({
        'status': "success",
      }) 

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods=['POST'])
  def search_all_questions():
      search_q = request.get_json()
      # selection = Question.query.order_by(Book.id).filter(or_(Book.title.ilike('%{}%'.format(search)), Book.author.ilike('%{}%'.format(search))))
      questions =  db.session.query(Question).filter(Question.question.ilike(f'%{search_q["searchTerm"]}%')).all()

      start = 0
      end = start + QUESTIONS_PER_PAGE
    
      formatted_questions = [question.format() for question in questions]

      return jsonify({
        'questions': formatted_questions[start:end],
        'total_questions': len(formatted_questions),
        'current_category': "Null",
      })


  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:cat_id>/questions')
  def get_a_category(cat_id):
      # page = request.args.get('page', 1, type=int)
      start = 0
      end = start + QUESTIONS_PER_PAGE
    
      
      categories = Category.query.get(cat_id)
      questions = Question.query.filter(Question.category==categories.id).all()
      formatted_questions = [question.format() for question in questions]

      # obj_str ="{"
      # obj_str += "}"
      # obj_str =obj_str[0:len(obj_str)-3]
      # obj_str +="}"
      # formatted_categories = json.loads(obj_str)

      return jsonify({
        'questions': formatted_questions[start:end],
        'total_questions': len(formatted_questions),
        'current_category': "Null",
      })
  

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=["POST"])
  def get_quiz():
    req= request.get_json()
    prev = req['previous_questions']
    category = req['quiz_category']
    
    questions = Question.query.filter(Question.category==category['id']).all()
    formatted_questions = [question.format() for question in questions]
    val = formatted_questions
    past = prev
    count = 0
    for x in past:
      num =0 
      for y in val:
        if y['id'] == past[count]:
          del val[num]
        num +=1
      count +=1
    
    rand = random.randint(0,len(val)-1)
  
    return jsonify({
  'question': val[rand]
  })
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    