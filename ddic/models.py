'''
    博客-数据模型
'''
from datetime import datetime
from ddic.exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
'''
    留言板表
'''
class TbMessage(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    title = db.Column(db.String(20))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow,index=True)

    def __repr__(self):
        return "<Message body %r>" %self.body

class TbAuthor(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    #关联文章,参数值为另一侧的模型名
    articles = db.relationship('TbArticle')

    def __repr__(self):
        return "<Author %s>" % self.name
class TbArticle(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    title = db.Column(db.String(20))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    #设置外键:键值为另一侧的表名和主键字段名
    author_id = db.Column(db.String(40), db.ForeignKey('tb_author.id'))

    def __repr__(self):
        return "<Article %s>" %self.title


association_table = db.Table('association',
    db.Column('student_id', db.String(40), db.ForeignKey('student.id')),
    db.Column('teacher_id', db.String(40), db.ForeignKey('teacher.id'))
)


class Student(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    grade = db.Column(db.String(10))
    clazz = db.Column(db.String(10))
    teachers = db.relationship('Teacher', secondary=association_table, back_populates='students')


class Teacher(db.Model):
    id = db.Column(db.String(40), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    subject = db.Column(db.String(10))
    students = db.relationship('Student', secondary=association_table, back_populates='teachers')

'''
    博客表-管理员
    UserMixin:flask-login的登录管理模块
'''
class Admin(db.Model, UserMixin):
    id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(40), unique=True)    #用户账号
    password_hash = db.Column(db.String(128))           #用户密码 - 密文存储
    blog_title = db.Column(db.String(100))              #博客标题
    blog_sub_title = db.Column(db.String(120))          #博客副标题
    name = db.Column(db.String(30))                     #用户姓名
    about = db.Column(db.Text)                          #关于
    logins = db.relationship('Login', back_populates='admin')#登录履历-反向关联
    #设置密码-使用werkzeug.security提供的加密方式
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    #校验密码
    def validate_password(self,password):
        return check_password_hash(self.password_hash, password)

#博客表-分类
class Category(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(30),unique=True)                 #分类名称
    posts = db.relationship('Post',back_populates='category')   #类别文章
#博客表-文章
class Post(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    title = db.Column(db.String(100))                                           #文章标题
    body = db.Column(db.Text)                                                   #文章内容
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)     #发表时间
    category_id = db.Column(db.String(32), db.ForeignKey('category.id'))        #所属分类ID-外键
    category = db.relationship('Category', back_populates='posts')              #所属分类-反向关联
    comments = db.relationship('Comment', back_populates='post',cascade='all')  #文章评论-反向关联
#博客表-评论
class Comment(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    author = db.Column(db.String(30))                                                   #作者
    email = db.Column(db.String(254))                                                   #邮箱
    site = db.Column(db.String(255))                                                    #个人网址
    body = db.Column(db.Text)                                                           #评论内容
    from_admin = db.Column(db.Boolean, default=False)                                   #来着博主
    reviewed = db.Column(db.Boolean, default=False)                                     #已审核
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)             #发表时间
    post_id = db.Column(db.String(32), db.ForeignKey('post.id'))                        #文章ID-外键
    post = db.relationship('Post', back_populates='comments')                           #文章-反向关联
    comment_id = db.Column(db.String(32), db.ForeignKey('comment.id'))                  #评论ID-自身外键
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])    #父评论-反向关联
    replies = db.relationship('Comment', back_populates='replied', cascade='all')       #子评论-反向关联
#登录履历
class Login(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)  #登录时间
    admin_id = db.Column(db.String(32), db.ForeignKey('admin.id'))           #登录账号
    admin = db.relationship('Admin', back_populates='logins')                #登录人员-反向关联