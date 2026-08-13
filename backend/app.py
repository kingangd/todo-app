# 导入核心模块
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import db  # 导入同目录下的 db.py 文件

# 初始化Flask应用，并启用CORS
app = Flask(__name__)
CORS(app)

# 在模块导入时初始化数据库（保证在 gunicorn 等 WSGI 服务器下也会执行）
# init_db 使用 IF NOT EXISTS 创建表，所以多次调用是安全的
db.init_db()

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
# 静态文件：将 frontend 目录作为单页面应用静态资源一起托管
# 这样在 Render 上只需部署一个 Web Service，即可同时提供前端页面与后端 API
# --------------------------
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    # 如果请求的静态资源存在，就直接返回它；否则返回 index.html（支持 SPA 路由）
    if path and os.path.exists(os.path.join(FRONTEND_DIR, path)):
        return send_from_directory(FRONTEND_DIR, path)
    return send_from_directory(FRONTEND_DIR, 'index.html')


# --------------------------
# 程序入口（仅在本地直接运行时使用）
# 在 Render 或使用 gunicorn 部署时，gunicorn 会导入这个模块并运行 app
# --------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # 本地启动仍使用 debug 模式以便调试
    app.run(debug=True, host='0.0.0.0', port=port)
