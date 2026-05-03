from flask import Flask, render_template, request, redirect, url_for
from models import db, Task, User

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tasks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)


def build_board_context():
    tasks = Task.query.all()
    users = User.query.all()

    # Group users by type (children first, then adults)
    children_users = [user for user in users if user.user_type == "child"]
    adult_users = [user for user in users if user.user_type == "adult"]

    # First, calculate points totals from ALL tasks (including completed ones)
    children_points_total = {}
    adult_points_total = {}

    for task in tasks:
        if task.assigned_user and task.status == "completed":
            if task.assigned_user.user_type == "child":
                if task.assigned_user not in children_points_total:
                    children_points_total[task.assigned_user] = 0
                children_points_total[task.assigned_user] += task.points or 0
            else:  # adult
                if task.assigned_user not in adult_points_total:
                    adult_points_total[task.assigned_user] = 0
                adult_points_total[task.assigned_user] += task.points or 0

    # Now group only NON-COMPLETED tasks for display
    children_tasks = {}
    adult_tasks = {}
    unassigned_tasks = []

    for task in tasks:
        # Skip completed tasks - don't show them on the board
        if task.status == "completed":
            continue

        if task.assigned_user:
            if task.assigned_user.user_type == "child":
                if task.assigned_user not in children_tasks:
                    children_tasks[task.assigned_user] = []
                children_tasks[task.assigned_user].append(task)
            else:  # adult
                if task.assigned_user not in adult_tasks:
                    adult_tasks[task.assigned_user] = []
                adult_tasks[task.assigned_user].append(task)
        else:
            unassigned_tasks.append(task)

    return {
        "children_tasks": children_tasks,
        "adult_tasks": adult_tasks,
        "unassigned_tasks": unassigned_tasks,
        "children_users": children_users,
        "adult_users": adult_users,
        "children_points_total": children_points_total,
        "adult_points_total": adult_points_total,
    }


@app.route("/")
def index():
    context = build_board_context()
    context["admin"] = False
    return render_template("index.html", **context)


@app.route("/admin/")
@app.route("/admin")
def admin_index():
    context = build_board_context()
    context["admin"] = True
    return render_template("index.html", **context)


@app.route("/admin/add", methods=["GET", "POST"])
def admin_add_task():
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
        return redirect(url_for("admin_index"))
    return render_template("add_task.html", users=users)


@app.route("/admin/add_user", methods=["GET", "POST"])
def admin_add_user():
    if request.method == "POST":
        name = request.form["name"].strip()
        user_type = request.form.get("user_type", "adult")
        avatar = request.form.get("avatar", "")
        if name:
            new_user = User(name=name, user_type=user_type, avatar=avatar)
            db.session.add(new_user)
            db.session.commit()
        return redirect(url_for("admin_index"))
    return render_template("add_user.html")


@app.route("/admin/edit/<int:task_id>", methods=["GET", "POST"])
def admin_edit_task(task_id):
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
        return redirect(url_for("admin_index"))
    return render_template("edit_task.html", task=task, users=users)


@app.route("/admin/delete/<int:task_id>")
def admin_delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("admin_index"))


@app.route("/admin/reset_all")
def admin_reset_all():
    # Delete all tasks
    Task.query.delete()

    # Reset all users' points to 0 (though we don't actually store points on users,
    # this is just in case we add that feature later)
    # For now, this just deletes all tasks which effectively resets everything

    db.session.commit()
    return redirect(url_for("admin_index"))


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
