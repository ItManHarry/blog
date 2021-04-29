from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField,HiddenField,PasswordField,BooleanField,SubmitField,SelectField
from wtforms.validators import DataRequired, Length, ValidationError, Email, URL,Optional
from flask_ckeditor import CKEditorField
from ddic.models import Category
#登录表单
class LoginForm(FlaskForm):
    username = StringField('User Name',validators=[DataRequired('请输入用户名!'),Length(1, 20)])
    password = PasswordField('Password',validators=[DataRequired('请输入密码!'),Length(8,128)])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
#文章表单
class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired('请输入标题！！！'), Length(1, 60, '标题必须满足1-60个字符!!!')])
    category = SelectField('分类')
    body = CKEditorField('内容', validators=[DataRequired()])
    submit = SubmitField('发布')
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        '''
            因为Flask-SQLAlchemy阶赖于程序上下文才能正
            常工作（内部使用current_app获取配置信息），所
            以这个查询调用妥放到构造方法中执
        '''
        self.category.choices=[(category.id, category.name) for category in Category.query.order_by(Category.name).all()]
#分类表单
class CategoryForm(FlaskForm):
    name = StringField('名称', validators=[DataRequired(), Length(1,30,'长度要介于(1-30)!')])
    submit = SubmitField('保存')
    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('类别名称已存在!')
#评论表单
class CommitForm(FlaskForm):
    author = StringField('姓名', validators=[DataRequired('请输入姓名!'), Length(1,30,'长度要介于1-30')])
    email = StringField('电子邮箱', validators=[DataRequired('请输入邮箱!'), Email(), Length(1,254,'长度要介于(1,254)！')])
    site = StringField('个人主页',validators=[Optional(), URL(), Length(0,255,'长度要小于255！')])
    body = TextAreaField('评论' , validators=[DataRequired('请输入评论！')])
    submit = SubmitField('发表')
#管理员评论表单
class AdminCommitForm(CommitForm):
    author = HiddenField()
    email = HiddenField()
    site = HiddenField()
#作者表单
class AuthorForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired('请输入姓名!'), Length(2, 20, '长度要介于(2-20)！')])
    phone = StringField('电话', validators=[DataRequired('请输入电话!'), Length(11, 11, '长度必须为11位！')])
    id = HiddenField()
#文章表单
class ArticleForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired('请输入标题!'), Length(5,20,'长度要介于(5-20)！')])
    body = TextAreaField('正文', validators=[DataRequired('请输入正文!')])
    id = HiddenField()             #文章id
    author_id = HiddenField()      #作者id