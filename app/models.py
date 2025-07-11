from .settings import Base
from sqlalchemy import TIMESTAMP, Integer, Column, String, Boolean
from sqlalchemy.sql.expression import text

class Post(Base):
    __tablename__ = "post"

    id = Column(Integer, primary_key = True, nullable =False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    public = Column(Boolean, server_default='True')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default= text('now()') )
    