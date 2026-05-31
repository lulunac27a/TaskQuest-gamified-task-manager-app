from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, User, Task
from math import floor

tasks_bp = Blueprint("tasks", __name__)

DIFFICULTY_XP = {
    1: 15,  # Easy
    2: 25,  # Medium
    3: 50,  # Hard
    4: 100,  # Very Hard
    5: 200,  # Extreme
    6: 300,  # Legendary
}

INTENSITY_MULTIPLIER = {
    1: 1.0,  # Low
    2: 1.5,  # Medium
    3: 2.0,  # High
    4: 2.5,  # Very High
    5: 3.0,  # Extreme
    6: 4.0,  # Legendary
}


@tasks_bp.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    user_id = get_jwt_identity()
    data = request.get_json()
    title = data.get("title")
    description = data.get("description", "")
    difficulty = data.get("difficulty", 1)
    intensity = data.get("intensity", 1)

    if not title:
        return jsonify({"error": "Title is required"}), 400

    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        difficulty=difficulty,
        intensity=intensity,
    )
    db.session.add(task)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Task created successfully",
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "difficulty": task.difficulty,
                    "intensity": task.intensity,
                    "completed": task.completed,
                },
            }
        ),
        201,
    )


@tasks_bp.route("/tasks/<int:task_id>/complete", methods=["POST"])
@jwt_required()
def complete_task(task_id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=task_id, user_id=user_id).first()

    if not task:
        return jsonify({"error": "Task not found"}), 404

    if task.completed:
        return jsonify({"error": "Task already completed"}), 400

    task.completed = True
    db.session.commit()

    user = User.query.get(user_id)
    xp_reward = floor(
        DIFFICULTY_XP.get(task.difficulty, 10)
        * INTENSITY_MULTIPLIER.get(task.intensity, 1.0)
    )
    user.add_xp(xp_reward)
    db.session.commit()

    return (
        jsonify({"message": "Task completed successfully", "xp_reward": xp_reward}),
        200,
    )
