from functools import wraps
from flask import g,redirect,url_for


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(g, 'user'):
            return func(*args, **kwargs)
        else:
            # return "未登录"
            return redirect(url_for("user.login"))

    return wrapper


def root_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(g, 'user') and g.user.power <= 0:
            return func(*args, **kwargs)
        else:
            # print("权限不足")
            return "权限不足"

    return wrapper


def teacher_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if hasattr(g, 'user') and g.user.power <= 1:
            return func(*args, **kwargs)
        else:
            # print("权限不足")
            return "权限不足"

    return wrapper
