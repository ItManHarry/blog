from flask import Blueprint, redirect,url_for,render_template,session,request
from ddic.models import Post
bp_blog = Blueprint('blog', __name__)
#博客首页
@bp_blog.route('/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts)