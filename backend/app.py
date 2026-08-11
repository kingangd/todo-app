# 导入核心模块
from flask import Flask
from flask_cors import CORS
import db
# 创建Flask后端应用实例
app=Flask(__name__)
# 开启全局跨域，允许前端访问
CORS(app)

# 定义路由：浏览器访问地址+接口功能
@app.route('/')
def hello_world():
    return "helloworld"
# 启动后端服务
if __name__=='__main__':
    app.run(debug=True)