from sqlalchemy.orm import Session
from dao.models import User

class UserDao:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, username: str, password: str, status: str = 'active') -> User:
        user = User(username=username, password=password, status=status)
        self.session.add(user)
        self.session.commit()
        return user

    def get_user_by_id(self, user_id: int) -> User:
        return self.session.query(User).filter_by(id=user_id).first()

    def get_user_by_username(self, username: str) -> User:
        return self.session.query(User).filter_by(username=username).first()
