'''
    博客-数据模型
'''
from datetime import datetime
from ddic.exts import db
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

#博客表-管理员
class Admin(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    username = db.Column(db.String(40))         #用户账号
    password_hash = db.Column(db.String(128))   #用户密码
    blog_title = db.Column(db.String(100))      #博客标题
    blog_sub_title = db.Column(db.String(120))  #博客副标题
    name = db.Column(db.String(30))             #用户姓名
    about = db.Column(db.Text)                  #关于
#博客表-分类
class Category(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    name = db.Column(db.String(30),unique=True)
    posts = db.relationship('Post',back_populates='category')
#博客表-文章
class Post(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    category_id = db.Column(db.String(32), db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post',cascade='all')
#博客表-评论
class Comment(db.Model):
    id = db.Column(db.String(32), primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    site = db.Column(db.String(255))
    body = db.Column(db.Text)
    from_admin = db.Column(db.Boolean, default=False)
    reviewed = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    post_id = db.Column(db.String(32), db.ForeignKey('post.id'))
    comment_id = db.Column(db.String(32), db.ForeignKey('comment.id'))
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])
    replies = db.relationship('Comment', back_populates='replied', cascade='all')
    post = db.relationship('Post', back_populates='comments')