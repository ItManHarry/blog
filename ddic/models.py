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