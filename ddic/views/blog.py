from flask import Blueprint, redirect,url_for,render_template,session,request,flash
from ddic.models import Post
from ddic.forms.all import PostForm
from ddic.exts import db
import uuid
bp_blog = Blueprint('blog', __name__)
#博客首页
@bp_blog.route('/')
def index():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts)
@bp_blog.route('/add', methods=['GET','POST'])
def add():
    form = PostForm()
    if form.validate_on_submit():
        #print('Title : ', form.title.data, ', category : ', form.category.data, ', body : ', form.body.data)
        post = Post(
            id=uuid.uuid4().hex,
            title=form.title.data,
            category_id=form.category.data,
            body=form.body.data
        )
        db.session.add(post)
        db.session.commit()
        flash('文章发布成功!!!')
        return redirect(url_for('.add'))
    return render_template('blog/add.html', form=form)