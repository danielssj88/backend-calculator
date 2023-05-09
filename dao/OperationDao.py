from sqlalchemy.orm import Session

from dao.models import Operation


class OperationDao:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.query(Operation).all()
