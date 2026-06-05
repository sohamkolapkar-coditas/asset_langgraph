from sqlalchemy import Column, UUID, String, DateTime, ForeignKey, Boolean
import datetime


class BaseClass:

    created_at = Column(DateTime, nullable=True, default=datetime.datetime.now)
    updated_at = Column(DateTime, nullable=True)
    deleted_at = Column(DateTime, nullable=True)
    created_by = Column(UUID, nullable=True)
    updated_by = Column(UUID, nullable=True)
    deleted_by = Column(UUID, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
