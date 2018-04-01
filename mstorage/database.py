# -*- coding: utf-8 -*-
import socket

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .logger import Logger
from .table import Model, ActiveModel


class Database(object):
    def __init__(self, conn):
        self.logger = Logger(prefix='Database')
        self.conn = conn
        self.engine = create_engine(
            '{protocol}://{user}:{password}@{host}:{port}/{dbname}{encode}'.format(
                protocol=conn['protocol'],
                user=conn['user'],
                password=conn['password'],
                host=conn['host'],
                port=conn['port'],
                dbname=conn['database'],
                encode=conn['encode'],
            ))
        self.Session = sessionmaker(bind=self.engine, autoflush=False)

    def insert(self, service, model, version, s3_key, local_fname, checksum, active=True):
        with self.engine.connect() as conn:
            session = self.Session(bind=conn)
            m = Model(service=service,
                      model=model,
                      version=version,
                      s3_key=s3_key,
                      local_fname=local_fname,
                      checksum=checksum,
                      ip=socket.gethostbyname(socket.gethostname()),
                      machine_name=socket.gethostname())
            session.merge(m)
            session.commit()

            if active:
                am = ActiveModel(service, model, version)
                session.merge(am)
                session.commit()

    def list(self, service, model, limit=10):
        with self.engine.connect() as conn:
            session = self.Session(bind=conn)
            rows = session.query(Model)\
                .filter_by(service=service)\
                .filter_by(model=model)\
                .order_by(-Model.create_ts)\
                .limit(limit)
            rows = [row.__dict__ for row in rows]
        return rows

    def get(self, service, model, version=None):
        with self.engine.connect() as conn:
            session = self.Session(bind=conn)
            if not version:
                active = session.query(ActiveModel)\
                    .filter(service==service)\
                    .filter(model==model)\
                    .one()
                version = active.version
                self.logger.info('fetch active version [%s]', version)
            meta = session.query(Model)\
                .filter(service==service)\
                .filter(model==model)\
                .filter(version==version)\
                .one()
        if not meta:
            self.logger.info('no model, service [%s], model[%s]', service, model)
            return None
        return meta.__dict__

