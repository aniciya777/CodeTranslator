from .db_session import SqlAlchemyBase
import sqlalchemy


class Languages(SqlAlchemyBase):
    __tablename__ = 'languages'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    code = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    title = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)

    def __repr__(self):
        return f'<{self.code} - {self.title}>'
