# -*- coding: utf-8 -*-
import sqlalchemy
from sqlalchemy.sql import func
from sqlalchemy import Table, Column
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class ActiveModel(Base):
    __tablename__ = 'active_model'

    service = Column(sqlalchemy.String(64), primary_key=True)
    model = Column(sqlalchemy.String(128), primary_key=True)
    version = Column(sqlalchemy.String(64), primary_key=True)

    def __init__(self, service, model, version, *args, **kwargs):
        self.service = service
        self.model = model
        self.version = version


class Model(Base):
    __tablename__ = 'model'

    service = Column(sqlalchemy.String(64), primary_key=True)
    model = Column(sqlalchemy.String(128), primary_key=True)
    version = Column(sqlalchemy.String(64), primary_key=True)
    s3_key = Column(sqlalchemy.String(512), nullable=False)
    local_fname = Column(sqlalchemy.String(512), nullable=False)
    checksum = Column(sqlalchemy.String(64), nullable=False)
    ip = Column(sqlalchemy.String(64), nullable=False)  # IPv6 requires 39 chars
    machine_name = Column(sqlalchemy.String(512), nullable=False)
    create_ts = Column(sqlalchemy.DateTime(timezone=True), nullable=False,
                       server_default=func.now(), index=True)

    def __init__(self, service, model, version, s3_key, local_fname, checksum, ip, machine_name, *args, **kwargs):
        self.service = service
        self.model = model
        self.version = version
        self.s3_key = s3_key
        self.local_fname = local_fname
        self.checksum = checksum
        self.ip = ip
        self.machine_name = machine_name


class PullLog(Base):
    __tablename__ = 'pull_log'

    id = Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    service = Column(sqlalchemy.String(64), nullable=False)
    model = Column(sqlalchemy.String(128), nullable=False)
    version = Column(sqlalchemy.String(64), nullable=False)
    ip = Column(sqlalchemy.String(64), nullable=False)  # IPv6 requires 39 chars
    machine_name = Column(sqlalchemy.String(512), nullable=False)
    local_fname = Column(sqlalchemy.String(512), nullable=False)
    pull_ts = Column(sqlalchemy.DateTime(timezone=True), nullable=False,
                     server_default=func.now(), index=True)

    def __init__(self, service, model, version, ip, machine_name, local_fname, *args, **kwargs):
        self.service = service
        self.model = model
        self.version = version
        self.ip = ip
        self.machine_name = machine_name
        self.local_fname = local_fname


def create_table(conn, logger):
    from sqlalchemy import create_engine

    engine = create_engine(
        '{protocol}://{user}:{password}@{host}:{port}/{dbname}{encode}'.format(
            protocol=conn['protocol'],
            user=conn['user'],
            password=conn['password'],
            host=conn['host'],
            port=conn['port'],
            dbname=conn['database'],
            encode=conn['encode'],
        ))

    if not engine.dialect.has_table(engine, 'model'):
        logger.info('create table')
        Base.metadata.create_all(bind=engine)
    else:
        logger.info('table already exist, skip create_table')
