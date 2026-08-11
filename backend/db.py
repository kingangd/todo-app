import sqlite3
import os
# 建立数据库文件路径
DB_PATH=os.path.join(os.path.dirname(__file__),'todo.db')
# 建立与数据库的连接
def get_db_conn():
    conn=sqlite3.connect(DB_PATH)
    conn.row_factory=sqlite3.Row
    return conn

# 初始化数据库
def init_db():
    # 程序启动时调用
    conn=get_db_conn()
    cursor=conn.cursor()
    # 创建任务表的sql语句
    cursor.execute('''
        create table if not exists todos(
        id integer primary key autoincrement,
        title text not null,
        content text default '',
        deadline text,
        status integer default 0,
        create_time timestamp default current_timestamp
)
''')
    conn.commit()
    conn.close()
    print("数据库初始化完成，数据表已经就绪")