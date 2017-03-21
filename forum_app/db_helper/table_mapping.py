import datetime

__author__ = 'kevin'
#coding=utf-8

from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Members(Base):
    __tablename__ = 'Members'
    MemberId = Column(Integer, primary_key=True, nullable=False)
    UserName = Column(String, nullable=False)
    PassWord = Column(String, nullable=False)
    RoleID = Column(Integer, ForeignKey('Role.RoleId'))
    PhoneNumber = Column(String, nullable=False)

class Categories(Base):
    __tablename__ = 'Categories'
    CId = Column(Integer, primary_key=True, nullable=False)
    CName = Column(String, nullable=False)
    PId = Column(Integer, ForeignKey('Posts.PId'), nullable=True)

class Posts(Base):
    __tablename__ = 'Posts'

    PId = Column(Integer, primary_key=True, nullable=False)
    Title = Column(String, nullable=True)
    Contents = Column(String, nullable=True)
    MemberId = Column(Integer, ForeignKey('Members.MemberId'))
    CId = Column(Integer, ForeignKey('Categories.CId'))
    Comments = Column(String, nullable=True)
    InsertTime = Column(DateTime )

class Role(Base):
    __tablename__ = 'Role'

    RoleId = Column(Integer, primary_key=True, nullable=False)
    RoleName = Column(String, nullable=False)
    Description = Column(String, nullable=True)

    Ref = relationship('Members', backref="Role")