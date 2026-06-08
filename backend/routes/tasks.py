from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import db, User, Task
from math import floor

tasks_bp = Blueprint("tasks", __name__)

DIFFICULTY_XP: dict[int, int] = {  # XP rewards based on task difficulty
    1: 15,  # Easy
    2: 25,  # Medium
    3: 50,  # Hard
    4: 100,  # Very Hard
    5: 200,  # Extreme
    6: 300,  # Legendary
}

INTENSITY_MULTIPLIER: dict[int, float] = {  # XP multipliers based on task intensity
    1: 1.0,  # Low
    2: 1.5,  # Medium
    3: 2.0,  # High
    4: 2.5,  # Very High
    5: 3.0,  # Extreme
    6: 4.0,  # Legendary
}


@tasks_bp.route("", methods=["GET"])
def get_tasks():
    current_user_id = 1  # Hardcoded test user ID
    tasks = Task.query.filter_by(user_id=current_user_id).all()
    return (
        jsonify(
            [
                {
                    "id": t.id,
                    "title": t.title,
                    "difficulty": (
                        int(t.difficulty) if str(t.difficulty).isdigit() else 2
                    ),
                    "is_completed": t.is_completed,
                }
                for t in tasks
            ]
        ),
        200,
    )


@tasks_bp.route("/create", methods=["POST"])
def create_task():  # function to create a new task for the hardcoded test user
    current_user_id = 1
    data = request.get_json() or {}
    title = data.get("title", "").strip()
    try:
        difficulty_input = int(data.get("difficulty", 2))
        if difficulty_input < 1 or difficulty_input > 6:
            return (
                jsonify({"error": "Difficulty rating must scale between 1 and 6"}),
                400,
            )
    except (ValueError, TypeError):
        return jsonify({"error": "Difficulty must be a valid integer"}), 400
    if not title:
        return jsonify({"error": "Quest title is required"}), 400

    new_task = Task(user_id=current_user_id, title=title,
                    difficulty=difficulty_input)
    db.session.add(new_task)
    db.session.commit()

    return (
        jsonify(
            {
                "id": new_task.id,
                "title": new_task.title,
                "difficulty": new_task.difficulty,
                "is_completed": new_task.is_completed,
            }
        ),
        201,
    )


@tasks_bp.route("/tasks", methods=["POST"])
@jwt_required()
def create_task2():  # function to create a new task for the authenticated user
    user_id = get_jwt_identity()  # get user id from JWT token
    data = request.get_json()  # get task data from request body
    title = data.get("title")  # get task title from request data
    description = data.get(
        "description", ""
    )  # get task description from request data, default to empty string if not provided
    difficulty = data.get(
        "difficulty", 1
    )  # get task difficulty from request data, default to 1 (Easy) if not provided
    intensity = data.get(
        "intensity", 1
    )  # get task intensity from request data, default to 1 (Low) if not provided

    if not title:  # if title is not provided in request data, return error response
        return jsonify({"error": "Title is required"}), 400

    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        difficulty=difficulty,
        intensity=intensity,
    )  # add new task to database with provided data and user id
    db.session.add(task)
    db.session.commit()  # commit changes to database

    return (
        jsonify(
            {
                "message": "Task created successfully",
                "task": {  # return created task data in response
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


@tasks_bp.route("/<int:task_id>/complete", methods=["POST"])
def complete_task(
    task_id,
):  # function to mark a task as completed and reward XP to the user
    current_user_id = 1
    task = Task.query.filter_by(
        id=task_id, user_id=current_user_id).first_or_404()

    if task.is_completed:
        return jsonify({"error": "Quest already resolved!"}), 400

    user = db.session.get(User, current_user_id)
    rewards = floor(
        DIFFICULTY_XP.get(task.difficulty, 10)
        * INTENSITY_MULTIPLIER.get(task.intensity, 1.0)
    )

    task.is_completed = True
    leveled_up = user.add_xp(rewards)

    db.session.commit()

    return (
        jsonify(
            {
                "message": "Quest Complete!",
                "leveled_up": leveled_up,
                "user": {"level": user.level, "xp": user.xp},
            }
        ),
        200,
    )


@tasks_bp.route("/tasks/<int:task_id>/complete", methods=["POST"])
@jwt_required()
def complete_task2(
    task_id,
):  # function to mark a task as completed and reward XP to the user
    user_id = get_jwt_identity()  # get user id from JWT token
    task = Task.query.filter_by(
        id=task_id, user_id=user_id
    ).first()  # find task by id and user id in database

    if not task:  # if task is not found in database, return error response
        return jsonify({"error": "Task not found"}), 404

    if task.completed:  # if task is already completed, return error response
        return jsonify({"error": "Task already completed"}), 400

    task.completed = True  # set task as completed
    db.session.commit()

    user = User.query.get(user_id)  # find user by id in database
    xp_reward: int = floor(
        DIFFICULTY_XP.get(task.difficulty, 10)
        * INTENSITY_MULTIPLIER.get(task.intensity, 1.0)
    )  # calculate XP reward based on task difficulty and intensity, default to 10 XP for difficulty and 1.0 multiplier for intensity if not found in dictionaries
    user.add_xp(xp_reward)  # add XP to user based on calculated reward
    db.session.commit()

    return (
        jsonify({"message": "Task completed successfully", "xp_reward": xp_reward}),
        200,
    )  # return success response with XP reward for completing the task


@tasks_bp.route("/<int:task_id>/delete", methods=["DELETE"])
def delete_task(task_id):  # function to delete a task for the hardcoded test user
    current_user_id = 1
    task = Task.query.filter_by(
        id=task_id, user_id=current_user_id).first_or_404()

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Quest deleted successfully"}), 200


@tasks_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task2(task_id):  # function to delete a task for the authenticated user
    user_id = get_jwt_identity()  # get user id from JWT token
    task = Task.query.filter_by(
        id=task_id, user_id=user_id
    ).first()  # find task by id and user id in database

    if not task:  # if task is not found in database, return error response
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)  # delete task from database
    db.session.commit()  # commit changes to database

    return (
        jsonify({"message": "Task deleted successfully"}),
        200,
    )  # return success response
