from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return f'<Task {self.id}: {self.content}>'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        if not task_content:
            return "Задача не может быть пустой! Пожалуйста, введите что-нибудь.", 400
        try:
            new_task = Task(content=task_content)
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"Произошла ошибка при добавлении задачи: {e}", 500
    else:
        tasks = Task.query.order_by(Task.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/add_task_page')
def add_task_page():
    return render_template('add_task.html')

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Произошла ошибка при удалении задачи: {e}", 500

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Task.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"Произошла ошибка при обновлении задачи: {e}", 500
    else:
        return render_template('update.html', task=task)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
