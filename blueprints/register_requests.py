from flask import g, Blueprint, redirect, url_for, request, jsonify, session
from models import RegisterRequests,User
from exts import db, delete_sa_instance_state
from decorations import root_required

bp = Blueprint("register_requests", __name__, url_prefix="/register_requests")


@bp.route('/get_register_requests_count', methods=['GET', 'POST'])
@root_required
def get_register_requests_count():
    user_list = RegisterRequests.query.all()
    data = {"count": len(user_list)}
    return data


@bp.route('/get_register_requests_data', methods=['GET', 'POST'])
@root_required
def get_register_requests_data():
    page = request.values.get('page')
    limit = request.values.get('limit')
    paginate = RegisterRequests.query.paginate(page=int(page), per_page=int(limit))
    return jsonify({"data": list(map(delete_sa_instance_state, map(vars, paginate.items)))})


@bp.route('/delete_register_requests', methods=['GET', 'POST'])
@root_required
def delete_register_requests():
    id_register_requests = request.values.get("id_register_requests")
    RegisterRequests.query.filter_by(id_register_requests=int(id_register_requests)).delete()
    db.session.commit()
    return "success"


@bp.route('/add_to_user', methods=['GET', 'POST'])
@root_required
def add_to_user():
    id_register_requests = request.values.get("id_register_requests")
    rr = RegisterRequests.query.filter_by(id_register_requests=int(id_register_requests)).first()
    user = User(username=rr.username,
                password=rr.password,
                name=rr.name,
                phone=rr.phone,
                role="学生",
                power=2,
                grade=rr.grade)
    db.session.add(user)
    RegisterRequests.query.filter_by(id_register_requests=int(id_register_requests)).delete()
    db.session.commit()
    return "success"


@bp.route("/register", methods=['GET', 'POST'])
def register():
    value = request.values
    user = RegisterRequests(
                username=value.get("username"),
                password=value.get("password"),
                name=value.get("name"),
                phone=value.get("phone"),
                role="学生",
                power=2,
                grade=value.get("grade"),
                )
    db.session.add(user)
    db.session.commit()
    return "注册申请已提交"
