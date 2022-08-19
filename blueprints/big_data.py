from flask import g, Blueprint, redirect, url_for, request, jsonify, session, render_template
from models import BigData, User
from exts import db, delete_sa_instance_state, get_time, add_name_from_user
import os
import time
from decorations import login_required

bp = Blueprint("big_data", __name__, url_prefix="/big_data")


# who_can_see=0:私有上传, 1:同等权限上传, 2:完全公开上传
@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    who_can_see = request.values.get("who_can_see")
    uploaded_file = request.files.get('file')

    # return "test"
    suffix = '.' + uploaded_file.filename.split('.')[-1]  # 获取文件后缀名
    filename = uploaded_file.filename.replace(".", "").replace("\\", "").replace("/", "")
    basedir = os.path.abspath(os.path.dirname(__file__)).replace("blueprints", "")  # 获取当前文件路径
    new_dir = os.path.join("static", "big_data_upload", filename + str(int(time.time())) + suffix)  # 拼接相对路径
    uploaded_file_path = os.path.join(basedir, new_dir)  # 拼接图片完整保存路径,时间戳命名文件防止重复
    uploaded_file.save(uploaded_file_path)  # 保存文件
    size = os.path.getsize(uploaded_file_path)
    print(size)
    # size = len(count_size_stream.stream.read())
    if size > 1000000000:
        file_size = f"{size / 1000000000} GB"
        print(size / 1000000000, "GB")
    elif size > 1000000:
        file_size = f"{size / 1000000} MB"
        print(size / 1000000, "MB")
    else:
        file_size = f"{size / 1000} KB"
        print(size / 1000, "KB")

    big_data = BigData(filename=filename,
                       path="/" + new_dir.replace("\\", "/"),
                       time=get_time(),
                       who_can_see=int(who_can_see),
                       user=g.user,
                       size=file_size)
    db.session.add(big_data)
    db.session.commit()
    return "success"


@bp.route('/get_big_data_count', methods=['GET', 'POST'])
@login_required
def get_big_file_count():
    device_list = BigData.query.all()
    for i in device_list:
        if i.who_can_see == 0 and g.user.id_user != i.id_user:
            device_list.remove(i)
        elif i.who_can_see == 1 and g.user.power != i.user.power:
            device_list.remove(i)
        else:
            pass
    data = {"count": len(device_list)}
    return data


@bp.route('/get_big_data_data', methods=['GET', 'POST'])
@login_required
def get_big_file_data():
    page = request.values.get('page')
    limit = request.values.get('limit')
    paginate = BigData.query.paginate(page=int(page), per_page=int(limit))
    for i in paginate.items:
        if i.who_can_see == 0 and g.user.id_user != i.id_user:
            paginate.items.remove(i)
        elif i.who_can_see == 1 and g.user.power != i.user.power:
            paginate.items.remove(i)
        else:
            pass
    return jsonify({"data": list(map(delete_sa_instance_state, map(add_name_from_user, paginate.items)))})


@bp.route("/find_big_data_html", methods=['GET', 'POST'])
@login_required
def find_big_data_html():
    filename = request.values.get("filename")
    author = request.values.get("author")
    if filename != "":
        list1 = db.session.query(BigData).filter(BigData.filename.like(f"%{filename}%")).all()
    else:
        list1 = []
    res_list = db.session.query(BigData).filter(BigData.user.has(User.name == author)).all()
    str1 = ""
    for i in list1 + res_list:
        if i.who_can_see == 0 and g.user.id_user != i.id_user:
            continue
        elif i.who_can_see == 1 and g.user.power != i.user.power:
            continue
        else:
            pass
        str1 += f'''
            <tr>
            <td>{i.id_big_data}</td>
            <td>{i.filename}</td>
            <td>{i.size}</td>
            <td>{i.user.name}</td>
            <td>{i.time}</td>
            <td><a href={i.path}>下载</a></td>
            </tr>
            '''
    if str1 == "":
        str1 += f'''
                    <tr>
                    <td>未找到</td>
                    </tr>
                    '''
    return str1
