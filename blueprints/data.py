from flask import g, Blueprint, redirect, url_for, request, jsonify, session
from models import Data, User
from exts import db, delete_sa_instance_state, get_time, add_name_from_user
from sqlalchemy import or_
import os
import time

bp = Blueprint("data", __name__, url_prefix="/data")


@bp.route('/get_data_count', methods=['GET', 'POST'])
def get_data_count():
    device_list = Data.query.all()
    data = {"count": len(device_list)}
    return data


@bp.route('/get_data_data', methods=['GET', 'POST'])
def get_data_data():
    page = request.values.get('page')
    limit = request.values.get('limit')
    paginate = Data.query.paginate(page=int(page), per_page=int(limit))
    return jsonify({"data": list(map(delete_sa_instance_state, map(add_name_from_user, paginate.items)))})


@bp.route("/find_data_data_html", methods=['GET', 'POST'])
def find_data_data_html():
    author = request.values.get("author")
    title = request.values.get("title")

    if title != "":
        list1 = db.session.query(Data).filter(Data.title.like(f"%{title}%")).all()
    else:
        list1 = []
    res_or = db.session.query(Data).filter(Data.user.has(User.name == author)).all()
    str1 = ""
    for data in list1 + res_or:
        str1 += f'''
            <tr>
            <td>{data.id_data}</td>
            <td>{data.title}</td>
            <td>{data.content}</td>
            <td><a href="{data.appendix}">{data.appendix_name}</a></td>
            <td>{data.user.name}</td>
            <td>{data.time}</td>
            </tr>
            '''
    if str1 == "":
        str1 += f'''
                    <tr>
                    <td>未找到</td>
                    </tr>
                    '''
    return str1


@bp.route("add_data", methods=['POST'])
def add_data():
    appendix = request.files.get('appendix')  # 从post请求中获取文件数据
    # 其他参数用request.form字典获取
    title = request.form.get('title', '')
    content = request.form.get('content', '')
    data = Data(title=title,
                content=content,
                time=get_time(),
                user=g.user)

    suffix = '.' + appendix.filename.split('.')[-1]  # 获取文件后缀名
    basedir = os.path.abspath(os.path.dirname(__file__)).replace("blueprints", "")  # 获取当前文件路径
    filename = appendix.filename.replace(".", "").replace("\\", "").replace("/", "")
    new_dir = os.path.join("static", "data_upload", filename + str(int(time.time())) + suffix)  # 拼接相对路径
    appendix_file_path = os.path.join(basedir, new_dir)  # 拼接图片完整保存路径,时间戳命名文件防止重复
    appendix.save(appendix_file_path)  # 保存文件
    size = os.path.getsize(appendix_file_path)

    if size == 0:
        data.appendix = "javascript:"
        data.appendix_name = "没有附件"
    else:
        data.appendix = "/" + new_dir.replace("\\", "/")
        data.appendix_name = filename

    db.session.add(data)
    db.session.commit()
    return "success"
