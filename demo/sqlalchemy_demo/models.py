from sqlalchemy import Column, TEXT
from sqlalchemy.dialects.mssql import DECIMAL, INTEGER, BIGINT, VARCHAR, DATETIME
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TestPlayerModel(Base):
    __tablename__ = 'test_player'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    snow_id = Column(BIGINT)
    name = Column(VARCHAR)
    age = Column(INTEGER)


class TestPlayerDetailModel(Base):
    __tablename__ = 'test_player_detail'

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    snow_id = Column(BIGINT)
    game_name = Column(VARCHAR)
    game_price = Column(DECIMAL)
    test_player_snow_id = Column(BIGINT)
    game_type = Column(VARCHAR)
    buy_date = Column(DATETIME)
