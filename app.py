from flask import Flask, render_template, request, redirect
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# create flask app
app = Flask(__name__)
Scss(app)

# configure data base
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

# create data base
db = SQLAlchemy(app)

# data class
class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String, nullable = False)
    complete = db.Column(db.Integer, default = 0)
    created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str:
        return f"Task: {self.id}"

# for navigation: "/" cause home page
@app.route("/", methods = ["POST","GET"])

# what in the home page
def index():
    # add task
    if request.method == "POST":
        current_task = request.form["content"]
        new_task = Task(content = current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"

    # see currents tasks
    else:
        tasks = Task.query.order_by(Task.created).all()
        return render_template("index.html", tasks = tasks)

# delete task
@app.route("/delete/<int:id>")
def delete(id:int):
    delete_task = Task.query.get_or_404(id)

    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"Error :{e}")
        return f"Error: {e}"

# update task
@app.route("/edit/<int:id>", methods=["POST","GET"])
def edit(id:int):
    task = Task.query.get_or_404(id)

    if request.method == "POST":
        task.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"Error: {e}")
            return f"Error: {e}"
    else:
        return render_template("edit.html", task = task)








# to run the app
if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)


