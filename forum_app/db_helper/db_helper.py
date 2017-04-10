# coding=utf-8
import time
from sqlalchemy import and_


from forum_app import app

__author__ = 'kevin'

from sqlalchemy import create_engine, text, func
from sqlalchemy.orm import sessionmaker
from wtforms import ValidationError

from forum_app.db_helper.table_mapping import Members, Categories, Posts

db_conn_string = '''mssql+pymssql://{username}:{password}@{server}/{db_name}?charset=utf8'''\
    .format(username=app.config["DB_USERNAME"], password=app.config["DB_PASSWORD"], \
            server=app.config["DB_SERVER"],db_name=app.config["DB_NAME"])

engine = create_engine(db_conn_string, encoding='utf-8', echo=True)

# Session = sessionmaker()
# Session.configure(bind=engine)

Session = sessionmaker(bind=engine)

session = Session()


def is_user_exist(username):
    user = session.query(Members).filter(Members.UserName==username.lower()).scalar()
    session.close()
    if user:
        return True
    else:
        return False

def create_user(username, password, phonenumber):
    sql = '''insert into Members(UserName,PassWord, PhoneNumber) values('{username}', '{password}', '{phonenumber}')'''.format(username=username, password=password, phonenumber=phonenumber)
    session.execute(text(sql))
    session.commit()
    session.close()

def is_username_password_match(username, password):
    sql = '''select * from Members where username='{}' and password = '{}' '''.format(username,password)
    match_result = session.execute(text(sql)).fetchall()
    if match_result:
        return True
    else:
        return False

def get_all_posts():
    all_posts = []
    all_records = session.query(Posts).all()
    for i in all_records:
        single_post = {}
        single_post["category_name"] = session.query(Categories.CName).filter(Categories.CId==i.CId).scalar()
        single_post["post_author_id"] = i.MemberId
        single_post["post_author"] = session.query(Members.UserName).filter(Members.MemberId == i.MemberId).scalar()
        single_post["post_id"] = i.PId
        single_post["post_title"] = i.Title
        single_post["post_contents"] = i.Contents
        single_post["post_comment"] = i.Comments if i.Comments else 'NULL'
        all_posts.append(single_post)
    session.close()
    return all_posts

def get_all_categories():
    all_category = []
    all_category_raw = session.query(Categories.CName, Categories.CId).all()
    for item in all_category_raw:
        valid_category_sql = '''select count(1) from categories c inner join posts p on c.CId=p.CId where c.CId='{cid}' and p.shownpost=1 '''.format(cid=item[1])
        if session.execute(text(valid_category_sql)).scalar():
            all_category.append(item[0])

    return all_category

def get_posts_by_page(page):
    results = []
    records_per_page_sql = '''select top {PER_PAGE} * from posts where pid not in (select top {target_page} pid from posts where shownpost=1 order by pid desc) and shownpost=1 order by pid desc'''.format(PER_PAGE=app.config["PER_PAGE"], target_page=(page-1)*app.config["PER_PAGE"])
    records_per_page = session.execute(text(records_per_page_sql)).fetchall()
    for i in records_per_page:
        single_post = {}
        single_post["category_name"] = session.query(Categories.CName).filter(Categories.CId==i.CId).scalar()
        single_post["post_author_id"] = i.MemberId
        single_post["post_author"] = session.query(Members.UserName).filter(Members.MemberId == i.MemberId).scalar()
        single_post["post_id"] = i.PId
        single_post["post_title"] = i.Title
        single_post["post_contents"] = i.Contents
        single_post["post_comment"] = i.Comments if i.Comments else 'NULL'
        single_post["post_insert_date"] = i.InsertTime.strftime('%Y-%m-%d')
        results.append(single_post)

    session.close()
    return results

def is_user_have_admin_right_to_post(user_name, post_id):
    count = 0
    if user_name and post_id:
        sql = '''select count(1) from posts where pid={post_id} and memberid=(select memberid from members where username={user_name})'''.format(user_name=user_name, post_id=post_id)
        count = session.execute(text(sql)).fetchall()
    return True if int(count)>0 else False

def get_posts_by_id(id):
    p = session.query(Posts.PId, Posts.Title, Posts.Contents, Members.UserName).filter(and_(Posts.PId==Members.MemberId), Posts.PId==id).all()
    session.close()
    return p

def get_member_id_by_username(username):
    sql = '''select memberid from members where username='{username}' '''.format(username=username)
    member_id = session.execute(text(sql)).scalar()
    session.close()
    return member_id

def count_post_numbers_by_category(category):
    if category and isinstance(category, str):
        category = category

    if category:
        all_records_num = '''select count(*) from categories c inner join posts p on c.CId=p.CId and c.CName='{category}' and p.shownpost=1'''.format(category=category)
        all_count = session.execute(text(all_records_num)).scalar()
        session.close()
    else:
        all_records_num = '''select count(*) from posts where shownpost=1'''
        all_count = session.execute(text(all_records_num)).scalar()
        session.close()
    return int(all_count)

def is_user_belong_to_admin_group(user):
    sql = '''select rolename from role where roleid=(select roleid from members where username='{username}')'''.format(username=user)
    is_admin = session.execute(text(sql)).fetchall()
    if is_admin:
        return True if is_admin[0][0] =='Admin' else False
    else:
        return False

def is_post_create_by_user(pid, memberid):
    sql = '''select count(1) from posts where memberid='{memberid}' and pid='{pid}' '''.format(pid=pid, memberid=memberid)
    count = session.execute(text(sql)).scalar()
    session.close()
    return True if count > 0 else False

def create_post(title, category, content, member_id):
    cid_query = '''select cid from Categories where cname = '{category}' '''.format(category=category)

    cid = session.execute(text(cid_query)).scalar()
    if not cid:
        cid_insert = '''insert into categories values('{category}')'''.format(category=category)
        session.execute(text(cid_insert))
        session.commit()
        time.sleep(1)
        cid = session.execute(text(cid_query)).scalar()
    sql_string = '''insert into posts(title, contents, memberid, cid) values('{title}', '{contents}', '{memberid}', '{cid}')'''.format(title=title, contents=content, memberid=member_id, cid=cid)
    session.execute(text(sql_string))
    session.commit()
    session.close()

def update_post(title, category, content, id):

    cid_query = '''select cid from Categories where cname = '{category}' '''.format(category=category)
    cid = session.execute(text(cid_query)).scalar()

    if not cid:
        cid_insert = '''insert into categories values('{category}')'''.format(category=category)
        session.execute(text(cid_insert))
        session.commit()
        time.sleep(1)
        cid = session.execute(text(cid_query)).scalar()
    sql_string = '''update posts set title='{title}', contents='{contents}', cid='{cid}' where pid='{id}' '''.format(title=title, contents=content,cid=int(cid), id=int(id))
    session.execute(text(sql_string))
    session.commit()
    session.close()

def delete_post(pid):
    sql_string = '''update posts set shownpost=0 where pid='{pid}' '''.format(pid=pid)
    session.execute(text(sql_string))
    session.commit()
    session.close()

def get_post_by_category(category, page):
    results = []
    records_per_page_sql = '''select top {PER_PAGE} * from posts p inner join categories c \
on p.cid=c.cid and c.cname= N'{category}' where p.pid not in (select top {target_page} p.pid from posts p inner join categories c \
on p.cid=c.cid and c.cname= N'{category}' order by p.pid desc) and p.shownpost=1 order by p.pid desc'''.format(PER_PAGE=app.config["PER_PAGE"], target_page=(page - 1) * app.config["PER_PAGE"], category=category)

    records_per_page = session.execute(text(records_per_page_sql)).fetchall()

    for i in records_per_page:
        single_post = {}
        single_post["category_name"] = session.query(Categories.CName).filter(Categories.CId == i.CId).scalar()
        single_post["post_author_id"] = i.MemberId
        single_post["post_author"] = session.query(Members.UserName).filter(Members.MemberId == i.MemberId).scalar()
        single_post["post_id"] = i.PId
        single_post["post_title"] = i.Title
        single_post["post_contents"] = i.Contents
        single_post["post_comment"] = i.Comments if i.Comments else 'NULL'
        single_post["post_insert_date"] = i.InsertTime.strftime('%Y-%m-%d')
        results.append(single_post)

    session.close()
    return results



