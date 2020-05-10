from .db_session import SqlAlchemyBase, orm
import sqlalchemy
import datetime


class Translations(SqlAlchemyBase):
    __tablename__ = 'translations'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    code_lang_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("code_languages.id"))
    code_lang = orm.relation('CodeLanguages', backref='translations')
    from_lang_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("languages.id"))
    from_lang = orm.relation('Languages', backref='translations_from',
                             primaryjoin="Languages.id == Translations.from_lang_id")
    to_lang_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("languages.id"))
    to_lang = orm.relation('Languages', backref='translations_to',
                           primaryjoin="Languages.id == Translations.to_lang_id")
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    filename = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    original_text = sqlalchemy.Column(sqlalchemy.UnicodeText)
    translated_text = sqlalchemy.Column(sqlalchemy.UnicodeText)

    def __repr__(self):
        return f'<Translations {self.id} {self.created_date} {self.user} {self.code_lang} ({self.from_lang}) "{self.original_text[:10]}" -> ({self.to_lang}) "{self.translated_text[:10]}">'
