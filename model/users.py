""" database dependencies to support sqliteDB examples """
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column(db.Text, unique=True, nullable=False)
    _fullname = db.Column(db.Text, unique=False, nullable=False)
    _password = db.Column(db.Text, unique=False, nullable=False)


    def __init__(self, username, fullname, password="letmein", grade=9):
        self._username = username
        self._fullname = fullname
        self.set_password(password)
        self._grade = grade

    @property
    def username(self):
        return self._username
    

    @username.setter
    def username(self, username):
        self._username = username
    

    @property
    def fullname(self):
        return self._fullname
    

    @fullname.setter
    def fullname(self, fullname):
        self._fullname = fullname
    
    @property
    def password(self):
        return self._password[0:5] + "..."


    def set_password(self, password):
        """Create a hashed password."""
        self._password = generate_password_hash(password, method='sha512')

    def is_password(self, password):
        """Check against hashed password."""
        result = check_password_hash(self._password, password)
        return result
    
    
    def __str__(self):
        return json.dumps(self.read())

    # Function to add new user entry to the table
    def create(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except IntegrityError:
            db.session.remove()
            return None

    # Function to read user from table, return id, username, and full name
    def read(self):
        return {
            "id": self.id,
            "username": self.username,
            "fullname": self.fullname
        }

    # Function to update a particular user entry, can use to change name, password, full-name etc.
    def update(self, username="", fullname="", password=""):
        """only updates values with length"""
        if len(username) > 0:
            self.username = username
        if len(fullname) > 0:
            self.fullname = fullname
        if len(password) > 0:
            self.set_password(password)
        db.session.commit()
        return self

    # delete a particular user entry
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None



# Builds working data for testing
def initUsers():
    """Create database and tables"""
    db.create_all()
    """Tester data for table"""
    u1 = User(username='eris29', fullname='Alexander Lu', password='Aevus!')
    u2 = User(username='testuser', fullname='test user', password='password')


    users = [u1, u2]

    """Builds sample user/note(s) data"""
    for user in users:
        try:
            user.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {user.uid}")