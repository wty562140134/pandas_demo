from sqlalchemy.orm import Session

from models import CCPGPSCGPHYCLMX
from sqlalchemy_session import CreateDB


def test_get_ccp_gpsc_gphy_clmx_by_id():
    with CreateDB() as db:
        db: Session
        # noinspection PyUnresolvedReferences
        result: CCPGPSCGPHYCLMX = db.query(CCPGPSCGPHYCLMX).filter(CCPGPSCGPHYCLMX.id == 29).one()
    print(result.id)


if __name__ == '__main__':
    test_get_ccp_gpsc_gphy_clmx_by_id()
