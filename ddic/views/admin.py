from flask import Blueprint,redirect,render_template,url_for,current_app,flash
from flask_login import login_required
from ddic.forms.all import PostForm
from ddic.exts import db
from ddic.models import Post
from ddic.utils import redirect_back
import uuid
bp_admin = Blueprint('admin', __name__)
@bp_admin.route('/', defaults={'page':1})
@bp_admin.route('/post/list/<int:page>')
def manage_post(page):
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['ITEM_COUNT_PER_PAGE'])
    posts = pagination.items
    return render_template('admin/post_manage.html', posts=posts, pagination=pagination)
#新增文章
@bp_admin.route('/post/add', methods=['GET','POST'])
@login_required
def add_post():
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
        return redirect(url_for('.add_post'))
    return render_template('admin/post_add.html', form=form)
#删除文章
@bp_admin.route('/post/del/<post_id>', methods=['POST'])
def del_post(post_id):
    #返回当前文章列表
    print('Now do the post delete action , post id is %s' %post_id)
    post = Post.query.get(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect_back()
@bp_admin.route('/post/edit/<post_id>', methods=['GET','POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.category_id=form.category.data
        post.body=form.body.data
        db.session.commit()
        flash('文章修改成功!!!')
        return redirect(url_for('.edit_post', post_id=post_id))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    form.id.data = post.id
    return render_template('admin/post_edit.html', form=form)