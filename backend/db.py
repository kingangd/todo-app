import sqlite3
import os

# 数据库文件路径（和当前文件同目录）
DB_PATH = os.path.join(os.path.dirname(__file__), 'todo.db')


# --------------------------
# 工具：获取数据库连接
# --------------------------
def get_db_conn():
    """创建数据库连接，查询结果自动转为字典格式"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# --------------------------
# 1. 初始化数据库（建表）
# --------------------------
def init_db():
    """程序启动时调用，自动创建数据表"""
    conn = get_db_conn()
    cursor = conn.cursor()

    # 创建任务表的SQL语句
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT DEFAULT '',
            deadline TEXT,
            status INTEGER DEFAULT 0,
            create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()
    print("✅ 数据库初始化完成，数据表已就绪")


# --------------------------
# 2. 查询：获取所有任务
# --------------------------
def get_all_todos():
    """查询所有任务，按创建时间倒序返回列表"""
    conn = get_db_conn()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM todos ORDER BY create_time DESC')
    todo_list = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return todo_list


# --------------------------
# 3. 新增：插入一条任务
# --------------------------
def insert_todo(title, content, deadline):
    """插入新任务，返回新任务的ID"""
    conn = get_db_conn()
    cursor = conn.cursor()

    cursor.execute(
        'INSERT INTO todos (title, content, deadline) VALUES (?, ?, ?)',
        (title, content, deadline)
    )

    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


# --------------------------
# 4. 更新：根据ID修改任务
# --------------------------
def update_todo_by_id(todo_id, update_data):
    """
    根据ID更新任务
    :param todo_id: 任务ID
    :param update_data: 字典，可包含 title、content、deadline、status
    :return: True=更新成功，False=任务不存在
    """
    conn = get_db_conn()
    cursor = conn.cursor()

    # 先检查任务是否存在
    cursor.execute('SELECT id FROM todos WHERE id = ?', (todo_id,))
    if not cursor.fetchone():
        conn.close()
        return False

    # 动态拼接要更新的字段
    fields = []
    values = []
    for key in ['title', 'content', 'deadline', 'status']:
        if key in update_data:
            fields.append(f'{key} = ?')
            values.append(update_data[key])

    if not fields:
        conn.close()
        return False

    # 拼接SQL并执行
    sql = f"UPDATE todos SET {', '.join(fields)} WHERE id = ?"
    values.append(todo_id)
    cursor.execute(sql, values)

    conn.commit()
    conn.close()
    return True


# --------------------------
# 5. 删除：根据ID删除任务
# --------------------------
def delete_todo_by_id(todo_id):
    """
    根据ID删除任务
    :return: True=删除成功，False=任务不存在
    """
    conn = get_db_conn()
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM todos WHERE id = ?', (todo_id,))
    if not cursor.fetchone():
        conn.close()
        return False

    cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
    conn.commit()
    conn.close()
    return True
