from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user import User, UserRole
from schemas.user import UserCreate
from core.security import hash_password


class UserService:
    @staticmethod
    def create_user(db: Session, user: UserCreate, role: UserRole = UserRole.USER) -> User:
        """Create a new user in the database."""
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password),
            role=role,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User | None:
        """Get a user by username."""
        stmt = select(User).where(User.username == username)
        return db.scalars(stmt).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User | None:
        """Get a user by ID."""
        stmt = select(User).where(User.id == user_id)
        return db.scalars(stmt).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User | None:
        """Get a user by email."""
        stmt = select(User).where(User.email == email)
        return db.scalars(stmt).first()
