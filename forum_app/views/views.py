#coding=utf-8
import os
import random
import time

import datetime
from flask import make_response
from flask import render_template, flash, redirect,request, url_for
from flask import session

from forum_app.db_helper.db_helper import is_user_exist, create_user, is_username_password_match, get_all_posts, get_posts_by_page, \
    count_post_numbers_by_category, is_user_have_admin_right_to_post, is_user_belong_to_admin_group, create_post, \
    get_member_id_by_username, delete_post, is_post_create_by_user, get_post_by_category, get_all_categories
from forum_app import app
from forum_app.pagination.pagination import PageHelper
from forum_app.forms import LoginForm, SignUpForm, PostEditor
from forum_app.wraps_api.auth_related import login_auth, admin_check, owner_check


@app.route('/logout')
def logout():
    if "remember_me" in session:
        session.pop('remember_me', None)
    if "username" in session:
        session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/index', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:

        return redirect(url_for('forum'))
    else:
        form = LoginForm()
        if form.validate_on_submit():
           remember = request.form.get('remember_me')
           username = request.form.get('username')
           password = request.form.get('password')

           if not is_user_exist(username):
               flash("User doesn't exit!")
           elif not is_username_password_match(username, password):
               flash("User name or password are not correct, please enter again ")
           else:
               session["username"] = username
               session["memberid"] = get_member_id_by_username(username)
               session["isadmin"] = is_user_belong_to_admin_group(username)
               if remember:
                   session["Remember_me"] = True
               return redirect(url_for('forum'))

    return render_template('login.html', title='Sign In', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
       username = request.form.get('username')
       password = request.form.get('password')
       pd_confirm = request.form.get("pd_confirm")
       phonenumber = request.form.get('phonenumber')
       if password !=pd_confirm:
        flash("Your password are not match")
       elif is_user_exist(username):
           flash("The user already exit")
       else:
            create_user(username, password, phonenumber)
            if is_user_exist(username):
                flash("User created successfully, now redirect you to login page")
                return redirect(url_for('login'))
            else:
                flash("Oops, create user failed with unknown reason, please try sign up again")
    return render_template('signup.html', title='Sign Up', form=form)


@app.route('/forum/', defaults={'page':1}, methods=['GET', 'POST'])
@app.route('/forum/<int:page>', methods=['GET', 'POST'])
@login_auth
def forum(page):
    form1 = PostEditor()
    category = request.args.get('category')

    if category:
        category = category.encode('utf-8')
        shown_posts = get_post_by_category(category, page)
    else:
        shown_posts = get_posts_by_page(page)

    total_count = count_post_numbers_by_category(category)
    all_categories = get_all_categories()
    is_admin = True if "isadmin" in session and session["isadmin"] == True else False
    username= session["username"] if 'username' in session else None

    def url_for_other_page(page):
        args = dict(request.view_args.items() + request.args.to_dict().items())
        args['page'] = page
        return url_for(request.endpoint, **args)

    app.jinja_env.globals['url_for_other_page'] = url_for_other_page


    pagination = PageHelper(page, app.config["PER_PAGE"], total_count)


    if request.method == "POST" or form1.validate_on_submit():
        title = request.form.get('title')
        category = request.form.get('category')
        content = request.form.get('post')
        content = request.form.get('editor1')

        if request.form.get('publish') == '发布'.decode('utf-8'):

            create_post(title, category, content, session["memberid"])
            total_count = count_post_numbers_by_category(category)
            pagination = PageHelper(page, app.config["PER_PAGE"], total_count)
            shown_posts = get_post_by_category(category, page)
            all_categories = get_all_categories()
            return redirect(url_for('forum', pagination=pagination, shown_posts=shown_posts, user_have_admin_right_to_post=username, is_admin=is_admin, all_categories=all_categories, form=form1))

    return render_template('forum.html', pagination=pagination, shown_posts=shown_posts, user_have_admin_right_to_post=username, is_admin=is_admin, all_categories=all_categories, form=form1)


@app.route('/deletepost/<int:pid>', methods=["GET", "POST"])
@login_auth
def deletepost(pid):
    memberid = session.get("memberid")
    is_admin = session.get("isadmin")
    if is_post_create_by_user(pid, memberid) or is_admin:
        delete_post(pid)
        time.sleep(1)
    return redirect(url_for('forum'))


def gen_rnd_filename():
    filename_prefix = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    return '{prefix}{ran}' .format(prefix=filename_prefix, ran=str(random.randrange(1000, 10000)))

@app.route('/ckupload/', methods=['POST'])
def ckupload():
    """CKEditor file upload"""
    error = ''
    url = ''
    callback = request.args.get("CKEditorFuncNum")
    if request.method == 'POST' and 'upload' in request.files:
        fileobj = request.files['upload']
        fname, fext = os.path.splitext(fileobj.filename)
        rnd_name = '{fname}{fext}' .format(fname=gen_rnd_filename(), fext=fext)
        filepath = os.path.join(app.static_folder, 'upload', rnd_name)
        # 检查路径是否存在，不存在则创建
        dirname = os.path.dirname(filepath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                error = 'ERROR_CREATE_DIR'
        elif not os.access(dirname, os.W_OK):
            error = 'ERROR_DIR_NOT_WRITEABLE'
        if not error:
            fileobj.save(filepath)
            url = url_for('static', filename='%s/%s' % ('upload', rnd_name))
    else:
        error = 'post error'
    res = """

<script type="text/javascript">
  window.parent.CKEDITOR.tools.callFunction(%s, '%s', '%s');
</script>

""" % (callback, url, error)
    response = make_response(res)
    response.headers["Content-Type"] = "text/html"
    return response