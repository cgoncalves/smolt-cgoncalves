# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy import *
from sqlalchemy.orm import *
from turbogears.database import metadata, session
#from sqlalchemy.ext.assignmapper import assign_mapper
from turbogears import identity
from datetime import timedelta, date, datetime
from turbogears.database import mapper

schema_changes = Table('schema_changes', metadata,
                       Column('id', Integer,
                              primary_key=True,
                              autoincrement=True),
                       Column('major', Integer),
                       Column('minor', Integer),
                       Column('point', Integer),
                       Column('branch', String(64),
                              default='main'),
                       Column('name', String(255)),
                       Column('date_applied', DateTime))

class SchemaChange(object):
    def __init__(self, **keys):
        if keys:
            self.major = keys['major']
            self.minor = keys['minor']
            self.point = keys['point']
            self.branch = keys['branch']
            self.name = keys['name']
        self.date_applied = datetime.today()

    def __str__(self):
        return str(self.__dict__)

    __repr__ = __str__
    pass

mapper(SchemaChange, schema_changes,
       order_by=[schema_changes.c.major
                ,schema_changes.c.minor
                ,schema_changes.c.point])
