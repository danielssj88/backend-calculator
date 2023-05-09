from datetime import datetime
from sqlalchemy.orm import Session
from dao.models import Record, Operation
from sqlalchemy import or_

class RecordDao:
    def __init__(self, session: Session):
        self.session = session

    def create_record(self, operation_id: int, user_id: int, amount: float, user_balance: float, operation_response: str) -> Record:
        record = Record(
            operation_id=operation_id,
            user_id=user_id,
            amount=amount,
            user_balance=user_balance,
            operation_response=operation_response,
            date=datetime.now()
        )
        self.session.add(record)
        self.session.commit()
        return record

    def get_records_by_user(self, user_id: int) -> list:
        return (
            self.session.query(Record)
            .filter_by(user_id=user_id)
            .order_by(Record.date.desc())
            .all()
        )

    def filter_records_by_user(self, user_id: int, searchValue: str) -> list:
        return (
            self.session.query(Record) \
            .join(Record.operation) \
            .filter(
                Record.user_id == user_id,
                or_(
                    Operation.type.like(searchValue + '%'),
                    Record.amount.like(searchValue + '%'),
                    Record.user_balance.like(searchValue + '%'),
                    Record.operation_response.like('%' + searchValue + '%'),
                    Record.date.like(searchValue + '%'),
                )
            ) \
            .order_by(Record.date.desc()) \
            .all()
        )
        

    def get_recent_record_by_user(self, user_id: int) -> Record:
        recent_record = (
            self.session.query(Record)
            .filter_by(user_id=user_id)
            .order_by(Record.date.desc())
            .first()
        )

        return recent_record

    def get_records_by_operation(self, operation_id: int) -> list:
        return self.session.query(Record).filter_by(operation_id=operation_id).all()

    def get_records_by_user_and_operation(self, user_id: int, operation_id: int) -> list:
        return self.session.query(Record).filter_by(user_id=user_id, operation_id=operation_id).all()
