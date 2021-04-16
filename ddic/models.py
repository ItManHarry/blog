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