from flask import Flask, jsonify, request, abort

app = Flask(__name__)
tasks = []
next_id = 1

@app.route('/')
def home():
    return 'hello world!'

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id: int):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        abort(404, description = 'task not found')
    return jsonify(task)

@app.route('/tasks/new', methods= ['POST'])
def create_task():
    global next_id
    if not request.json or 'description' not in request.json:
        abort(400, description= "the task needs a description!")
    new_task = {
        'id':  next_id,
        'description': request.json['description'],
        'status': False,
    }
    tasks.append(new_task)
    next_id += 1
    return jsonify(new_task), 201

@app.route('/tasks/delete/<int:task_id>', methods = ['DELETE'])
def delete_task(task_id: int):
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        abort(404, description = "task not found")
    tasks = next(t for t in tasks if t['id'] != task_id)
    return 201

@app.route ('/tasks/update/<int:task_id>')
def to_update_task(task_id: int):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        abort(404, description="task not found")
    data = request.json or {}
    task['description'] = data.get('description', task['description'])
    task['status'] = data.get('status', task['status'])
    return jsonify(task)

if __name__ == '__main__':
    app.run(debug=True)

