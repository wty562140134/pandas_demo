from sqlalchemy.orm import Session

from demo.sqlalchemy_demo.models import TestPlayerModel, TestPlayerDetailModel
from demo.sqlalchemy_demo.sqlalchemy_session import CreateDB


def test_get_test_player():
    with CreateDB() as db:
        db: Session
        # noinspection PyUnresolvedReferences
        result: TestPlayerModel = db.query(TestPlayerModel).filter(TestPlayerModel.id == 1).one()
    print(result)


def test_get_test_player_and_detail():
    with CreateDB() as db:
        db: Session
        query = db.query(TestPlayerModel,TestPlayerDetailModel.game_name, TestPlayerDetailModel.game_price). \
            join(TestPlayerDetailModel, TestPlayerDetailModel.test_player_snow_id == TestPlayerModel.snow_id). \
            filter(TestPlayerDetailModel.test_player_snow_id == 1682197602864603136)
        print(query.all())


if __name__ == '__main__':
    # test_get_test_player()
    test_get_test_player_and_detail()
