import os
from flask import Flask
from flask_sqlalachemy import SQLAlchemy


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///taskquest.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecretkey")

    db.init_app(app)

    with app.app_context():
        from routes.auth import auth_bp
        from routes.tasks import tasks_bp

        app.register_blueprint(auth_bp)
        app.register_blueprint(tasks_bp)

        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    tasks = db.relationship("Task", backref="user", lazy=True)

    def add_xp(self, amount):
        self.xp += amount
        xp_needed = self.level * 100
        while self.xp >= xp_needed:
            self.xp -= xp_needed
            self.level += 1
            xp_needed = self.level * 100


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    # 1: Easy, 2: Medium, 3: Hard
    difficulty = db.Column(db.Integer, default=1)
    intensity = db.Column(db.Integer, default=1)  # 1: Low, 2: Medium, 3: High
    completed = db.Column(db.Boolean, default=False)
