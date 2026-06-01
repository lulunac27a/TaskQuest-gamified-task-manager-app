import os
from flask import Flask
from flask_sqlalachemy import SQLAlchemy


def create_app():  # function to create and configure the Flask app
    app = Flask(__name__)  # create Flask app instance
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///taskquest.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecretkey")

    db.init_app(app)  # initialize database with app context

    with app.app_context():
        from routes.auth import auth_bp
        from routes.tasks import tasks_bp

        # register blueprints for authentication and task management routes
        app.register_blueprint(auth_bp)
        app.register_blueprint(tasks_bp)

        db.create_all()  # create database tables

    return app


if __name__ == "__main__":
    app = create_app()  # create app instance
    app.run(
        host="127.0.0.1", port=5000, debug=True
    )  # run app on localhost with debug mode enabled


class User(db.Model):  # user model with XP and level
    id = db.Column(db.Integer, primary_key=True)  # user id
    username = db.Column(db.String(80), unique=True,
                         nullable=False)  # username
    xp = db.Column(db.Integer, default=0)  # user XP
    level = db.Column(db.Integer, default=1)  # user level
    tasks = db.relationship("Task", backref="user",
                            lazy=True)  # user tasks list

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
    completed = db.Column(db.Boolean, default=False)  # is task completed
