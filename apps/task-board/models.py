from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(
        db.String(20), default="pending"
    )  # pending, in_progress, completed
    assigned_to = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)
    assigned_user = db.relationship("User", backref="tasks")
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    avatar = db.Column(db.String(10), nullable=True)  # Store emoji or short code
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
