'''
    留言板 - Form
'''
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,SubmitField
from wtforms.validators import DataRequired, Length

class MessageForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired('请输入标题!'), Length(5,20,'长度要介于(5-20)！')])
    body = TextAreaField('消息', validators=[DataRequired('请输入消息!'),Length(10,200,'长度要介于(10-200)')])
    submit = SubmitField('发布')