from flask_sqlalachemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    xp = db.Column(db.Integer, default=0)
    level = db.Column(db.Integer, default=1)
    tasks = db.relationship('Task', backref='user', lazy=True)

    def add_xp(self, amount):
        self.xp += amount
        xp_needed = self.level * 100
        while self.xp >= xp_needed:
            self.xp -= xp_needed
            self.level += 1
            xp_needed = self.level * 100

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    difficulty = db.Column(db.Integer, default=1)  # 1: Easy, 2: Medium, 3: Hard
    completed = db.Column(db.Boolean, default=False)