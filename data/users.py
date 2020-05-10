from .db_session import SqlAlchemyBase, orm
import sqlalchemy
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    avatar_s = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    avatar_m = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    avatar_l = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    translations = orm.relation("Translations", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f'<User {self.id} email: {self.email}>'
