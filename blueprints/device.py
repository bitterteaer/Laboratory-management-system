from flask import g, Blueprint, redirect, url_for, request, jsonify, session
from models import Device,User
from exts import db, delete_sa_instance_state, get_time, add_name_from_user
from sqlalchemy import or_
import os
import time
from decorations import login_required

bp = Blueprint("device", __name__, url_prefix="/device")


@bp.route('/get_device_count', methods=['GET', 'POST'])
@login_required
def get_device_count():
    device_list = Device.query.all()
    data = {"count": len(device_list)}
    return data


@bp.route('/get_device_data', methods=['GET', 'POST'])
@login_required
def get_device_data():
    page = request.values.get('page')
    limit = request.values.get('limit')
    paginate = Device.query.paginate(page=int(page), per_page=int(limit))
    return jsonify({"data": list(map(delete_sa_instance_state, map(add_name_from_user, paginate.items)))})


@bp.route("add_device", methods=['POST'])
@login_required
def add_device():
    img = request.files.get('pic')  # 从post请求中获取图片数据
    suffix = '.' + img.filename.split('.')[-1]  # 获取文件后缀名
    if suffix[1:] not in set(['png', 'jpg', 'JPG', 'PNG']):
        return "error: 请上传 png/jpg 类型文件"

    filename = img.filename.replace(".", "").replace("\\", "").replace("/", "")
    basedir = os.path.abspath(os.path.dirname(__file__)).replace("blueprints", "")  # 获取当前文件路径
    new_path = os.path.join("static", "device_pic", filename + str(int(time.time())) + suffix)  # 拼接相对路径
    img_path = os.path.join(basedir, new_path)  # 拼接图片完整保存路径,时间戳命名文件防止重复
    img.save(img_path)  # 保存图片

    # 其他参数用request.form字典获取
    name = request.form.get('name', '')
    # 这些值都可直接保存到数据库中
    device = Device(name=name,
                    user=g.user,
                    pic="/" + new_path.replace("\\", "/"),
                    time=get_time())
    db.session.add(device)
    db.session.commit()
    return "success"


@bp.route("/find_device_data_html", methods=['GET', 'POST'])
@login_required
def find_device_data_html():
    name = request.values.get("name")
    holder = request.values.get("holder")
    if name != "":
        list1 = db.session.query(Device).filter(Device.name.like(f"%{name}%")).all()
    else:
        list1 = []
    res_list = db.session.query(Device).filter(Device.user.has(User.name == holder)).all()
    str1 = ""
    for i in list1+res_list:
        str1 += f'''
            <tr>
            <td>{i.id_device}</td>
            <td>{i.name}</td>
            <td><img src="{i.pic}" alt="pic"/></td>
            <td>{i.time}</td>
            <td>{i.user.name}</td>
            </tr>
            '''
    if str1 == "":
        str1 += f'''
                    <tr>
                    <td>未找到</td>
                    </tr>
                    '''
    return str1
