from .db_session import SqlAlchemyBase
import sqlalchemy


class CodeLanguages(SqlAlchemyBase):
    __tablename__ = 'code_languages'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    code = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    desc = sqlalchemy.Column(sqlalchemy.String, index=True)

    def __repr__(self):
        return f'<{self.code} - {self.desc}>'
