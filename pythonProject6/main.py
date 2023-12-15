import os
from flask import Flask, request, jsonify, render_template, redirect, url_for, send_file,send_from_directory
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # 使用 SQLite 数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
root_path = './'
db = SQLAlchemy(app)
# 定义模型
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    
class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)

# pythonCopy codeimport os
# 设置文件的读写权限
# os.chmod('./', 0o777)
folder_path = os.path.abspath(root_path)
# ... 其他路由和函数 ...

# 示例：插入数据接口
@app.route('/insert_message', methods=['POST'])
def insert_message():
    data = request.get_json()
    username = data.get('username', '')
    message = data.get('message', '')

    if username and message:
        new_message = Message(username=username, message=message)
        db.session.add(new_message)
        db.session.commit()
        response = {'message': '数据插入成功'}
    else:
        response = {'message': '请提供有效的用户名和消息'}

    return jsonify(response)

# 示例：请求数据接口
@app.route('/get_messages')
def get_messages():
    messages = Message.query.all()
    message_list = [{'username': msg.username, 'message': msg.message} for msg in messages]
    return jsonify({'messages': message_list})
# 示例：插入数据接口
@app.route('/insert_topic', methods=['POST'])
def insert_topic():
    data = request.get_json()
    title = data.get('title', '')
    description = data.get('description', '')

    if title and description:
        new_message = Topic(title=title, description=description)
        db.session.add(new_message)
        db.session.commit()
        response = {'message': '数据插入成功'}
    else:
        response = {'message': '请提供有效的标题和描述'}

    return jsonify(response)

# 示例：请求数据接口
@app.route('/get_topics')
def get_topics():
    topics = Topic.query.all()
    topic_list = [{'title': topic.title, 'description': topic.description} for topic in topics]
    return jsonify({'topics': topic_list})

@app.route('/')
def welcome1():
    return render_template('2222.html')
@app.route('/1')
def welcome2():
    return render_template('1.html')
@app.route('/a')
def a():
    return render_template('1.html')
@app.route('/b')
def b():
    return render_template('2222.html')
@app.route('/Answer_home_page')
def welcome3():
    return render_template('Answer_home_page.html')
@app.route('/c')
def c():
    return render_template('Answer_home_page.html')
@app.route('/Answer')
def welcome4():
    return render_template('Answer.html')
@app.route('/d')
def d():
    return render_template('Answer.html')
@app.route('/QAQ')
def welcome5():
    return render_template('QAQ.html')
@app.route('/e')
def e():
    return render_template('QAQ.html')

@app.route('/show_file_list')
def show_file_list():
    uploads_path = os.path.join(folder_path, 'uploads')
    if os.path.exists(uploads_path) and os.path.isdir(uploads_path):
        file_list = os.listdir(uploads_path)
        return render_template('file_list.html', files=file_list)
    else:
        return "Uploads folder not found", 404


@app.route('/delete_files', methods=['POST'])
def delete_files():
    # 解析请求数据
    data = request.get_json()
    folder_path = data.get('folderPath', '')
    if folder_path:
        file_list = os.listdir(folder_path)
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        response = {'message': '文件删除成功'}
    else:
        response = {'message': '未提供文件夹路径'}

    return jsonify(response)
@app.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return redirect(url_for('show_file_list'))

@app.route('/download_file/<path:filename>')
def download_file(filename):
    # file_path = os.path.join(folder_path, filename)
    uploads_path = os.path.join(folder_path, 'uploads')
    file_path = os.path.join(uploads_path, filename)

    if is_valid_path(file_path):
        if os.path.isdir(file_path):
            print(file_path)
            print(folder_path)
            print(filename)
            # 如果是文件夹，使用 send_from_directory 发送文件夹
            return send_from_directory(folder_path,filename, as_attachment=True)
        else:
            # 如果是文件，使用 send_file 发送文件
            return send_file(file_path, as_attachment=True)
    else:
        # 如果路径无效，返回 404 错误
        return "Invalid path or file not found", 404

def is_valid_path(path):
    # 使用 os.path.isdir 判断是否是文件夹
    return os.path.exists(path) and (os.path.isfile(path) or os.path.isdir(path))

if __name__ == '__main__':
    with app.app_context():
        # Create the database tables
        db.create_all()
    app.run()