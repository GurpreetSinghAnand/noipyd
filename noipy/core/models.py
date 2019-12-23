# Apache License 2.0
# 
# Copyright (c) 2010-2019 Gurpreet Anand (http://gurpreetanand.com)
#
# See README.rst and LICENSE for details.
#
# Author: Gurpreet Singh Anand
# Email: gurpreetsinghanand@live.com
# Project Repository: https://github.com/GurpreetSinghAnand/noipyd/noipyd/core
# Filename: models.py
# Description:

import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()


class Account(Base):
    __tablename__ = 'account'
    # Here we define columns for the table account
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False, unique=True)
    password = Column(String(250), nullable=False)


class Domain(Base):
    __tablename__ = 'domain'
    # Here we define columns for the table domain.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    hostname = Column(String(250), nullable=False)
    last_renewed = Column(Integer)
    expires = Column(Integer, nullable=False)
    ip_address = Column(String(16), nullable=False)
    type = Column(String(5), nullable=False)
    owner_id = Column(Integer, ForeignKey('account.id'))
    owner = relationship(Account)


# Create an engine that stores data in the local directory's
engine = create_engine('sqlite:///.noip.sqlite3.db')
Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker())


