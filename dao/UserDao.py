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

    def update_user(self, user_id: int, username: str = None, password: str = None, status: str = None) -> User:
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        if username:
            user.username = username
        if password:
            user.password = password
        if status:
            user.status = status
        self.session.commit()
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if not user:
            return False
        self.session.delete(user)
        self.session.commit()
        return True
