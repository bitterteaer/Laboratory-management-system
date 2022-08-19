from exts import db


# orm模型
class User(db.Model):
    __tablename__ = "user"
    id_user = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(45), nullable=False)
    name = db.Column(db.String(45), nullable=False)
    phone = db.Column(db.String(45), nullable=False)
    role = db.Column(db.String(45), nullable=False)
    power = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(45), nullable=False)


class RegisterRequests(db.Model):
    __tablename__ = "register_requests"
    id_register_requests = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    password = db.Column(db.String(45), nullable=False)
    name = db.Column(db.String(45), nullable=False)
    phone = db.Column(db.String(45), nullable=False)
    role = db.Column(db.String(45), nullable=False)
    power = db.Column(db.Integer, nullable=False)
    grade = db.Column(db.String(45), nullable=False)


class Device(db.Model):
    __tablename__ = "device"
    id_device = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(45), nullable=False)
    pic = db.Column(db.String(200), nullable=False)
    time = db.Column(db.String(45), nullable=False)

    # 外键
    id_user = db.Column(db.Integer, db.ForeignKey("user.id_user"))
    user = db.relationship("User", backref="devices")


class Data(db.Model):
    __tablename__ = "data"
    id_data = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(45), nullable=False)
    content = db.Column(db.Text, nullable=False)
    appendix = db.Column(db.String(200), nullable=False)
    appendix_name = db.Column(db.String(45), nullable=False)
    time = db.Column(db.String(45), nullable=False)

    # 外键
    id_user = db.Column(db.Integer, db.ForeignKey("user.id_user"))
    user = db.relationship("User", backref="data_s")


class BigData(db.Model):
    __tablename__ = "big_data"
    id_big_data = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(45), nullable=False)
    path = db.Column(db.String(200), nullable=False)
    time = db.Column(db.String(45), nullable=False)
    who_can_see = db.Column(db.Integer, nullable=False)
    size = db.Column(db.String(45), nullable=False)

    # 外键
    id_user = db.Column(db.Integer, db.ForeignKey("user.id_user"))
    user = db.relationship("User", backref="big_data_s")