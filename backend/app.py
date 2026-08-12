# 导入核心模块
from flask import Flask, request, jsonify
from flask_cors import CORS
import db  # 导入同目录下的 db.py 文件

# 初始化Flask应用
app = Flask(__name__)
CORS(app)  # 解决跨域


# --------------------------
# 接口1：获取所有任务
# --------------------------
@app.route('/api/todos', methods=['GET'])
def get_todos():
    todo_list = db.get_all_todos()  # 调用db层的查询方法
    return jsonify(todo_list)


# --------------------------
# 接口2：新增任务
# --------------------------
@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.get_json()

    # 参数校验
    if not data or 'title' not in data or not data['title'].strip():
        return jsonify({'error': '任务标题不能为空'}), 400

    title = data['title'].strip()
    content = data.get('content', '').strip()
    deadline = data.get('deadline', '')

    # 调用db层新增方法
    new_id = db.insert_todo(title, content, deadline)

    return jsonify({
        'message': '任务创建成功',
        'id': new_id,
        'title': title
    }), 201


# --------------------------
# 接口3：更新任务
# --------------------------
@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': '更新参数不能为空'}), 400

    # 调用db层更新方法
    success = db.update_todo_by_id(todo_id, data)

    if not success:
        return jsonify({'error': '任务不存在或无有效更新字段'}), 404

    return jsonify({'message': '任务更新成功'})


# --------------------------
# 接口4：删除任务
# --------------------------
@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    success = db.delete_todo_by_id(todo_id)

    if not success:
        return jsonify({'error': '任务不存在'}), 404

    return jsonify({'message': '任务删除成功'})


# --------------------------
# 程序入口
# --------------------------
if __name__ == '__main__':
    db.init_db()  # 启动时调用db层的初始化函数
    app.run(debug=True, port=5000)
