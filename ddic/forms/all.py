from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,HiddenField
from wtforms.validators import DataRequired, Length
#作者form
class AuthorForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired('请输入姓名!'), Length(2, 20, '长度要介于(2-20)！')])
    phone = StringField('电话', validators=[DataRequired('请输入电话!'), Length(11, 11, '长度必须为11位！')])
    id = HiddenField()
class ArticleForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired('请输入标题!'), Length(5,20,'长度要介于(5-20)！')])
    body = TextAreaField('正文', validators=[DataRequired('请输入正文!')])
    id = HiddenField()             #文章id
    author_id = HiddenField()      #作者id