from loginandregistration_app.config.mysqlconnection import connectToMySQL
from loginandregistration_app import app
from flask import flash, session

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
USER_REGEX = re.compile()

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

class Login:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.age = data['age']
        self.password = data['password']

    @staticmethod
    def register_validation(data):
        is_valid = True
        user = Login.get_by_email(data)
        if len(user) > 0:
            flash("Email already taken.")
            is_valid=False
        if not EMAIL_REGEX.match(data['email']):
            flash("Please provide a valid email address.","register")
            is_valid=False
        if len(data['first_name']) <2:
            flash("First name should include more than 2 characters.","register")
            is_valid=False
        if len(data['last_name']) <2:
            flash("Last name should include more than 2 characters.","register")
            is_valid=False
        if data['age'] == "None":
            flash("Please select a valid age range.","register")
            is_valid=False
        if len(data['password']) < 8:
            flash("Password should include more than 8 characters.","register")
            is_valid=False
        if data['password'] != data['password_confirmation']:
            flash("Passwords do not match, please review.","register")
            is_valid=False
        return is_valid

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM core_users WHERE email = %(email)s;"
        results = connectToMySQL('mydb').query_db(query,data)
        user = []
        for line in results:
            user.append(Login(line))
        return user

    @staticmethod
    def login_validation(data):
        is_valid = True
        user = Login.get_by_email(data)
        if len(user) < 1:
            flash("Email not valid.","login")
            is_valid=False
        elif not bcrypt.check_password_hash(user[0].password, data['password']):
            flash("Incorrect password, please try again.","login")
            is_valid=False
        else:
            session['userid'] = user[0].id
        return is_valid
        

    @classmethod
    def register(cls,data):
        query = "INSERT INTO core_users (first_name,last_name,age,email,password) VALUES (%(first_name)s,%(last_name)s,%(age)s,%(email)s,%(password)s);"
        results = connectToMySQL('mydb').query_db(query,data)
        return results

    @classmethod
    def getsubmission(cls,id):
        query = "SELECT * FROM core_users WHERE id = %(id)s"
        data = {
            'id' : id
        }
        results = connectToMySQL('mydb').query_db(query,data)
        submissions = []
        for line in results:
            submissions.append(Login(line))
        return submissions