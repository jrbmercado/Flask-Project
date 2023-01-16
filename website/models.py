# This is where we create database models

# Import the database object from __init__.py
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    # Gets current date and time for default value for date
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    # All of our notes must belong to a user, so we need to make a relationship between note and user objects using foreign keys
    # A column in database that always a column that belongs to a different database
    # We match the same type, 1 to many relationship between 1 user and many notes
    # Foreignkey is looking for a valid user.id in order for us to create a Note entry. REQUIRES LOWERCASE IN FOREIGNKEY
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    # Define schema for database
    # Primary key that will be unique for each user
    id = db.Column(db.Integer, primary_key=True)
    # No user is allowed to have an email that already exists
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))  # Max len is 150 for password
    first_name = db.Column(db.String(150))  # Max len is 150 for name
    # Everytime we create a note, add the note ID to a list that stores all this user's notes. REQUIRES CAPITAL
    notes = db.relationship('Note')
