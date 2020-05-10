from .db_session import SqlAlchemyBase, orm
import sqlalchemy
import datetime


class Dictionaries(SqlAlchemyBase):
    __tablename__ = 'dictionaries'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    code_lang = sqlalchemy.Column(sqlalchemy.String)
    from_lang = sqlalchemy.Column(sqlalchemy.String)
    to_lang = sqlalchemy.Column(sqlalchemy.String)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    filename = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    original_text = sqlalchemy.Column(sqlalchemy.UnicodeText)
    translated_text = sqlalchemy.Column(sqlalchemy.UnicodeText)
    from_translate_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
