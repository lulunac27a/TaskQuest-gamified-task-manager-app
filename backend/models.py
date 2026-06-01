import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):  # user model with XP and level
    id = db.Column(db.Integer, primary_key=True)  # user id
    username = db.Column(db.String(80), unique=True,
                         nullable=False)  # username
    password_hash = db.Column(db.String(128), nullable=False)  # password hash
    xp = db.Column(db.Integer, default=0)  # user XP
    level = db.Column(db.Integer, default=1)  # user level
    tasks = db.relationship("Task", backref="user",
                            lazy=True)  # user tasks list

    def set_password(self, password):  # function to set user password
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):  # function to check user password
        return check_password_hash(self.password_hash, password)

    def add_xp(self, amount):  # function to add XP and level up if necessary
        self.xp += amount  # add XP to user
        xp_needed = self.level * 100  # XP needed to level up
        while self.xp >= xp_needed:  # check if user has enough XP to level up
            self.xp -= xp_needed  # subtract XP needed to level up from user XP
            self.level += 1  # increase user level
            xp_needed = self.level * 100  # update XP needed for next level


class Task(db.Model):  # task model with difficulty and intensity
    id = db.Column(db.Integer, primary_key=True)  # task id
    user_id = db.Column(db.Integer, db.ForeignKey(
        "user.id"), nullable=False)  # user id
    title = db.Column(db.String(120), nullable=False)  # task title
    description = db.Column(db.Text, nullable=True)  # task description
    difficulty = db.Column(db.Integer, default=1)  # task difficulty
    intensity = db.Column(db.Integer, default=1)  # task intensity
    is_completed = db.Column(db.Boolean, default=False)  # is task completed
