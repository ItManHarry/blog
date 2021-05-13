from flask import Blueprint, redirect,url_for,render_template,session,request,flash,current_app,abort,make_response
from flask_login import login_required
from ddic.models import Post,Category,Comment,PostComment
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
#文章详情
@bp_blog.route('/show/<post_id>', methods=['GET','POST'])
def show(post_id):
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ITEM_COUNT_PER_PAGE']
    pagination = PostComment.query.with_parent(post).order_by(PostComment.timestamp.desc()).paginate(page, per_page=per_page)
    comments = pagination.items
    from ddic.forms.all import PostCommitForm
    print('Request method is : >>>>>>>>>>>>>>>>>>>>>>>', request.method)
    form = PostCommitForm()
    if form.validate_on_submit():
        print('save the commit ...')
        pc = PostComment(id=uuid.uuid4().hex, body=form.body.data,post_id=post_id)
        db.session.add(pc)
        db.session.commit()
        return redirect(url_for('.show', post_id=post_id))
    return render_template('blog/show.html', post=post, comments=comments, pagination=pagination, form=form)
#主题切换
@bp_blog.route('/theme/<theme_name>')
def theme(theme_name):
    if theme_name not in current_app.config['BLOG_THEMES'].keys():
        abort(404)
    response = make_response(redirect_back())
    response.set_cookie('theme', theme_name, max_age=30*24*60*60)
    return response