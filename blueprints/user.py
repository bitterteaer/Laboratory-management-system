from flask import g, Blueprint, redirect, url_for, request, jsonify, session
from models import User
from exts import db, delete_sa_instance_state, get_time
from sqlalchemy import or_
from decorations import root_required, login_required, teacher_required
from flask import current_app

bp = Blueprint("user", __name__, url_prefix="/user")


@bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return redirect(url_for('static', filename='login.html'))
    else:
        username = request.values.get("username")
        password = request.values.get("password")
        user = User.query.filter_by(username=username).first()
        if user is None:
            return "没有此用户"
            # return redirect(url_for("user.login"))
        else:
            if user.password == password:
                session['id_user'] = user.id_user
                return redirect(url_for('index'))
            else:
                return "密码错误"
                # return redirect(url_for("user.login"))


@bp.route('/get_user_count', methods=['GET', 'POST'])
@teacher_required
def get_user_count():
    user_list = db.session.query(User).filter(User.power >= g.user.power).all()
    data = {"count": len(user_list)}
    return data


@bp.route('/get_user_data', methods=['GET', 'POST'])
@teacher_required
def get_user_data():
    page = request.values.get('page')
    limit = request.values.get('limit')
    paginate = db.session.query(User).filter(User.power >= g.user.power).paginate(page=int(page), per_page=int(limit))
    return jsonify({"data": list(map(delete_sa_instance_state, map(vars, paginate.items)))})


@bp.route('/user_data_is_login', methods=['GET', 'POST'])
def user_data_is_login():
    try:
        user = g.user
    except:
        return "error"
    return jsonify(delete_sa_instance_state((vars(user))))


@bp.route('/delete_user', methods=['GET', 'POST'])
@root_required
def delete_user():
    id_user = request.values.get("id_user")
    User.query.filter_by(id_user=int(id_user)).delete()
    db.session.commit()
    return "success"


@bp.route('/update_user_and_pwd', methods=['GET', 'POST'])
@login_required
def update_user_and_pwd():
    username = request.values.get("username")
    password = request.values.get("password")
    user = g.user
    user.username = username
    user.password = password
    db.session.commit()
    return "success"


@bp.route("/find_user_data_html", methods=['GET', 'POST'])
@teacher_required
def find_user_data_html():
    name = request.values.get("name")
    role = request.values.get("role")
    grade = request.values.get("grade")

    res_or = db.session.query(User).filter(or_(User.name == name, User.role == role, User.grade == grade)).all()
    str1 = ""
    for user in res_or:
        print(vars(user))
        str1 += f'''
            <tr>
            <td>{user.id_user}</td>
            <td>{user.name}</td>
            <td>{user.username}</td>
            <td>{user.phone}</td>
            <td>{user.grade}</td>
            <td>{user.role}</td>
            <td>{user.password}</td>
            </tr>
            '''
    return str1


@bp.route("/login_out", methods=['GET', 'POST'])
@login_required
def login_out():
    """删除session数据"""
    if session.get("id_user"):
        del session["id_user"]
    return "success"


@bp.route("/teacher_register", methods=['GET', 'POST'])
@root_required
def teacher_register():
    value = request.values
    user = User(username=value.get("username"),
                password=value.get("password"),
                name=value.get("name"),
                phone=value.get("phone"),
                role="教师",
                power=1,
                grade="null",
                )
    db.session.add(user)
    db.session.commit()
    return "注册成功"
