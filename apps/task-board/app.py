from flask import Flask, render_template, request, redirect, url_for
from models import db, Task, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


@app.route("/")
def index():
    tasks = Task.query.all()
    users = User.query.all()

    # Group users by type (children first, then adults)
    children_users = [user for user in users if user.user_type == "child"]
    adult_users = [user for user in users if user.user_type == "adult"]

    # Group tasks by user type and calculate completed points totals
    children_tasks = {}
    adult_tasks = {}
    children_points_total = {}
    adult_points_total = {}
    unassigned_tasks = []

    for task in tasks:
        # Skip completed tasks - don't show them on the board
        if task.status == "completed":
            continue

        if task.assigned_user:
            if task.assigned_user.user_type == "child":
                if task.assigned_user not in children_tasks:
                    children_tasks[task.assigned_user] = []
                    children_points_total[task.assigned_user] = 0
                children_tasks[task.assigned_user].append(task)
                if task.status == "completed":
                    children_points_total[task.assigned_user] += task.points or 0
            else:  # adult
                if task.assigned_user not in adult_tasks:
                    adult_tasks[task.assigned_user] = []
                    adult_points_total[task.assigned_user] = 0
                adult_tasks[task.assigned_user].append(task)
                if task.status == "completed":
                    adult_points_total[task.assigned_user] += task.points or 0
        else:
            unassigned_tasks.append(task)

    return render_template(
        "index.html",
        children_tasks=children_tasks,
        adult_tasks=adult_tasks,
        unassigned_tasks=unassigned_tasks,
        children_users=children_users,
        adult_users=adult_users,
        children_points_total=children_points_total,
        adult_points_total=adult_points_total,
    )


@app.route("/add", methods=["GET", "POST"])
def add_task():
    users = User.query.all()
    if request.method == "POST":
        title = request.form["title"]
        description = request.form.get("description", "")
        status = request.form.get("status", "pending")
        points = request.form.get("points", "0")
        points = int(points) if points.isdigit() else 0
        assigned_to = request.form.get("assigned_to")
        assigned_to = (
            int(assigned_to) if assigned_to and assigned_to.isdigit() else None
        )
        new_task = Task(
            title=title,
            description=description,
            status=status,
            points=points,
            assigned_to=assigned_to,
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add_task.html", users=users)


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        name = request.form["name"].strip()
        user_type = request.form.get("user_type", "adult")
        avatar = request.form.get("avatar", "")
        if name:
            new_user = User(name=name, user_type=user_type, avatar=avatar)
            db.session.add(new_user)
            db.session.commit()
        return redirect(url_for("index"))
    return render_template("add_user.html")


@app.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    users = User.query.all()
    if request.method == "POST":
        task.title = request.form["title"]
        task.description = request.form.get("description", "")
        task.status = request.form.get("status", "pending")
        points = request.form.get("points", "0")
        task.points = int(points) if points.isdigit() else 0
        assigned_to = request.form.get("assigned_to")
        task.assigned_to = (
            int(assigned_to) if assigned_to and assigned_to.isdigit() else None
        )
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit_task.html", task=task, users=users)


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
