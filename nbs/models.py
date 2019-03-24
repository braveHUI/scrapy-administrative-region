from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base


DeclarativeBase=declarative_base()
def db_connect():
    DB_CONNECT = 'mysql+pymysql://root:hgh15070417641@localhost/nbs'
    return create_engine(DB_CONNECT,echo=True)
class Stats(DeclarativeBase):
    __tablename__='stats'
    id=Column(Integer,primary_key=True)
    # 地区代码
    area_code = Column(String(200))
    # 地区
    level = Column(String(200))
    # 地区名
    area_name = Column(String(200))
    # 全名
    full_name = Column(String(200))
    # 父类代码
    parent = Column(String(200))
def create_tables(engine):
    DeclarativeBase.metadata.create_all(engine)