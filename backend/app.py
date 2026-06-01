def create_app():  # function to create and configure the Flask app
    app = Flask(__name__)  # create Flask app instance
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///taskquest.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecretkey")

    db.init_app(app)  # initialize database with app context
    JWTManager(app)  # initialize JWT manager with app context
    CORS(app)  # enable CORS for all routes

    with app.app_context():
        from routes.auth import auth_bp
        from routes.tasks import tasks_bp

        # register blueprints for authentication and task management routes
        app.register_blueprint(auth_bp)
        app.register_blueprint(
            tasks_bp, url_prefix="/api/tasks"
        )  # prefix task routes with /api

        db.create_all()  # create database tables
        # Seed a test user if none exists
        if not User.query.get(1):  # check if test user with id 1 exists in database
            test_user = User(
                id=1, username="TestHero", xp=0, level=1, gold=100
            )  # create test user with default values
            test_user.set_password("password123")  # set password for test user
            db.session.add(test_user)  # add test user to database session
            db.session.commit()  # commit changes to database
            print("📦 Test user generated successfully.")
    return app


if __name__ == "__main__":
    app = create_app()  # create app instance
    app.run(
        host="127.0.0.1", port=5000, debug=True
    )  # run app on localhost with debug mode enabled
