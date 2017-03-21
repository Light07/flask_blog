#coding=utf-8

from functools import wraps
from flask import flash, redirect, url_for
from flask import session, request
from werkzeug.exceptions import abort


from forum_app.db_helper.db_helper import is_post_create_by_user


def login_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        username = session.get('username')
        if not username:
            flash("You must login first")
            return redirect(url_for('login'))

        else:
            return func(*args, **kwargs)
    return wrapper

def admin_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        is_admin = session.get("isadmin")
        if is_admin != True:
            abort(403, "You have no authentication to operate this!")
        else:
            return func(*args, **kwargs)

def owner_check(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        pid = request.args.get("id")
        memberid = session.get("memberid")

        if pid and memberid:
            if is_post_create_by_user(pid, memberid) !=True:
                abort(403, "You have no authentication to operate this!")
            else:
                return func(*args, **kwargs)
        else:
            abort(403, "Wrong parameter were received {pid}".format(pid=pid))
    return wrapper


