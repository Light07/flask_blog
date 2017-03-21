#coding=utf-8
from flask import render_template, request, Blueprint

blue_user = Blueprint('blue_user', __name__, template_folder='user_forums')


@blue_user.route('/detail_posts', methods =['GET', 'POST'])
def posts_detail():
    id = request.args.get("id")
    post_title = request.args.get("title")
    post_category = request.args.get("category")
    post_author = request.args.get("author")
    post_contents = request.args.get("contents")
    blue_print_name = "blue_user"
    post_create_time = request.args.get("create_time")

    return render_template('user_forums/posts.html', post_title=post_title,\
                          post_category=post_category, \
                        post_author=post_author, post_contents=post_contents, \
                           blue_print_name=blue_print_name, post_create_time=post_create_time)
