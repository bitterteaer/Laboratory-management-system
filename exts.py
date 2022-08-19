from flask_sqlalchemy import SQLAlchemy
import time

db = SQLAlchemy()


def delete_sa_instance_state(data):
    del data['_sa_instance_state']
    # data["href"] = "<a href=\"edit.html?id={}\">详情</a>".format(data['id_user'])
    return data


def get_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def add_name_from_user(data):
    author = data.user.name
    data = vars(data)
    data['author'] = author
    del data["user"]
    return data
