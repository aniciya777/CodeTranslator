from .db_session import SqlAlchemyBase, orm
import sqlalchemy
import datetime


class Dictionaries(SqlAlchemyBase):
    __tablename__ = 'dictionaries'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    user = orm.relation('User')
    code_lang_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("code_languages.id"))
    code_lang = orm.relation('CodeLanguages', backref='dictionaries')
    from_lang_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("languages.id"))
    from_lang = orm.relation('Languages', backref='dictionaries_from',
                             primaryjoin="Languages.id == Dictionaries.from_lang_id")
    to_lang_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("languages.id"))
    to_lang = orm.relation('Languages', backref='dictionaries_to',
                           primaryjoin="Languages.id == Dictionaries.to_lang_id")
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    filename = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    original_text = sqlalchemy.Column(sqlalchemy.UnicodeText)
    translated_text = sqlalchemy.Column(sqlalchemy.UnicodeText)
    from_translate_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    def __repr__(self):
        return f'<Dictionaries {self.id}.{self.from_translate_id} {self.created_date} {self.user} {self.code_lang} ({self.from_lang}) "{self.original_text[:10]}" -> ({self.to_lang}) "{self.translated_text[:10]}">'

    @property
    def formatdate(self):
        return self.created_date.strftime("%d.%m.%Y %H:%M")

    @property
    def savefilename(self):
        if self.filename:
            return self.filename
        file = self.code_lang.files.split(', ')[0]
        return f'record{self.id}.{file}'

    @property
    def alldata(self):
        return f'''{self.code_lang}
{self.from_lang}
{self.to_lang}
{self.created_date}
{self.formatdate}
{self.savefilename}
{self.original_text}
{self.translated_text}
'''.lower()

    def like(self, pattern):
        return pattern.lower() in self.alldata
