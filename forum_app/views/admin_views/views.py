#coding=utf-8
import time
from flask import render_template,request, Blueprint, redirect, url_for

from forum_app.db_helper.db_helper import update_post
from forum_app.forms import PostEditor

blue_admin = Blueprint('blue_admin', __name__, template_folder='admin_forums')


@blue_admin.route('/detail_posts', methods =['GET', 'POST'])
def posts_detail():
    form = PostEditor()
    pid = request.args.get("id")
    post_title = request.args.get("title")
    post_category = request.args.get("category")
    post_author = request.args.get("author")
    post_contents = request.args.get("contents")
    post_create_time = request.args.get("create_time")
    blue_print_name = "blue_admin"

    form.category.data = request.args.get("category")
    form.title.data = request.args.get("title")

    if request.method == "POST" and form.validate_on_submit():
        if request.form.get('publish') == '发布':
            update_post(request.form.get('title'), request.form.get('category'),  request.form.get('editor1'), id=pid)
            return redirect(url_for('forum'))

    return render_template('admin_forums/posts.html', post_title=post_title,\
                          post_category=post_category, \
                        post_author=post_author, post_contents=post_contents, \
                           blue_print_name=blue_print_name, post_create_time=post_create_time, pid=pid, form=form)

