from flask import Blueprint, redirect,url_for,render_template,session,request,flash,current_app,abort,make_response
from flask_login import login_required
from ddic.models import Post,Category,Comment
from ddic.forms.all import PostForm
from ddic.exts import db
from ddic.utils import redirect_back
import uuid
bp_blog = Blueprint('blog', __name__)
#博客首页
@bp_blog.route('/', defaults={'page':1})
@bp_blog.route('/page/<int:page>')
def index(page):
    #page = request.args.get('page', 1, type=int)
    #per_page = current_app.config['ITEM_COUNT_PER_PAGE']
    pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config['ITEM_COUNT_PER_PAGE'])
    posts = pagination.items
    #posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', posts=posts, pagination=pagination)
@bp_blog.route('/category/<category_id>')
def show_category(category_id):
    category = Category.query.get_or_404(category_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ITEM_COUNT_PER_PAGE']
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page=per_page)
    posts = pagination.items
    return render_template('blog/category.html', category=category, posts=posts, pagination=pagination)
#新增文章
@bp_blog.route('/add', methods=['GET','POST'])
@login_required
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
#文章详情
@bp_blog.route('/show/<post_id>')
def show(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ITEM_COUNT_PER_PAGE']
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(page, per_page=per_page)
    comments = pagination.items
    return render_template('blog/show.html', post=post, comments=comments, pagination=pagination)
#主题切换
@bp_blog.route('/theme/<theme_name>')
def theme(theme_name):
    if theme_name not in current_app.config['BLOG_THEMES'].keys():
        abort(404)
    response = make_response(redirect_back())
    response.set_cookie('theme', theme_name, max_age=30*24*60*60)
    return response