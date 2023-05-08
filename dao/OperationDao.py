from sqlalchemy.orm import Session

from dao.models import Operation


class OperationDao:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        return self.session.query(Operation).all()

    def get_by_id(self, id: int):
        return self.session.query(Operation).get(id)

    def create(self, operation: Operation):
        self.session.add(operation)
        self.session.commit()
        return operation

    def update(self, id: int, operation_data: dict):
        operation = self.get_by_id(id)
        if operation:
            for key, value in operation_data.items():
                setattr(operation, key, value)
            self.session.commit()
            return operation
        else:
            return None

    def delete(self, id: int):
        operation = self.get_by_id(id)
        if operation:
            self.session.delete(operation)
            self.session.commit()
            return operation
        else:
            return None
